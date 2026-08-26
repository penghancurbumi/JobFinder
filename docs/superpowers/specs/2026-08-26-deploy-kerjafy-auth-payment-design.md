# Desain: Deploy Kerjafy (Docker + Tunnel) + Auth + Payment Premium

**Status:** 🅿️ DIPARKIR — desain disetujui secara lisan oleh user pada 2026-08-26; eksekusi ditunda karena user sedang mengerjakan fitur lain (Organizational Experience di CV Builder). Lanjutkan dari bagian [Langkah Resume](#langkah-resume).

## Konteks

JobFinder akan direbranding menjadi **Kerjafy** (kerja + -fy). Platform di-deploy ke home server (laptop Asus, Ubuntu Desktop + Docker, diakses admin via Tailscale). Koneksi internet rumah terdeteksi **CGNAT** (traceroute: dua lapis NAT operator `10.x.x.x` sebelum IP publik `103.26.189.24` / PT Telemedia Komunikasi Pratama) sehingga port forwarding tidak mungkin — jalur publik wajib lewat tunnel.

## Keputusan yang Sudah Disetujui

| Area | Keputusan |
|---|---|
| Nama & domain | **Kerjafy** — beli `kerjafy.online` di Jagoan Hosting (tersedia per 2026-08-26; `jobsphere.online` ternyata sudah diambil orang sampai 2026-09-23) |
| Strategi TLD | `.online` dulu selama tahap develop; upgrade `.com` nanti (`kerjafy.com` MASIH TERSEDIA — beli sebagai asuransi begitu ada budget ~Rp150rb) |
| Ekspos publik | Cloudflare DNS (gratis) + **Cloudflare Tunnel** mode token; HTTPS otomatis di edge; port router tetap tertutup |
| Container | Pendekatan A: **satu container app** (Node 20 + Python + Chromium) + satu container `cloudflared`; frontend build diserve Express (`express.static`) — tanpa nginx |
| Auth | **Firebase Auth**: Google sign-in (`signInWithPopup`) + email/password; backend verifikasi ID token via `firebase-admin`; user di-upsert ke SQLite |
| Payment | **Midtrans Snap**, pembayaran sekali per durasi (bukan langganan otomatis); QRIS sebagai metode utama (fee ±0,7%; hindari VA flat Rp4rb untuk nominal kecil) |
| Harga paket | 1 bulan Rp15.000 · 3 bulan Rp40.000 · 12 bulan Rp120.000 (harga fix tersimpan di server, tidak percaya klien) |
| Scope | Web app + auth + payment dalam SATU fase. Telegram bot & scheduler.py TIDAK ikut deploy |
| Brand check | Nama "Kerjafy" belum ditemukan dipakai siapa pun (web search 2026-08-26); nama mirip hanya JobiFy/Careerfy/Jobifiy |

## Arsitektur

```
[Pengunjung] → HTTPS kerjafy.online
                    ↓
            [Cloudflare Edge — SSL otomatis]
                    ↑ outbound tunnel
            [cloudflared container]
                    ↓ jaringan internal docker
            ┌─────────────────────────────────────┐
            │  app container                      │
            │  Node 20 + Python + Chromium        │
            │  ├─ express.static → frontend/dist  │
            │  ├─ /api/* + Socket.IO              │
            │  ├─ POST /api/payments/notify       │
            │  └─ spawn scrapy saat scrape        │
            └─────────────────────────────────────┘
                    ↓ volume persist
            [jobfinder-data: jobs.sqlite + exports/json]

  Layanan eksternal: Firebase Auth · Midtrans
  Akses admin server: Tailscale SSH
```

## Detail Deployment

### Dockerfile (root, multi-stage)

1. **Stage `frontend-build`**: `node:20-alpine` → copy `frontend/package*.json`, `npm ci`, copy source, `npm run build` → hasil `/frontend/dist`
2. **Stage `app`**: base `mcr.microsoft.com/playwright/python:<versi-pinned>-jammy` (Python + deps browser sudah siap) → install Node 20 via NodeSource → `npm ci` backend → `pip install -r requirements.txt` → `python -m playwright install chromium` (sinkron dengan versi pip) → copy backend + `COPY --from=frontend-build dist`
3. `WORKDIR /app/backend`, `CMD ["node","server.js"]`

Alasan satu image: `scrapers/index.js` memanggil Python via `spawn` langsung dari proses Node — bukan service terpisah.

### docker-compose.yml

- Service `app`: env_file `.env.production`, environment `PYTHON_EXE=python`, `DATA_DIR=/app/backend/data`, `EXPORTS_DIR=/app/backend/data/exports/json`, `NODE_ENV=production`; volume `jobfinder-data:/app/backend/data`; healthcheck via `node -e` fetch ke `/api/status` (Node pasti ada di image; hindari ketergantungan wget/curl); `restart: unless-stopped`
- Service `cloudflared`: image `cloudflare/cloudflared:latest`, command `tunnel run --token ${CF_TUNNEL_TOKEN}`, `restart: unless-stopped`
- Volume named: `jobfinder-data`
- `.dockerignore`: node_modules, jobs.sqlite*, *.log, .git, .env*

### Refactor Kode Wajib (kecil, env-driven)

| File | Perubahan |
|---|---|
| `backend/scrapers/index.js` | `PYTHON_EXE` dan path exports bisa dioverride via env (`PYTHON_EXE`, `EXPORTS_DIR`); default Windows tetap untuk dev lokal |
| `backend/db.js` | Path SQLite dari `process.env.DATA_DIR \|\| __dirname` |
| `backend/server.js` | Tambah `express.static(../frontend/dist)` + fallback SPA ke `index.html` (vue-router history mode), dipasang SETELAH semua route `/api` agar tidak menutupi API |

### Domain & Tunnel (langkah manual user)

1. Checkout `kerjafy.online` di Jagoan Hosting
2. Daftar gratis di Cloudflare → add site `kerjafy.online` → dapat 2 nameserver
3. Ganti nameserver domain di dashboard Jagoan Hosting ke NS Cloudflare, tunggu aktif
4. Zero Trust dashboard → Create Tunnel (token mode) → public hostname `kerjafy.online` → service `http://app:3000`
5. Paste token ke `.env.production` (`CF_TUNNEL_TOKEN`)

## Autentikasi

- **Frontend**: Firebase JS SDK; tombol "Masuk dengan Google" + form email/password (daftar & masuk); interceptor axios menyisipkan `Authorization: Bearer <idToken>` ke semua request API
- **Backend**: middleware `firebase-admin` → `verifyIdToken()` untuk endpoint terlindungi; on-first-request upsert baris `users`
- **Wajib login**: chatbot history, endpoint payment. **Publik**: browse/search lowongan (SEO & adopsi)
- Env: kredensial service account Firebase via file/env (tidak pernah masuk image)

## Payment Premium (Midtrans Snap)

- Paket fix di server: `{code:'1m', days:30, price:15000}`, `{code:'3m', days:90, price:40000}`, `{code:'12m', days:365, price:120000}`
- Flow: pilih paket → backend buat `order_id` berformat `KF-{userId}-{timestamp}` → Snap API → token ke frontend → popup Snap → bayar QRIS → webhook `POST /api/payments/notify` → verifikasi signature sha512(`order_id+status_code+gross_amount+serverKey`) → status `settlement/capture` → `premium_until = max(now, premium_until_lama) + durasi`
- Idempoten per `order_id` (UNIQUE)
- Mulai dari sandbox (`MIDTRANS_IS_PRODUCTION=false`); akun produksi butuh KYC KTP — daftarkan paralel
- ⚠️ Webhook butuh URL publik → integrasi payment dites SETELAH tunnel aktif

## Skema Database Tambahan

```sql
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  firebase_uid TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  display_name TEXT,
  photo_url TEXT,
  provider TEXT,
  premium_until TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS payments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL REFERENCES users(id),
  order_id TEXT UNIQUE NOT NULL,
  package_code TEXT NOT NULL CHECK (package_code IN ('1m','3m','12m')),
  amount INTEGER NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('pending','settlement','deny','expire','cancel')),
  paid_at TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
```

Migrasi mengikuti pola `db.js` existing (buat tabel jika belum ada, tanpa merusak data lama).

## Batasan Free vs Premium (USULAN — masih bisa diubah user)

| Fitur | Free | Premium |
|---|---|---|
| Cari & filter lowongan | unlimited | unlimited |
| CV Builder | template Modern ATS saja | semua template |
| CV Analyzer (Scan ATS) | 3x/bulan | unlimited |
| Chatbot karier AI | 10 pesan/hari | unlimited |

## Frontend Baru

Modal/halaman Login-Daftar · badge akun + menu profil · halaman Pricing + tombol Upgrade · banner "Premium" di fitur terkunci · halaman Status Pembayaran (sukses/pending/gagal). Mengikuti gaya Tailwind existing.

## Urutan Pengerjaan (saat dieksekusi)

1. Refactor env-path + express.static → verifikasi lokal (`node --check`, build, uji manual)
2. Dockerfile + compose + .dockerignore → build & jalankan di laptop server → tes via localhost/Tailscale
3. Beli domain → Cloudflare NS → Tunnel aktif → tes publik dari HP
4. Firebase project → fitur auth (SDK frontend, middleware backend, tabel users)
5. Midtrans sandbox → pricing page + webhook → E2E test premium flow
6. Switch gateway production setelah akun Midtrans disetujui

## Verifikasi Akhir

Buka domain dari HP ✔ HTTPS lock ✔ login Google ✔ beli paket QRIS sandbox ✔ webhook memperpanjang `premium_until` ✔ scraping jalan ✔ data selamat `docker compose down/up` ✔

## Hal yang Belum Selesai Saat Diparkir (open items)

- [ ] Cek trademark "Kerjafy" di PDKI (pdkki.dgip.go.id), kelas 35 & 42
- [ ] Amankan sosial media handle `@kerjafy` (IG/TikTok/X)
- [ ] Beli `kerjafy.com` sebagai asuransi (masih tersedia per 2026-08-26)
- [ ] Daftar akun Midtrans produksi (proses KYC bisa lama)
- [ ] Finalisasi batasan Free vs Premium (masih usulan)
- [ ] Buat project Firebase + ambil kredensial service account
- [ ] Spec ini belum melalui tahap writing-plans (implementation plan belum dibuat)

## Langkah Resume

1. Review spec ini bersama user; finalisasi open items di atas
2. Invoke skill `superpowers:writing-plans` untuk membuat implementation plan
3. Eksekusi plan sesuai urutan pengerjaan
