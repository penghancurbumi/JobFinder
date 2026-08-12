# Desain: Hapus langsung lowongan yang ditutup/inaktif/not-found

Tanggal: 2026-08-12

## Ringkasan

Mengubah arah fitur "lowongan ditutup" yang sebelumnya diimplementasikan sebagai
**tandai** (`isClosed`) + tampilkan via toggle. Sesuai keputusan user, lowongan
yang terdeteksi **ditutup / tidak aktif / not-found** sekarang langsung
**dihapus** dari database. Tidak ada lagi UI untuk menampilkannya.

## Latar belakang

Branch sebelumnya (commit `85472d7`..`9223552`) membangun:

- Kolom `isClosed`/`closedAt` + helper `markClosedUrls` (db.js)
- `markClosedJobs()` yang menandai alih-alih menghapus (scrapers/index.js)
- Param API `showClosed` + `closedCount` (server.js)
- Toggle "Tampilkan lowongan ditutup" + badge "Ditutup" (JobsPage.vue)
- Deteksi konten lowongan tutup di sisi Scrapy (`closed.txt` via `has_closed_content`)

User memutuskan: **tidak perlu menampilkan lowongan yang dihapus/ditutup. Cukup
hapus dari database jika ada yang ditutup, tidak aktif, atau not found.**

## Keputusan desain

1. **Deteksi dipertahankan** — Pertahankan deteksi konten (Task 4: `closed.txt`
   via `has_closed_content`) dan deteksi 404/not-found (`not_found.txt`). Keduanya
   menjadi sumber URL yang akan dihapus.
2. **Hapus, bukan tandai** — Kembalikan perilaku lama: URL yang ditemukan di
   `not_found.txt`/`closed.txt` dihapus via `deleteByUrls` (helper ini masih ada).
3. **Bersihkan schema** — Hapus kolom `isClosed` & `closedAt` + index terkait dari tabel `jobs`.
4. **Hapus fitur UI/API show-closed** — Semua kode toggle/badge/closedCount/showClosed dihapus.

## Perubahan per file

### `backend/db.js`
- Hapus migrasi kolom `isClosed`/`closedAt` + `idx_jobs_closed` dari skema.
- Hapus helper `markClosedUrls`.
- Pertahankan `deleteByUrls`.

### `backend/scrapers/index.js`
- Ganti `markClosedJobs()` → `deleteClosedJobs()`: baca `not_found.txt` **dan**
  `closed.txt`, gabungkan URL, hapus via `deleteByUrls`, lalu bersihkan file.
- `runCleanup()` memanggil `deleteClosedJobs()`; log cleanup kembali
  menyebut "not-found/closed … removed" (bukan "closed-marked").
- Hapus baris reset `isClosed = 0, closedAt = NULL` pada branch duplikat dan
  pada klausa `ON CONFLICT` upsert — kembalikan ke upsert polos tanpa kolom closed.
- Hapus import `markClosedUrls` yang tidak terpakai.

### `backend/server.js`
- `getFilteredJobs()`: hapus param `showClosed`, hitung `closedCount`, filter
  `!isClosed`, dan `closedRank` pada semua cabang sorting. Sorting kembali polos.
- Hapus `closedCount` dari payload respons.
- Socket `filter-jobs` dan endpoint `/api/jobs`: hapus `showClosed`.

### `frontend/src/views/JobsPage.vue`
- Hapus toggle "Tampilkan lowongan ditutup (N)".
- Hapus badge "Ditutup" dan `:class opacity-60` pada kartu.
- Hapus ref `showClosed`/`closedCount`, kait `showClosed` pada `watch`,
  param pada `fetchPage`, set `closedCount` di `applyJobsPayload`, dan reset
  keduanya di `resetFilters`.

### Scrapy (`backend/scrapping-job/`) — TIDAK diubah
- Deteksi konten tetap menulis `closed.txt`. Yang berubah hanya konsumennya
  (Node) dari "mark" menjadi "delete".

## Data flow

```
Scrapy spider (detail page)
  ├─ 404/410  → middleware → not_found.txt
  └─ konten "closed" → has_closed_content → closed.txt
        ↓
Node scrapeOnePlatform → runCleanup → deleteClosedJobs()
        ↓
deleteByUrls(urls) → baris dihapus dari jobs
```

Konsekuensi: jika suatu lowongan tertutup lalu dibuka kembali di sumbernya,
lowongan tersebut akan muncul **lagi sebagai entri baru** pada scrape berikutnya
(karena entri lama sudah dihapus). Dianggap dapat diterima.

## Verifikasi

1. `node --check` server.js/db.js/scrapers/index.js — tanpa output.
2. `python -m unittest tests.test_closed_detector` — OK (tidak berubah, tetap valid).
3. Simulasi scrape satu platform — log cleanup menunjukkan "removed" bukan "closed-marked".
4. `npm run build` frontend — sukses, tanpa sisa referensi `isClosed`/`showClosed`/`closedCount`.
5. Grep seluruh repo (backend + frontend src) untuk `isClosed`, `showClosed`,
   `closedCount`, `markClosedUrls`, `markClosedJobs` — tidak ada sisa kecuali
   artefak DB biner/log yang diabaikan.

## Catatan

- Skema SQLite: kolom dihapus via runtime migration (DROP COLUMN).
- Cleanup `not-seen`/`age-expired`/duplikat/kualitas buruk tetap berjalan seperti sebelumnya.