import "dotenv/config"
import express from "express"
import cors from "cors"
import multer from "multer"
import { createRequire } from "module"
const require = createRequire(import.meta.url)
const pdfParse = require("pdf-parse")
import { createServer } from "http"
import { Server } from "socket.io"
import { scrapeAll } from "./scrapers/index.js"
import { analyzeCV } from "./cvAnalyzer.js"
import { getBuilderSections, getSuggestion } from "./cvBuilder.js"
import { chat } from "./chatbot.js"
import { runBot } from "./telegramBot.js"
import { EXPERTISE_AREAS } from "./constants.js"

const app = express()
const httpServer = createServer(app)
const io = new Server(httpServer, {
  cors: { origin: "*" }
})

const upload = multer({ storage: multer.memoryStorage(), limits: { fileSize: 5 * 1024 * 1024 } })
const PORT = process.env.PORT || 3000

app.use(cors())
app.use(express.json())

let scrapedJobs = []
let isScraping = false

async function performScrape() {
  if (isScraping) return
  isScraping = true
  io.emit("scrape-status", { status: "scraping" })
  try {
    const newJobs = await scrapeAll()
    // Merge new jobs, avoiding duplicates by title & company
    const existingIds = new Set(scrapedJobs.map(j => `${j.title}-${j.company}`))
    const uniqueNewJobs = newJobs.filter(j => !existingIds.has(`${j.title}-${j.company}`))
    scrapedJobs = [...uniqueNewJobs, ...scrapedJobs]
    
    console.log(`Scraped ${newJobs.length} jobs. Total unique: ${scrapedJobs.length}`)
    io.emit("jobs-updated", getFilteredJobs())
    io.emit("scrape-status", { status: "idle", lastUpdated: new Date() })
  } catch (e) {
    console.error("Scrape failed:", e.message)
    io.emit("scrape-status", { status: "error", message: e.message })
  } finally {
    isScraping = false
  }
}

function getFilteredJobs(search = "", jobType = "all") {
  const currentDate = new Date("2026-07-15T00:00:00Z")
  let filtered = scrapedJobs.filter(j => {
    if (j.deadlineDate) {
      const deadline = new Date(j.deadlineDate)
      if (deadline < currentDate) return false
    }
    return true
  })

  if (search) {
    const q = search.toLowerCase()
    filtered = filtered.filter(j => 
      j.expertise.toLowerCase().includes(q) || 
      j.title.toLowerCase().includes(q)
    )
  }
  if (jobType && jobType !== 'all') {
    filtered = filtered.filter(j => j.jobType === jobType)
  }
  return filtered
}

io.on("connection", (socket) => {
  console.log("Client connected via WebSocket")
  socket.emit("jobs-updated", getFilteredJobs())
  
  socket.on("request-scrape", () => {
    performScrape()
  })

  socket.on("filter-jobs", ({ search, jobType }) => {
    socket.emit("jobs-updated", getFilteredJobs(search, jobType))
  })
})

// Initial scrape and periodic refresh
performScrape()
setInterval(performScrape, 30 * 60 * 1000)

app.get("/api/expertise-areas", (req, res) => res.json(EXPERTISE_AREAS))

app.get("/api/jobs", (req, res) => {
  const { search, jobType } = req.query
  res.json(getFilteredJobs(search, jobType))
})

app.post("/api/cv/analyze", upload.single("cv"), async (req, res) => {
  try {
    let cvText = ""
    if (!req.file) {
      return res.status(400).json({ error: "CV file required (PDF format)" })
    }
    
    if (req.file.mimetype === "application/pdf") {
      const pdfData = await pdfParse(req.file.buffer)
      cvText = pdfData.text
    } else {
      cvText = req.file.buffer.toString("utf-8")
    }

    const expertise = req.body.expertise || "Others"
    const result = await analyzeCV(cvText, expertise)
    // Wrap the string result back into the expected object structure for frontend
    res.json({
        ats: result.ats,
        eligible: result.eligible,
        analysis: result.analysis
    })
  } catch (e) {
    res.status(500).json({ error: e.message })
  }
})

app.get("/api/cv/builder-sections", (req, res) => res.json(getBuilderSections()))

app.post("/api/cv/suggestion", async (req, res) => {
  const { fieldLabel, expertise } = req.body
  if (!fieldLabel) return res.status(400).json({ error: "fieldLabel required" })
  const suggestion = await getSuggestion(fieldLabel, expertise || "Others")
  res.json({ suggestion })
})

app.post("/api/chat", async (req, res) => {
  const { message, history } = req.body
  if (!message) return res.status(400).json({ error: "message required" })
  const reply = await chat(message, history)
  res.json({ reply })
})

httpServer.listen(PORT, () => {
  console.log(`Backend running on http://localhost:${PORT}`)
  runBot()
})
