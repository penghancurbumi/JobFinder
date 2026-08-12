import "dotenv/config"
import express from "express"
import cors from "cors"
import multer from "multer"
import { createRequire } from "module"
const require = createRequire(import.meta.url)
const { PDFParse } = require("pdf-parse")
import { createServer } from "http"
import { Server } from "socket.io"
import { scrapeOnePlatform, runCleanup, PLATFORMS } from "./scrapers/index.js"
import { analyzeCV } from "./cvAnalyzer.js"
import { getBuilderSections, getSuggestion } from "./cvBuilder.js"
import { chat } from "./chatbot.js"
import { runBot } from "./telegramBot.js"
import { EXPERTISE_AREAS } from "./constants.js"
import { fetchAll, fetchOne, runQuery, getJobsCache, loadJobsCache, refreshJobsCache, getScrapingState, updateScrapingState } from "./db.js"

const app = express()
const httpServer = createServer(app)
const io = new Server(httpServer, {
  cors: { origin: "*" }
})

const upload = multer({ storage: multer.memoryStorage(), limits: { fileSize: 5 * 1024 * 1024 } })
const PORT = process.env.PORT || 3000

app.use(cors())
app.use(express.json())

// ---- Per-platform round-robin scraping (persistent state) ----
// Each "Perbarui Data" press scrapes ONE platform, cycling through PLATFORMS
// in order (jobstreet → glints → kalibrr → techinasia → linkedin → kitalulus
// → pintarnya → jobstreet → ...). The next platform is stored persistently in
// scraping_state so it survives restarts and is never decided by the frontend.
// On failure the same platform is retried on the next press.
let isScraping = false

// Starts one platform scrape in the background and returns immediately.
// Guards against concurrent runs (in-memory flag + persistent "running" state).
async function startScrape() {
  if (isScraping) {
    return { status: "running", message: "Update data sedang berlangsung." }
  }
  const state = await getScrapingState()
  if (state?.status === "running") {
    return { status: "running", message: "Update data sedang berlangsung." }
  }

  const platform = state?.current_platform || PLATFORMS[0]
  const idx = PLATFORMS.indexOf(platform)
  isScraping = true
  const now = new Date().toISOString()
  await updateScrapingState({ status: "running", current_platform: platform, last_run_at: now, error_message: "" })
  io.emit("scrape-status", { status: "started", platform, message: `Scraping ${platform} sedang diproses.` })

  performScrape(platform, idx)
    .catch(async (e) => {
      console.error(`Scraping ${platform} failed:`, e.message)
      await updateScrapingState({ status: "failed", error_message: e.message, last_run_at: new Date().toISOString() })
      io.emit("scrape-status", { status: "failed", platform, message: `Scraping ${platform} gagal: ${e.message}` })
    })
    .finally(() => {
      isScraping = false
    })

  return { status: "started", platform, message: `Scraping ${platform} sedang diproses.` }
}

async function performScrape(platform, idx) {
  const result = await scrapeOnePlatform(platform, idx + 1, PLATFORMS.length, (evt) => io.emit("scrape-progress", evt))
  await refreshJobsCache()
  const next = PLATFORMS[(idx + 1) % PLATFORMS.length]
  await updateScrapingState({
    status: "completed",
    current_platform: next,
    last_platform: platform,
    total_jobs_scraped: result.added,
    last_run_at: new Date().toISOString(),
    error_message: "",
  })
  const jobsPayload = await getFilteredJobs("", "all", "all", "newest", "", "", false, 1, 200)
  io.emit("jobs-updated", jobsPayload)
  io.emit("scrape-status", {
    status: "completed",
    platform,
    total_scraped: result.added,
    next_platform: next,
    message: `Data ${platform} berhasil diperbarui.`,
  })
  console.log(`Platform ${platform} selesai. Next: ${next} (${result.added} diproses)`)
}

