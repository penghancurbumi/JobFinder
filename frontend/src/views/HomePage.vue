<template>
  <div class="home">
    <!-- Hero Section (Dark) -->
    <section class="marketing-section-dark" style="padding-top: var(--spacing-section-lg);">
      <div class="container">
        <div style="max-width: 960px;">
          <span class="mono-eyebrow" style="margin-bottom: var(--spacing-lg); display: block; color: var(--color-mute);">Job Aggregator Indonesia</span>
          <h1 class="display-mega" style="margin-bottom: var(--spacing-lg);">
            <span style="display: block;">Temukan Karier</span>
            <span style="display: block; color: var(--color-brand);">Masa Depanmu</span>
          </h1>
          <p class="subtitle" style="color: var(--color-ash); max-width: 640px; margin-bottom: var(--spacing-xl);">
            Platform agregasi lowongan kerja dan magang dari seluruh sumber terpercaya.
            Lengkap dengan analisis CV dan pembuatan dokumen ATS berstandar industri.
          </p>

          <div v-if="statsLoading" style="color: var(--color-mute); margin-bottom: var(--spacing-lg);" class="mono-micro">Memuat statistik...</div>
          <div v-else style="display: flex; gap: var(--spacing-xl); margin-bottom: var(--spacing-xl); padding: var(--spacing-lg) 0; border-top: 1px solid var(--color-hairline-soft); border-bottom: 1px solid var(--color-hairline-soft);">
            <div style="display: flex; flex-direction: column; gap: 4px;">
              <span class="display-sm" style="letter-spacing: -1.14px;">{{ formatNumber(totalJobs) }}</span>
              <span class="mono-caps" style="color: var(--color-mute);">Total Lowongan</span>
            </div>
            <div style="width: 1px; background: var(--color-hairline-soft);"></div>
            <div style="display: flex; flex-direction: column; gap: 4px;">
              <span class="display-sm" style="letter-spacing: -1.14px;">{{ sourceCount }}</span>
              <span class="mono-caps" style="color: var(--color-mute);">Sumber</span>
            </div>
            <div style="width: 1px; background: var(--color-hairline-soft);"></div>
            <div style="display: flex; flex-direction: column; gap: 4px;">
              <span class="display-sm" style="letter-spacing: -1.14px;">{{ expertiseCount }}</span>
              <span class="mono-caps" style="color: var(--color-mute);">Bidang Keahlian</span>
            </div>
          </div>

          <div style="display: flex; align-items: center; gap: var(--spacing-md); margin-bottom: var(--spacing-xl);">
            <span class="mono-micro" style="color: var(--color-mute); white-space: nowrap;">Dari platform:</span>
            <div style="display: flex; flex-wrap: wrap; gap: var(--spacing-sm) var(--spacing-lg);">
              <span class="badge-neutral" style="background: transparent; color: var(--color-ash); border: 1px solid var(--color-hairline-soft);">LinkedIn</span>
              <span class="badge-neutral" style="background: transparent; color: var(--color-ash); border: 1px solid var(--color-hairline-soft);">Glints</span>
              <span class="badge-neutral" style="background: transparent; color: var(--color-ash); border: 1px solid var(--color-hairline-soft);">Jobstreet</span>
              <span class="badge-neutral" style="background: transparent; color: var(--color-ash); border: 1px solid var(--color-hairline-soft);">Fastwork</span>
              <span class="badge-neutral" style="background: transparent; color: var(--color-ash); border: 1px solid var(--color-hairline-soft);">Pintarnya</span>
            </div>
          </div>

          <div style="display: flex; gap: var(--spacing-sm); flex-wrap: wrap;">
            <router-link to="/jobs" class="btn btn-brand">Cari Lowongan</router-link>
            <router-link to="/cv-analyzer" class="btn btn-secondary-dark" style="height: 44px; padding: 0 var(--spacing-lg); display: flex; align-items: center;">Analisis CV</router-link>
            <router-link to="/cv-builder" class="btn btn-ghost-dark" style="height: 44px; padding: 0 var(--spacing-lg); display: flex; align-items: center;">Buat CV</router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section (Dark) -->
    <section class="marketing-section-dark">
      <div class="container">
        <div style="margin-bottom: var(--spacing-section);">
          <span class="mono-eyebrow" style="color: var(--color-mute); margin-bottom: var(--spacing-lg); display: block;">Fitur Unggulan</span>
          <h2 class="display-md">Satu Platform, Semua Kebutuhan Kariermu</h2>
        </div>
        <div class="grid grid-2">
          <div class="feature-card-dark">
            <span class="mono-eyebrow" style="margin-bottom: var(--spacing-xs); color: var(--color-mute);">Multi-Source</span>
            <h3 class="heading-sm" style="margin-bottom: var(--spacing-sm);">Agregasi Lowongan</h3>
            <p class="body" style="color: var(--color-ash); margin-bottom: var(--spacing-lg); flex: 1;">Kumpulan lowongan kerja dan magang dari LinkedIn, Glints, Jobstreet, Fastwork, dan Pintarnya dalam satu tampilan.</p>
            <router-link to="/jobs" class="btn btn-ghost-dark" style="padding-left: 0;">Lihat Lowongan →</router-link>
          </div>

          <div class="feature-card-dark">
            <span class="mono-eyebrow" style="margin-bottom: var(--spacing-xs); color: var(--color-mute);">ATS Check</span>
            <h3 class="heading-sm" style="margin-bottom: var(--spacing-sm);">Analisis CV</h3>
            <p class="body" style="color: var(--color-ash); margin-bottom: var(--spacing-lg); flex: 1;">Evaluasi kompatibilitas CV-mu terhadap sistem ATS dan dapatkan skor kecocokan dengan bidang keahlian spesifik.</p>
            <router-link to="/cv-analyzer" class="btn btn-ghost-dark" style="padding-left: 0;">Analisis Sekarang →</router-link>
          </div>

          <div class="feature-card-dark">
            <span class="mono-eyebrow" style="margin-bottom: var(--spacing-xs); color: var(--color-mute);">Builder</span>
            <h3 class="heading-sm" style="margin-bottom: var(--spacing-sm);">Pembuat CV</h3>
            <p class="body" style="color: var(--color-ash); margin-bottom: var(--spacing-lg); flex: 1;">Buat dokumen CV ATS-minimalis dengan panduan pengisian dari asisten AI. Format rapi dan siap pakai.</p>
            <router-link to="/cv-builder" class="btn btn-ghost-dark" style="padding-left: 0;">Buat CV →</router-link>
          </div>

          <div class="feature-card-dark" style="background: var(--color-brand); color: var(--color-ink);">
            <span class="mono-eyebrow" style="margin-bottom: var(--spacing-xs); color: rgba(11,11,11,0.6);">AI-Powered</span>
            <h3 class="heading-sm" style="margin-bottom: var(--spacing-sm);">AI Chatbot</h3>
            <p class="body" style="color: var(--color-ink); opacity: 0.8; margin-bottom: var(--spacing-lg); flex: 1;">Tanya apapun seputar karier, lowongan, atau penyusunan CV. Dapatkan saran personal dari asisten AI.</p>
            <router-link to="/chatbot" class="btn btn-ghost-dark" style="padding-left: 0; color: var(--color-ink);">Mulai Chat →</router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Documentation Section (Paper Light) -->
    <section class="marketing-section-paper">
      <div class="container">
        <div style="margin-bottom: var(--spacing-section);">
          <span class="mono-eyebrow" style="color: var(--color-mute); margin-bottom: var(--spacing-lg); display: block;">Panduan</span>
          <h2 class="display-md">Mulai dengan JobFinder</h2>
        </div>
        <div class="grid grid-3">
          <div class="card" style="background: var(--color-canvas-light); border: 1px solid var(--color-hairline);">
            <span class="mono-caps" style="color: var(--color-brand); margin-bottom: var(--spacing-sm); display: block;">Langkah 1</span>
            <h3 class="heading-sm" style="margin-bottom: var(--spacing-sm);">Jelajahi Lowongan</h3>
            <p class="body-sm" style="color: var(--color-graphite);">Gunakan filter canggih untuk menemukan posisi yang sesuai dengan keahlian dan preferensimu.</p>
          </div>
          <div class="card" style="background: var(--color-canvas-light); border: 1px solid var(--color-hairline);">
            <span class="mono-caps" style="color: var(--color-brand); margin-bottom: var(--spacing-sm); display: block;">Langkah 2</span>
            <h3 class="heading-sm" style="margin-bottom: var(--spacing-sm);">Analisis CV</h3>
            <p class="body-sm" style="color: var(--color-graphite);">Uji CV-mu terhadap standar ATS dan dapatkan rekomendasi perbaikan yang spesifik.</p>
          </div>
          <div class="card" style="background: var(--color-canvas-light); border: 1px solid var(--color-hairline);">
            <span class="mono-caps" style="color: var(--color-brand); margin-bottom: var(--spacing-sm); display: block;">Langkah 3</span>
            <h3 class="heading-sm" style="margin-bottom: var(--spacing-sm);">Buat & Lamar</h3>
            <p class="body-sm" style="color: var(--color-graphite);">Bangun CV yang dioptimalkan untuk ATS dan lamar pekerjaan impianmu dengan percaya diri.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="marketing-section-dark" style="padding: var(--spacing-section) 0 var(--spacing-lg); border-top: 1px solid var(--color-hairline-soft);">
      <div class="container">
        <div class="grid" style="grid-template-columns: 1.5fr 1fr 1fr 1fr; margin-bottom: var(--spacing-section);">
          <div style="display: flex; flex-direction: column; gap: var(--spacing-sm);">
            <div style="display: flex; align-items: center; gap: var(--spacing-xs); margin-bottom: var(--spacing-sm);">
              <span class="brand-dot"></span>
              <span class="heading-sm">JobFinder</span>
            </div>
            <p class="body-sm" style="color: var(--color-ash); max-width: 280px;">Platform agregasi lowongan kerja dan alat karier untuk pencari kerja di Indonesia.</p>
          </div>
          <div style="display: flex; flex-direction: column; gap: var(--spacing-sm);">
            <span class="mono-caps" style="color: var(--color-mute); margin-bottom: var(--spacing-xs);">Fitur</span>
            <router-link to="/jobs" style="color: var(--color-ash); text-decoration: none; font-size: 13px;">Cari Lowongan</router-link>
            <router-link to="/cv-analyzer" style="color: var(--color-ash); text-decoration: none; font-size: 13px;">Analisis CV</router-link>
            <router-link to="/cv-builder" style="color: var(--color-ash); text-decoration: none; font-size: 13px;">Buat CV</router-link>
            <router-link to="/chatbot" style="color: var(--color-ash); text-decoration: none; font-size: 13px;">AI Chatbot</router-link>
          </div>
          <div style="display: flex; flex-direction: column; gap: var(--spacing-sm);">
            <span class="mono-caps" style="color: var(--color-mute); margin-bottom: var(--spacing-xs);">Sumber</span>
            <span style="color: var(--color-ash); font-size: 13px;">LinkedIn</span>
            <span style="color: var(--color-ash); font-size: 13px;">Glints</span>
            <span style="color: var(--color-ash); font-size: 13px;">Jobstreet</span>
            <span style="color: var(--color-ash); font-size: 13px;">Fastwork</span>
            <span style="color: var(--color-ash); font-size: 13px;">Pintarnya</span>
          </div>
          <div style="display: flex; flex-direction: column; gap: var(--spacing-sm);">
            <span class="mono-caps" style="color: var(--color-mute); margin-bottom: var(--spacing-xs);">Hubungi</span>
            <a href="mailto:hello@jobfinder.id" style="color: var(--color-ash); text-decoration: none; font-size: 13px;">hello@jobfinder.id</a>
            <span class="mono-micro" style="margin-top: auto; color: var(--color-mute);">v2.0.0</span>
          </div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding-top: var(--spacing-lg); border-top: 1px solid var(--color-hairline-soft);">
          <span class="mono-micro" style="color: var(--color-mute);">&copy; {{ new Date().getFullYear() }} JobFinder. All rights reserved.</span>
          <span class="mono-micro" style="color: var(--color-mute);">Built with editorial precision</span>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"

