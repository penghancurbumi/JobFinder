# Product Requirements Document (PRD)

**Project Name:** JobFinder

**Version:** 2.0

**Status:** Draft

**Document Owner:** Development Team

**Last Updated:** July 2026

---

# 1. Project Overview

## 1.1 Latar Belakang

Mencari pekerjaan di Indonesia saat ini mengharuskan pengguna membuka banyak platform seperti JobStreet, Kalibrr, Glints, Tech in Asia, LinkedIn, KitaLulus, dan Pintarnya. Setiap platform memiliki data lowongan yang berbeda sehingga proses pencarian menjadi kurang efisien.

Selain itu, banyak pencari kerja mengalami kesulitan dalam membuat CV yang sesuai dengan standar Applicant Tracking System (ATS), memahami kekurangan CV yang dimiliki, serta memperoleh rekomendasi pekerjaan yang relevan dengan kemampuan mereka.

JobFinder dikembangkan sebagai platform agregator lowongan kerja berbasis Artificial Intelligence yang menggabungkan berbagai sumber lowongan pekerjaan ke dalam satu aplikasi. Selain menyediakan pencarian pekerjaan, platform ini juga membantu pengguna meningkatkan kualitas dokumen lamaran melalui AI CV Analyzer, AI CV Builder, AI Career Chatbot, dan Telegram Bot.

---

# 2. Vision

Menjadi platform pencarian kerja dan pengembangan karier berbasis Artificial Intelligence yang menyediakan informasi lowongan kerja secara lengkap, akurat, dan mudah diakses oleh seluruh pencari kerja di Indonesia.

---

# 3. Mission

JobFinder memiliki beberapa misi utama:

* Mengumpulkan lowongan pekerjaan dari berbagai platform dalam satu sistem.
* Membantu pengguna menemukan pekerjaan yang sesuai dengan kemampuan dan minat.
* Menyediakan analisis CV berbasis AI agar lebih sesuai dengan standar ATS.
* Membantu pengguna membuat CV profesional secara mudah.
* Menyediakan asisten karier berbasis AI yang dapat memberikan rekomendasi pekerjaan, saran karier, serta tips wawancara.
* Menyediakan pembaruan data lowongan secara berkala dengan proses scraping otomatis.
* Mengembangkan platform yang modern, responsif, dan mudah digunakan.

---

# 4. Product Goals

Platform JobFinder dikembangkan untuk mencapai tujuan berikut:

1. Menjadi pusat agregasi lowongan kerja dari berbagai platform.
2. Mempermudah pencarian kerja melalui fitur pencarian dan filter yang lengkap.
3. Mengurangi waktu yang dibutuhkan pengguna dalam mencari pekerjaan.
4. Meningkatkan kualitas CV pengguna melalui AI.
5. Membantu pengguna memperoleh rekomendasi pekerjaan yang sesuai dengan profil mereka.
6. Menyediakan pengalaman pengguna yang sederhana, cepat, dan modern.

---

# 5. Scope

## In Scope

Fitur yang termasuk dalam ruang lingkup pengembangan:

* Job Aggregation
* Job Search
* Job Filtering
* Job Sorting
* Job Detail
* AI CV Analyzer
* AI CV Builder
* AI Career Chatbot
* Telegram Bot
* Real-time Update
* Documentation Center
* Help Center

## Out of Scope

Fitur berikut belum termasuk dalam pengembangan versi saat ini:

* Login menggunakan LinkedIn
* Sistem pembayaran
* Marketplace kursus
* Video interview
* Job application langsung ke perusahaan
* Mobile Application (Android/iOS)

---

# 6. Target Users

Platform ditujukan untuk:

### Mahasiswa

Mencari program magang maupun pekerjaan paruh waktu.

### Fresh Graduate

Mencari pekerjaan pertama setelah lulus.

### Professional

Mencari peluang karier baru.

### Freelancer

Mencari pekerjaan berbasis proyek maupun remote.

### Career Switcher

Pengguna yang ingin berpindah bidang pekerjaan.

---

# 7. User Persona

## Persona 1

Nama: Andi

Usia: 22 Tahun

Profesi: Fresh Graduate

Kebutuhan:

