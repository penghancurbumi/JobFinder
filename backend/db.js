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

    // Link-health tracking: verifies stored URLs still resolve (not 404/410).
    // NULL linkStatus = never checked. linkCheckedAt drives re-check staleness.
    db.run("ALTER TABLE jobs ADD COLUMN linkStatus TEXT", () => {})
    db.run("ALTER TABLE jobs ADD COLUMN linkCheckedAt TEXT", () => {})
    db.run("CREATE INDEX IF NOT EXISTS idx_jobs_linkstatus ON jobs(linkStatus)", () => {})

    // Remove the discontinued closed-listing markers (isClosed/closedAt) from
    // databases created during the "mark-closed" iteration. The index must be
    // dropped first, otherwise ALTER TABLE ... DROP COLUMN fails. Errors are
    // ignored: on a fresh DB the columns never existed.
    db.run("DROP INDEX IF EXISTS idx_jobs_closed", () => {
      db.run("ALTER TABLE jobs DROP COLUMN isClosed", () => {
        db.run("ALTER TABLE jobs DROP COLUMN closedAt", () => {})
      })
    })

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

    // Persistent round-robin pointer for per-platform scraping. The next
    // platform to scrape is stored here so it survives restarts and is never
    // decided by the frontend. Seeded to start at jobstreet.
    db.run(`
      CREATE TABLE IF NOT EXISTS scraping_state (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        current_platform TEXT NOT NULL DEFAULT 'jobstreet',
        last_platform TEXT,
        status TEXT NOT NULL DEFAULT 'idle',
        last_run_at TEXT,
        total_jobs_scraped INTEGER DEFAULT 0,
        error_message TEXT
      )
    `, (err) => {
      if (err) console.error('Error creating scraping_state table:', err.message)
    })
    db.run(
      `INSERT OR IGNORE INTO scraping_state (id, current_platform, status) VALUES (1, 'jobstreet', 'idle')`,
      () => {}
    )
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

// ---- Data freshness / staleness ----
// Used to decide whether a background refresh is needed. A dataset is "stale"
// when some active job hasn't been re-seen within the last 24h (i.e. the top
// listing pages may have changed) — the background cycle then refreshes it.
export async function getDataStatus() {
  const totalRow = await fetchOne("SELECT COUNT(*) AS c FROM jobs")
  const lastSeenRow = await fetchOne(
    "SELECT MAX(lastSeenAt) AS max FROM jobs WHERE lastSeenAt IS NOT NULL AND lastSeenAt != ''"
  )
  const staleRow = await fetchOne(
    `SELECT COUNT(*) AS c FROM jobs
       WHERE lastSeenAt IS NOT NULL AND lastSeenAt != '' AND lastSeenAt < ?`,
    [new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString()]
  )
  return {
    total: totalRow?.c || 0,
    lastUpdatedAt: lastSeenRow?.max || null,
    staleCount: staleRow?.c || 0,
  }
}

// ---- Scraping state (persistent round-robin pointer) ----
export function getScrapingState() {
  return fetchOne("SELECT * FROM scraping_state WHERE id = 1")
}

