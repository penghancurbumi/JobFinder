import { spawn } from "child_process"
import fs from "fs/promises"
import path from "path"
import { runQuery, deleteByUrls, deleteExpiredJobs, findDuplicate } from "../db.js"

const SCRAPY_PROJECT_DIR = path.join(process.cwd(), "scrapping-job")
const EXPORTS_DIR = path.join(SCRAPY_PROJECT_DIR, "exports", "json")
const ARCHIVE_DIR = path.join(EXPORTS_DIR, "archive")
const NOT_FOUND_FILE = path.join(EXPORTS_DIR, "not_found.txt")

// Real Python interpreter. The `python` on PATH is the Windows Store alias stub
// that cannot launch from a hidden/background process (shell:false).
const PYTHON_EXE = "C:\\Users\\Muhammad Al Fakhreza\\AppData\\Local\\Python\\bin\\python.exe"

// Run up to N category scrapes at the same time
const CONCURRENCY = 2
// How many listing pages to paginate per spider per category
const MAX_PAGES = 1
// Safety cap per category (way above realistic run time)
const CATEGORY_TIMEOUT_MS = 15 * 60 * 1000
// Expired-job cleanup thresholds (see db.js deleteExpiredJobs)
const EXPIRED_OPTIONS = { maxAgeDays: 90, notSeenDays: 30, notSeenMinAgeDays: 7 }

export async function insertScrapedFiles(jobTypeFilter) {
  let count = 0
  let skipped = 0
  
  // Ensure archive directory exists
  await fs.mkdir(ARCHIVE_DIR, { recursive: true })
  
  try {
    const files = await fs.readdir(EXPORTS_DIR)
    const jsonFiles = files.filter(f => f.endsWith(".json"))
    
    for (const file of jsonFiles) {
      const filePath = path.join(EXPORTS_DIR, file)
      try {
        const content = await fs.readFile(filePath, "utf-8")
        const scrapedItems = JSON.parse(content)
        
        for (const item of scrapedItems) {
          const lastSeenAt = new Date().toISOString()

          // Skip re-listings that already exist under a different URL, but keep
          // their lastSeenAt fresh so they aren't pruned as "not seen".
          // Only dedupe when title/company/location are real values — items with
          // placeholder fields ("Unknown Title/Company") would otherwise falsely
          // collapse distinct jobs together.
          const real = (s) => {
            const v = String(s || "").trim()
            return v && !/^(unknown|n\/a|na|tbd)$/i.test(v)
          }
          const dup = real(item.title) && real(item.company_name) && real(item.location)
            ? await findDuplicate(item.title, item.company_name, item.location)
            : null
          if (dup) {
            await runQuery("UPDATE jobs SET lastSeenAt = ? WHERE id = ?", [lastSeenAt, dup.id])
            skipped++
            continue
          }

          let salary = ""
          if (item.salary_min || item.salary_max) {
            const currency = item.salary_currency || "IDR"
            if (item.salary_min && item.salary_max) {
              salary = `${currency} ${item.salary_min.toLocaleString()} - ${item.salary_max.toLocaleString()}`
            } else if (item.salary_min) {
              salary = `${currency} ${item.salary_min.toLocaleString()}`
            }
          }
          
          const expertise = item.skills && item.skills.length > 0 ? item.skills.slice(0, 3).join(", ") : "Others"
          const postedDate = item.updated_at ? item.updated_at.substring(0, 10) : new Date().toISOString().substring(0, 10)
          
          // Insert into SQLite, refreshing type/description/salary on duplicate URL
          const query = `
            INSERT INTO jobs 
            (title, company, location, jobType, workType, expertise, source, url, description, postedDate, deadlineDate, salary, lastSeenAt)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(url) DO UPDATE SET
              jobType = CASE WHEN excluded.jobType != 'Full-time' THEN excluded.jobType ELSE jobType END,
              workType = CASE WHEN excluded.workType != 'On-site' THEN excluded.workType ELSE workType END,
              description = CASE WHEN excluded.description != '' THEN excluded.description ELSE description END,
              salary = CASE WHEN excluded.salary != '' THEN excluded.salary ELSE salary END,
              postedDate = excluded.postedDate,
              lastSeenAt = excluded.lastSeenAt
          `
          const params = [
            item.title || "Unknown Title",
            item.company_name || "Unknown Company",
            item.location || "Remote",
            item.job_type || "Full-time",
            item.work_type || "On-site",
            expertise,
            item.platform || "Scraper",
            item.source_url || "",
            item.description || "",
            postedDate,
            null, // deadlineDate
            salary,
            lastSeenAt
          ]
          
          const res = await runQuery(query, params)
          if (res.changes > 0) count++
        }
        
        // Move to archive so we don't read it again
        const archivePath = path.join(ARCHIVE_DIR, file)
        await fs.rename(filePath, archivePath)
        
      } catch (err) {
        console.error(`Error processing file ${file}:`, err.message)
      }
    }
  } catch(e) {
    console.error("Error reading exports:", e.message)
  }
  
  console.log(`Import done: ${count} added/updated, ${skipped} duplicate skipped`)
  return count
}

