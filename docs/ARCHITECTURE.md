# System Architecture Document

**Project Name:** JobFinder

**Version:** 2.0

**Status:** Draft

**Last Updated:** July 2026

---

# 1. Overview

## 1.1 Deskripsi

JobFinder merupakan platform agregator lowongan kerja berbasis Artificial Intelligence yang dirancang untuk membantu pencari kerja menemukan informasi lowongan dari berbagai platform dalam satu aplikasi.

Selain menyediakan layanan pencarian pekerjaan, JobFinder juga memiliki beberapa layanan AI seperti AI CV Analyzer, AI CV Builder, AI Career Chatbot, serta Telegram Bot yang saling terintegrasi.

Platform dibangun menggunakan arsitektur modular sehingga setiap layanan dapat dikembangkan secara independen tanpa mempengaruhi layanan lainnya.

---

# 2. Architecture Goals

Arsitektur sistem dirancang dengan tujuan sebagai berikut.

- Modular
- Scalable
- Maintainable
- Reusable
- Easy to Extend
- Easy to Debug
- AI Friendly
- High Performance

---

# 3. Architecture Principles

Pengembangan JobFinder mengikuti beberapa prinsip berikut.

## Modular Architecture

Setiap fitur dipisahkan menjadi module yang berdiri sendiri sehingga mudah dikembangkan.

Contoh:

- CV Analyzer
- CV Builder
- Chatbot
- Telegram Bot
- Scraping

masing-masing memiliki service sendiri.

---

## Separation of Concern

Frontend

↓

Backend

↓

Scraping

↓

Database

↓

AI

dipisahkan menjadi service yang berbeda.

---

## Layered Architecture

Presentation Layer

↓

Business Layer

↓

Data Layer

↓

External Service

---

## Reusability

Seluruh komponen dibuat reusable.

Contoh

Frontend

- Button
- Card
- Modal
- Input
- Table

Backend

- AI Service
- Job Service
- Scraping Service
- CV Service

---

## Scalability

Platform harus mudah dikembangkan.

Contoh

Saat ingin menambahkan platform baru seperti Indeed.

Developer hanya perlu menambahkan Spider baru tanpa mengubah seluruh sistem.

---

# 4. High Level Architecture

```

                    +--------------------+
                    |     Frontend       |
                    |      Vue 3         |
                    +---------+----------+
                              |
                              |
                    REST API / Socket.IO
                              |
                              |
                    +---------v----------+
                    |      Backend       |
                    |     Express.js     |
                    +---------+----------+
                              |
         +--------------------+--------------------+
         |                    |                    |
         |                    |                    |
+--------v-------+   +--------v-------+   +--------v-------+
|  SQLite DB     |   | Google Gemini  |   | Telegram Bot   |
+----------------+   +----------------+   +----------------+

                              |
                              |
                    +---------v----------+
                    | Python Scrapy      |
                    | Job Aggregation    |
                    +--------------------+

```

---

# 5. System Components

JobFinder terdiri dari beberapa komponen utama.

## Frontend

Berfungsi sebagai antarmuka pengguna.

Teknologi

- Vue 3
- Vue Router
- Tailwind CSS
- Vite
- Axios
- Socket.IO Client

Tanggung jawab

- Menampilkan data
- Form CV
- Upload PDF
- Chat Interface
- Dashboard
- Search
- Filter

---

## Backend

Berfungsi sebagai pusat logika aplikasi.

Teknologi

- Express.js
- Node.js

Tanggung jawab

- REST API
- WebSocket
- Authentication
- Job Service
- AI Service
- CV Service
- Telegram Service

---

## Database

Menggunakan SQLite sebagai database utama.

Data yang disimpan

- Jobs
- Companies
- Chat Sessions
- CV History
- User Preferences

Database dapat diganti ke PostgreSQL atau MySQL apabila diperlukan.

---

## Scraping Service

Menggunakan Python Scrapy.

Tanggung jawab

- Crawling
- Parsing
- Cleaning
- Deduplication
- Export JSON

