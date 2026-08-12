# Hapus Langsung Lowongan Ditutup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Mengubah perilaku lowongan tutup dari "tandai + tampilkan via toggle" menjadi "hapus langsung dari DB", sambil mempertahankan deteksi konten di sisi Scrapy.

**Architecture:** Deteksi Scrapy (Task 4, tidak berubah) tetap menulis URL 404 ke `not_found.txt` dan URL ber-konten "closed" ke `closed.txt`. Node `runCleanup()` membaca kedua file dan **menghapus** baris via `deleteByUrls`. Semua artefak fitur "mark/show-closed" (`isClosed`/`closedAt`, `markClosedUrls`, `markClosedJobs`, `showClosed`, `closedCount`, toggle/badge UI) dihapus.

**Tech Stack:** Node 26 (ESM), Express + sqlite3 (Promise wrapper) di `backend/`, Vue 3 + Vite di `frontend/`, Scrapy di `backend/scrapping-job/`.

## Global Constraints

- Jangan ubah apa pun di `backend/scrapping-job/` — deteksi konten (`has_closed_content`, `closed.txt`) tetap seperti sekarang.
- `deleteByUrls(urls)` di `backend/db.js` adalah satu-satunya jalur penghapusan. Tanda tangannya: `(urls: string[]) => Promise<number>` (jumlah baris terhapus).
- Python interpreter: `C:\Users\Muhammad Al Fakhreza\AppData\Local\Python\bin\python.exe`.
- Semua perintah Node dijalankan dari `D:\job-scrapper\backend`; build frontend dari `D:\job-scrapper\frontend`.
- Jangan pakai `git add -A` / `git add .`. Stage file spesifik saja.
- Kolom DB terhapus via runtime migration di `db.js` saat startup (tidak pakai tool SQLite eksternal).
- Skema tabel baru (fresh DB) tidak memuat `isClosed`/`closedAt`.

---

### Task 1: Bersihkan schema + helper di `backend/db.js`

**Files:**
- Modify: `backend/db.js:51-56` (migrasi kolom closed → migrasi drop)
- Modify: `backend/db.js:215-226` (`markClosedUrls` → dihapus)

**Interfaces:**
- Consumes: tidak ada (task pertama).
- Produces: `deleteByUrls(urls)` tetap tersedia; `markClosedUrls` **dihilangkan**. Tidak ada lagi kolom `isClosed`/`closedAt`/index `idx_jobs_closed`.

- [ ] **Step 1: Ubah blok migrasi kolom closed menjadi migrasi drop**

Di `backend/db.js`, ganti blok berikut (baris 51–56):

```js
    // Closed-listing markers: jobs closed by the provider are flagged, not deleted
    // (migration for existing DBs).
    db.run("ALTER TABLE jobs ADD COLUMN isClosed INTEGER DEFAULT 0", () => {})
    db.run("ALTER TABLE jobs ADD COLUMN closedAt TEXT", () => {})
    db.run("UPDATE jobs SET isClosed = 0 WHERE isClosed IS NULL", () => {})
    db.run("CREATE INDEX IF NOT EXISTS idx_jobs_closed ON jobs(isClosed)", () => {})
```

dengan:

```js
    // Remove the discontinued closed-listing markers (isClosed/closedAt) from
    // databases created during the "mark-closed" iteration. The index must be
    // dropped first, otherwise ALTER TABLE ... DROP COLUMN fails. Errors are
    // ignored: on a fresh DB the columns never existed.
    db.run("DROP INDEX IF EXISTS idx_jobs_closed", () => {
      db.run("ALTER TABLE jobs DROP COLUMN isClosed", () => {
        db.run("ALTER TABLE jobs DROP COLUMN closedAt", () => {})
      })
    })
```

- [ ] **Step 2: Hapus helper `markClosedUrls`**

Di `backend/db.js`, hapus seluruh blok berikut (baris 215–226):

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

- [ ] **Step 3: Syntax check**

Run (dari `D:\job-scrapper\backend`): `node --check db.js`
Expected: tanpa output (exit 0).

