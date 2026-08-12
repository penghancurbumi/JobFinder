# Tandai Lowongan "Ditutup" — Implementation Plan

> **Untuk pekerja agentic:** WAJIB SUB-SKILL: gunakan superpowers:subagent-driven-development (disarankan) atau superpowers:executing-plans untuk mengimplementasikan plan ini task per task. Step memakai syntax checkbox (`- [ ]`) untuk penelusuran.

**Goal:** Mendeteksi lowongan yang ditutup penyedia (saat scrape, via konten halaman detail) lalu menandainya `isClosed=1` di DB; lowongan "Ditutup" disembunyikan dari daftar default, dengan toggle untuk menampilkannya, badge "Ditutup", dan auto-balik aktif jika lowongan muncul terbuka lagi.

**Architecture:** Tiga lapisan — (1) Scrapy mendeteksi penanda "closed" pada halaman detail (404/410 atau konten) dan menulis URL ke file; (2) backend Node membaca file itu, menandai `isClosed=1` (bukan menghapus), dan mereset saat lowongan terlihat terbuka lagi lewat upsert; (3) frontend memfilter/menandai/urutan via `showClosed`.

**Tech Stack:** Python/Scrapy (middleware + spider), Node.js/Express/SQLite (backend), Vue 3/Vite (frontend).

## Global Constraints

- **Perilaku 404 berubah:** deteksi 404/410 sekarang **menandai** `isClosed=1`, bukan menghapus. Cleanup lain (umur, not-seen, duplikat, kualitas buruk) tetap menghapus.
- **Auto-balik aktif:** upsert `ON CONFLICT(url)` dan cabang duplikat harus mereset `isClosed=0, closedAt=NULL` saat lowongan kembali terlihat.
- **Kolom baru:** `isClosed INTEGER DEFAULT 0` dan `closedAt TEXT` pada tabel `jobs`; wajib backfill `0` dan index `idx_jobs_closed`.
- **Python interpreter tetap:** `C:\Users\Muhammad Al Fakhreza\AppData\Local\Python\bin\python.exe` (bukan `python` di PATH).
- **Frontend filter lewat HTTP `/api/jobs`** (bukan socket `filter-jobs`), tapi socket handler tetap ikut diperbarui untuk konsistensi.
- **Tidak ada test framework Node** — verifikasi Node memakai `node --check` + skrip verifikasi sekali pakai di temp dir (`C:\Users\MUHAMM~1\AppData\Local\Temp\opencode`).
- **Python test** memakai `unittest` bawaan (tanpa install tambahan); scrapy 2.17.0 sudah terpasang.
- Konvensi file mengikuti struktur eksisting; tidak ada restrukturisasi.

---

### Task 1: Migrasi DB + helper `markClosedUrls` (`backend/db.js`)

**Files:**
- Modify: `backend/db.js` (migration di blok init, helper baru di bagian cleanup)

**Interfaces:**
- Produces: kolom `jobs.isClosed` (0/1), `jobs.closedAt`; fungsi ekspor `markClosedUrls(urls: string[]) => Promise<number>` (jumlah baris yang berubah).

- [ ] **Step 1: Tulis skrip verifikasi** `C:\Users\MUHAMM~1\AppData\Local\Temp\opencode\verify_t1.mjs`

```js
import { runQuery, fetchOne, markClosedUrls, deleteByUrls } from "file:///D:/job-scrapper/backend/db.js"

const U = "https://example.com/verify-t1-job"
async function main() {
  const cols = await (await import("file:///D:/job-scrapper/backend/db.js")).fetchAll("PRAGMA table_info(jobs)")
  const names = cols.map((c) => c.name)
  if (!names.includes("isClosed") || !names.includes("closedAt")) throw new Error("columns missing")
  await runQuery("INSERT OR IGNORE INTO jobs (title, company, url, isClosed) VALUES ('VerifyT1','C','" + U + "',0)")
  const changed = await markClosedUrls([U])
  const row = await fetchOne("SELECT isClosed, closedAt FROM jobs WHERE url='" + U + "'")
  await deleteByUrls([U])
  console.log({ columns: names.filter((n) => n === "isClosed" || n === "closedAt"), changed, row, ok: changed === 1 && row.isClosed === 1 && !!row.closedAt })
  if (changed !== 1 || row.isClosed !== 1 || !row.closedAt) process.exit(1)
}
main().catch((e) => { console.error(e); process.exit(1) })
```