---

## Artificial Intelligence

Menggunakan Google Gemini.

Digunakan untuk

- CV Analyzer

- CV Builder

- Career Chatbot

- Resume Summary

- Skill Recommendation

---

## Telegram Bot

Berfungsi sebagai media alternatif pengguna.

Fitur

- Cari Lowongan

- Chat AI

- Tips Karier

- Update Lowongan

---

# 6. Technology Stack

## Frontend

Framework

Vue 3

Build Tool

Vite

Styling

Tailwind CSS

Routing

Vue Router

HTTP Client

Axios

Realtime

Socket.IO Client

---

## Backend

Runtime

Node.js

Framework

Express.js

Realtime

Socket.IO

Database

SQLite

File Upload

Multer

PDF Parser

pdf-parse

---

## Scraping

Language

Python

Framework

Scrapy

Scheduler

APScheduler

ORM

SQLAlchemy

Migration

Alembic

HTML Parser

BeautifulSoup4

lxml

---

## Artificial Intelligence

Provider

Google Gemini

Model

Gemma-4-26B

---

# 7. Directory Structure

```

job-scrapper/

├── backend/
│
├── frontend/
│
├── docs/
│
├── docker/
│
├── scripts/
│
├── .env
│
├── package.json
│
└── README.md

```

---

# 8. Backend Structure

backend/

```
backend/

controllers/

services/

routes/

middlewares/

database/

scrapers/

telegram/

ai/

utils/

server.js

```

Setiap folder memiliki tanggung jawab yang berbeda sehingga struktur kode tetap bersih dan mudah dipelihara.

---

# 9. Frontend Structure

frontend/src/

```
components/

layouts/

pages/

router/

stores/

services/

assets/

composables/

utils/

```

Frontend menggunakan pendekatan Component-Based Architecture.

Seluruh halaman dibangun menggunakan reusable component.

---

# 10. Data Flow Overview

Aliran data utama pada sistem.

```

Python Scrapy

↓

JSON

↓

Backend

↓

SQLite

↓

REST API

↓

Frontend

↓

User

```

Seluruh proses data berjalan satu arah sehingga memudahkan debugging dan pemeliharaan sistem.

---

---

# 11. Scraping Architecture

## Overview

Scraping Service merupakan komponen yang bertanggung jawab untuk mengambil data lowongan pekerjaan dari berbagai platform dan mengubahnya menjadi data yang dapat digunakan oleh JobFinder.

Scraping dijalankan sebagai service terpisah menggunakan Python dan Scrapy sehingga tidak membebani Backend API.

---

## Supported Platforms

Platform yang wajib didukung.

- JobStreet
- Kalibrr
- Tech in Asia
- Glints
- LinkedIn Jobs
- KitaLulus
- Pintarnya

Arsitektur dibuat modular sehingga platform baru dapat ditambahkan dengan membuat Spider baru tanpa mengubah komponen lain.

---

## Scraping Pipeline

Setiap Spider mengikuti alur berikut.

```
Scheduler / Manual Trigger

↓

Spider

↓

Request

↓

Response

↓

HTML Parsing

↓

Data Extraction

↓

Validation

↓

Cleaning

↓

Normalization

↓

Duplicate Detection

↓

JSON Export

↓

Backend Import

↓

Database
```

---

## Spider Structure

Setiap platform memiliki Spider sendiri.

```
job_scraper/

spiders/

base_spider.py

jobstreet.py

kalibrr.py

techinasia.py

glints.py

linkedin.py

kitalulus.py

pintarnya.py
```

Seluruh Spider mewarisi `base_spider.py` agar kode lebih konsisten.

---

## Data Validation

Data yang berhasil diambil harus memenuhi informasi minimal.

- Job Title
- Company
- Location
- Work Type
- Description
- Source URL
- Posted Date

Data yang tidak memenuhi syarat tidak akan disimpan.

---

## Duplicate Detection

Sistem melakukan deduplikasi menggunakan beberapa parameter.

Prioritas pertama

```
URL
```