* Membuat CV ATS.
* Menemukan pekerjaan pertama.
* Mendapatkan rekomendasi pekerjaan.

Pain Point:

* Tidak mengetahui kualitas CV.
* Sulit menemukan lowongan yang sesuai.

---

## Persona 2

Nama: Siti

Usia: 20 Tahun

Profesi: Mahasiswa

Kebutuhan:

* Program Magang.
* Remote Internship.
* CV sederhana.

Pain Point:

* Harus membuka banyak website.
* Sulit menemukan lowongan magang terbaru.

---

# 8. User Journey

Pengguna membuka JobFinder.

↓

Melihat Hero Section.

↓

Mencari pekerjaan.

↓

Melakukan filter.

↓

Membuka detail lowongan.

↓

Mengunggah CV untuk dianalisis.

↓

Memperbaiki CV menggunakan AI.

↓

Membuat CV baru menggunakan AI CV Builder.

↓

Menggunakan AI Career Chatbot.

↓

Melamar pekerjaan yang sesuai.

---

# 9. Functional Requirements

## Job Aggregation

Platform harus mampu mengumpulkan lowongan pekerjaan dari berbagai sumber.

Platform yang wajib didukung:

* JobStreet
* Kalibrr
* Tech in Asia
* Glints
* LinkedIn Jobs
* KitaLulus
* Pintarnya

Setiap lowongan minimal memiliki informasi:

* Judul pekerjaan
* Nama perusahaan
* Lokasi
* Tipe pekerjaan
* Deskripsi
* Persyaratan
* Gaji (jika tersedia)
* Tanggal publikasi
* URL sumber

---

## Job Search

Sistem harus menyediakan pencarian berdasarkan:

* Kata kunci
* Perusahaan
* Lokasi
* Posisi
* Skill

---

## Job Filter

Pengguna dapat melakukan filter berdasarkan:

* Full Time
* Part Time
* Internship
* Freelance
* Contract
* Hybrid
* Remote
* Salary
* Experience Level

---

## Job Sorting

Sistem harus menyediakan pengurutan berdasarkan:

* Terbaru
* Terlama
* Relevansi
* Nama Perusahaan
* Lokasi

---

## Job Detail

Setiap lowongan harus memiliki halaman detail yang menampilkan:

* Informasi perusahaan
* Deskripsi pekerjaan
* Kualifikasi
* Benefit
* Tautan lamaran
* Lowongan terkait
* Tanggal publikasi
* Platform sumber

---

# 10. AI CV Analyzer

## Deskripsi

AI CV Analyzer merupakan fitur yang membantu pengguna menganalisis Curriculum Vitae (CV) menggunakan Artificial Intelligence berbasis Google Gemini.

Fitur ini bertujuan untuk mengetahui apakah CV telah memenuhi standar Applicant Tracking System (ATS) yang umum digunakan oleh perusahaan.

---

## Tujuan

- Membantu pengguna meningkatkan kualitas CV.
- Mengidentifikasi kekurangan CV.
- Memberikan rekomendasi perbaikan.
- Menampilkan hasil analisis yang mudah dipahami.

---

## Input

- Upload CV dalam format PDF.
- Maksimal ukuran file 5 MB.
- Bahasa Indonesia maupun Bahasa Inggris.

---

## Output

Sistem harus menampilkan:

### ATS Score

Persentase kecocokan CV terhadap standar ATS.

Contoh:

```
ATS Score

87%
```

---

### Overall Score

Penilaian keseluruhan CV.

---

### Skill Match

Daftar skill yang ditemukan.

---

### Missing Skills

Skill yang belum dimiliki.

---

### Resume Summary

Ringkasan isi CV.

---

### Strength

Kelebihan CV.

---

### Weakness

Kekurangan CV.

---

### Improvement Recommendation

Saran AI mengenai bagian yang perlu diperbaiki.

---

### Charts

Versi berikutnya wajib menampilkan visualisasi berupa:

- Radar Chart
- Bar Chart
- Pie Chart
- Persentase setiap kategori

Kategori penilaian:

- ATS Compatibility
- Experience
- Education
- Skills
- Projects
- Certificates
- Soft Skills