async function getFilteredJobs(search = "", bidang = "all", tipe = "all", sortBy = "newest", location = "", experience = "", hasSalary = false, education = "all", page = 1, limit = 200) {
  page = Math.max(parseInt(page, 10) || 1, 1)
  limit = Math.min(Math.max(parseInt(limit, 10) || 200, 1), 500)
  const offset = (page - 1) * limit

  let jobs = getJobsCache()
  if (!jobs) {
    try {
      jobs = await loadJobsCache()
    } catch {
      jobs = []
    }
  }

  const lower = (s) => String(s || "").toLowerCase()

  jobs = jobs.filter((j) => {
    if (bidang && bidang !== 'all') {
      if (!String(j.jobType || "").includes(bidang)) return false
    }

    if (tipe && tipe !== 'all') {
      const jt = lower(j.jobType)
      const wt = lower(j.workType).replace(/-/g, "")
      if (tipe === "hybrid" || tipe === "remote" || tipe === "onsite") {
        if (!wt.includes(tipe)) return false
      } else if (tipe === "fulltime") {
        if (!(jt.includes("full") && jt.includes("time"))) return false
      } else if (tipe === "parttime") {
        if (!(jt.includes("part") && jt.includes("time"))) return false
      } else if (tipe === "intern") {
        if (!(jt.includes("intern") || j.jobType === "Internship" || j.jobType === "Magang")) return false
      } else if (tipe === "freelance" || tipe === "contract") {
        if (!jt.includes(tipe)) return false
      }
    }

    if (search) {
      const term = lower(search)
      if (!(lower(j.title).includes(term) || lower(j.expertise).includes(term) || lower(j.company).includes(term))) return false
    }

    if (location && location !== 'all') {
      if (!lower(j.location).includes(lower(location))) return false
    }

    if (hasSalary) {
      if (!j.salary || j.salary === "") return false
    }

    if (experience && experience !== 'all') {
      const t = lower(j.title)
      if (experience === 'entry') {
        if (!(t.includes("junior") || t.includes("entry") || t.includes("staff"))) return false
      } else if (experience === 'mid') {
        if (t.includes("junior") || t.includes("senior") || t.includes("lead") || t.includes("manager")) return false
      } else if (experience === 'senior') {
        if (!(t.includes("senior") || t.includes("lead") || t.includes("principal"))) return false
      } else if (experience === 'manager') {
        if (!(t.includes("manager") || t.includes("head") || t.includes("director"))) return false
      }
    }

    if (education && education !== 'all') {
      const text = lower(j.title) + " " + lower(j.description)
      if (education === 's3') {
        if (!text.includes("s3") && !text.includes("doktor")) return false
      } else if (education === 's2') {
        if (!text.includes("s2") && !text.includes("magister") && !text.includes("master")) return false
      } else if (education === 's1') {
        if (!text.includes("s1") && !text.includes("sarjana") && !text.includes("bachelor")) return false
      } else if (education === 'diploma' || education === 'd3' || education === 'd4') {
        if (!text.includes("d3") && !text.includes("d4") && !text.includes("diploma") && !text.includes("d1") && !text.includes("d2")) return false
      } else if (education === 'sma' || education === 'smk') {
        if (!text.includes("sma") && !text.includes("smk") && !text.includes("sederajat") && !text.includes("slta")) return false
      }
    }

    return true
  })

  const cmpAsc = (a, b) => (a > b ? 1 : a < b ? -1 : 0)
  if (sortBy === "az") {
    jobs.sort((a, b) => cmpAsc(a.title || "", b.title || ""))
  } else if (sortBy === "za") {
    jobs.sort((a, b) => cmpAsc(b.title || "", a.title || ""))
  } else if (sortBy === "oldest") {
    jobs.sort((a, b) => cmpAsc(a.postedDate || "", b.postedDate || "") || (a.id - b.id))
  } else {
    jobs.sort((a, b) => cmpAsc(b.postedDate || "", a.postedDate || "") || (b.id - a.id))
  }

  const total = jobs.length
  const pageJobs = jobs.slice(offset, offset + limit)
  return { jobs: pageJobs, total, page, limit, totalPages: Math.ceil(total / limit) }
}

io.on("connection", async (socket) => {
  console.log("Client connected via WebSocket")
  try {
    const state = await getScrapingState()
    socket.emit("scrape-status", {
      status: isScraping || state?.status === "running" ? "running" : "idle",
      platform: state?.current_platform || PLATFORMS[0],
      last_run_at: state?.last_run_at,
      total_jobs_scraped: state?.total_jobs_scraped,
    })
  } catch { /* ignore */ }
  const result = await getFilteredJobs()
  socket.emit("jobs-updated", result)
  
  socket.on("request-scrape", async () => {
    const resp = await startScrape()
    if (resp.status === "running") {
      socket.emit("scrape-status", { status: "running", message: resp.message })
    }
  })

  socket.on("filter-jobs", async ({ search, bidang, tipe, sortBy, location, experience, hasSalary, education, page, limit }) => {
    const result = await getFilteredJobs(search, bidang, tipe, sortBy, location, experience, hasSalary, education, page, limit)
    socket.emit("jobs-updated", result)
  })
})

// No auto-scraping: each "Perbarui Data" press scrapes exactly one platform,
// cycling through PLATFORMS via the persistent scraping_state pointer.

// Remove expired jobs daily (and once at startup) so data doesn't pile up.
async function runScheduledCleanup() {
  try {
    const cleanup = await runCleanup()
    await refreshJobsCache()
    if (cleanup.total > 0) console.log("Scheduled cleanup removed:", cleanup.total, "job(s)")
  } catch (e) {
    console.error("Scheduled cleanup failed:", e.message)
  }
}
setInterval(runScheduledCleanup, 24 * 60 * 60 * 1000)
setTimeout(runScheduledCleanup, 5000)

