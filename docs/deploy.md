# Deploy JobFinder ke VPS Laptop (Ubuntu, RAM 4GB) + Cloudflare Tunnel

Panduan langkah demi langkah dari nol sampai live publik.
Arsitektur: **backend (Node+Python) + frontend/nginx + cloudflared** dalam 3 container.

---

## 0. Prasyarat di laptop server

- Ubuntu terinstall (Desktop boleh, tapi **Server lebih hemat RAM** — lihat catatan di bawah)
- Docker + Docker Compose plugin sudah terinstall (konfirmasi: `docker compose version`)
- Git, dan akses internet stabil
- RAM 4GB

> **Catatan RAM:** GNOME (Ubuntu Desktop) memakai 1.2–2GB hanya untuk idle.
> Untuk 4GB + scraping Chromium, sangat disarankan boot tanpa GUI:
> ```bash
> sudo systemctl set-default multi-user.target
> sudo reboot
> # kalau sesekali butuh GUI: login TTY lalu jalankan `startx`
> ```

---

## 1. (Sekali saja) Beli domain + pindahkan nameserver ke Cloudflare

Cloudflare Tunnel butuh domain yang dikelola Cloudflare (gratis).

1. Beli domain di registrar pilihanmu (Namecheap, Cloudflare Registrar, Rumahweb, Niagahoster, dll).
2. Buat akun di https://dash.cloudflare.com → **Add a site** → masukkan domainmu → pilih plan **Free**.
3. Cloudflare akan memberi 2 **nameserver** (mis. `ada.ns.cloudflare.com`).
4. Di registrar, ganti nameserver domainmu ke 2 NS dari Cloudflare itu.
5. Tunggu propagasi (5 menit – 24 jam). Status di Cloudflare jadi **Active**.

> Tidak perlu buka port apa pun di router. Tidak perlu IP publik. Inilah keunggulan Cloudflare Tunnel.

---

## 2. Siapkan kode di server

Pindahkan repo ke laptop server (mis. lewat Tailscale SSH / git clone):

```bash
git clone https://github.com/penghancurbumi/JobFinder.git
cd JobFinder
git checkout <branch-yang-kamu-pakai>
```

> Kalau sudah memakai perubahan Docker (branch ini), lanjut. Kalau belum, pastikan
> file `docker-compose.yml`, `backend/Dockerfile`, `frontend/Dockerfile`,
> `frontend/nginx.conf`, dan `.dockerignore` sudah ada di repo.

---

## 3. Isi environment backend

Buat `backend/.env` dari contohnya:

```bash
cp backend/.env.example backend/.env
nano backend/.env
```

Isi minimal:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxx      # WAJIB untuk fitur AI
PORT=3000
LINK_DEAD_GRACE_DAYS=2
AUTO_SCRAPE_INTERVAL_HOURS=12           # dilonggarkan utk RAM 4GB
AUTO_LINK_CHECK_HOURS=12
MAX_JOBS=20000
```

> Nilai `AUTO_SCRAPE_*` di `backend/.env` **menimpa** default di docker-compose,
> jadi set ke 12 di sini agar konsisten.

---

## 4. (Sekali saja) Buat Cloudflare Tunnel & ambil token

1. Buka https://one.dash.cloudflare.com → **Networks → Tunnels → Create a tunnel**.
2. Pilih **Cloudflared**, beri nama (mis. `jobfinder`).
3. Pilih environment **Docker**. Cloudflare menampilkan perintah seperti:
   ```
   cloudflared service install eyJhIjoi...panjang...token
   ```
   Copy nilai token panjang itu (setelah `install`).
4. Di tab **Public Hostname**, klik **Add a public hostname**:
   - **Subdomain**: `jobfinder` (atau `www`)
   - **Domain**: domainmu
   - **Service Type**: `HTTP`
   - **URL**: `frontend:80`   ← nama service docker-compose + port container
5. Save. Nanti `https://jobfinder.domainmu.com` otomatis mengarah ke container.

---

## 5. Isi token tunnel di server

Di **root repo** (`JobFinder/`):

```bash
cp .env.example .env
nano .env
```

Isi:

