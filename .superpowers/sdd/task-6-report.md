# Task 5 Report: Verifikasi end-to-end + bersihkan artefak

Plan: `docs/superpowers/plans/2026-08-12-delete-closed-jobs.md`
Spec: `docs/superpowers/specs/2026-08-12-delete-closed-jobs-design.md`
Base/previous commit: `5781832` (Task 4). Pebisnis commit: `docs: laporan verifikasi end-to-end fitur hapus lowongan tutup`

Verdict: **ALL PASS** — feature "mark closed jobs" telah sepenuhnya dibuang; lowongan ditutup kini dihapus (delete) bukan ditandai.

---

## Step 1: Syntax check menyeluruh — PASS

Command (dari `D:\job-scrapper\backend`):
```powershell
node --check server.js; if ($?) { node --check db.js }; if ($?) { node --check scrapers/index.js }
```
Actual output: `SYNTAX_EXIT=0`, tidak ada error/cetakan dari `node --check` (ketiga file valid).

Command (dari `D:\job-scrapper\backend\scrapping-job`):
```powershell
& "C:\Users\Muhammad Al Fakhreza\AppData\Local\Python\bin\python.exe" -m unittest tests.test_closed_detector -v
```
Actual output (5/5 OK = `OK`):
```
test_case_insensitive ... ok
test_general_marker_english ... ok
test_general_marker_indonesian ... ok
test_open_job_not_detected ... ok
test_platform_marker_jobstreet ... ok
Ran 5 tests in 0.000s
OK
```
Kode Python (deteksi Scrapy + `closed.txt`) tidak disentuh dan tetap hijau.

## Step 2: Simulasi scrape nyata (JobStreet) — PASS

Pre-check: port 3000 bebas sejak awal (`Port 3000 free`, tidak ada proses yang dihentikan).

Command (dari `D:\job-scrapper\backend`):
```powershell
node --input-type=module -e "import { scrapeOnePlatform } from './scrapers/index.js'; const r = await scrapeOnePlatform('jobstreet', 1, 7, (e)=>console.log(e.message||JSON.stringify(e))); console.log(JSON.stringify(r, null, 2))"
```
Actual output (baris relevan):
```
Mulai scrape jobstreet (1/7)
Scraping platform: jobstreet (1/7)...
Connected to SQLite database.
Importing exports for jobstreet...
Import done: 3 added/updated, 27 duplicate skipped
Cleanup done: 0 closed/not-found removed, 0 age-expired, 0 not-seen, 0 duplicates, 0 unclear-quality (total 0)
Platform jobstreet done. Added: 3 | removed: 0
{
  "platform": "jobstreet",
  "added": 3,
  "cleanup": { "removedClosed": 0, "age": 0, "notSeen": 0, "duplicates": 0, "unclear": 0, "total": 0 }
}
```
Verifikasi terhadap ekspektasi brief:
- Log `Import done: ...` ✔ (3 added/updated, 27 duplicate skipped)
- Log `Cleanup done: ... closed/not-found removed ...` ✔ (bukan "closed-marked")
- Output berisi `removedClosed` ✔ dan TIDAK ada `closedMarked` ✔

## Step 3: Cek API tanpa fitur lama — PASS

Start: `Start-Process -FilePath "node" -ArgumentList "server.js" -WorkingDirectory "D:\job-scrapper\backend" -WindowStyle Hidden` → `Started PID 9008`, tunggu ~3 detik.

Command:
```powershell
$r = Invoke-RestMethod "http://localhost:3000/api/jobs"; "total=$($r.total)"; "closedCount=$($r.closedCount)"
$r2 = Invoke-RestMethod "http://localhost:3000/api/jobs?showClosed=true"; "$($r.total) == $($r2.total)"
```
Actual output:
```
total=1923
closedCount=
1923 == 1923
```
Verifikasi:
- Baris `closedCount=` kosong → property tidak lagi dikirim oleh API ✔
- `1923 == 1923` → `showClosed=true` tak berdampak apa pun ✔

Cleanup: backend dihentikan (`Stopping PID 9008`), port 3000 kembali bebas. Frontend dev (Step 4, cek browser manual) sengaja TIDAK dijalankan — ditangani controller.

## Step 4: UI manual di browser — SKIPPED (oleh desain)

Langkah interaktif browser ditangani controller secara manual, bukan oleh tugas ini.

## Step 5: Grep menyeluruh + bersihkan temp — PASS (2 hit benign)

Command (dari repo root):
```powershell
git grep -n -e isClosed -e showClosed -e closedCount -e markClosedUrls -e markClosedJobs -e Ditutup -e closedRank -- backend frontend/src
```
Actual output:
```
backend/db.js:51:    // Remove the discontinued closed-listing markers (isClosed/closedAt) from
backend/db.js:56:      db.run("ALTER TABLE jobs DROP COLUMN isClosed", () => {
backend/scrapping-job/job_scraper/spiders/kitalulus.py:98:            if job.get("isClosed"):
```
Penilaian:
- `backend/db.js:51-56` — komentar + migrasi `DROP COLUMN isClosed/closedAt` yang memang wajib menyebut nama kolom lama. Ini adalah artefak Task 1 yang benar, bukan sisa fitur.
- `backend/scrapping-job/.../kitalulus.py:98` — spider Scrapy yang membaca field `isClosed` dari payload **situs sumber** (Kitalulus), bukan marker aplikasi. Kerenanya Python sengaja tak disentuh (Global Constraints).
- Tidak ada hit di `frontend/src` → toggle/badge benar-benar hilang dari UI.

Penghapusan temp: `Remove-Item ...\setup_closed_demo.mjs` → `Removed / not present` ✔.

## Step 6: Laporan

File ini ditulis ke `.superpowers/sdd/task-6-report.md`, `progress.md` di-update dengan entry `Task 5: complete ...`, dan keduanya di-commit dengan pesan `docs: laporan verifikasi end-to-end fitur hapus lowongan tutup`.

## Self-review akhir

1. Semua sisa marker (kolom, helper, param API, toggle/badge UI) sudah dihapus; verifikasi e2e di atas membuktikannya.
2. Backlog minor dari Task 2 & 4 (komentar `runCleanup` ketinggalan, indentasi `</aside>`) bukan regresi fungsional dan tidak disentuh (tugas verifikasi ini tidak boleh menyentuh source).
3. Artefak build (`frontend/dist/**`, `backend/jobs.sqlite*`, `backend/server.log`) dibiarkan kotor seperti yang diharapkan; tidak di-stage.