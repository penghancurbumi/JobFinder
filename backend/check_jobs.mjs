import sqlite3 from 'sqlite3'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const db = new sqlite3.Database(path.join(__dirname, 'jobs.sqlite'))

const threeDaysAgo = new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString()
const sevenDaysAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString()

db.get("SELECT COUNT(*) as total FROM jobs", (err, row) => {
  console.log('Total jobs di database:', row.total)
})

db.get("SELECT MIN(lastSeenAt) as oldest, MAX(lastSeenAt) as newest FROM jobs", (err, row) => {
  console.log('lastSeenAt terlama :', row.oldest)
  console.log('lastSeenAt terbaru :', row.newest)
})

db.get("SELECT COUNT(*) as stale FROM jobs WHERE lastSeenAt < ?", [threeDaysAgo], (err, row) => {
  console.log('Tidak terlihat > 3 hari (kemungkinan tutup):', row.stale)
})

db.all("SELECT title, company, source, lastSeenAt FROM jobs WHERE lastSeenAt < ? ORDER BY lastSeenAt ASC LIMIT 10", [sevenDaysAgo], (err, rows) => {
  console.log('\nContoh 10 lowongan paling lama tidak terlihat (> 7 hari):')
  if (!rows || rows.length === 0) {
    console.log('  Tidak ada')
  } else {
    rows.forEach(r => console.log(`  [${r.source}] ${r.title} - ${r.company} | lastSeen: ${r.lastSeenAt}`))
  }
  db.close()
})