export async function updateScrapingState(fields) {
  const allowed = [
    "current_platform",
    "last_platform",
    "status",
    "last_run_at",
    "total_jobs_scraped",
    "error_message",
  ]
  const set = []
  const params = []
  for (const key of allowed) {
    if (key in fields) {
      set.push(`${key} = ?`)
      params.push(fields[key])
    }
  }
  if (!set.length) return
  params.push(1)
  await runQuery(`UPDATE scraping_state SET ${set.join(", ")} WHERE id = ?`, params)
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

// ---- Link health (active/404 verification) ----
// linkStatus: 'active' (2xx), 'not_found' (404/410), 'unknown' (bot-blocked
// 401/403/429, 5xx, timeout — inconclusive, never treated as dead),
// NULL/'unchecked' (not verified yet).
export async function updateLinkStatus(url, status, checkedAt) {
  await runQuery(
    "UPDATE jobs SET linkStatus = ?, linkCheckedAt = ? WHERE url = ?",
    [status, checkedAt, url]
  )
}

// Never-checked rows first, then rows whose last check is older than
// staleDays, oldest check first — so repeated runs walk through the whole
// table evenly.
export async function getJobsToCheck(limit = 300, staleDays = 14) {
  const staleCutoff = new Date(Date.now() - staleDays * 24 * 60 * 60 * 1000).toISOString()
  return fetchAll(
    `SELECT id, url, source FROM jobs
      WHERE linkStatus IS NULL OR linkCheckedAt IS NULL OR linkCheckedAt < ?
      ORDER BY (linkCheckedAt IS NULL) DESC, linkCheckedAt ASC
      LIMIT ?`,
    [staleCutoff, limit]
  )
}

export async function getLinkCheckStats() {
  const rows = await fetchAll(
    "SELECT COALESCE(NULLIF(linkStatus, ''), 'unchecked') AS status, COUNT(*) AS c FROM jobs GROUP BY status"
  )
  const stats = { total: 0, active: 0, not_found: 0, unknown: 0, unchecked: 0 }
  for (const r of rows) {
    if (r.status in stats) stats[r.status] = r.c
    stats.total += r.c
  }
  return stats
}

// Remove jobs confirmed dead by the link checker after a grace period, so a
// temporary outage on the source site doesn't wipe good data.
export async function deleteDeadLinkJobs(maxAgeDays = 7) {
  const cutoff = new Date(Date.now() - maxAgeDays * 24 * 60 * 60 * 1000).toISOString()
  const res = await runQuery(
    `DELETE FROM jobs WHERE linkStatus = 'not_found' AND linkCheckedAt IS NOT NULL AND linkCheckedAt < ?`,
    [cutoff]
  )
  return res.changes
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

// ---- Data-quality cleanup ----
// Remove rows that are exact duplicates (same title+company+location+posted
// date+salary+deadline) keeping the most recently seen row of each group, and
// rows whose title/company/location are obviously garbage (URL-as-title,
// non-Latin scripts like Chinese/Japanese/Thai that don't belong on an
// Indonesian job board). These checks also run at scrape time (see
// scrapers/index.js) so bad data is rejected before it ever reaches the DB.

// Non-Latin script ranges we consider "unclear" for an Indonesian job site:
// CJK, Cyrillic, Arabic, Devanagari, Thai, Lao, Tibetan, Myanmar, Hangul Jamo.
export const NON_LATIN_RE =
  /[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uac00-\ud7af\uf900-\ufaff\u0400-\u04ff\u0600-\u06ff\u0900-\u097f\u0e00-\u0e7f\u0f00-\u0fff\u1000-\u109f\u1100-\u11ff]/

export const URL_RE = /^https?:\/\/[^\s]+$/i

export function isValidJobText(title, company, location) {
  const t = String(title || "").trim()
  const c = String(company || "").trim()
  const l = String(location || "").trim()
  if (!t || t.length < 3) return false
  if (URL_RE.test(t) || URL_RE.test(c)) return false
  return !NON_LATIN_RE.test(`${t} ${c} ${l}`)
}

export async function deleteDuplicateJobs() {
  const res = await runQuery(
    `DELETE FROM jobs WHERE id NOT IN (
       SELECT id FROM (
         SELECT id,
           ROW_NUMBER() OVER (
             PARTITION BY lower(trim(title)), lower(trim(company)), lower(trim(location)),
                          COALESCE(postedDate, ''), COALESCE(salary, ''), COALESCE(deadlineDate, '')
             ORDER BY lastSeenAt DESC, id ASC
           ) AS rn
         FROM jobs
       ) WHERE rn = 1
     )`
  )
  return res.changes
}

export async function deleteBadQualityJobs() {
  const rows = await fetchAll("SELECT id, title, company, location FROM jobs")
  const badIds = rows
    .filter((r) => !isValidJobText(r.title, r.company, r.location))
    .map((r) => r.id)
  if (!badIds.length) return 0
  const placeholders = badIds.map(() => "?").join(",")
  const res = await runQuery(`DELETE FROM jobs WHERE id IN (${placeholders})`, badIds)
  return res.changes
}

export default db
