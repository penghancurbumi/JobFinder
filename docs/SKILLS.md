# AI Skills Documentation

**Project Name:** JobFinder

**Version:** 2.0

**Status:** Active

**Last Updated:** July 2026

---

# 1. Overview

## Deskripsi

Dokumen ini mendefinisikan seluruh AI Skill yang digunakan selama proses pengembangan platform JobFinder.

Tujuan utama dokumen ini adalah memberikan standar penggunaan skill sehingga seluruh AI Agent, developer, dan kontributor menghasilkan implementasi yang konsisten, terdokumentasi, dan sesuai dengan kebutuhan proyek.

Seluruh AI Agent yang bekerja pada proyek ini wajib mengacu pada dokumen ini sebelum melakukan analisis, penulisan kode, refactoring, debugging, desain, maupun dokumentasi.

---

# 2. Objectives

Penggunaan AI Skill bertujuan untuk:

- Meningkatkan kualitas kode.
- Mempercepat proses pengembangan.
- Mengurangi bug.
- Menjaga konsistensi implementasi.
- Mempermudah proses debugging.
- Menghasilkan dokumentasi yang lengkap.
- Membantu proses desain antarmuka.
- Memastikan implementasi sesuai dengan PRD dan Architecture.

---

# 3. Skill Categories

AI Skill dibagi menjadi beberapa kategori.

- Development
- Debugging
- UI / UX
- Documentation
- Architecture
- Performance
- Code Quality
- Testing
- Research

---

# 4. Development Skills

## 4.1 Superpowers

### Tujuan

Superpowers digunakan sebagai skill utama selama proses pengembangan.

### Digunakan Untuk

- Menulis kode baru.
- Refactoring.
- Clean Code.
- Best Practice.
- Modular Architecture.
- Optimasi struktur proyek.
- Membuat reusable component.

### Input

- Requirement dari PRD.
- Source code.
- Dokumentasi.

### Output

- Source code yang bersih.
- Struktur project yang lebih baik.
- Dokumentasi perubahan.

---

## 4.2 Caveman

### Tujuan

Membantu proses debugging.

### Digunakan Untuk

- Root Cause Analysis.
- Error Investigation.
- Stack Trace Analysis.
- Dependency Conflict.
- Runtime Error.
- Build Error.

### Output

- Penyebab error.
- Solusi.
- Langkah reproduksi.
- Rekomendasi perbaikan.

---

## 4.3 Sequential Thinking

### Tujuan

Membantu AI memecahkan masalah kompleks secara bertahap.

### Digunakan Untuk

- Perancangan fitur baru.
- Analisis sistem.
- Penyusunan algoritma.
- Optimasi arsitektur.

---

# 5. UI / UX Skills

## 5.1 Ponytail

### Tujuan

Mengembangkan antarmuka pengguna yang modern dan mudah digunakan.

### Digunakan Untuk

- Layout.
- Responsive Design.
- Accessibility.
- Navigation.
- Dashboard.
- Landing Page.
- Mobile Layout.

---

## 5.2 Taste

### Tujuan

Meningkatkan kualitas visual aplikasi.

### Digunakan Untuk

- Color Palette.
- Typography.
- Component Style.
- Card Design.
- Button Design.
- Form Design.
- Icon Style.
- Shadow.
- Spacing.

---

## 5.3 GetDesign

### Tujuan

Sebagai referensi desain antarmuka.

### Digunakan Untuk

- Landing Page.
- Dashboard.
- Hero Section.
- CV Builder.
- CV Analyzer.
- Chatbot.
- Empty State.
- Loading State.
- Statistics Section.

Seluruh implementasi UI harus mengacu pada DESIGN.md.

---

# 6. Documentation Skills

AI wajib menghasilkan dokumentasi yang konsisten.

Dokumen yang harus diperbarui ketika terjadi perubahan fitur:

- README.md
- PRD.md
- DESIGN.md
- ARCHITECTURE.md
- ROADMAP.md
- CHANGELOG.md

---

# 7. Architecture Skills

AI harus memahami struktur sistem sebelum membuat implementasi.

Referensi utama:

- ARCHITECTURE.md
- PRD.md

AI tidak diperbolehkan mengubah arsitektur tanpa memperbarui dokumentasi.

---

# 8. Performance Skills

Selama pengembangan AI harus memperhatikan performa aplikasi.

Prioritas:

- Optimasi query.
- Optimasi API.
- Optimasi frontend.
- Lazy Loading.
- Code Splitting.
- Pagination.
- Efficient Scraping.

---

# 9. Code Quality Skills

Seluruh kode harus memenuhi standar berikut:

- Clean Code.
- SOLID Principle.
- DRY (Don't Repeat Yourself).
- KISS (Keep It Simple).
- Modular.
- Readable.
- Reusable.
- Well Documented.

---

# 10. Testing Skills

Sebelum fitur dinyatakan selesai AI harus memastikan:

- Tidak ada syntax error.
- Tidak ada dependency conflict.
- Tidak ada runtime error.
- Validasi input berjalan.
- API dapat digunakan.
- UI sesuai desain.

---

# 11. Research Skills

Ketika menemukan masalah yang belum diketahui, AI harus:

- Melakukan analisis terlebih dahulu.
- Mencari referensi resmi.
- Membandingkan beberapa solusi.
- Memilih solusi yang paling sesuai dengan arsitektur JobFinder.

---

# 12. Skill Priority

Urutan penggunaan skill adalah:

1. Superpowers (systematic-debugging, brainstorming)
2. Sequential Thinking (bawaan AI)
3. Caveman (systematic-debugging)
4. Skill lain apabila diperlukan

Skill lain dapat digunakan apabila diperlukan dan tetap mengikuti standar proyek.

## Skill Mapping

| Nama di SKILLS.md | Skill Aktual |
|---|---|
| Caveman | `systematic-debugging` |
| Brainstorming | `brainstorming` |
| Sequential Thinking | Bawaan AI (bukan file skill) |

---

# 13. Rules

AI Agent wajib:

- Mengikuti PRD.md.
- Mengikuti DESIGN.md.
- Mengikuti ARCHITECTURE.md.
- Mengikuti ROADMAP.md.
- Menulis kode modular.
- Memperbarui dokumentasi jika terdapat perubahan.

AI Agent tidak diperbolehkan:

- Mengubah requirement tanpa persetujuan.
- Menghapus dokumentasi.
- Mengubah arsitektur tanpa pembaruan dokumen.
- Menambahkan dependency tanpa alasan yang jelas.

---

# 14. Best Practices

- Gunakan reusable component.
- Hindari duplikasi kode.
- Pisahkan business logic.
- Gunakan penamaan yang konsisten.
- Dokumentasikan perubahan penting.
- Lakukan refactoring secara berkala.

---

# Penutup

Dokumen ini menjadi standar penggunaan AI Skill dalam pengembangan JobFinder.

Seluruh AI Agent dan developer diharapkan mengikuti panduan ini agar proses pengembangan berlangsung secara konsisten, efisien, dan sesuai dengan tujuan proyek.