Visualisasi harus membantu pengguna memahami bagian mana yang perlu diperbaiki.

---

# 11. AI CV Builder

## Deskripsi

AI CV Builder merupakan fitur untuk membuat Curriculum Vitae secara interaktif menggunakan sistem wizard.

Pengguna akan mengisi informasi sedikit demi sedikit sehingga proses pembuatan CV menjadi lebih mudah.

---

## Layout

Halaman menggunakan dua panel.

### Sidebar Kiri

Berisi navigasi:

- Informasi Pribadi
- Pendidikan
- Pengalaman
- Organisasi
- Sertifikat
- Project
- Skill
- Bahasa
- Referensi
- Ringkasan
- Preview

Sidebar juga menampilkan progress penyelesaian CV.

---

### Panel Kanan

Berisi form sesuai section yang dipilih.

---

## Wizard

Pengguna wajib menyelesaikan langkah sebelumnya sebelum berpindah ke langkah berikutnya.

Urutan:

Personal Information

↓

Education

↓

Experience

↓

Projects

↓

Certificates

↓

Skills

↓

Languages

↓

Summary

↓

Review

↓

Export PDF

---

## AI Suggestion

Setiap field memiliki tombol "Generate with AI".

Contoh:

Job Description

↓

AI memberikan contoh deskripsi pekerjaan.

Skill

↓

AI memberikan rekomendasi skill.

Professional Summary

↓

AI membantu membuat ringkasan profesional.

---

## Validation

Setiap langkah harus memiliki validasi.

Contoh:

Nama belum diisi.

↓

Tidak dapat melanjutkan ke Education.

---

## Auto Save

Data otomatis tersimpan ketika pengguna mengisi form.

---

# 12. AI Career Chatbot

## Tujuan

Membantu pengguna memperoleh informasi karier.

---

## Kemampuan

- Menjawab pertanyaan karier.
- Memberikan tips interview.
- Memberikan tips membuat CV.
- Memberikan rekomendasi pekerjaan.
- Menjelaskan posisi pekerjaan.
- Memberikan saran pengembangan skill.

---

## Integrasi Database

Chatbot harus mampu membaca database lowongan sehingga dapat memberikan rekomendasi pekerjaan yang relevan.

---

# 13. Telegram Bot

Telegram Bot menyediakan akses cepat terhadap JobFinder melalui Telegram.

Fitur:

- Cari pekerjaan.
- Chat AI.
- Tips CV.
- Tips Interview.
- Update lowongan terbaru.
- Rekomendasi pekerjaan.

---

# 14. Real-time Update

Platform menggunakan Socket.IO.

Fungsi:

- Update lowongan terbaru.
- Update status scraping.
- Update hasil filter.
- Sinkronisasi frontend.

---

# 15. Help Center

Platform harus memiliki halaman bantuan.

Minimal berisi:

- Cara mencari pekerjaan.
- Cara menggunakan filter.
- Cara menggunakan CV Analyzer.
- Cara membuat CV.
- Cara menggunakan Chatbot.
- Cara menggunakan Telegram Bot.
- Frequently Asked Questions (FAQ).

---

# 16. Product Improvements (Version 2)

Dokumen berikut merupakan daftar kebutuhan pengembangan (Product Backlog) yang wajib diimplementasikan pada versi berikutnya dari platform JobFinder.

Seluruh poin pada bagian ini bersifat **Mandatory** dan menjadi acuan utama selama proses pengembangan.

---

# 16.1 Penambahan Platform Scraping

## Kondisi Saat Ini

Saat ini JobFinder hanya mendukung proses scraping dari tiga platform:

- JobStreet
- Kalibrr
- Tech in Asia

Jumlah sumber lowongan masih terbatas sehingga data pekerjaan yang diperoleh belum cukup lengkap.

---

## Tujuan

Menjadikan JobFinder sebagai platform agregator lowongan kerja yang menyediakan informasi pekerjaan dari berbagai sumber terpercaya di Indonesia.

---

## Requirement

Platform wajib mendukung scraping dari:

- JobStreet
- Kalibrr
- Tech in Asia
- Glints
- LinkedIn Jobs
- KitaLulus
- Pintarnya