- [ ] **Step 2: Jalankan verifikasi (harus GAGAL karena `markClosedUrls` belum ada)**

Run (dari `D:\job-scrapper\backend`): `node C:\Users\MUHAMM~1\AppData\Local\Temp\opencode\verify_t1.mjs`
Expected: error `markClosedUrls is not exported` / import error.

- [ ] **Step 3: Implementasi migration.** Di `backend/db.js`, tepat setelah blok backfill `lastSeenAt` (baris ~49), tambahkan:

```js
    // Closed-listing markers: jobs closed by the provider are flagged, not deleted
    // (migration for existing DBs).
    db.run("ALTER TABLE jobs ADD COLUMN isClosed INTEGER DEFAULT 0", () => {})
    db.run("ALTER TABLE jobs ADD COLUMN closedAt TEXT", () => {})
    db.run("UPDATE jobs SET isClosed = 0 WHERE isClosed IS NULL", () => {})
    db.run("CREATE INDEX IF NOT EXISTS idx_jobs_closed ON jobs(isClosed)", () => {})
```

- [ ] **Step 4: Implementasi helper.** Tambahkan setelah `deleteByUrls` (baris ~206):

```js
// Flag jobs whose detail pages are gone or show a "closed" marker. Used by
// markClosedJobs() in scrapers/index.js (replaces the old delete behaviour).
export async function markClosedUrls(urls) {
  if (!urls || !urls.length) return 0
  const now = new Date().toISOString()
  const placeholders = urls.map(() => "?").join(",")
  const res = await runQuery(
    `UPDATE jobs SET isClosed = 1, closedAt = ? WHERE url IN (${placeholders}) AND isClosed = 0`,
    [now, ...urls]
  )
  return res.changes
}
```

- [ ] **Step 5: Jalankan verifikasi (harus PASS)**

Run (dari `D:\job-scrapper\backend`): `node C:\Users\MUHAMM~1\AppData\Local\Temp\opencode\verify_t1.mjs`
Expected: `ok: true`, `changed: 1`, `row.isClosed: 1`, `closedAt` terisi.

- [ ] **Step 6: Syntax check**

Run: `node --check db.js` (dari `D:\job-scrapper\backend`)
Expected: tidak ada output (sukses).

- [ ] **Step 7: Commit**

```bash
git add backend/db.js
git commit -m "feat: tambah kolom isClosed/closedAt + helper markClosedUrls"
```

---

### Task 2: `markClosedJobs()` + reset saat terlihat terbuka (`backend/scrapers/index.js`)

**Files:**
- Modify: `backend/scrapers/index.js` (import, konstanta, ganti `deleteNotFoundJobs`, `runCleanup`, upsert, cabang duplikat)

**Interfaces:**
- Consumes: `markClosedUrls` (Task 1)
- Produces: `markClosedJobs() => Promise<number>`; `runCleanup()` sekarang me-return `{ closedMarked, age, notSeen, duplicates, unclear, total }`.

- [ ] **Step 1: Tulis skrip verifikasi** `C:\Users\MUHAMM~1\AppData\Local\Temp\opencode\verify_t2.mjs`

```js
import fs from "fs/promises"
import path from "path"
import { runQuery, fetchOne, deleteByUrls } from "file:///D:/job-scrapper/backend/db.js"
import { markClosedJobs } from "file:///D:/job-scrapper/backend/scrapers/index.js"

const EXPORTS = "D:/job-scrapper/backend/scrapping-job/exports/json"
const U1 = "https://example.com/verify-t2-a"
const U2 = "https://example.com/verify-t2-b"
async function main() {
  await runQuery("INSERT OR IGNORE INTO jobs (title, company, url, isClosed) VALUES ('T2A','C','" + U1 + "',0)")
  await runQuery("INSERT OR IGNORE INTO jobs (title, company, url, isClosed) VALUES ('T2B','C','" + U2 + "',0)")
  await fs.writeFile(path.join(EXPORTS, "closed.txt"), U1 + "\n")
  await fs.writeFile(path.join(EXPORTS, "not_found.txt"), U2 + "\n")
  const marked = await markClosedJobs()
  const r1 = await fetchOne("SELECT isClosed FROM jobs WHERE url='" + U1 + "'")
  const r2 = await fetchOne("SELECT isClosed FROM jobs WHERE url='" + U2 + "'")
  const listing = await fs.readdir(EXPORTS)
  const filesGone = !listing.includes("closed.txt") && !listing.includes("not_found.txt")
  await deleteByUrls([U1, U2])
  console.log({ marked, r1, r2, filesGone, ok: marked === 2 && r1.isClosed === 1 && r2.isClosed === 1 && filesGone })
  if (marked !== 2 || r1.isClosed !== 1 || r2.isClosed !== 1 || !filesGone) process.exit(1)
}
main().catch((e) => { console.error(e); process.exit(1) })
```