```env
TUNNEL_TOKEN=eyJhIjoi...token-dari-langkah-4...
```

> `docker compose` otomatis membaca `.env` di root untuk variabel `${TUNNEL_TOKEN}`.

---

## 6. Build & jalankan

```bash
docker compose up -d --build
```

Build pertama lama (karena install Scrapy + Chromium ~5–10 menit). Cek status:

```bash
docker compose ps
docker compose logs -f backend     # pantau sampai "Backend running on http://0.0.0.0:3000"
```

Kalau ketiga service `Up`:

```bash
curl -I http://127.0.0.1:8080/healthz    # harus 200 ok
```

---

## 7. Uji dari luar

Buka di browser: `https://jobfinder.domainmu.com`

Cloudflare otomatis memberi HTTPS + sertifikat. Uji juga tombol **Perbarui Data**
(trigger scraping) dan fitur AI (butuh `GROQ_API_KEY` benar).

---

## 8. Operasional harian

```bash
# Lihat log
docker compose logs -f
docker compose logs -f backend

# Restart salah satu
docker compose restart backend

# Update kode
git pull
docker compose up -d --build

# Stop semua
docker compose down

# Cek pemakaian RAM nyata
docker stats --no-stream
free -h
```

---

## 9. Backup (WAJIB)

Database ada di volume `backend-data`. Backup rutin ke luar container:

```bash
# Dump SQLite dengan aman (WAL)
docker compose exec backend sh -c 'sqlite3 /data/jobs.sqlite ".backup /data/backup.sqlite"' 2>/dev/null \
  || docker compose cp backend:/data/jobs.sqlite ./backup-$(date +%F).sqlite

# Simpan
mkdir -p ~/backups
docker compose cp backend:/data/jobs.sqlite ~/backups/jobs-$(date +%F).sqlite
```

Jadwalkan harian via cron:

```bash
crontab -e
# tambahkan:
0 3 * * * cd /home/USER/JobFinder && docker compose cp backend:/data/jobs.sqlite /home/USER/backups/jobs-$(date +\%F).sqlite
```

> Kalau nanti pindah ke PostgreSQL, ganti dengan `pg_dump`.

---

## 10. Monitoring & kesehatan

- **Cloudflare dashboard** → Tunnel status (connected/down).
- **Uptime Kuma** (opsional, container kecil) untuk alert kalau `https://jobfinder.domainmu.com/healthz` down.
- Cek disk: `df -h` — SQLite + exports akan tumbuh. `MAX_JOBS=20000` membatasi jumlah job.
- Cek suhu laptop: `sudo apt install lm-sensors && sensors` (laptop tua 24/7 rawan panas).

---

## Troubleshooting

| Gejala | Penyebab umum | Solusi |
|---|---|---|
| `curl` 502 dari tunnel | frontend/backend belum siap | `docker compose logs frontend`; pastikan `backend` Up |
| Halaman putih di domain | SPA fallback / build gagal | cek `docker compose logs frontend`; pastikan `npm run build` sukses |
| Scraping gagal "python: not found" | PYTHON_EXE salah | pastikan env `PYTHON_EXE=python3` (sudah default di compose) |
| Scraping error Playwright | Chromium/OS deps kurang | rebuild image backend; cek `docker compose logs backend` |
| AI tidak jalan | `GROQ_API_KEY` kosong | isi `backend/.env` lalu `docker compose up -d backend` |
| OOM / mesin hang saat scraping | RAM 4GB kewalahan | naikkan `AUTO_SCRAPE_INTERVAL_HOURS`, atau turunkan `mem_limit` Chromium; pertimbangkan upgrade RAM ke 8GB |
| Tunnel tidak connect | token salah | buat ulang token, update `.env`, `docker compose up -d cloudflared` |

---

## Yang sebaiknya ditambahkan setelah live

- **Rate limiting** endpoint AI (biar API key GROQ tidak disalahgunakan) — pakai `express-rate-limit`.
- **Fail2ban** kalau nanti buka SSH ke internet (atau cukup lewat Tailscale).
- **Watchtower** untuk auto-update image, atau tetap manual `git pull`.
- **Migrasi SQLite → PostgreSQL** kalau user bertambah.
