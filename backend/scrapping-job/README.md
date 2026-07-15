# 🔍 Job Scraper — Multi-Platform Job Scraping System

Sistem scraping lowongan kerja otomatis yang mengumpulkan data dari berbagai platform job board Indonesia menggunakan **Scrapy + Playwright**.

## ✨ Fitur

- 🕷️ **7 Platform**: JobStreet, Glints, Kalibrr, Indeed, LinkedIn, JobsDB, Tech in Asia
- 🎭 **Playwright**: Full JavaScript rendering untuk SPA/React sites
- 🧹 **Pipeline Otomatis**: Validasi → Cleaning → Normalisasi → Deduplikasi → Database
- 🗄️ **PostgreSQL**: Penyimpanan dengan indexing optimal
- 📊 **Export**: JSON, CSV, Excel
- ⏰ **Scheduler**: Cron job otomatis (hourly/6h/daily)
- 🔄 **Deduplikasi**: URL exact match + title+company+city fingerprint
- 🪵 **Logging**: Terpisah (scraping, error, stats)
- 🧪 **Tested**: Unit tests untuk semua services

## 📋 Prasyarat

- Python 3.12+
- PostgreSQL 14+
- Chromium (diinstall otomatis oleh Playwright)

## 🚀 Instalasi

### 1. Clone & Setup Virtual Environment

```bash
cd d:\scrapping-job

# Buat virtual environment
python -m venv venv

# Aktivasi (Windows)
venv\Scripts\activate

# Aktivasi (Linux/Mac)
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Playwright Browsers

```bash
playwright install chromium
```

### 4. Konfigurasi Environment

```bash
# Copy template
copy .env.example .env

# Edit .env dengan konfigurasi Anda
```

### 5. Setup Database

```sql
-- Buat database di PostgreSQL
CREATE DATABASE job_scraper;
```

Tabel akan dibuat otomatis saat spider pertama kali dijalankan.

## ⚙️ Konfigurasi

Edit file `.env` untuk mengatur:

| Variable | Default | Deskripsi |
|---|---|---|
| `DB_HOST` | localhost | Host PostgreSQL |
| `DB_PORT` | 5432 | Port PostgreSQL |
| `DB_NAME` | job_scraper | Nama database |
| `DB_USER` | postgres | User database |
| `DB_PASSWORD` | - | Password database |
| `CONCURRENT_REQUESTS` | 8 | Jumlah request bersamaan |
| `DOWNLOAD_DELAY` | 1.0 | Delay antar request (detik) |
| `PLAYWRIGHT_HEADLESS` | true | Jalankan browser tanpa UI |
| `PROXY_ENABLED` | false | Aktifkan proxy |
| `EXPORT_ENABLED` | false | Aktifkan export otomatis |
| `EXPORT_FORMAT` | json | Format export (json/csv/excel) |

## 🕷️ Menjalankan Spider

### Spider Individual

```bash
# Crawl satu platform
scrapy crawl glints
scrapy crawl jobstreet
scrapy crawl kalibrr
scrapy crawl indeed
scrapy crawl linkedin
scrapy crawl jobsdb
scrapy crawl techinasia
```

### Semua Spider

```bash
scrapy crawl_all
```

### Dengan Filter

```bash
# Hanya lowongan magang
scrapy crawl glints -a job_type=internship

# Hanya remote
scrapy crawl glints -a work_type=remote

# Dengan keyword
scrapy crawl glints -a keyword="software engineer"

# Limit halaman
scrapy crawl glints -a max_pages=5
```

### Menjalankan Semua dengan Filter

```bash
scrapy crawl_all --job-type internship
scrapy crawl_all --work-type remote
scrapy crawl_all --max-pages 10
```

## ⏰ Scheduler

Jalankan scheduler untuk crawling otomatis:

```bash
# Default: setiap 6 jam
python scheduler.py

