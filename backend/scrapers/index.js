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

// The 7 supported platforms, scraped one at a time (round-robin) on demand.
const PLATFORMS = ["glints", "jobstreet", "kalibrr", "kitalulus", "linkedin", "pintarnya", "techinasia"]
// How many listing pages to paginate per scrape
const MAX_PAGES = 1
// Safety cap per scrape (way above realistic run time)
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

// Scrape a single platform. Each "Perbarui Data" press scrapes one platform
// only (fast); the backend advances through PLATFORMS round-robin.
export async function scrapeOnePlatform(platform, index, total, onProgress) {
  onProgress?.({ status: "platform-start", platform, index, total, message: `Mulai scrape ${platform} (${index}/${total})` })
  console.log(`Scraping platform: ${platform} (${index}/${total})...`)

  const cmd = `python -m scrapy crawl ${platform} -a max_pages=${MAX_PAGES}`
  await runCategory(cmd, platform, (evt) => {
    if (evt.spider) {
      onProgress?.({ status: "platform-spider", platform, spider: evt.spider, done: evt.status === "done", items: evt.items, message: evt.message })
    } else {
      onProgress?.(evt)
    }
  })

  console.log(`Importing exports for ${platform}...`)
  const added = await insertScrapedFiles("all")
  const cleanup = await runCleanup()
  console.log(`Platform ${platform} done. Added: ${added} | removed: ${cleanup.total}`)
  onProgress?.({ status: "done", platform, added, removed: cleanup })
  return { platform, added, cleanup }
}

export { PLATFORMS }

// Run one full refresh pass across all platforms, one at a time, with a short
// politeness delay between them. Used by the background stale-data scheduler
// so the whole dataset gets freshened without hammering the source sites.
export async function runFullCycle(onProgress) {
  const results = []
  const pauseMs = 15000
  for (let i = 0; i < PLATFORMS.length; i++) {
    const platform = PLATFORMS[i]
    onProgress?.({ status: "cycle-platform", platform, index: i + 1, total: PLATFORMS.length })
    const result = await scrapeOnePlatform(platform, i + 1, PLATFORMS.length, onProgress)
    results.push(result)
    if (i < PLATFORMS.length - 1) {
      await new Promise((r) => setTimeout(r, pauseMs))
    }
  }
  return results
}