Apabila URL tidak tersedia maka digunakan kombinasi.

```
Company

+

Title

+

Location
```

---

## Scheduling

Scheduler berjalan otomatis setiap 30 menit.

Selain Scheduler, scraping juga dapat dijalankan secara manual melalui tombol **Perbarui Data**.

---

# 12. Job Update Flow

## Kondisi Lama

```
User membuka /jobs

↓

Backend langsung menjalankan Scraping

↓

Loading lama

↓

Frontend menunggu
```

Cara tersebut menyebabkan halaman menjadi lambat.

---

## Arsitektur Baru

```
User membuka /jobs

↓

Frontend meminta data

↓

Backend membaca SQLite

↓

Frontend menampilkan data

↓

Selesai
```

Tidak ada proses scraping.

---

## Ketika User Menekan Tombol "Perbarui Data"

```
Button

↓

Backend

↓

Run Scrapy

↓

Export JSON

↓

Import Database

↓

Socket.IO

↓

Frontend Refresh
```

---

## Ketika User Reload Halaman

```
Reload

↓

Backend

↓

Check Data Age

↓

Jika data masih baru

↓

Gunakan Database

↓

Jika data sudah lama

↓

Run Scraping

↓

Update Database

↓

Frontend Refresh
```

Dengan mekanisme ini proses scraping menjadi lebih efisien.

---

# 13. Backend Architecture

Backend menggunakan pendekatan Service Layer.

```
Controller

↓

Service

↓

Repository

↓

Database
```

---

## Controllers

Controller menerima request dari frontend.

Contoh.

```
JobsController

CVController

ChatbotController

TelegramController
```

Controller tidak boleh berisi Business Logic.

---

## Services

Seluruh logika aplikasi berada pada Service.

Contoh.

```
JobService

CVService

ChatbotService

TelegramService

ScrapingService
```

---

## Repository

Repository bertanggung jawab terhadap Database.

```
JobRepository

ChatRepository

CVRepository
```

---

## Benefits

- Mudah Testing

- Mudah Debugging

- Mudah Refactoring

- Mudah Maintenance

---

# 14. Database Architecture

SQLite digunakan sebagai database utama.

Database dapat diganti menjadi PostgreSQL tanpa mengubah Business Logic.

---

## Main Tables

```
jobs

companies

categories

chat_sessions

cv_history

settings
```

---

## Jobs Table

Data minimal.

```
id

title

company

location

salary

work_type

description

requirements

source

url

created_at

updated_at
```

---

## Chat Sessions

Menyimpan histori percakapan AI.

```
id

session_id

question

answer

created_at
```

---

## CV History

Menyimpan histori analisis CV.

```
id

filename

score

summary

recommendation

created_at
```

---

# 15. WebSocket Architecture

Socket.IO digunakan untuk komunikasi real-time.

---

## Events

Frontend mengirim.

```
refresh-jobs

filter-jobs

search-jobs
```

Backend mengirim.

```
jobs-updated

scraping-started

scraping-progress

scraping-finished

error
```

---

## Flow

```
Frontend

↓

Socket.IO

↓

Backend

↓

Database

↓

Socket.IO

↓

Frontend
```

---

# 16. REST API Flow

```
Frontend

↓

Axios

↓

Express API

↓

Service

↓

Repository

↓

Database

↓

Response

↓

Frontend
```

---

# 17. AI Architecture

Seluruh AI menggunakan Google Gemini.

```
Frontend

↓

Backend

↓

Gemini Service

↓

Response

↓

Frontend
```

---

## AI Modules

### CV Analyzer

Input

```
PDF
```

Output

```
ATS Score

Charts

Recommendation

Summary
```

---

### CV Builder

Input

```
Form
```

Output

```
Suggestion

Professional Summary

Project Description

Skill Suggestion
```

---

### Career Chatbot

Input

```
Question
```

Output

```
Answer

Job Recommendation

Interview Tips
```

---

# 18. Telegram Bot

Telegram Bot menggunakan service yang sama dengan Chatbot.

