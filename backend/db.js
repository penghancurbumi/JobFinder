import sqlite3 from 'sqlite3'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const dbPath = path.join(__dirname, 'jobs.sqlite')

// Initialize SQLite database
const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error('Error opening SQLite database:', err.message)
  } else {
    console.log('Connected to SQLite database.')

    // Performance tuning: WAL allows concurrent reads/writes, NORMAL speeds up commits
    db.run("PRAGMA journal_mode = WAL", () => {})
    db.run("PRAGMA synchronous = NORMAL", () => {})
    db.run("PRAGMA cache_size = -16000", () => {})
    db.run("PRAGMA mmap_size = 268435456", () => {})

    // Create jobs table if it doesn't exist
    db.run(`
      CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        company TEXT,
        location TEXT,
        jobType TEXT,
        workType TEXT,
        expertise TEXT,
        source TEXT,
        url TEXT UNIQUE,
        description TEXT,
        postedDate TEXT,
        deadlineDate TEXT,
        salary TEXT
      )
    `, (err) => {
      if (err) console.error('Error creating table:', err.message)
    })

    // Add workType column if missing (migration for existing DBs)
    db.run("ALTER TABLE jobs ADD COLUMN workType TEXT", () => {})

    // Add lastSeenAt for expired-job pruning (migration for existing DBs).
    // Backfill so existing rows are treated as "seen just now" (prevents an
    // immediate mass-delete on the first cleanup after upgrade).
    db.run("ALTER TABLE jobs ADD COLUMN lastSeenAt TEXT", () => {})
    db.run("UPDATE jobs SET lastSeenAt = ? WHERE lastSeenAt IS NULL", [new Date().toISOString()], () => {})

    // Indexes for the most common filters/ordering
    db.run("CREATE INDEX IF NOT EXISTS idx_jobs_posted ON jobs(postedDate DESC, id DESC)", (err) => {
      if (err) console.error('Error creating index:', err.message)
    })
    db.run("CREATE INDEX IF NOT EXISTS idx_jobs_source ON jobs(source)", () => {})
    db.run("CREATE INDEX IF NOT EXISTS idx_jobs_jobtype ON jobs(jobType)", () => {})
    db.run("CREATE INDEX IF NOT EXISTS idx_jobs_worktype ON jobs(workType)", () => {})
    db.run("CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company)", () => {})
    db.run("CREATE INDEX IF NOT EXISTS idx_jobs_lastseen ON jobs(lastSeenAt)", () => {})

    db.run(`
      CREATE TABLE IF NOT EXISTS chat_sessions (
        session_id TEXT PRIMARY KEY,
        messages TEXT DEFAULT '[]',
        created_at TEXT DEFAULT (datetime('now')),
        updated_at TEXT DEFAULT (datetime('now'))
      )
    `, (err) => {
      if (err) console.error('Error creating chat_sessions table:', err.message)
    })
  }
})

// Promisified helper functions
export function runQuery(query, params = []) {
  return new Promise((resolve, reject) => {
    db.run(query, params, function (err) {
      if (err) reject(err)
      else resolve({ id: this.lastID, changes: this.changes })
    })
  })
}

export function fetchAll(query, params = []) {
  return new Promise((resolve, reject) => {
    db.all(query, params, (err, rows) => {
      if (err) reject(err)
      else resolve(rows)
    })
  })
}

export function fetchOne(query, params = []) {
  return new Promise((resolve, reject) => {
    db.get(query, params, (err, row) => {
      if (err) reject(err)
      else resolve(row)
    })
  })
}

// ---- In-memory cache ----
// The jobs table is small (thousands of rows). Loading it into memory once and
// serving reads from RAM removes almost all SQLite load from read requests.
let jobsCache = null

export function getJobsCache() {
  return jobsCache
}

export async function loadJobsCache() {
  jobsCache = await fetchAll("SELECT * FROM jobs")
  return jobsCache
}

export async function refreshJobsCache() {
  return loadJobsCache()
}

export function invalidateJobsCache() {
  jobsCache = null
}

// ---- Expired-job cleanup ----
// Delete jobs that no longer exist on the source platforms so the dataset
// stays bounded instead of accumulating forever.
//  - 404/410 detected during scraping (see NotFoundCollector middleware)
//  - hard age cap: posted too long ago
//  - not seen recently: absent from the top listing pages across scrape cycles

export async function deleteByUrls(urls) {
  if (!urls || !urls.length) return 0
  const placeholders = urls.map(() => "?").join(",")
  const res = await runQuery(`DELETE FROM jobs WHERE url IN (${placeholders})`, urls)
  return res.changes
}

// Same listing can reappear under a new URL (sites re-post jobs / rotate URLs).
// Match on normalized title+company+location so re-listings don't bloat the DB.
export async function findDuplicate(title, company, location) {
  return fetchOne(
    `SELECT id, url FROM jobs
      WHERE lower(trim(title)) = ? AND lower(trim(company)) = ?
        AND lower(trim(location)) = ?
      ORDER BY id DESC LIMIT 1`,
    [
      String(title || "").trim().toLowerCase(),
      String(company || "").trim().toLowerCase(),
      String(location || "").trim().toLowerCase(),
    ]
  )
}

export async function deleteExpiredJobs({
  maxAgeDays = 90,
  notSeenDays = 30,
  notSeenMinAgeDays = 7,
} = {}) {
  const iso = (offsetDays) => {
    const d = new Date()
    d.setDate(d.getDate() - offsetDays)
    return d.toISOString().substring(0, 10)
  }
  const ageRes = await runQuery(
    "DELETE FROM jobs WHERE postedDate IS NOT NULL AND postedDate != '' AND postedDate < ?",
    [iso(maxAgeDays)]
  )
  const notSeenRes = await runQuery(
    `DELETE FROM jobs
       WHERE lastSeenAt IS NOT NULL AND lastSeenAt != '' AND lastSeenAt < ?
         AND postedDate IS NOT NULL AND postedDate != '' AND postedDate < ?`,
    [iso(notSeenDays), iso(notSeenMinAgeDays)]
  )
  return { age: ageRes.changes, notSeen: notSeenRes.changes }
}

export default db