// Delete jobs whose detail pages returned 404/410 during scraping.
// The Scrapy NotFoundCollectorMiddleware appends expired URLs to not_found.txt.
export async function deleteNotFoundJobs() {
  try {
    const content = await fs.readFile(NOT_FOUND_FILE, "utf-8")
    const urls = [...new Set(content.split(/\r?\n/).map(l => l.trim()).filter(Boolean))]
    if (!urls.length) return 0
    const removed = await deleteByUrls(urls)
    await fs.unlink(NOT_FOUND_FILE)
    console.log(`Not-found cleanup: ${removed} expired job(s) removed (${urls.length} URL checked)`)
    return removed
  } catch (e) {
    if (e.code !== "ENOENT") console.error("Error reading not_found file:", e.message)
    return 0
  }
}

// Remove jobs that are no longer on the source platforms: 404-detected,
// past the age cap, or absent from recent scrape cycles.
export async function runCleanup() {
  const removedNotFound = await deleteNotFoundJobs()
  const removedExpired = await deleteExpiredJobs(EXPIRED_OPTIONS)
  const total = removedNotFound + removedExpired.age + removedExpired.notSeen
  console.log(`Cleanup done: ${removedNotFound} not-found, ${removedExpired.age} age-expired, ${removedExpired.notSeen} not-seen (total ${total})`)
  return { removedNotFound, ...removedExpired, total }
}

// Run a single category scrape, streaming per-spider progress events as they happen.
function runCategory(cmd, category, onProgress) {
  return new Promise((resolve) => {
    let child
    try {
      // Windows: `python` in PATH is the Microsoft Store alias stub which fails to
      // launch from a background/hidden process with shell:false. Use the real
      // interpreter explicitly (fall back to PATH resolution if it is absent).
      const exe = PYTHON_EXE || "python"
      const args = cmd.split(/\s+/).slice(1)
      child = spawn(exe, args, { cwd: SCRAPY_PROJECT_DIR, shell: false })
    } catch (e) {
      console.error(`Failed to start scrape for ${category}:`, e.message)
      return resolve()
    }

    const timer = setTimeout(() => {
      console.error(`Scrape timeout for category ${category}, killing process`)
      try { child.kill() } catch { /* ignore */ }
    }, CATEGORY_TIMEOUT_MS)

    const doneSpiders = new Set()
    let buf = ""

    function processLine(line) {
      const start = line.match(/Starting spider '(\w+)'/)
      if (start) {
        const spider = start[1]
        if (!doneSpiders.has(spider)) onProgress?.({ category, spider, status: "start", message: `Mulai ${spider}` })
        return
      }
      const closed = line.match(/SPIDER CLOSED \| Name: (\w+)[^|]*\| Items: (\d+)/)
      if (closed) {
        const spider = closed[1]
        const items = parseInt(closed[2], 10) || 0
        if (!doneSpiders.has(spider)) {
          doneSpiders.add(spider)
          onProgress?.({ category, spider, items, status: "done", message: `Selesai ${spider} (${items} item)` })
        }
        return
      }
      if (line.includes("All spiders completed.")) {
        onProgress?.({ category, status: "category-done", message: `Kategori ${category} selesai` })
      }
    }

    child.stdout.on("data", (chunk) => {
      buf += chunk.toString()
      let idx
      while ((idx = buf.indexOf("\n")) >= 0) {
        const line = buf.slice(0, idx)
        buf = buf.slice(idx + 1)
        processLine(line)
      }
    })
    child.stderr.on("data", (chunk) => {
      buf += chunk.toString()
      let idx
      while ((idx = buf.indexOf("\n")) >= 0) {
        const line = buf.slice(0, idx)
        buf = buf.slice(idx + 1)
        processLine(line)
      }
    })

    child.on("error", (err) => {
      console.error(`Scrape error for ${category}:`, err.message)
      clearTimeout(timer)
      resolve()
    })
    child.on("close", () => {
      clearTimeout(timer)
      if (buf.trim()) buf.split(/\r?\n/).forEach(processLine)
      resolve()
    })
  })
}

export async function scrapeAll(onProgress) {
  console.log("Starting Python Scrapy jobs for 5 job types (parallel)...")

  const jobTypes = [
    { type: "fulltime", cmd: `python -m scrapy crawl_all -a job_type=fulltime -a max_pages=${MAX_PAGES}` },
    { type: "parttime", cmd: `python -m scrapy crawl_all -a job_type=parttime -a max_pages=${MAX_PAGES}` },
    { type: "intern", cmd: `python -m scrapy crawl_all -a job_type=internship -a max_pages=${MAX_PAGES}` },
    { type: "hybrid", cmd: `python -m scrapy crawl_all -a work_type=hybrid -a max_pages=${MAX_PAGES}` },
    { type: "freelance", cmd: `python -m scrapy crawl_all -a job_type=contract -a max_pages=${MAX_PAGES}` }
  ]

  let idx = 0
  const categoryDone = new Set()

  async function worker() {
    while (idx < jobTypes.length) {
      const jt = jobTypes[idx++]
      onProgress?.({ category: jt.type, status: "category-start", message: `Mulai kategori ${jt.type}` })
      await runCategory(jt.cmd, jt.type, (evt) => {
        if (evt.status === "category-done") categoryDone.add(evt.category)
        onProgress?.(evt)
      })
    }
  }

  const workers = Array.from({ length: Math.min(CONCURRENCY, jobTypes.length) }, worker)
  await Promise.all(workers)

  console.log("All categories scraped. Importing exports into DB...")
  const added = await insertScrapedFiles("all")
  const cleanup = await runCleanup()
  console.log(`Scrapy execution completed. Total new jobs added: ${added} | removed: ${cleanup.total}`)
  onProgress?.({ status: "done", added, removed: cleanup })
  return { added, cleanup }
}