const totalJobs = ref(0)
const sourceCount = ref(0)
const expertiseCount = ref(0)
const statsLoading = ref(true)

function formatNumber(n) {
  if (n >= 1000) return (n / 1000).toFixed(1).replace(/\.0$/, "") + "rb"
  return n.toString()
}

onMounted(async () => {
  try {
    const [jobsRes, expertiseRes] = await Promise.all([
      fetch("http://localhost:3000/api/jobs"),
      fetch("http://localhost:3000/api/expertise-areas"),
    ])

    if (jobsRes.ok) {
      const jobs = await jobsRes.json()
      totalJobs.value = Array.isArray(jobs) ? jobs.length : 0
      const sources = new Set()
      if (Array.isArray(jobs)) {
        jobs.forEach((j) => {
          if (j.source) sources.add(j.source)
        })
      }
      sourceCount.value = sources.size || 5
    }

    if (expertiseRes.ok) {
      const areas = await expertiseRes.json()
      expertiseCount.value = Array.isArray(areas) ? areas.length : 0
    }
  } catch {
    totalJobs.value = 0
    sourceCount.value = 5
    expertiseCount.value = 12
  } finally {
    statsLoading.value = false
  }
})
</script>

<style scoped>
@media (max-width: 960px) {
  .display-mega {
    font-size: 64px;
    letter-spacing: -2.5px;
  }
}
@media (max-width: 768px) {
  .display-mega {
    font-size: 48px;
    letter-spacing: -1.5px;
  }
  .display-md {
    font-size: 36px;
    letter-spacing: -1px;
  }
  .grid[style*="1.5fr"] {
    grid-template-columns: 1fr;
  }
}
</style>