- [ ] **Step 4: Verifikasi migrasi hidup**

Run (dari `D:\job-scrapper\backend`):
`node --input-type=module -e "const {fetchAll}=await import('./db.js'); const rows=await fetchAll('PRAGMA table_info(jobs)'); const names=rows.map(r=>r.name); console.log('has isClosed:', names.includes('isClosed'), '| has closedAt:', names.includes('closedAt')); if(names.includes('isClosed')||names.includes('closedAt')) process.exit(1)"`
Expected: `has isClosed: false | has closedAt: false`, exit 0.

> Catatan: jika backend sedang berjalan, prosesnya memegang koneksi DB terpisah. Migrasi di atas baru berjalan saat **modul db.js di-require**; verifikasi ini meng-require db.js langsung sehingga migrasi dieksekusi.

- [ ] **Step 5: Commit**

```bash
git add backend/db.js
git commit -m "chore: hapus kolom isClosed/closedAt + helper markClosedUrls (hape lowongan tutup)"
```

---

### Task 2: Ubah `scrapers/index.js` — mark menjadi hapus

**Files:**
- Modify: `backend/scrapers/index.js:4` (import)
- Modify: `backend/scrapers/index.js:65` (reset dup)
- Modify: `backend/scrapers/index.js:95-96` (reset upsert)
- Modify: `backend/scrapers/index.js:134-152` (`markClosedJobs` → `deleteClosedJobs`)
- Modify: `backend/scrapers/index.js:157-168` (`runCleanup`)

**Interfaces:**
- Consumes: `deleteByUrls(urls)` dari `../db.js`; konstanta `NOT_FOUND_FILE`, `CLOSED_FILE` (sudah ada, baris 9–10).
- Produces: `deleteClosedJobs() => Promise<number>` — membaca `not_found.txt` + `closed.txt`, menghapus URL, memunculkan file, mengembalikan jumlah terhapus. `runCleanup()` kini memanggil `deleteClosedJobs()`.

- [ ] **Step 1: Perbaiki import**

Di `backend/scrapers/index.js` baris 4, ganti:

```js
import { runQuery, deleteByUrls, deleteExpiredJobs, findDuplicate, deleteDuplicateJobs, deleteBadQualityJobs, isValidJobText, markClosedUrls } from "../db.js"
```

dengan:

```js
import { runQuery, deleteByUrls, deleteExpiredJobs, findDuplicate, deleteDuplicateJobs, deleteBadQualityJobs, isValidJobText } from "../db.js"
```

- [ ] **Step 2: Hapus reset `isClosed` pada branch duplikat**

Ganti (baris 64–68):

```js
          if (dup) {
            await runQuery("UPDATE jobs SET lastSeenAt = ?, isClosed = 0, closedAt = NULL WHERE id = ?", [lastSeenAt, dup.id])
            skipped++
            continue
          }
```

dengan:

```js
          if (dup) {
            await runQuery("UPDATE jobs SET lastSeenAt = ? WHERE id = ?", [lastSeenAt, dup.id])
            skipped++
            continue
          }
```

- [ ] **Step 3: Hapus reset `isClosed` pada `ON CONFLICT` upsert**

Ganti (baris 94–96):

```js
              postedDate = excluded.postedDate,
              lastSeenAt = excluded.lastSeenAt,
              isClosed = 0,
              closedAt = NULL
          `
```

dengan:

```js
              postedDate = excluded.postedDate,
              lastSeenAt = excluded.lastSeenAt
          `
```

- [ ] **Step 4: Ganti `markClosedJobs` → `deleteClosedJobs`**

Ganti seluruh blok (baris 134–152):

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

dengan:

```js
// Delete jobs whose detail pages returned 404/410 or showed closed content.
// The Scrapy NotFoundCollectorMiddleware appends 404 URLs to not_found.txt and
// content-closed URLs to closed.txt; both lists are turned into deletions.
export async function deleteClosedJobs() {
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
  const removed = await deleteByUrls([...urls])
  if (removed) console.log(`Closed/not-found cleanup: ${removed} job(s) removed (${urls.size} URL checked)`)
  return removed
}
```

