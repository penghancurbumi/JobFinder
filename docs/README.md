# JobFinder

## Overview

JobFinder adalah platform agregator pencarian kerja dan magang berbasis web yang dirancang khusus untuk pasar Indonesia. Platform ini mengumpulkan lowongan pekerjaan dari berbagai website penyedia lowongan sehingga pengguna tidak perlu membuka banyak platform secara terpisah.

Selain sebagai mesin pencari lowongan kerja, JobFinder juga menyediakan berbagai fitur berbasis Artificial Intelligence (AI) untuk membantu pengguna mempersiapkan karier, seperti analisis CV berbasis ATS, pembuat CV interaktif, chatbot karier, serta integrasi Telegram Bot.

Platform dikembangkan menggunakan arsitektur terpisah (Frontend, Backend, dan Scraping Service) sehingga mudah dikembangkan dan dipelihara.

---

# Tujuan Platform

JobFinder dibuat untuk membantu pencari kerja memperoleh informasi lowongan secara lebih cepat, lengkap, dan terpusat.

Tujuan utama platform meliputi:

* Mengumpulkan lowongan pekerjaan dari berbagai platform.
* Mengurangi waktu pencarian kerja.
* Membantu pengguna meningkatkan kualitas CV.
* Memberikan rekomendasi karier berbasis AI.
* Menyediakan pembuat CV yang ramah ATS.
* Memberikan update lowongan secara real-time.
* Menjadi platform karier berbasis AI yang lengkap.

---

# Fitur Utama

## Job Aggregation

Mengumpulkan data lowongan kerja dari berbagai platform menjadi satu tempat.

Platform yang didukung saat ini:

* JobStreet ✓
* Kalibrr ✓
* Tech in Asia ✓
* Glints ✓
* LinkedIn ✓
* KitaLulus ✓ (*under development*)
* Pintarnya ✓ (*under development*)

Pengembangan berikutnya dapat menambahkan platform lain sesuai kebutuhan.

---

## Smart Search

Pencarian lowongan berdasarkan:

* Kata kunci
* Nama perusahaan
* Lokasi
* Jenis pekerjaan
* Work Type
* Salary
* Experience Level

---

## Job Filter

Filter berdasarkan:

* Fulltime
* Parttime
* Internship
* Freelance
* Contract
* Hybrid
* Remote

---

## AI CV Analyzer

Pengguna dapat mengunggah file PDF CV untuk dianalisis menggunakan Google Gemini.

Hasil analisis meliputi:

* ATS Score
* Resume Score
* Missing Skills
* Keyword Analysis
* AI Recommendation
* Strength
* Weakness
* Improvement Suggestion

Pengembangan berikutnya akan menambahkan visualisasi berupa grafik dan persentase penilaian agar hasil analisis lebih mudah dipahami.

---

## AI CV Builder

CV Builder memungkinkan pengguna membuat CV secara bertahap menggunakan sistem wizard.

Fitur yang tersedia:

* Informasi Pribadi
* Pendidikan
* Pengalaman Kerja
* Organisasi
* Sertifikat
* Skill
* Bahasa
* Proyek
* Referensi
* Ringkasan Profil

Setiap bagian dilengkapi saran AI sehingga pengguna dapat membuat CV yang lebih profesional.

---

## AI Career Chatbot

Chatbot berbasis Google Gemini yang dapat membantu pengguna:

* Memberikan saran karier.
* Menjelaskan posisi pekerjaan.
* Memberikan tips wawancara.
* Memberikan rekomendasi pekerjaan dari database JobFinder.
* Menjawab pertanyaan mengenai CV.

---

## Telegram Bot

Telegram Bot memungkinkan pengguna:

* Mencari lowongan kerja.
* Mendapatkan tips karier.
* Menggunakan AI Chat.
* Menerima update lowongan.

---

## Real-time Job Update

Menggunakan Socket.IO sehingga perubahan data lowongan dapat langsung diterima oleh frontend tanpa perlu memuat ulang seluruh halaman.

---

## Help Center

Platform menyediakan halaman Help Center di rute `/help` yang berisi panduan penggunaan seluruh fitur, FAQ, dan informasi bantuan lainnya.

---

# Teknologi yang Digunakan

## Frontend

* Vue 3
* Vue Router
* Vite
* Tailwind CSS
* Axios
* Socket.IO Client

## Backend

* Node.js
* Express.js
* Socket.IO
* SQLite3
* Multer
* pdf-parse
* Cheerio

## Artificial Intelligence

* Google Gemini
* Gemma-4-26B

## Scraping

* Python
* Scrapy
* BeautifulSoup4
* SQLAlchemy
* Alembic
* APScheduler
* Fake User Agent

---

# Struktur Project

```text
job-scrapper/
│
├── backend/
│   ├── server.js
│   ├── scrapers/
│   ├── scrapping-job/     (Python Scrapy project)
│   ├── db.js
│   ├── cvAnalyzer.js
│   ├── cvBuilder.js
│   ├── chatbot.js
│   └── telegramBot.js
├── frontend/
│   ├── src/
│   │   ├── views/
│   │   ├── router/
│   │   └── assets/
│   └── package.json
├── docs/
│   ├── README.md
│   ├── PRD.md
│   ├── DESIGN.md
│   ├── ARCHITECTURE.md
│   ├── ROADMAP.md
│   ├── SKILLS.md
│   ├── AGENT.md
│   └── planning/
└── package.json
```

---

# Cara Kerja Sistem

## 1. Scraping

Python Scrapy mengambil data lowongan dari berbagai platform.

↓

Membersihkan data.

↓

Menghapus data duplikat.

↓

Menyimpan JSON.

---

## 2. Data Ingestion

Backend membaca file JSON.

↓

Melakukan validasi.

↓

Menyimpan data ke SQLite.

↓

Mengirim event WebSocket.

---

## 3. Frontend

Frontend mengambil data dari backend.

↓

Menampilkan daftar lowongan.

↓

User melakukan pencarian dan filter.

↓

Backend mengembalikan hasil secara real-time.

---

## 4. Artificial Intelligence

Google Gemini digunakan untuk:

* Analisis CV.
* CV Builder.
* Career Chatbot.
* Telegram AI Assistant.

---

# Dokumentasi

Dokumentasi lengkap tersedia pada folder `docs/`.

* README.md
* PRD.md
* DESIGN.md
* ARCHITECTURE.md
* ROADMAP.md
* SKILLS.md
* AGENT.md
* planning/

---

# Pengembangan Selanjutnya

Beberapa pengembangan yang direncanakan:

* Meningkatkan jumlah hasil scraping menjadi minimal 60 lowongan dari setiap platform.
* Optimalisasi mekanisme scraping agar hanya berjalan saat halaman dimuat ulang atau ketika pengguna menekan tombol "Perbarui Data".
* Penyempurnaan hasil AI CV Analyzer dengan grafik, persentase, dan visualisasi yang lebih informatif.
* Redesain AI CV Builder menggunakan wizard dengan sidebar navigasi, validasi setiap tahap, indikator progres, serta navigasi langkah demi langkah.

---

# Kontribusi

Kontribusi terhadap pengembangan JobFinder sangat terbuka.

Sebelum melakukan perubahan kode, pastikan membaca:

* PRD.md
* DESIGN.md
* AGENT.md

agar implementasi tetap mengikuti standar proyek.

---

# License

Project ini dikembangkan sebagai platform pembelajaran dan pengembangan sistem agregator lowongan kerja berbasis Artificial Intelligence.