- [ ] **Step 2: Jalankan verifikasi (harus GAGAL)**

Run (dari `D:\job-scrapper\backend`): `node C:\Users\MUHAMM~1\AppData\Local\Temp\opencode\verify_t2.mjs`
Expected: import error `markClosedJobs is not exported`.

- [ ] **Step 3: Implementasi konstanta & import.** Ubah baris 4 dan 9:

```js
import { runQuery, deleteByUrls, deleteExpiredJobs, findDuplicate, deleteDuplicateJobs, deleteBadQualityJobs, isValidJobText, markClosedUrls } from "../db.js"
```
```js
const NOT_FOUND_FILE = path.join(EXPORTS_DIR, "not_found.txt")
const CLOSED_FILE = path.join(EXPORTS_DIR, "closed.txt")
```

- [ ] **Step 4: Ganti `deleteNotFoundJobs` dengan `markClosedJobs`** (baris 131–146):

```js
// Flag jobs whose detail pages returned 404/410 or showed closed content
// instead of deleting them. The Scrapy NotFoundCollectorMiddleware appends
// 404 URLs to not_found.txt and content-closed URLs to closed.txt.
export async function markClosedJobs() {
  const urls = new Set()
  for (const file of [NOT_FOUND_FILE, CLOSED_FILE]) {
    try {
      const content = await fs.readFile(file, "utf-8")
      content.split(/\r?\n/).map((l) => l.trim()).filter(Boolean).forEach((u) => urls.add(u))
      await fs.unlink(file)
    } catch (e) {
      if (e.code !== "ENOENT") console.error(`Error reading ${file}:`, e.message)
    }
  }
  if (!urls.size) return 0
  const marked = await markClosedUrls([...urls])
  if (marked) console.log(`Closed cleanup: ${marked} job(s) marked closed (${urls.size} URL checked)`)
  return marked
}
```

- [ ] **Step 5: Perbarui `runCleanup`** (baris 148–162):

```js
// Flag jobs that are no longer on the source platforms (404/closed) and remove
// jobs past the age cap, absent from recent scrape cycles, exact duplicates, or
// of unclear quality (URL-as-title, non-Latin scripts).
export async function runCleanup() {
  const closedMarked = await markClosedJobs()
  const removedExpired = await deleteExpiredJobs(EXPIRED_OPTIONS)
  const removedDupes = await deleteDuplicateJobs()
  const removedBad = await deleteBadQualityJobs()
  const total = closedMarked + removedExpired.age + removedExpired.notSeen + removedDupes + removedBad
  console.log(
    `Cleanup done: ${closedMarked} closed-marked, ${removedExpired.age} age-expired, ` +
    `${removedExpired.notSeen} not-seen, ${removedDupes} duplicates, ${removedBad} unclear-quality (total ${total})`
  )
  return { closedMarked, ...removedExpired, duplicates: removedDupes, unclear: removedBad, total }
}
```

- [ ] **Step 6: Reset `isClosed` pada upsert** (baris 83–94) — tambahkan dua baris di klausa `ON CONFLICT`:

```sql
            ON CONFLICT(url) DO UPDATE SET
              jobType = CASE WHEN excluded.jobType != 'Full-time' THEN excluded.jobType ELSE jobType END,
              workType = CASE WHEN excluded.workType != 'On-site' THEN excluded.workType ELSE workType END,
              description = CASE WHEN excluded.description != '' THEN excluded.description ELSE description END,
              salary = CASE WHEN excluded.salary != '' THEN excluded.salary ELSE salary END,
              postedDate = excluded.postedDate,
              lastSeenAt = excluded.lastSeenAt,
              isClosed = 0,
              closedAt = NULL
```

