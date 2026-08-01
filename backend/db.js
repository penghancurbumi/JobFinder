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

    // Indexes for the most common filters/ordering
    db.run("CREATE INDEX IF NOT EXISTS idx_jobs_posted ON jobs(postedDate DESC, id DESC)", (err) => {
      if (err) console.error('Error creating index:', err.message)
    })
    db.run("CREATE INDEX IF NOT EXISTS idx_jobs_source ON jobs(source)", () => {})
    db.run("CREATE INDEX IF NOT EXISTS idx_jobs_jobtype ON jobs(jobType)", () => {})
    db.run("CREATE INDEX IF NOT EXISTS idx_jobs_worktype ON jobs(workType)", () => {})
    db.run("CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company)", () => {})

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

export default db