Platform lain dapat ditambahkan pada pengembangan berikutnya apabila memungkinkan secara teknis maupun legal.

---

## Acceptance Criteria

- Semua platform berhasil melakukan scraping.
- Data berhasil disimpan ke database.
- Tidak terjadi duplikasi data.
- Status scraping setiap platform dapat dipantau.

---

# 16.2 Peningkatan Jumlah Data Scraping

## Kondisi Saat Ini

Scraper hanya mengambil satu halaman (`max_pages = 1`) sehingga jumlah data sangat sedikit.

---

## Requirement

Scraper harus dapat mengambil minimal **60 lowongan pekerjaan** dari setiap platform.

Selain itu sistem harus mendukung konfigurasi jumlah halaman scraping agar mudah disesuaikan tanpa mengubah source code.

---

## Ketentuan

Scraping harus memiliki proses:

- Validation
- Data Cleaning
- Normalization
- Duplicate Detection
- Export JSON
- Database Import

---

## Duplicate Detection

Data dianggap sama apabila memiliki:

- URL yang sama

atau

- Judul pekerjaan
- Nama perusahaan
- Lokasi

yang identik.

---

## Acceptance Criteria

- Minimal 60 data berhasil diperoleh dari setiap platform.
- Tidak terdapat data duplikat.
- Data berhasil masuk ke database.
- Data lama diperbarui apabila terdapat perubahan.

---

# 16.3 Penyempurnaan User Interface

## Kondisi Saat Ini

Tampilan antarmuka masih sederhana dan belum memiliki identitas visual yang kuat.

Beberapa halaman juga belum memiliki konsistensi desain.

---

## Requirement

Seluruh halaman wajib mengikuti standar desain yang telah ditentukan pada dokumen `DESIGN.md`.

Perbaikan meliputi:

### Landing Page

- Hero Section
- Features Section
- Statistics
- Documentation
- CTA
- Footer

---

### Jobs Page

- Search Bar
- Filter Sidebar
- Job Card
- Pagination
- Empty State
- Loading Skeleton

---

### CV Analyzer

- Upload Area
- Result Card
- Charts
- Recommendation
- Score Card

---

### CV Builder

- Wizard Layout
- Sidebar Navigation
- Progress Indicator
- Form Validation

---

### Chatbot

- Modern Chat Interface
- Typing Indicator
- Suggested Prompt
- Conversation History

---

### Dashboard

- Statistics
- Recent Jobs
- Activity
- Quick Actions

---

## UI Standard

Seluruh halaman harus memiliki:

- Responsive Layout
- Consistent Typography
- Consistent Color Palette
- Consistent Spacing
- Modern Card Design
- Smooth Animation

---

# 16.4 Peningkatan User Experience

## Tujuan

Memberikan pengalaman penggunaan yang lebih sederhana, cepat, intuitif, dan nyaman.

---

## Requirement

Platform harus memperhatikan aspek UX berikut:

### Navigation

Navigasi harus mudah dipahami.

---

### Feedback

Setiap aksi pengguna harus memberikan umpan balik.

Contoh:

- Loading
- Success
- Warning
- Error

---

### Loading State

Setiap halaman harus memiliki Loading Skeleton.

---

### Empty State

Apabila data kosong, tampilkan ilustrasi beserta penjelasan.

---

### Error Handling

Kesalahan harus ditampilkan dalam bahasa yang mudah dipahami.

---

### Progressive Disclosure

Informasi ditampilkan secara bertahap agar pengguna tidak merasa kewalahan.

---

### Accessibility

Platform harus memenuhi standar aksesibilitas dasar.

Minimal:

- Keyboard Navigation
- Focus Indicator
- Color Contrast
- Screen Reader Friendly

---

## Acceptance Criteria

- Seluruh halaman mudah digunakan.
- Navigasi konsisten.
- Tidak ada halaman yang membingungkan pengguna.
- Seluruh fitur dapat diakses dalam maksimal tiga langkah.

---

# 16.5 Branding Platform

## Kondisi Saat Ini

Platform belum memiliki identitas visual yang konsisten.

---

## Requirement

Untuk versi saat ini belum diperlukan pembuatan logo.