- [ ] **Step 7: Reset `isClosed` pada cabang duplikat** (baris 63–67):

```js
          if (dup) {
            await runQuery("UPDATE jobs SET lastSeenAt = ?, isClosed = 0, closedAt = NULL WHERE id = ?", [lastSeenAt, dup.id])
            skipped++
            continue
          }
```

- [ ] **Step 8: Jalankan verifikasi (harus PASS)**

Run (dari `D:\job-scrapper\backend`): `node C:\Users\MUHAMM~1\AppData\Local\Temp\opencode\verify_t2.mjs`
Expected: `ok: true`, `marked: 2`, `filesGone: true`.

- [ ] **Step 9: Syntax check**

Run: `node --check scrapers/index.js` (dari `D:\job-scrapper\backend`)
Expected: tidak ada output.

- [ ] **Step 10: Commit**

```bash
git add backend/scrapers/index.js
git commit -m "feat: tandai lowongan ditutup (404/closed) alih-alih menghapus + reset saat terbuka"
```

---

### Task 3: `getFilteredJobs(showClosed)` + pass-through API (`backend/server.js`)

**Files:**
- Modify: `backend/server.js` (getFilteredJobs, socket `filter-jobs`, `GET /api/jobs`)

**Interfaces:**
- Consumes: kolom `isClosed` (Task 1)
- Produces: `getFilteredJobs(..., showClosed=false)` yang me-return `{ jobs, total, page, limit, totalPages, closedCount }`; query param `showClosed` di `/api/jobs` dan event `filter-jobs`.

- [ ] **Step 1: Tulis skrip verifikasi** `C:\Users\MUHAMM~1\AppData\Local\Temp\opencode\verify_t3.mjs` (seed + cek API via fetch ke server yang berjalan dengan kode baru)

```js
import { runQuery, deleteByUrls } from "file:///D:/job-scrapper/backend/db.js"

const U = "https://example.com/verify-t3-job"
async function main() {
  await runQuery("INSERT OR IGNORE INTO jobs (title, company, url, isClosed, postedDate) VALUES ('VerifyT3','C','" + U + "',1,'2099-01-01')")
  const hide = await (await fetch("http://localhost:3000/api/jobs?search=VerifyT3")).json()
  const show = await (await fetch("http://localhost:3000/api/jobs?search=VerifyT3&showClosed=true")).json()
  await deleteByUrls([U])
  const hiddenOk = hide.total === 0
  const shownOk = show.total === 1 && show.jobs[0].url === U && show.closedCount === 1
  console.log({ hide, show, ok: hiddenOk && shownOk })
  if (!hiddenOk || !shownOk) process.exit(1)
}
main().catch((e) => { console.error(e); process.exit(1) })
```

- [ ] **Step 2: Implementasi `getFilteredJobs`.** Ubah signature (baris 93):

```js
async function getFilteredJobs(search = "", bidang = "all", tipe = "all", sortBy = "newest", location = "", experience = "", hasSalary = false, education = "all", page = 1, limit = 200, showClosed = false) {
```

Tambahkan filter di dalam callback `.filter` (sebelum `return true`, baris ~171):

```js
    if (!showClosed && j.isClosed) return false

    return true
```

Ganti blok sort (baris 174–183):

```js
  const closedRank = (j) => (j.isClosed ? 1 : 0)
  const cmpAsc = (a, b) => (a > b ? 1 : a < b ? -1 : 0)
  if (sortBy === "az") {
    jobs.sort((a, b) => closedRank(a) - closedRank(b) || cmpAsc(a.title || "", b.title || ""))
  } else if (sortBy === "za") {
    jobs.sort((a, b) => closedRank(a) - closedRank(b) || cmpAsc(b.title || "", a.title || ""))
  } else if (sortBy === "oldest") {
    jobs.sort((a, b) => closedRank(a) - closedRank(b) || cmpAsc(a.postedDate || "", b.postedDate || "") || (a.id - b.id))
  } else {
    jobs.sort((a, b) => closedRank(a) - closedRank(b) || cmpAsc(b.postedDate || "", a.postedDate || "") || (b.id - a.id))
  }

  const closedCount = jobs.filter((j) => j.isClosed).length
```