- [ ] **Step 5: Update `runCleanup`**

Ganti (baris 157–168):

```js
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

dengan:

```js
export async function runCleanup() {
  const removedClosed = await deleteClosedJobs()
  const removedExpired = await deleteExpiredJobs(EXPIRED_OPTIONS)
  const removedDupes = await deleteDuplicateJobs()
  const removedBad = await deleteBadQualityJobs()
  const total = removedClosed + removedExpired.age + removedExpired.notSeen + removedDupes + removedBad
  console.log(
    `Cleanup done: ${removedClosed} closed/not-found removed, ${removedExpired.age} age-expired, ` +
    `${removedExpired.notSeen} not-seen, ${removedDupes} duplicates, ${removedBad} unclear-quality (total ${total})`
  )
  return { removedClosed, ...removedExpired, duplicates: removedDupes, unclear: removedBad, total }
}
```

- [ ] **Step 6: Syntax check + grep sisa**

Run (dari `D:\job-scrapper\backend`): `node --check scrapers/index.js`
Expected: tanpa output.

Run: `rg -n "markClosed|isClosed|closedAt" scrapers/index.js`
Expected: tanpa hasil (tidak ada baris).

- [ ] **Step 7: Commit**

```bash
git add backend/scrapers/index.js
git commit -m "feat: hapus langsung lowongan tutup/not-found (deleteClosedJobs) alih-alih menandai"
```

---

### Task 3: Hapus `showClosed`/`closedCount` dari `backend/server.js`

**Files:**
- Modify: `backend/server.js:93-194` (`getFilteredJobs`)
- Modify: `backend/server.js:217-218` (socket `filter-jobs`)
- Modify: `backend/server.js:267-282` (route `/api/jobs`)

**Interfaces:**
- Consumes: tidak ada.
- Produces: `getFilteredJobs(search, bidang, tipe, sortBy, location, experience, hasSalary, education, page, limit)` — tanpa parameter `showClosed`; respons `{ jobs, total, page, limit, totalPages }` tanpa `closedCount`.

- [ ] **Step 1: Rapikan signature `getFilteredJobs`**

Ubah baris 93:

```js
async function getFilteredJobs(search = "", bidang = "all", tipe = "all", sortBy = "newest", location = "", experience = "", hasSalary = false, education = "all", page = 1, limit = 200, showClosed = false) {
```

menjadi:

```js
async function getFilteredJobs(search = "", bidang = "all", tipe = "all", sortBy = "newest", location = "", experience = "", hasSalary = false, education = "all", page = 1, limit = 200) {
```

- [ ] **Step 2: Hapus filter & hitung `closedCount`**

Hapus dua baris (174–177):

```js
  const closedCount = jobs.filter((j) => j.isClosed).length
  if (!showClosed) {
    jobs = jobs.filter((j) => !j.isClosed)
  }
```

- [ ] **Step 3: Kembalikan sorting polos**

Ganti blok (179–189):

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
```

dengan:

```js
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
```

- [ ] **Step 4: Rapikan `return`**

Ganti baris 193:

```js
  return { jobs: pageJobs, total, page, limit, totalPages: Math.ceil(total / limit), closedCount }
```

dengan:

```js
  return { jobs: pageJobs, total, page, limit, totalPages: Math.ceil(total / limit) }
```

- [ ] **Step 5: Hapus `showClosed` pada socket `filter-jobs`**

Ganti (217–218):

```js
  socket.on("filter-jobs", async ({ search, bidang, tipe, sortBy, location, experience, hasSalary, education, page, limit, showClosed }) => {
    const result = await getFilteredJobs(search, bidang, tipe, sortBy, location, experience, hasSalary, education, page, limit, showClosed)
    socket.emit("jobs-updated", result)
  })
```

dengan:

```js
  socket.on("filter-jobs", async ({ search, bidang, tipe, sortBy, location, experience, hasSalary, education, page, limit }) => {
    const result = await getFilteredJobs(search, bidang, tipe, sortBy, location, experience, hasSalary, education, page, limit)
    socket.emit("jobs-updated", result)
  })
```

- [ ] **Step 6: Hapus `showClosed` pada route `/api/jobs`**

Ganti (268–281):

```js
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
```

dengan:

```js
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
```

- [ ] **Step 7: Syntax check + grep sisa**

Run (dari `D:\job-scrapper\backend`): `node --check server.js`
Expected: tanpa output.

Run: `rg -n "showClosed|closedCount" server.js`
Expected: tanpa hasil.

- [ ] **Step 8: Commit**

```bash
git add backend/server.js
git commit -m "feat: hapus showClosed/closedCount dari API dan socket"
```

---

### Task 4: Hapus toggle/badge dari `frontend/src/views/JobsPage.vue`

**Files:**
- Modify: `frontend/src/views/JobsPage.vue:76-81` (toggle)
- Modify: `frontend/src/views/JobsPage.vue:114` (`opacity-60`)
- Modify: `frontend/src/views/JobsPage.vue:127-129` (badge)
- Modify: `frontend/src/views/JobsPage.vue:319-320` (refs)
- Modify: `frontend/src/views/JobsPage.vue:440` (`applyJobsPayload`)
- Modify: `frontend/src/views/JobsPage.vue:458` (param `fetchPage`)
- Modify: `frontend/src/views/JobsPage.vue:470` (simpan `closedCount`)
- Modify: `frontend/src/views/JobsPage.vue:510` (`watch`)
- Modify: `frontend/src/views/JobsPage.vue:525-526` (`resetFilters`)

**Interfaces:**
- Consumes: respons `/api/jobs` tanpa `closedCount` (Task 3).
- Produces: UI tanpa toggle/badge/`isClosed`.

- [ ] **Step 1: Hapus blok toggle di sidebar**

Hapus (76–81):

```html
          <div class="mt-xl flex flex-col">
            <label class="flex items-center gap-[8px] font-normal text-[13px] normal-case cursor-pointer text-on-dark-mute">
              <input type="checkbox" v-model="showClosed" class="w-[12px] h-[12px] min-h-[12px] cursor-pointer" />
              Tampilkan lowongan ditutup{{ closedCount ? ` (${closedCount})` : '' }}
            </label>
          </div>
```

(biarkan blok "Rentang Gaji" di atasnya dan `</aside>` di bawahnya tetap).

- [ ] **Step 2: Hapus `opacity-60` pada kartu**

Ganti (113–114):

```html
              class="bg-surface-elevated rounded-md p-lg flex flex-col justify-between h-full border border-hairline-dark hover:border-white/20 transition-all duration-200 shadow-sm"
              :class="{ 'opacity-60': job.isClosed }"
```

dengan:

```html
              class="bg-surface-elevated rounded-md p-lg flex flex-col justify-between h-full border border-hairline-dark hover:border-white/20 transition-all duration-200 shadow-sm"
```

- [ ] **Step 3: Hapus badge "Ditutup"**

Hapus (127–129):

```html
                    <span v-if="job.isClosed" class="bg-accent-danger/15 text-accent-danger border border-accent-danger/40 rounded-full px-[12px] py-[4px] text-[12px] font-semibold">
                      Ditutup
                    </span>
```

- [ ] **Step 4: Hapus ref state**

Ganti (318–320):

```js
const hasSalary = ref(false)
const showClosed = ref(false)
const closedCount = ref(0)
const sortBy = ref("newest")
```

dengan:

```js
const hasSalary = ref(false)
const sortBy = ref("newest")
```

- [ ] **Step 5: Hapus `closedCount` di `applyJobsPayload`**

Ganti (435–445):

```js
function applyJobsPayload(data) {
  if (!data) return
  jobs.value = data.jobs || []
  total.value = data.total || 0
  totalPages.value = data.totalPages || 0
  closedCount.value = data.closedCount || 0
  page.value = data.page || 1
  jobTotal.value = data.total || 0
  loading.value = false
  loadingMore.value = false
}
```

dengan:

```js
function applyJobsPayload(data) {
  if (!data) return
  jobs.value = data.jobs || []
  total.value = data.total || 0
  totalPages.value = data.totalPages || 0
  page.value = data.page || 1
  jobTotal.value = data.total || 0
  loading.value = false
  loadingMore.value = false
}
```

- [ ] **Step 6: Hapus param `showClosed` di `fetchPage`**

Ganti (450–461):

```js
  const params = new URLSearchParams({
    search: searchQuery.value,
    tipe: activeTipe.value,
    sortBy: sortBy.value,
    location: locationQuery.value,
    experience: experienceLevel.value,
    education: educationlevel.value,
    hasSalary: hasSalary.value ? 'true' : 'false',
    showClosed: showClosed.value ? 'true' : 'false',
    page: String(p),
    limit: String(limit)
  })
```

dengan:

```js
  const params = new URLSearchParams({
    search: searchQuery.value,
    tipe: activeTipe.value,
    sortBy: sortBy.value,
    location: locationQuery.value,
    experience: experienceLevel.value,
    education: educationlevel.value,
    hasSalary: hasSalary.value ? 'true' : 'false',
    page: String(p),
    limit: String(limit)
  })
```

- [ ] **Step 7: Hapus simpan `closedCount` di `fetchPage`**

Ganti (466–471):

```js
      else jobs.value = data.jobs || []
      total.value = data.total || 0
      totalPages.value = data.totalPages || 0
      closedCount.value = data.closedCount || 0
      page.value = p
```

dengan:

```js
      else jobs.value = data.jobs || []
      total.value = data.total || 0
      totalPages.value = data.totalPages || 0
      page.value = p
```

- [ ] **Step 8: Hapus `showClosed` dari `watch`**

Ganti (510):

```js
watch([activeTipe, searchQuery, locationQuery, experienceLevel, educationlevel, hasSalary, sortBy, showClosed], () => {
```

dengan:

```js
watch([activeTipe, searchQuery, locationQuery, experienceLevel, educationlevel, hasSalary, sortBy], () => {
```

- [ ] **Step 9: Hapus reset state di `resetFilters`**

Ganti (524–527):

```js
  hasSalary.value = false
  showClosed.value = false
  closedCount.value = 0
}
```

dengan:

```js
  hasSalary.value = false
}
```

- [ ] **Step 10: Build + verifikasi**

Run (dari `D:\job-scrapper\frontend`): `npm run build`
Expected: `✓ built` tanpa error (warning chunk-size lama boleh).

Run: `rg -n "isClosed|showClosed|closedCount|Ditutup" src/views/JobsPage.vue`
Expected: tanpa hasil.

- [ ] **Step 11: Commit**

```bash
git add frontend/src/views/JobsPage.vue
git commit -m "feat: hapus toggle/badge lowongan ditutup dari UI"
```

---

### Task 5: Verifikasi end-to-end + bersihkan artefak

**Files:**
- Tidak ada perubahan kode baru.

- [ ] **Step 1: Syntax check menyeluruh**

Run (dari `D:\job-scrapper\backend`): `node --check server.js; if ($?) { node --check db.js }; if ($?) { node --check scrapers/index.js }`
Expected: tanpa output.

Run (dari `D:\job-scrapper\backend\scrapping-job`): `& "C:\Users\Muhammad Al Fakhreza\AppData\Local\Python\bin\python.exe" -m unittest tests.test_closed_detector -v`
Expected: `OK` (5 tests) — kode Python tidak disentuh, harus tetap hijau.

- [ ] **Step 2: Simulasi scrape nyata (JobStreet)**

Pastikan backend tidak berjalan (heap 3000 bebas). Hentikan bila ada:
`Get-NetTCPConnection -LocalPort 3000 -State Listen | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }`

Run (dari `D:\job-scrapper\backend`):
`node --input-type=module -e "import { scrapeOnePlatform } from './scrapers/index.js'; const r = await scrapeOnePlatform('jobstreet', 1, 7, (e)=>console.log(e.message||JSON.stringify(e))); console.log(JSON.stringify(r, null, 2))"`
Expected: log ada `Import done: ...`, `Cleanup done: ... closed/not-found removed ...` (bukan "closed-marked"), dan `removed.closedMarked` TIDAK ada di output (diganti `removedClosed`).

- [ ] **Step 3: Cek API tanpa fitur lama**

Start backend: `Start-Process -FilePath "node" -ArgumentList "server.js" -WorkingDirectory "D:\job-scrapper\backend" -WindowStyle Hidden`, tunggu ~3 detik.

Run: `$r = Invoke-RestMethod "http://localhost:3000/api/jobs"; "total=$($r.total)"; "closedCount=$($r.closedCount)"`
Expected: baris `closedCount=` kosong (property tidak ada) — karena JSON tidak lagi mengirim `closedCount`, baris ke-2 menampilkan string kosong. Juga pastikan `showClosed=true` tidak mengubah apa pun:
Run: `$r2 = Invoke-RestMethod "http://localhost:3000/api/jobs?showClosed=true"; "$($r.total) == $($r2.total)"`
Expected: `N == N` (total identik — param tak berdampak).

- [ ] **Step 4: UI manual di browser**

Jalankan frontend dev: `cmd /c "cd /d D:\job-scrapper\frontend && npm run dev"` (background), lalu buka http://localhost:5173.
1. Pastikan sidebar **tidak lagi** menampilkan checkbox "Tampilkan lowongan ditutup".
2. Pastikan **tidak ada** kartu berbadge "Ditutup" atau yang tampak redup (opacity 60%).
3. Klik salah satu kartu → link terbuka di tab baru.

- [ ] **Step 5: Grep menyeluruh + bersihkan temp**

Run (dari `D:\job-scrapper\backend`): `rg -n "isClosed|showClosed|closedCount|markClosedUrls|markClosedJobs|Ditutup|closedRank" --glob '!node_modules/**' --glob '!jobs.sqlite*' .`
Expected: TIDAK ada hasil (semua sisa referensi hilang). Catatan: `docs/superpowers/` milik riwayat lama non-kode boleh diabaikan atau disaring: `rg ... backend frontend/src`.

Run: `Remove-Item C:\Users\MUHAMM~1\AppData\Local\Temp\opencode\setup_closed_demo.mjs -ErrorAction SilentlyContinue`

- [ ] **Step 6: Tambah laporan Task 5**

Tulis `D:\job-scrapper\.superpowers\sdd\task-6-report.md` merangkum hasil langkah 1–5 di atas, dan commitnya bersama progress:

```bash
git add .superpowers/sdd/task-6-report.md .superpowers/sdd/progress.md
git commit -m "docs: laporan verifikasi end-to-end fitur hapus lowongan tutup"
```

---

## Self-Review

Dijalankan oleh penulis plan setelah menulis dokumen ini (cek inline sebelum eksekusi):

1. **Cakupan spec:** spec menuntut — hapus marker di db.js (Task 1 ✓), `deleteClosedJobs` menggantikan mark (Task 2 ✓), hapus `showClosed`/`closedCount` di API/socket (Task 3 ✓), hapus toggle/badge UI (Task 4 ✓), deteksi Scrapy tidak disentuh (dilindungi di Global Constraints ✓), verifikasi e2e (Task 5 ✓).
2. **Placeholder scan:** tidak ada TBD/TODO; setiap step berisi kode/command konkret (perbaikan dilakukan inline pada "Step 1 Task 1" yang awalnya berisi stub, diganti perintah `node -e` eksplisit).
3. **Konsistensi tipe:** `deleteByUrls` ditandatangani sama di Task 1 (Produces) dan Task 2 (Consumes). `getFilteredJobs` signature 10-arg konsisten antara Task 3 (definisi) dan pemanggil socket/route yang diubah di step yang sama. Nama `removedClosed` konsisten di `runCleanup` return & log. `deleteClosedJobs` disebut sama di Task 2 dan Task 5 (verifikasi log).