Identitas platform cukup menggunakan teks:

**JobFinder**

---

## Branding

Gunakan identitas berikut:

Nama Platform

JobFinder

---

Tagline

Find Your Future Career Faster

---

Brand Personality

- Modern
- Professional
- Friendly
- Simple
- AI Powered

---

Seluruh warna, icon, tipografi, dan komponen harus mengikuti standar pada `DESIGN.md`.

---

# 16.6 Hero Section

Hero Section menjadi bagian pertama yang dilihat pengguna sehingga harus menjelaskan fungsi platform secara singkat namun jelas.

---

## Requirement

Hero Section minimal berisi:

Headline utama.

Subheadline.

Deskripsi singkat platform.

Statistik jumlah lowongan.

Daftar platform sumber lowongan.

Tombol:

- Cari Lowongan
- Analisis CV
- Buat CV

Section Dokumentasi.

Call To Action.

---

## Acceptance Criteria

Pengguna baru dapat memahami fungsi JobFinder dalam waktu kurang dari 10 detik setelah membuka halaman utama.
---

# 16.7 Help Center

## Kondisi Saat Ini

Platform belum memiliki dokumentasi penggunaan yang dapat membantu pengguna memahami setiap fitur yang tersedia.

Pengguna baru harus dapat memahami cara menggunakan platform tanpa perlu bantuan pihak lain.

---

## Tujuan

Menyediakan pusat bantuan (Help Center) yang menjelaskan penggunaan seluruh fitur JobFinder.

---

## Requirement

Tambahkan halaman **Help Center** yang dapat diakses dari Navbar maupun Footer.

Halaman ini minimal berisi:

### Getting Started

Menjelaskan:

- Apa itu JobFinder.
- Cara menggunakan platform.
- Alur penggunaan.

---

### Job Search Guide

Menjelaskan:

- Cara mencari pekerjaan.
- Cara menggunakan Search.
- Cara menggunakan Filter.
- Cara menggunakan Sorting.
- Cara membuka Detail Job.

---

### CV Analyzer Guide

Menjelaskan:

- Cara upload CV.
- Format file yang didukung.
- Maksimal ukuran file.
- Cara membaca ATS Score.
- Cara memahami hasil analisis.
- Cara memperbaiki CV berdasarkan rekomendasi AI.

---

### CV Builder Guide

Menjelaskan:

- Cara membuat CV.
- Cara berpindah section.
- Cara menggunakan AI Suggestion.
- Cara export PDF.

---

### AI Career Chatbot Guide

Menjelaskan:

- Cara bertanya kepada AI.
- Contoh prompt.
- Cara memperoleh rekomendasi pekerjaan.

---

### Telegram Bot Guide

Menjelaskan:

- Cara menggunakan Telegram Bot.
- Daftar perintah yang tersedia.
- Cara menerima update lowongan.

---

### Frequently Asked Questions (FAQ)

Minimal berisi:

- Bagaimana cara mencari pekerjaan?
- Bagaimana cara membuat CV?
- Bagaimana AI menganalisis CV?
- Mengapa hasil ATS Score berbeda?
- Bagaimana cara memperbarui data lowongan?

---

# 16.8 Project Documentation

## Tujuan

Seluruh dokumentasi proyek harus tersusun secara lengkap agar memudahkan proses pengembangan dan pemeliharaan aplikasi.

---

## Requirement

Repository harus memiliki dokumentasi berikut:

- README.md
- PRD.md
- DESIGN.md
- ARCHITECTURE.md
- ROADMAP.md
- SKILLS.md
- AGENT.md

Dokumentasi tambahan yang direkomendasikan:

- API.md
- DATABASE.md
- SCRAPING.md
- DEPLOYMENT.md
- CHANGELOG.md

---

## Acceptance Criteria

- Seluruh dokumentasi tersedia.
- Dokumentasi selalu diperbarui ketika terdapat perubahan fitur.
- Dokumentasi mudah dipahami oleh developer maupun AI Agent.

---

# 16.9 AI Development Skills

## Tujuan

Seluruh proses pengembangan memanfaatkan AI Skill yang terdokumentasi dengan baik sehingga AI Agent dapat bekerja secara konsisten.