Ganti baris return (187):

```js
  return { jobs: pageJobs, total, page, limit, totalPages: Math.ceil(total / limit), closedCount }
```

- [ ] **Step 3: Pass-through socket `filter-jobs`** (baris ~211):

```js
  socket.on("filter-jobs", async ({ search, bidang, tipe, sortBy, location, experience, hasSalary, education, page, limit, showClosed }) => {
    const result = await getFilteredJobs(search, bidang, tipe, sortBy, location, experience, hasSalary, education, page, limit, showClosed)
    socket.emit("jobs-updated", result)
  })
```

- [ ] **Step 4: Pass-through `GET /api/jobs`** (baris 261–276):

```js
app.get("/api/jobs", async (req, res) => {
  const { search, bidang, tipe, sortBy, location, experience, hasSalary, education, page, limit, showClosed } = req.query
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
    limit,
    showClosed === 'true' || showClosed === true
  )
  res.json(result)
})
```

- [ ] **Step 5: Syntax check**

Run (dari `D:\job-scrapper\backend`): `node --check server.js`
Expected: tidak ada output.

- [ ] **Step 6: Verifikasi API.** Pastikan backend baru berjalan (jika port 3000 belum ada: `Start-Process node -ArgumentList 'server.js' -WorkingDirectory 'D:\job-scrapper\backend' -NoNewWindow`), lalu jalankan:

Run (dari `D:\job-scrapper\backend`): `node C:\Users\MUHAMM~1\AppData\Local\Temp\opencode\verify_t3.mjs`
Expected: `ok: true` — `hide.total === 0`, `show.total === 1`, `show.closedCount === 1`.

- [ ] **Step 7: Commit**

```bash
git add backend/server.js
git commit -m "feat: filter/urutkan lowongan ditutup via showClosed + closedCount di API"
```

---

### Task 4: Deteksi konten "closed" di Scrapy (Python)

**Files:**
- Modify: `backend/scrapping-job/job_scraper/constants.py`
- Create: `backend/scrapping-job/job_scraper/services/closed_detector.py`
- Create: `backend/scrapping-job/tests/test_closed_detector.py`
- Modify: `backend/scrapping-job/job_scraper/spiders/base_spider.py`
- Modify: `backend/scrapping-job/job_scraper/middlewares.py`

**Interfaces:**
- Produces: `has_closed_content(text: str, platform: str | None = None) -> bool`; middleware menulis `exports/json/closed.txt` untuk detail 200 yang kontennya closed; request detail punya `meta["is_detail"] = True`.

- [ ] **Step 1: Tulis test GAGAL** — create `backend/scrapping-job/tests/test_closed_detector.py`:

```python
import unittest

from job_scraper.services.closed_detector import has_closed_content


class TestClosedDetector(unittest.TestCase):
    def test_general_marker_indonesian(self):
        self.assertTrue(has_closed_content("<html><body>Lowongan telah ditutup oleh perusahaan</body></html>"))

    def test_general_marker_english(self):
        self.assertTrue(has_closed_content("This job is no longer accepting applications"))

    def test_platform_marker_jobstreet(self):
        self.assertTrue(has_closed_content('data-automation="jobClosedHeader"', "jobstreet"))

    def test_open_job_not_detected(self):
        self.assertFalse(has_closed_content("Software Engineer - Jakarta - Full-time - Apply now"))

    def test_case_insensitive(self):
        self.assertTrue(has_closed_content("This position is NO LONGER AVAILABLE"))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Jalankan test (harus GAGAL)**

Run (dari `D:\job-scrapper\backend\scrapping-job`): `& "C:\Users\Muhammad Al Fakhreza\AppData\Local\Python\bin\python.exe" -m unittest tests.test_closed_detector -v`
Expected: error import `No module named 'job_scraper.services.closed_detector'` atau `ModuleNotFoundError`.

- [ ] **Step 3: Implementasi marker** — tambahkan di akhir `backend/scrapping-job/job_scraper/constants.py`:

```python
# Phrases (matched case-insensitively on plain page text) that indicate a job
# detail page is no longer accepting applications even though HTTP is 200.
CLOSED_MARKERS: dict[str, list[str]] = {
    "general": [
        "lowongan telah ditutup",
        "lowongan ini telah ditutup",
        "lowongan telah ditutup oleh",
        "lowongan ditutup",
        "lowongan telah berakhir",
        "lowongan ini telah berakhir",
        "tidak menerima lamaran",
        "posisi telah ditutup",
        "lowongan ini tidak tersedia",
        "position closed",
        "this position has been closed",
        "this position is closed",
        "job closed",
        "this job is closed",
        "this job has been closed",
        "no longer accepting applications",
        "is no longer accepting applications",
        "not accepting applications",
        "no longer available",
        "position is no longer available",
        "this position is no longer available",
        "job is no longer available",
        "this job is no longer available",
        "vacancy closed",
        "this vacancy has been filled",
        "application closed",
        "jobClosedHeader",
    ],
    "jobstreet": [
        "this job is no longer accepting applications",
    ],
    "linkedin": [
        "this position is no longer available",
        "no longer accepting applications",
    ],
}
```

- [ ] **Step 4: Implementasi detector** — create `backend/scrapping-job/job_scraper/services/closed_detector.py`:

```python
import re