# Konfigurasi interval di .env:
# SCHEDULER_INTERVAL_HOURS=1   (setiap jam)
# SCHEDULER_INTERVAL_HOURS=6   (setiap 6 jam)
# SCHEDULER_INTERVAL_HOURS=24  (setiap hari)
```

## 📊 Export Data

### Otomatis (via Pipeline)

Set di `.env`:
```
EXPORT_ENABLED=true
EXPORT_FORMAT=json   # json, csv, atau excel
```

File export akan disimpan di folder `exports/`.

### Manual

```bash
# Export ke JSON
scrapy crawl glints -o exports/json/glints.json

# Export ke CSV
scrapy crawl glints -o exports/csv/glints.csv
```

## 🧪 Testing

```bash
# Jalankan semua tests
python -m pytest tests/ -v

# Dengan coverage
python -m pytest tests/ -v --cov=job_scraper

# Test specific
python -m pytest tests/test_validator.py -v
python -m pytest tests/test_cleaner.py -v
python -m pytest tests/test_normalizer.py -v
python -m pytest tests/test_deduplicator.py -v
```

## 📁 Struktur Project

```
scrapping-job/
├── scrapy.cfg                 # Scrapy config
├── requirements.txt           # Dependencies
├── .env.example               # Template environment
├── scheduler.py               # Cron scheduler
│
├── job_scraper/               # Main package
│   ├── settings.py            # Scrapy settings
│   ├── items.py               # Item definitions
│   ├── pipelines.py           # Pipeline chain
│   ├── middlewares.py         # Custom middlewares
│   ├── database.py            # DB connection
│   ├── constants.py           # Enums & mappings
│   ├── logger.py              # Logging config
│   ├── utils.py               # Utilities
│   │
│   ├── spiders/               # Spider implementations
│   │   ├── base_spider.py     # Abstract base
│   │   ├── glints.py          # Glints spider
│   │   └── ...                # Other spiders
│   │
│   ├── services/              # Business logic
│   │   ├── cleaner.py         # HTML cleaning
│   │   ├── validator.py       # Validation
│   │   ├── normalizer.py      # Normalization
│   │   └── deduplicator.py    # Dedup logic
│   │
│   ├── models/                # ORM models
│   │   └── job.py             # Job table model
│   │
│   └── commands/              # Custom CLI commands
│       └── crawl_all.py       # Run all spiders
│
├── exports/                   # Export output
├── logs/                      # Log files
├── storage/                   # Temp storage
├── tests/                     # Unit tests
└── docs/                      # Documentation
```

## 🔧 Troubleshooting

### Playwright Browser Error

```bash
# Reinstall browser
playwright install chromium --with-deps
```

### Database Connection Error

1. Pastikan PostgreSQL berjalan
2. Cek kredensial di `.env`
3. Pastikan database sudah dibuat: `CREATE DATABASE job_scraper;`

### Spider Blocked / 403 Error

1. Naikkan `DOWNLOAD_DELAY` di `.env`
2. Aktifkan proxy: `PROXY_ENABLED=true`
3. Cek log di `logs/error_*.log`

### Import Error

```bash
# Pastikan virtual environment aktif
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Reinstall dependencies
pip install -r requirements.txt
```

## 📝 Pipeline Flow

```
Scraped Item
    │
    ▼
┌─────────────────┐
│ 1. Validation   │ → Drop jika field wajib kosong
├─────────────────┤
│ 2. Cleaning     │ → Hapus HTML, special chars
├─────────────────┤
│ 3. Normalization│ → Standarisasi lokasi, tipe, gaji
├─────────────────┤
│ 4. Deduplication│ → Drop jika duplikat (URL/fingerprint)
├─────────────────┤
│ 5. PostgreSQL   │ → INSERT atau UPDATE ke database
├─────────────────┤
│ 6. Export       │ → Simpan ke JSON/CSV/Excel (opsional)
└─────────────────┘
```

## 📄 License

Private project.