---

## Requirement

Minimal skill yang digunakan:

### Superpowers

Digunakan untuk:

- Refactoring
- Optimasi kode
- Clean Architecture
- Best Practice

---

### Caveman

Digunakan untuk:

- Debugging
- Root Cause Analysis
- Error Investigation

---

### Ponytail

Digunakan untuk:

- UI
- UX
- Accessibility
- Responsive Layout

---

### TasteSkill

Digunakan untuk:

- Color Palette
- Typography
- Component
- Layout

---

### GetDesign

Digunakan untuk:

- Landing Page
- Dashboard
- Modern Component
- Design Inspiration

---

### Skill Tambahan

AI Agent dapat menggunakan skill lain apabila dibutuhkan, seperti:

- Context7
- Sequential Thinking
- Memory
- Playwright
- Browser Automation
- Documentation Assistant

---

# 16.10 Design System

## Tujuan

Seluruh tampilan platform harus mengikuti satu standar desain sehingga memiliki identitas visual yang konsisten.

---

## Requirement

Implementasi UI wajib mengacu pada dokumen `DESIGN.md`.

Standar desain meliputi:

- Color Palette
- Typography
- Layout
- Grid System
- Button
- Form
- Card
- Modal
- Alert
- Sidebar
- Navigation
- Icon
- Loading
- Empty State
- Chart

Referensi desain utama menggunakan **GetDesign**.

---

# 16.11 Optimalisasi Mekanisme Scraping

## Kondisi Saat Ini

Saat pengguna membuka halaman `/jobs`, sistem selalu menjalankan proses scraping.

Hal ini menyebabkan:

- Waktu muat menjadi lebih lama.
- Beban server meningkat.
- Proses scraping dilakukan secara berulang meskipun data masih baru.

---

## Requirement

Perilaku tersebut harus diubah.

Scraping hanya dijalankan ketika:

- Pengguna melakukan **reload halaman**, atau
- Pengguna menekan tombol **Perbarui Data**.

Selain dua kondisi tersebut, halaman `/jobs` hanya mengambil data yang telah tersedia pada database.

---

## Alur Baru

User membuka `/jobs`

↓

Frontend mengambil data dari database

↓

Menampilkan hasil

↓

Apabila pengguna menekan tombol **Perbarui Data**

↓

Backend menjalankan Scrapy

↓

Database diperbarui

↓

Frontend menerima update melalui Socket.IO

↓

Daftar lowongan diperbarui secara real-time

---

## Acceptance Criteria

- Membuka halaman `/jobs` tidak langsung menjalankan scraping.
- Waktu loading halaman lebih cepat.
- Scraping hanya berjalan saat benar-benar dibutuhkan.

---

# 16.12 Penyempurnaan AI CV Analyzer

## Kondisi Saat Ini

Output analisis CV masih berupa teks sehingga sulit dipahami.

---

## Requirement

Hasil analisis harus ditampilkan dalam bentuk dashboard interaktif.

Dashboard minimal menampilkan:

- ATS Score
- Overall Score
- Resume Summary
- Strength
- Weakness
- Missing Skills
- Keyword Match
- AI Recommendation

Visualisasi yang wajib ditambahkan:

- Radar Chart
- Bar Chart
- Pie Chart
- Progress Bar
- Persentase setiap kategori penilaian

Kategori penilaian meliputi:

- Skills
- Experience
- Education
- Projects
- Certificates
- ATS Compatibility
- Soft Skills

Seluruh hasil harus mudah dipahami oleh pengguna dan dapat digunakan sebagai dasar untuk memperbaiki CV.

---

# 16.13 Penyempurnaan AI CV Builder

## Kondisi Saat Ini

Halaman `/cv-builder` masih menggunakan layout `grid-cols-4` sehingga kurang nyaman digunakan.

---

## Requirement

CV Builder harus diubah menjadi sistem **Wizard Step-by-Step**.

Layout terdiri dari:

### Sidebar Kiri

Berisi navigasi:

- Informasi Pribadi
- Pendidikan
- Pengalaman
- Organisasi
- Sertifikat
- Proyek
- Skill
- Bahasa
- Referensi
- Ringkasan
- Preview