from job_scraper.constants import CLOSED_MARKERS

_TAG_RE = re.compile(r"<[^>]+>")


def _plain(text: str) -> str:
    return _TAG_RE.sub(" ", text or "").lower()


def has_closed_content(text: str, platform: str | None = None) -> bool:
    haystack = _plain(text)
    for marker in CLOSED_MARKERS.get("general", []):
        if marker in haystack:
            return True
    if platform:
        for marker in CLOSED_MARKERS.get(platform, []):
            if marker in haystack:
                return True
    return False
```

- [ ] **Step 5: Jalankan test (harus PASS)**

Run (dari `D:\job-scrapper\backend\scrapping-job`): `& "C:\Users\Muhammad Al Fakhreza\AppData\Local\Python\bin\python.exe" -m unittest tests.test_closed_detector -v`
Expected: `Ran 5 tests ... OK`.

- [ ] **Step 6: Tandai request detail** — di `backend/scrapping-job/job_scraper/spiders/base_spider.py`, `_make_detail_request` (baris 69–77):

```python
    def _make_detail_request(self, url: str, callback, meta: dict | None = None) -> Request:
        req_meta = dict(
            playwright=True,
            playwright_page_goto_kwargs={"wait_until": "domcontentloaded", "timeout": 30000},
            playwright_page_methods=[PageMethod("wait_for_timeout", 2000)],
            is_detail=True,
        )
        if meta:
            req_meta.update(meta)
        return Request(url=url, callback=callback, meta=req_meta)
```

- [ ] **Step 7: Deteksi konten di middleware** — `backend/scrapping-job/job_scraper/middlewares.py`, kelas `NotFoundCollectorMiddleware`:

Ubah `__init__` (tambah state & file closed):

```python
    def __init__(self) -> None:
        export_dir = os.getenv("EXPORT_DIR", "exports")
        self._file = os.path.join(export_dir, "json", "not_found.txt")
        self._closed_file = os.path.join(export_dir, "json", "closed.txt")
        self._urls: set[str] = set()
        self._closed: set[str] = set()
```

Ubah `process_response`:

```python
    def process_response(self, request: Request, response: Response, spider: Spider) -> Response:
        if response.status in (404, 410):
            self._urls.add(request.url)
        elif request.meta.get("is_detail") and has_closed_content(response.text, spider.name):
            self._closed.add(request.url)
        return response
```

Ubah `spider_closed` (tulis kedua file; blok 404 lama dibungkus helper):

```python
    def spider_closed(self, spider: Spider) -> None:
        self._write_urls(self._file, self._urls, "not-found", spider)
        self._write_urls(self._closed_file, self._closed, "closed-content", spider)

    def _write_urls(self, filepath: str, urls: set[str], label: str, spider: Spider) -> None:
        if not urls:
            return
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "a", encoding="utf-8") as f:
                for url in sorted(urls):
                    f.write(url + "\n")
            logger.info(
                "NotFoundCollectorMiddleware: wrote %d %s URL(s) for %s",
                len(urls), label, spider.name,
            )
        except Exception as e:
            logger.error("NotFoundCollectorMiddleware: failed to write %s file: %s", label, e)
