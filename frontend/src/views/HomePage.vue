<template>
  <div class="page">
    <div class="hero stagger-1">
      <h1 class="editorial-serif" style="font-size: 3rem; margin-bottom: 24px; color: var(--text-primary); line-height: 1.1;">Penempatan Premium.<br/>Analisis Mendalam.</h1>
      <p style="color: var(--text-muted); font-size: 1.1rem; max-width: 600px; margin: 0 auto 40px;">Cari pekerjaan dan magang terkurasi dari berbagai sumber. Dapatkan analisis CV berstandar editorial dan bangun dokumen yang ramah ATS.</p>
      <div class="hero-actions">
        <router-link to="/jobs" class="btn btn-primary">Eksplorasi Peluang</router-link>
        <router-link to="/cv-analyzer" class="btn btn-outline">Analisis Dokumen</router-link>
      </div>
    </div>

    <div class="bento-grid stagger-2" style="margin-top: 64px;">
      <div class="card feature-card">
        <h3 class="editorial-serif">Agregasi Multi-Sumber</h3>
        <p>Dikurasi dari LinkedIn, Glints, Jobstreet, Fastwork, dan Pintarnya.</p>
        <router-link to="/jobs" class="btn btn-sm btn-outline" style="margin-top: 16px;">Lihat Daftar</router-link>
      </div>
      <div class="card feature-card">
        <h3 class="editorial-serif">Analisis CV</h3>
        <p>Evaluasi kompatibilitas ATS dan skor kecocokan terhadap keahlian spesifik Anda.</p>
        <router-link to="/cv-analyzer" class="btn btn-sm btn-outline" style="margin-top: 16px;">Mulai Analisis</router-link>
      </div>
      <div class="card feature-card">
        <h3 class="editorial-serif">Pembuat Dokumen</h3>
        <p>Buat dokumen ATS minimalis dengan panduan pengisian dari asisten AI.</p>
        <router-link to="/cv-builder" class="btn btn-sm btn-outline" style="margin-top: 16px;">Buat Dokumen</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.hero { text-align: center; padding: 80px 0 60px; }
.hero h1 { letter-spacing: -0.04em; }
.hero-actions { display: flex; gap: 16px; justify-content: center; }
.feature-card { text-align: left; display: flex; flex-direction: column; align-items: flex-start; }
.feature-card h3 { margin-bottom: 12px; font-size: 1.25rem; font-weight: 400; }
.feature-card p { color: var(--text-muted); font-size: 14px; line-height: 1.6; flex: 1; }
</style>