```
Telegram

↓

Telegram Bot API

↓

Backend

↓

Gemini

↓

Response
```

Dengan pendekatan ini tidak ada duplikasi kode AI.

---

# 19. Error Handling

Seluruh service harus memiliki standar Error Handling.

Contoh.

```
Validation Error

Authentication Error

Network Error

Database Error

AI Error

Scraping Error
```

Seluruh error harus dicatat ke dalam log sehingga mudah dianalisis.

---

---

# 20. Deployment Architecture

## Overview

JobFinder dirancang menggunakan arsitektur yang mendukung pengembangan lokal maupun deployment ke lingkungan production.

Seluruh komponen aplikasi dipisahkan menjadi beberapa service sehingga mudah dikembangkan, dipelihara, dan diskalakan.

Komponen utama meliputi:

- Frontend
- Backend API
- Database
- Scraping Service
- AI Service
- Telegram Bot

---

## Development Environment

Pada lingkungan pengembangan, seluruh service dapat dijalankan secara lokal.

```

Frontend (Vue)

↓

Backend (Express)

↓

SQLite

↓

Scrapy

↓

Google Gemini

↓

Telegram Bot

```

---

## Production Environment

Pada lingkungan production setiap service dapat berjalan secara terpisah.

```

Internet

↓

Reverse Proxy (Nginx)

↓

Frontend

↓

Backend API

↓

Database

↓

Scraping Service

↓

Google Gemini

↓

Telegram Bot

```

Arsitektur ini memungkinkan setiap service diperbarui tanpa menghentikan keseluruhan sistem.

---

# 21. Docker Architecture

Seluruh aplikasi direkomendasikan berjalan menggunakan Docker.

## Services

Frontend

Backend

Database

Scraping

Nginx

Telegram Bot

---

## Docker Compose

Contoh struktur service.

```

docker-compose.yml

frontend

backend

database

scraper

nginx

telegram

```

Setiap service memiliki container masing-masing sehingga proses deployment menjadi lebih sederhana.

---

# 22. Security Architecture

Keamanan merupakan bagian penting dalam pengembangan JobFinder.

---

## Environment Variables

Seluruh informasi sensitif harus disimpan pada file `.env`.

Contoh:

- API Key Gemini
- Telegram Bot Token
- Database URL
- Secret Key

Tidak diperbolehkan menyimpan informasi sensitif secara langsung pada source code.

---

## File Upload Security

CV Analyzer hanya menerima file:

- PDF

Ukuran file dibatasi sesuai konfigurasi sistem.

Seluruh file harus divalidasi sebelum diproses.

---

## API Security

Seluruh endpoint harus melakukan:

- Input Validation
- Data Sanitization
- Error Handling
- Rate Limiting (direkomendasikan)
- Authentication (untuk fitur yang memerlukannya)

---

## Database Security

Seluruh query database harus menggunakan parameter binding untuk mencegah SQL Injection.

---

## Scraping Security

Scraping menggunakan:

- User-Agent Rotation
- Retry Middleware
- Proxy (opsional)
- Request Delay
- Respect Robots.txt jika diperlukan

---

# 23. Performance Optimization

Platform harus tetap memiliki performa yang baik meskipun jumlah data semakin besar.

---

## Frontend

Optimasi yang digunakan:

- Lazy Loading
- Dynamic Import
- Component Reuse
- Image Optimization
- Loading Skeleton

---

## Backend

Optimasi:

- Service Layer
- Modular Architecture
- Pagination
- Query Optimization
- Connection Reuse

---

## Database

Optimasi:

- Indexing
- Duplicate Detection
- Efficient Query
- Backup

---

## Scraping

Optimasi:

- Concurrent Request
- Retry
- Queue
- Scheduler
- Incremental Scraping

---

# 24. Logging Architecture

Seluruh aktivitas sistem harus dicatat.

Kategori log meliputi:

- API Request
- API Error
- Database Error
- Scraping Activity
- AI Request
- Telegram Activity
- Authentication
- Validation Error