// ===================== GOOGLE FONTS PROXY =====================
let googleFontsCache = null
let googleFontsCacheTime = 0
const FONTS_CACHE_TTL = 24 * 60 * 60 * 1000 // 24 jam

app.get("/api/google-fonts", async (req, res) => {
  try {
    const now = Date.now()
    if (googleFontsCache && (now - googleFontsCacheTime) < FONTS_CACHE_TTL) {
      return res.json(googleFontsCache)
    }
    const response = await fetch("https://fonts.google.com/metadata/fonts")
    const json = await response.json()
    const fonts = json.familyMetadataList.map(f => ({
      family: f.family,
      category: f.category,
    }))
    googleFontsCache = fonts
    googleFontsCacheTime = now
    res.json(fonts)
  } catch (e) {
    console.error("Failed to fetch Google Fonts metadata:", e.message)
    res.status(500).json({ error: "Gagal mengambil daftar font" })
  }
})

app.get("/api/expertise-areas", (req, res) => res.json(EXPERTISE_AREAS))

app.get("/api/jobs", async (req, res) => {
  const { search, bidang, tipe, sortBy, location, experience, hasSalary, education, page, limit } = req.query
  const result = await getFilteredJobs(
    search, 
    bidang, 
    tipe, 
    sortBy, 
    location, 
    experience, 
    hasSalary === 'true' || hasSalary === true,
    education,
    page,
    limit
  )
  res.json(result)
})

app.get("/api/status", async (req, res) => {
  try {
    const state = await getScrapingState()
    const platform = state?.current_platform || PLATFORMS[0]
    const nextIdx = (PLATFORMS.indexOf(platform) + 1) % PLATFORMS.length
    res.json({
      platform,
      status: isScraping || state?.status === "running" ? "running" : (state?.status || "idle"),
      last_platform: state?.last_platform || null,
      last_run_at: state?.last_run_at || null,
      total_jobs_scraped: state?.total_jobs_scraped || 0,
      next_platform: PLATFORMS[nextIdx],
      error_message: state?.error_message || null,
    })
  } catch (e) {
    res.status(500).json({ error: e.message })
  }
})

app.post("/api/cv/analyze", upload.single("cv"), async (req, res) => {
  try {
    let cvText = ""
    if (!req.file) {
      return res.status(400).json({ error: "CV file required (PDF format)" })
    }
    
    if (req.file.mimetype === "application/pdf") {
      try {
        const parser = new PDFParse({ data: req.file.buffer })
        const pdfData = await parser.getText()
        cvText = pdfData.text
      } catch (err) {
        throw new Error("Failed to parse PDF: " + err.message)
      }
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
  const { message, sessionId } = req.body
  if (!message) return res.status(400).json({ error: "message required" })

  let chatHistory = []
  if (sessionId) {
    try {
      const row = await fetchOne("SELECT messages FROM chat_sessions WHERE session_id = ?", [sessionId])
      if (row) chatHistory = JSON.parse(row.messages)
    } catch { /* start fresh */ }
  }

  // Get jobs from cache for chatbot context (fallback to DB if cache not loaded)
  let dbJobs = getJobsCache() || []
  if (!dbJobs.length) {
    try {
      dbJobs = await fetchAll("SELECT * FROM jobs LIMIT 200")
    } catch { /* ignore */ }
  }

  const reply = await chat(message, chatHistory, dbJobs)

  const updatedHistory = [...chatHistory, { role: "user", content: message }, { role: "assistant", content: reply }]

  if (sessionId) {
    try {
      await runQuery(
        "INSERT OR REPLACE INTO chat_sessions (session_id, messages, updated_at) VALUES (?, ?, datetime('now'))",
        [sessionId, JSON.stringify(updatedHistory)]
      )
    } catch { /* ignore */ }
  }

  res.json({ reply, history: updatedHistory })
})

app.get("/api/chat/history/:sessionId", async (req, res) => {
  const { sessionId } = req.params
  try {
    const row = await fetchOne("SELECT messages FROM chat_sessions WHERE session_id = ?", [sessionId])
    const messages = row ? JSON.parse(row.messages) : []
    res.json({ messages })
  } catch {
    res.json({ messages: [] })
  }
})

httpServer.listen(PORT, async () => {
  try {
    await loadJobsCache()
    const cached = getJobsCache() || []
    console.log(`Loaded ${cached.length} jobs into memory cache`)
  } catch (e) {
    console.error("Failed to load jobs cache:", e.message)
  }
  console.log(`Backend running on http://localhost:${PORT}`)
  runBot()
})