Sidebar juga menampilkan progress penyelesaian CV.

---

### Panel Kanan

Menampilkan form sesuai tahap yang sedang aktif.

---

### Validasi Tahapan

Pengguna tidak dapat membuka tahap berikutnya sebelum tahap sebelumnya selesai.

Contoh:

Informasi Pribadi

↓

Pendidikan

↓

Pengalaman

↓

Skill

↓

Preview

---

### Fitur Tambahan

- Progress Indicator
- Auto Save
- AI Suggestion
- Previous / Next Navigation
- Form Validation
- Resume Preview
- Export PDF

---

## Acceptance Criteria

- Layout lebih sederhana dan mudah dipahami.
- Pengguna hanya fokus pada satu tahap.
- Seluruh data tersimpan otomatis.
- Navigasi antar section berjalan dengan baik.

---

# 16.14 Kesimpulan Product Improvements

Seluruh Product Improvements pada versi 2.0 bertujuan untuk meningkatkan kualitas platform JobFinder dari sisi fitur, performa, desain, pengalaman pengguna, serta integrasi Artificial Intelligence.

Seluruh requirement pada bagian ini bersifat **Mandatory** dan menjadi acuan utama sebelum platform dinyatakan siap memasuki tahap produksi (Production Release).
---

# 17. Non-Functional Requirements

Selain memenuhi seluruh kebutuhan fungsional, JobFinder juga harus memenuhi kebutuhan non-fungsional agar platform memiliki performa, keamanan, dan skalabilitas yang baik.

---

## 17.1 Performance

Platform harus memiliki performa yang optimal.

### Requirement

- Waktu loading halaman utama maksimal 3 detik.
- Waktu pencarian pekerjaan maksimal 2 detik.
- Waktu filter maksimal 1 detik.
- Analisis CV maksimal 30 detik.
- AI Chatbot memberikan respon maksimal 10 detik.
- Proses scraping tidak mengganggu pengguna yang sedang menggunakan aplikasi.
- Database harus mampu menangani ribuan data lowongan.

---

## 17.2 Scalability

Platform harus mudah dikembangkan.

Requirement:

- Mudah menambah platform scraping baru.
- Mudah mengganti database.
- Mudah menambah AI Provider.
- Mudah menambah fitur baru.
- Menggunakan arsitektur modular.

---

## 17.3 Security

Platform harus memperhatikan keamanan data pengguna.

Requirement:

- Validasi seluruh input.
- Sanitasi seluruh data.
- Proteksi terhadap SQL Injection.
- Proteksi terhadap XSS.
- Validasi upload file PDF.
- Maksimal ukuran file upload.
- API menggunakan environment variable.
- API Key tidak boleh ditulis di source code.

---

## 17.4 Reliability

Platform harus tetap stabil.

Requirement:

- Error handling pada seluruh API.
- Retry ketika scraping gagal.
- Logging setiap proses scraping.
- Backup database secara berkala.

---

## 17.5 Maintainability

Kode harus mudah dipelihara.

Requirement:

- Modular Architecture.
- Reusable Component.
- Dokumentasi lengkap.
- Naming Convention konsisten.
- Clean Code.
- Unit Testing.

---

## 17.6 Accessibility

Platform harus dapat digunakan oleh seluruh pengguna.

Requirement:

- Responsive Design.
- Keyboard Navigation.
- Color Contrast.
- Screen Reader Friendly.
- Focus Indicator.

---

# 18. Business Rules

Berikut aturan bisnis yang harus diterapkan pada platform.

---

## Lowongan

- Data duplikat tidak boleh disimpan.
- URL menjadi identitas utama lowongan.
- Lowongan yang sudah tidak aktif dapat diarsipkan.
- Lowongan terbaru memiliki prioritas lebih tinggi.

---

## Scraping

- Scraping tidak dijalankan ketika halaman pertama kali dibuka.
- Scraping hanya berjalan ketika:
  - User melakukan reload halaman.
  - User menekan tombol **Perbarui Data**.
  - Scheduler menjalankan scraping otomatis.

---

## CV Analyzer