Log disimpan dalam format yang mudah dianalisis untuk proses debugging maupun monitoring.

---

# 25. Monitoring

Monitoring digunakan untuk mengetahui kondisi sistem secara real-time.

Parameter yang dipantau:

- Status Backend
- Status Frontend
- Status Database
- Status Scraper
- Status AI Service
- Status Telegram Bot

Statistik yang dipantau:

- Jumlah Request
- Response Time
- Error Rate
- Scraping Success Rate
- AI Response Time
- Active User

---

# 26. Backup Strategy

Data penting harus memiliki mekanisme pencadangan.

Data yang perlu dibackup:

- Database
- Konfigurasi
- Dokumentasi
- Export JSON (opsional)

Backup dilakukan secara berkala sesuai kebutuhan.

---

# 27. Scalability Strategy

Arsitektur JobFinder dirancang agar mudah dikembangkan.

Pengembangan yang dapat dilakukan di masa depan meliputi:

- Menambah platform scraping baru.
- Mengganti SQLite menjadi PostgreSQL atau MySQL.
- Menambahkan AI Provider lain.
- Menambahkan Authentication Service.
- Menambahkan Company Dashboard.
- Menambahkan Mobile Application.
- Menambahkan Notification Service.

Perubahan tersebut dapat dilakukan tanpa mengubah keseluruhan arsitektur.

---

# 28. Recommended Future Architecture

Arsitektur yang direkomendasikan untuk skala besar adalah sebagai berikut.

```

                Internet
                    │
          Reverse Proxy (Nginx)
                    │
        ┌───────────┼───────────┐
        │           │           │
   Frontend     Backend API   Telegram Bot
        │           │
        │     ┌─────┴─────┐
        │     │           │
        │  AI Service   Job Service
        │     │           │
        │     └─────┬─────┘
        │           │
        │      PostgreSQL
        │           │
        │    Redis Cache
        │           │
        └────── Scraping Service
                    │
          Multiple Scrapy Spiders

```

Arsitektur ini memungkinkan sistem menangani lebih banyak pengguna, lebih banyak platform scraping, dan volume data yang lebih besar.

---

# 29. Architecture Decision Records (ADR)

Dokumen ini mencatat keputusan arsitektur utama yang diambil selama pengembangan.

## ADR-001

Menggunakan Vue 3 sebagai frontend.

Alasan:

- Ringan.
- Mudah dikembangkan.
- Composition API.

---

## ADR-002

Menggunakan Express.js sebagai backend.

Alasan:

- Sederhana.
- Cepat.
- Ekosistem besar.

---

## ADR-003

Menggunakan Python Scrapy untuk scraping.

Alasan:

- Stabil.
- Cepat.
- Mudah menambah Spider.

---

## ADR-004

Menggunakan Google Gemini sebagai AI.

Alasan:

- Mendukung analisis teks.
- Cocok untuk CV Analyzer.
- Cocok untuk Career Chatbot.

---

## ADR-005

Menggunakan Socket.IO.

Alasan:

- Mendukung komunikasi real-time.
- Mudah diintegrasikan dengan Vue.

---

## ADR-006

Menggunakan arsitektur modular.

Alasan:

- Mudah dipelihara.
- Mudah dikembangkan.
- Memudahkan refactoring.

---

# 30. Kesimpulan

Arsitektur JobFinder dirancang menggunakan pendekatan modular yang memisahkan Frontend, Backend, Database, Scraping Service, Artificial Intelligence, dan Telegram Bot menjadi komponen yang saling terintegrasi namun tetap independen.

Pendekatan ini memberikan beberapa keuntungan:

- Mudah dikembangkan.
- Mudah dipelihara.
- Mudah menambahkan fitur baru.
- Mendukung skalabilitas.
- Mendukung integrasi AI.
- Siap untuk deployment ke lingkungan production.

Seluruh implementasi teknis pada proyek JobFinder harus mengacu pada dokumen Architecture ini agar pengembangan tetap konsisten, terdokumentasi, dan sesuai dengan tujuan sistem.