```

Tambahkan import di bagian atas `middlewares.py`:

```python
from job_scraper.services.closed_detector import has_closed_content
```

- [ ] **Step 8: Syntax check**

Run (dari `D:\job-scrapper\backend\scrapping-job`): `& "C:\Users\Muhammad Al Fakhreza\AppData\Local\Python\bin\python.exe" -m py_compile job_scraper/services/closed_detector.py job_scraper/constants.py job_scraper/spiders/base_spider.py job_scraper/middlewares.py`
Expected: tidak ada output.

- [ ] **Step 9: Jalankan test lagi (regression)**

Run (dari `D:\job-scrapper\backend\scrapping-job`): `& "C:\Users\Muhammad Al Fakhreza\AppData\Local\Python\bin\python.exe" -m unittest tests.test_closed_detector -v`
Expected: `Ran 5 tests ... OK`.

- [ ] **Step 10: Commit**

```bash
git add backend/scrapping-job/job_scraper/constants.py backend/scrapping-job/job_scraper/services/closed_detector.py backend/scrapping-job/tests/test_closed_detector.py backend/scrapping-job/job_scraper/spiders/base_spider.py backend/scrapping-job/job_scraper/middlewares.py
git commit -m "feat: deteksi konten lowongan ditutup di Scrapy (closed.txt + is_detail)"
```

---

### Task 5: UI toggle, badge, dan urutan (`frontend/src/views/JobsPage.vue`)

**Files:**
- Modify: `frontend/src/views/JobsPage.vue`

**Interfaces:**
- Consumes: `closedCount`, `showClosed` dari `/api/jobs` (Task 3); field `isClosed` di tiap job.

- [ ] **Step 1: Tulis cek verifikasi** (build + cek teks pada dist). Tulis `C:\Users\MUHAMM~1\AppData\Local\Temp\opencode\verify_t5.ps1`:

```powershell
$built = $false
if (Test-Path "D:\job-scrapper\frontend\dist\index.html") { $built = $true }
$src = Get-Content "D:\job-scrapper\frontend\src\views\JobsPage.vue" -Raw
$checks = @(
  $src.Contains("showClosed = ref(false)"),
  $src.Contains("closedCount = ref(0)"),
  $src.Contains("Tampilkan lowongan ditutup"),
  $src.Contains("Ditutup"),
  $src.Contains("showClosed: showClosed.value ? 'true' : 'false'")
)
Write-Output "built=$built checks=$($checks -join ',')"
if (-not $built -or $checks -contains $false) { exit 1 }
```

- [ ] **Step 2: Implementasi state.** Tambahkan di dekat `hasSalary` (baris ~335):

```js
const showClosed = ref(false)
const closedCount = ref(0)
```

- [ ] **Step 3: Watch + fetch.** Ubah array `watch` (baris 494) menjadi:

```js
watch([activeTipe, searchQuery, locationQuery, experienceLevel, educationlevel, hasSalary, sortBy, showClosed], () => {
```

Di `fetchPage` (baris 436–455), tambahkan param & simpan `closedCount`:

```js
    showClosed: showClosed.value ? 'true' : 'false',
```
```js
      total.value = data.total || 0
      totalPages.value = data.totalPages || 0
      closedCount.value = data.closedCount || 0
      page.value = p
```

- [ ] **Step 4: `applyJobsPayload`.** Tambahkan satu baris (setelah `page.value = data.page || 1`):

```js
  closedCount.value = data.closedCount || 0
```

- [ ] **Step 5: `resetFilters`.** Tambahkan:

```js
  showClosed.value = false
  closedCount.value = 0
```

- [ ] **Step 6: Toggle di sidebar.** Setelah blok "Rentang Gaji" (baris 68–74), tambahkan:

```html
          <div class="mt-xl flex flex-col">
            <label class="flex items-center gap-[8px] font-normal text-[13px] normal-case cursor-pointer text-on-dark-mute">
              <input type="checkbox" v-model="showClosed" class="w-[12px] h-[12px] min-h-[12px] cursor-pointer" />
              Tampilkan lowongan ditutup{{ closedCount ? ` (${closedCount})` : '' }}
            </label>
          </div>
```

- [ ] **Step 7: Badge di kartu.** Di dalam `<div class="flex gap-[6px] shrink-0 flex-wrap items-center">` (baris 118–125), tambahkan badge pertama:

```html
                    <span v-if="job.isClosed" class="bg-accent-danger/15 text-accent-danger border border-accent-danger/40 rounded-full px-[12px] py-[4px] text-[12px] font-semibold">
                      Ditutup
                    </span>
```

- [ ] **Step 8: Redupkan kartu.** Ubah class kartu (baris 106):

```html
              class="bg-surface-elevated rounded-md p-lg flex flex-col justify-between h-full border border-hairline-dark hover:border-white/20 transition-all duration-200 shadow-sm"
              :class="{ 'opacity-60': job.isClosed }"
```

- [ ] **Step 9: Build + verifikasi**

Run (dari `D:\job-scrapper\frontend`): `npm run build`
Expected: `✓ built` tanpa error.
Run: `powershell -File C:\Users\MUHAMM~1\AppData\Local\Temp\opencode\verify_t5.ps1`
Expected: `built=True checks=True,True,True,True,True`.

- [ ] **Step 10: Commit**

```bash
git add frontend/src/views/JobsPage.vue
git commit -m "feat: toggle + badge + urutan untuk lowongan ditutup di UI"
```

---

### Task 6: Verifikasi end-to-end

- [ ] **Step 1: Semua syntax check sekali lagi**

Run (dari `D:\job-scrapper\backend`): `node --check server.js; if ($?) { node --check db.js }; if ($?) { node --check scrapers/index.js }`
Expected: tanpa output.
Run (dari `D:\job-scrapper\backend\scrapping-job`): `& "C:\Users\Muhammad Al Fakhreza\AppData\Local\Python\bin\python.exe" -m unittest tests.test_closed_detector -v`
Expected: `OK`.

- [ ] **Step 2: Simulasi scrape nyata (opsional, JobStreet).** Pastikan backend berhenti dulu, lalu dari `D:\job-scrapper\backend` jalankan: `node --input-type=module -e "import { scrapeOnePlatform } from './scrapers/index.js'; const r = await scrapeOnePlatform('jobstreet', 1, 7, (e)=>console.log(e.message||JSON.stringify(e))); console.log(JSON.stringify(r, null, 2))"`
Expected: `Import done: ...` dan `Cleanup done: ... closed-marked ...`; log menampilkan pesan cleanup.

- [ ] **Step 3: Cek UI manual di browser.** Jalankan backend + `npm run dev` frontend:
  1. Pastikan daftar default tidak menampilkan lowongan "Ditutup".
  2. Centang "Tampilkan lowongan ditutup (N)" → kartu berbadge "Ditutup" muncul, diurutkan di bawah.
  3. Klik salah satu kartu → buka link di tab baru.
  4. (Jika tersedia data) setelah scrape berikutnya yang menemukan lowongan sama terbuka, centang toggle → badge hilang.

- [ ] **Step 4: Bersihkan temp scripts**

Run: `Remove-Item C:\Users\MUHAMM~1\AppData\Local\Temp\opencode\verify_t1.mjs, C:\Users\MUHAMM~1\AppData\Local\Temp\opencode\verify_t2.mjs, C:\Users\MUHAMM~1\AppData\Local\Temp\opencode\verify_t3.mjs, C:\Users\MUHAMM~1\AppData\Local\Temp\opencode\verify_t5.ps1 -ErrorAction SilentlyContinue`

---

## Self-Review

**Cakupan spec:** DB columns ✓ (T1), deteksi konten saat scrape ✓ (T4), tandai bukan hapus ✓ (T2), auto-balik aktif ✓ (T2 upsert + dup branch), default sembunyi + toggle + badge + urutan bawah ✓ (T3+T5), `closedCount` ✓ (T3+T5), `/api/jobs` pass-through ✓ (T3), socket `filter-jobs` konsisten ✓ (T3), verifikasi ✓ (T1–T6). Tidak ada celah.

**Placeholder scan:** Semua step berisi kode/command konkret; tidak ada TBD/TODO.

**Konsistensi tipe:** `markClosedUrls(urls)=>number` dipakai T2; `markClosedJobs()=>number` di T2; `closedCount` konsisten di respons API (T3) dan UI (T5); `has_closed_content(text, platform)` konsisten di T4; `showClosed` konsisten antara `/api/jobs` dan `fetchPage`. `deleteNotFoundJobs` dihapus T2 — tidak dipakai lagi (verifikasi: hanya dipakai di `runCleanup`).
