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
import { fetchAll } from "./db.js"

const app = express()
const httpServer = createServer(app)
const io = new Server(httpServer, {
  cors: { origin: "*" }
})

const upload = multer({ storage: multer.memoryStorage(), limits: { fileSize: 5 * 1024 * 1024 } })
const PORT = process.env.PORT || 3000

app.use(cors())
app.use(express.json())

let isScraping = false

async function performScrape() {
  if (isScraping) return
  isScraping = true
  io.emit("scrape-status", { status: "scraping" })
  try {
    await scrapeAll() // This now inserts into DB
    const jobs = await getFilteredJobs()
    io.emit("jobs-updated", jobs)
    io.emit("scrape-status", { status: "idle", lastUpdated: new Date() })
  } catch (e) {
    console.error("Scrape failed:", e.message)
    io.emit("scrape-status", { status: "error", message: e.message })
  } finally {
    isScraping = false
  }
}

async function getFilteredJobs(search = "", bidang = "all", tipe = "all", sortBy = "newest") {
  let query = "SELECT * FROM jobs WHERE 1=1"
  const params = []
  
  if (bidang && bidang !== 'all') {
    query += " AND jobType LIKE ?"
    params.push(`%${bidang}%`)
  }

  if (tipe && tipe !== 'all') {
    query += " AND (description LIKE ? OR title LIKE ?)"
    params.push(`%${tipe}%`, `%${tipe}%`)
  }
  
  if (search) {
    query += " AND (title LIKE ? OR expertise LIKE ? OR company LIKE ?)"
    const term = `%${search}%`
    params.push(term, term, term)
  }
  
  if (sortBy === "az") {
    query += " ORDER BY title ASC"
  } else if (sortBy === "za") {
    query += " ORDER BY title DESC"
  } else if (sortBy === "oldest") {
    query += " ORDER BY postedDate ASC, id ASC"
  } else if (sortBy === "newest") {
    query += " ORDER BY postedDate DESC, id DESC"
  } else {
    query += " ORDER BY postedDate DESC, id DESC"
  }
  
  query += " LIMIT 200"
  
  try {
    const jobs = await fetchAll(query, params)
    return jobs
  } catch (err) {
    console.error("DB Error:", err.message)
    return []
  }
}

io.on("connection", async (socket) => {
  console.log("Client connected via WebSocket")
  const jobs = await getFilteredJobs()
  socket.emit("jobs-updated", jobs)
  
  socket.on("request-scrape", () => {
    performScrape()
  })

  socket.on("filter-jobs", async ({ search, bidang, tipe, sortBy }) => {
    const jobs = await getFilteredJobs(search, bidang, tipe, sortBy)
    socket.emit("jobs-updated", jobs)
  })
})

// Initial scrape and periodic refresh
// We don't necessarily want to scrape immediately on server start anymore since it takes long,
// but we'll fetch existing jobs on mount and only auto-scrape every 30 mins
setInterval(performScrape, 30 * 60 * 1000)

app.get("/api/expertise-areas", (req, res) => res.json(EXPERTISE_AREAS))

app.get("/api/jobs", async (req, res) => {
  const { search, bidang, tipe, sortBy } = req.query
  const jobs = await getFilteredJobs(search, bidang, tipe, sortBy)
  res.json(jobs)
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
