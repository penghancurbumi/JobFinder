# Desain: Tandai Lowongan "Ditutup"

Tanggal: 2026-08-12
Status: Disetujui (brainstorming)

## Masalah

Sebagian lowongan yang tersimpan di aplikasi sudah ditutup oleh penyedia
(akun perusahaan) saat link-nya dibuka. Deteksi yang ada sekarang hanya
menangkap halaman detail yang membalas HTTP **404/410**
(`NotFoundCollectorMiddleware` menulis URL-nya ke `not_found.txt`, lalu
backend menghapusnya). Banyak platform membalas **HTTP 200** dengan halaman
berisi teks penanda "lowongan ditutup" — lolos dari deteksi sehingga tetap
tampil sebagai lowongan aktif.

## Tujuan

1. Deteksi lowongan yang ditutup penyedia **saat proses scrape** dengan
   memindai konten halaman detail (bukan hanya status HTTP).
2. Tandai lowongan tersebut **"Ditutup"** dan **tetap simpan** di DB (tidak
   dihapus), konsisten dengan preferensi pengguna.
3. Jika lowongan yang sama dibuka kembali oleh penyedia (relist), status
   otomatis **balik aktif** pada scrape berikutnya.
4. Di daftar lowongan: lowongan "Ditutup" **disembunyikan secara default**,
   ada toggle untuk menampilkannya; saat tampil diberi badge dan diurutkan ke
   paling bawah.

## Perubahan Perilaku yang Disepakati

- Perilaku deteksi 404/410 berubah dari **hapus** → **tandai** `isClosed=1`
  (demi konsistensi dengan "tetap tampil").
- Cleanup lain (umur maksimal, not-seen, duplikat, kualitas buruk) **tetap
  menghapus** seperti sekarang.

## Arsitektur / Komponen

### 1. Data model (`backend/db.js`)

Tambah dua kolom pada tabel `jobs` (migration untuk DB lama, jalankan di init
setelah tabel dibuat):

- `isClosed INTEGER DEFAULT 0` — `1` = lowongan ditutup penyedia.
- `closedAt TEXT` — timestamp saat ditandai (untuk info/sort).

Backfill: `UPDATE jobs SET isClosed = 0 WHERE isClosed IS NULL`.

Index: `CREATE INDEX IF NOT EXISTS idx_jobs_closed ON jobs(isClosed)`.

Kolom ikut terbaca otomatis lewat `SELECT *` pada jobs cache.

### 2. Deteksi saat scrape (Python)

#### `backend/scrapping-job/job_scraper/middlewares.py` — `NotFoundCollectorMiddleware`

- `process_response`:
  - status `404`/`410` → masukkan `request.url` ke set `not_found` (perilaku
    sekarang).
  - Selain itu, jika `request.meta.get("is_detail")` dan konten halaman
    mengandung penanda closed → masukkan ke set `closed`.
- `spider_closed`: tulis `not_found` ke `exports/json/not_found.txt` (tidak
  berubah) dan `closed` ke file baru `exports/json/closed.txt`.

#### `backend/scrapping-job/job_scraper/spiders/base_spider.py`

- `_make_detail_request` menambahkan `meta["is_detail"] = True` pada request
  detail.
- Helper `_is_closed_content(text)` di middleware/base yang mencocokkan teks
  terhadap daftar penanda (regex, case-insensitive).

#### `backend/scrapping-job/job_scraper/constants.py`

- `CLOSED_MARKERS`: daftar frasa penanda per platform (dan umum). Contoh
  penanda umum: "lowongan telah ditutup", "lowongan ditutup", "position
  closed", "job closed", "no longer accepting applications", "is no longer
  available", "not accepting applications", "tidak menerima lamaran",
  "lowongan ini telah berakhir". Bisa diperkaya per platform sesuai selector
  aktual (mis. JobStreet `jobClosedHeader`/"This job is no longer accepting
  applications").

### 3. Backend (Node.js)

#### `backend/scrapers/index.js`

- `markClosedJobs()` (menyatukan penanganan `not_found.txt` dan `closed.txt`,
  menggantikan `deleteNotFoundJobs`):
  - Baca `exports/json/not_found.txt` **dan** `exports/json/closed.txt`
    (jika ada), gabungkan jadi daftar URL unik.
  - `UPDATE jobs SET isClosed = 1, closedAt = ? WHERE url IN (...)` (hanya
    yang `isClosed = 0` untuk menahan `changes` yang akurat).
  - Hapus kedua file setelah diproses. Return jumlah yang ditandai.
  - Ini menerapkan poin "Perubahan Perilaku" (404 → tandai, bukan hapus).
- `runCleanup()`: panggil `markClosedJobs()` (bukan `deleteByUrls`);
  komponen lain (`deleteExpiredJobs`, `deleteDuplicateJobs`,
  `deleteBadQualityJobs`) tetap.
- Upsert di `insertScrapedFiles` (`INSERT ... ON CONFLICT(url) DO UPDATE SET`):
  tambahkan `isClosed = 0, closedAt = NULL` sehingga lowongan yang kembali
  terlihat terbuka otomatis aktif lagi.
- Pesan progress "done" menyertakan jumlah yang ditandai closed.

#### `backend/server.js`

- `getFilteredJobs(..., showClosed = false, ...)`:
  - Filter: `if (!showClosed && j.isClosed) return false`.
  - Sort: kriteria utama `isClosed` ascending (open dulu, closed di bawah),
    lalu kriteria sort yang ada.
  - Respons menyertakan `closedCount` (jumlah lowongan tertutup di hasil
    filter setelah filter lain, sebelum sort/limit).
- Socket `filter-jobs` meneruskan `showClosed`.
- Endpoint `GET /api/jobs` (server.js:261): baca `showClosed` dari query dan
  teruskan ke `getFilteredJobs`.

#### `backend/db.js`

- Migration kolom + index (poin 1).
- Helper `markClosedUrls(urls)` (UPDATE bertanda waktu) dipakai `markClosedJobs()`.

### 4. Frontend (`frontend/src/views/JobsPage.vue`)

- State baru `showClosed` (default `false`).
- Toggle di sidebar: checkbox "Tampilkan lowongan ditutup (N)" dengan
  `N = closedCount` dari respons.
- `fetchPage` dan emit `filter-jobs` mengirim `showClosed`.
- Kartu: jika `job.isClosed`, tampilkan badge "Ditutup" (accent-danger) dan
  redupkan kartu (mis. `opacity-60`).

### 5. Verifikasi

- Python: `python -m py_compile` pada file yang diubah.
- Node: `node --check` pada file yang diubah.
- Frontend: `npm run build`.
- Uji manual:
  - Buat `closed.txt` berisi 1–2 URL palsu → jalankan fungsi tandai →
    cek `isClosed` di SQLite berubah.
  - Upsert lowongan yang sama dengan status terbuka → cek `isClosed` kembali 0.
  - Cek toggle "Ditampilkan lowongan ditutup" di UI dan badge/urutan.
  - Cek deteksi konten pada 1 platform (mis. JobStreet) lewat scrape nyata.

## Catatan / Batasan

- Deteksi konten hanya menjangkau lowongan yang detail-nya di-request saat
  scrape (`max_detail_pages`). Lowongan yang tidak pernah dicek ulang akan
  tertangani oleh cleanup "not seen" yang sudah ada.
- Penanda closed bersifat heuristic; akurasi bisa ditingkatkan per platform
  seiring berjalannya waktu.
- `chatbot.js` membaca cache `jobs`; kolom `isClosed` tidak akan mengganggu
  (diabaikan oleh chatbot).