- Hanya menerima file PDF.
- Maksimal ukuran file sesuai konfigurasi.
- Hasil analisis tidak disimpan permanen kecuali pengguna mengizinkan.

---

## CV Builder

- Data otomatis disimpan.
- Pengguna tidak dapat melanjutkan apabila section sebelumnya belum selesai.
- Export PDF hanya dapat dilakukan setelah seluruh section selesai.

---

## Chatbot

- Chat history disimpan.
- AI dapat membaca database lowongan.
- AI tidak boleh memberikan informasi di luar konteks karier apabila tidak diminta.

---

# 19. Success Metrics

Keberhasilan platform diukur berdasarkan indikator berikut.

## Job Aggregation

- Minimal 7 platform scraping.
- Minimal 60 lowongan dari setiap platform.
- Tingkat duplikasi kurang dari 5%.

---

## Search

- Waktu pencarian kurang dari 2 detik.
- Akurasi hasil pencarian tinggi.

---

## CV Analyzer

- ATS Score berhasil ditampilkan.
- Visualisasi grafik tampil dengan benar.
- AI Recommendation relevan.

---

## CV Builder

- Pengguna dapat menyelesaikan CV hingga export PDF.
- Wizard berjalan tanpa error.
- Progress tersimpan otomatis.

---

## Chatbot

- Respon AI kurang dari 10 detik.
- AI mampu memberikan rekomendasi pekerjaan.

---

## User Experience

- Navigasi mudah dipahami.
- Responsive pada Desktop, Tablet, dan Mobile.
- Seluruh halaman mengikuti DESIGN.md.

---

# 20. Acceptance Criteria

Project dianggap selesai apabila seluruh poin berikut telah terpenuhi.

## Job Aggregation

- Mendukung seluruh platform yang direncanakan.
- Tidak terdapat data duplikat.
- Data tersimpan dengan benar.

---

## Frontend

- Seluruh halaman responsive.
- UI sesuai DESIGN.md.
- Tidak terdapat broken layout.

---

## Backend

- Seluruh API berjalan.
- Error handling tersedia.
- Logging tersedia.

---

## AI

- CV Analyzer berjalan.
- CV Builder berjalan.
- Chatbot berjalan.
- Telegram Bot berjalan.

---

## Documentation

Repository minimal memiliki dokumen berikut:

- README.md
- PRD.md
- DESIGN.md
- ARCHITECTURE.md
- ROADMAP.md
- SKILLS.md
- AGENT.md

---

# 21. Future Development

Pengembangan berikutnya dapat mencakup fitur-fitur berikut.

## Authentication

- Login Google.
- Login LinkedIn.
- Multi Role User.

---

## Company Dashboard

- HR Dashboard.
- Posting Lowongan.
- Applicant Tracking.

---

## AI

- Interview Simulation.
- Career Roadmap.
- Salary Prediction.
- Skill Recommendation.
- Learning Recommendation.

---

## Job Recommendation

- AI Recommendation berdasarkan CV.
- AI Recommendation berdasarkan riwayat pencarian.
- AI Recommendation berdasarkan skill.

---

## Mobile Application

- Android.
- iOS.

---

## Notification

- Email Notification.
- Telegram Notification.
- Push Notification.

---

## Analytics Dashboard

- Statistik lowongan.
- Statistik perusahaan.
- Statistik pengguna.
- Statistik AI.

---

# 22. Revision History

| Version | Date | Description |
|----------|------------|--------------------------------------|
| 1.0 | Initial Release | Dokumen awal |
| 2.0 | Current Version | Penambahan AI, CV Builder, CV Analyzer, Telegram Bot, Product Improvements, dan dokumentasi lengkap |

---

# Penutup

Dokumen Product Requirements Document (PRD) ini menjadi acuan utama dalam proses pengembangan platform JobFinder.

Seluruh developer, UI/UX Designer, AI Agent, maupun kontributor diwajibkan mengacu pada dokumen ini sebelum melakukan penambahan fitur, perubahan sistem, maupun proses refactoring.

Perubahan requirement hanya dapat dilakukan melalui pembaruan PRD sehingga seluruh pengembangan tetap terdokumentasi, terstruktur, dan konsisten.