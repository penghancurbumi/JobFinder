<template>
  <div class="home bg-canvas-dark text-on-dark font-sans">
    <!-- Hero Section (Dark Canvas) -->
    <section class="bg-canvas-dark py-[100px]">
      <div class="w-full max-w-[1200px] mx-auto px-xl">
        <div class="max-w-[960px]">
          <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] mb-lg block text-stone">Job Aggregator Indonesia</span>
          <h1 class="font-medium leading-[1.0] tracking-[-0.8px] mb-xl">
            <span class="text-[48px] md:text-[64px] lg:text-[80px] block">Temukan Karier</span>
            <span class="text-[48px] md:text-[64px] lg:text-[90px] block font-instrument-serif italic tracking-normal">Masa Depanmu</span>
          </h1>
          
          <p class="text-[18px] font-normal leading-[1.56] tracking-[-0.09px] text-on-dark-mute max-w-[640px] mb-xl">
            Platform agregasi lowongan kerja dan magang dari seluruh sumber terpercaya.
            Lengkap dengan analisis CV dan pembuatan dokumen ATS berstandar industri.
          </p>

          <div class="flex items-center gap-md mb-xl">
            <span class="font-mono text-[11px] uppercase tracking-[0.5px] font-semibold text-stone whitespace-nowrap">Dari platform:</span>
            <div class="flex flex-wrap gap-x-lg gap-y-sm">
              <span class="bg-transparent text-on-dark-mute border border-hairline-dark rounded-full px-[12px] py-[4px] text-[13px]">LinkedIn</span>
              <span class="bg-transparent text-on-dark-mute border border-hairline-dark rounded-full px-[12px] py-[4px] text-[13px]">Glints</span>
              <span class="bg-transparent text-on-dark-mute border border-hairline-dark rounded-full px-[12px] py-[4px] text-[13px]">Jobstreet</span>
              <span class="bg-transparent text-on-dark-mute border border-hairline-dark rounded-full px-[12px] py-[4px] text-[13px]">Fastwork</span>
              <span class="bg-transparent text-on-dark-mute border border-hairline-dark rounded-full px-[12px] py-[4px] text-[13px]">Pintarnya</span>
            </div>
          </div>

          <div class="flex gap-sm flex-wrap">
            <router-link to="/jobs" class="inline-flex items-center justify-center font-semibold rounded-full transition-all duration-200 cursor-pointer text-[16px] px-[24px] h-[48px] bg-on-dark text-ink hover:bg-white/90">Cari Lowongan</router-link>
            <router-link to="/cv-analyzer" class="inline-flex items-center justify-center font-semibold rounded-full transition-all duration-200 cursor-pointer text-[16px] px-[24px] h-[48px] bg-transparent border border-hairline-dark text-on-dark hover:bg-surface-elevated">Analisis CV</router-link>
            <router-link to="/cv-builder" class="inline-flex items-center justify-center font-semibold rounded-full transition-all duration-200 cursor-pointer text-[16px] px-[24px] h-[48px] bg-transparent text-on-dark hover:bg-surface-elevated">Buat CV</router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section (Dark Canvas) -->
    <section class="bg-canvas-dark py-[80px]">
      <div class="w-full max-w-[1200px] mx-auto px-xl">
        <div class="mb-xxl">
          <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-stone mb-lg block">Fitur Unggulan</span>
          <h2 class="text-[32px] md:text-[40px] font-medium leading-[1.2] tracking-[-0.4px] text-on-dark">Satu Platform, Semua Kebutuhan Kariermu</h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-xl">
          <div class="bg-surface-elevated rounded-[20px] p-xxl flex flex-col">
            <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] mb-xs text-stone">Multi-Source</span>
            <h3 class="text-[20px] font-medium leading-[1.4] mb-sm text-on-dark">Agregasi Lowongan</h3>
            <p class="text-[16px] font-normal leading-[1.6] text-on-dark-mute mb-lg flex-1">Kumpulan lowongan kerja dan magang dari LinkedIn, Glints, Jobstreet, Fastwork, dan Pintarnya dalam satu tampilan.</p>
            <router-link to="/jobs" class="inline-flex items-center font-semibold transition-all duration-200 cursor-pointer text-[16px] bg-transparent text-on-dark hover:text-white pl-0">Lihat Lowongan →</router-link>
          </div>

          <div class="bg-surface-elevated rounded-[20px] p-xxl flex flex-col">
            <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] mb-xs text-stone">ATS Check</span>
            <h3 class="text-[20px] font-medium leading-[1.4] mb-sm text-on-dark">Analisis CV</h3>
            <p class="text-[16px] font-normal leading-[1.6] text-on-dark-mute mb-lg flex-1">Evaluasi kompatibilitas CV-mu terhadap sistem ATS dan dapatkan skor kecocokan dengan bidang keahlian spesifik.</p>
            <router-link to="/cv-analyzer" class="inline-flex items-center font-semibold transition-all duration-200 cursor-pointer text-[16px] bg-transparent text-on-dark hover:text-white pl-0">Analisis Sekarang →</router-link>
          </div>

          <div class="bg-surface-elevated rounded-[20px] p-xxl flex flex-col">
            <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] mb-xs text-stone">Builder</span>
            <h3 class="text-[20px] font-medium leading-[1.4] mb-sm text-on-dark">Pembuat CV</h3>
            <p class="text-[16px] font-normal leading-[1.6] text-on-dark-mute mb-lg flex-1">Buat dokumen CV ATS-minimalis dengan panduan pengisian dari asisten AI. Format rapi dan siap pakai.</p>
            <router-link to="/cv-builder" class="inline-flex items-center font-semibold transition-all duration-200 cursor-pointer text-[16px] bg-transparent text-on-dark hover:text-white pl-0">Buat CV →</router-link>
          </div>

          <!-- Featured card — cobalt violet inversion -->
          <div class="bg-surface-elevated rounded-[20px] p-xxl flex flex-col">
            <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] mb-xs text-stone">AI-Powered</span>
            <h3 class="text-[20px] font-medium leading-[1.4] mb-sm text-on-dark">Diskusi Karier</h3>
            <p class="text-[16px] font-normal leading-[1.6] text-on-dark-mute mb-lg flex-1">Tanya apapun seputar karier, lowongan, atau penyusunan CV. Dapatkan saran personal dari asisten AI.</p>
            <router-link to="/chatbot" class="inline-flex items-center font-semibold transition-all duration-200 cursor-pointer text-[16px] bg-transparent text-on-dark hover:text-white pl-0">Mulai Chat →</router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Documentation Section -->
    <section class="bg-canvas-dark py-[80px]">
      <div class="w-full max-w-[1200px] mx-auto px-xl">
        <div class="mb-xxl">
          <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-stone mb-lg block">Panduan</span>
          <h2 class="text-[32px] md:text-[40px] font-medium leading-[1.2] tracking-[-0.4px] text-on-dark">Mulai dengan JobFinder</h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-xl">
          <div class="bg-surface-elevated rounded-[20px] p-xxl flex flex-col border border-hairline-dark shadow-sm">
            <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-primary mb-sm block">Langkah 1</span>
            <h3 class="text-[20px] font-medium leading-[1.4] mb-sm text-on-dark">Jelajahi Lowongan</h3>
            <p class="text-[14px] font-normal leading-[1.5] text-on-dark-mute">Gunakan filter canggih untuk menemukan posisi yang sesuai dengan keahlian dan preferensimu.</p>
          </div>
          <div class="bg-surface-elevated rounded-[20px] p-xxl flex flex-col border border-hairline-dark shadow-sm">
            <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-primary mb-sm block">Langkah 2</span>
            <h3 class="text-[20px] font-medium leading-[1.4] mb-sm text-on-dark">Analisis CV</h3>
            <p class="text-[14px] font-normal leading-[1.5] text-on-dark-mute">Uji CV-mu terhadap standar ATS dan dapatkan rekomendasi perbaikan yang spesifik.</p>
          </div>
          <div class="bg-surface-elevated rounded-[20px] p-xxl flex flex-col border border-hairline-dark shadow-sm">
            <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-primary mb-sm block">Langkah 3</span>
            <h3 class="text-[20px] font-medium leading-[1.4] mb-sm text-on-dark">Buat &amp; Lamar</h3>
            <p class="text-[14px] font-normal leading-[1.5] text-on-dark-mute">Bangun CV yang dioptimalkan untuk ATS dan lamar pekerjaan impianmu dengan percaya diri.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer (Dark Canvas) -->
    <footer class="bg-canvas-dark pt-block pb-lg border-t border-hairline-dark">
      <div class="w-full max-w-[1200px] mx-auto px-xl">
        <div class="grid grid-cols-1 md:grid-cols-[1.5fr_1fr_1fr_1fr] gap-xxl md:gap-xl mb-block">
          <div class="flex flex-col gap-sm">
            <div class="flex items-center gap-xs mb-sm">
              <span class="w-3 h-3 rounded-full bg-primary inline-block"></span>
              <span class="text-[20px] font-medium leading-[1.4] text-on-dark">JobFinder</span>
            </div>
            <p class="text-[14px] font-normal leading-[1.5] text-on-dark-mute max-w-[280px]">Platform agregasi lowongan kerja dan alat karier untuk pencari kerja di Indonesia.</p>
          </div>
          <div class="flex flex-col gap-sm">
            <span class="font-mono text-[12px] uppercase tracking-[1px] font-bold text-stone mb-xs">Fitur</span>
            <router-link to="/jobs" class="text-on-dark-mute hover:text-on-dark text-[14px] transition-colors no-underline">Cari Lowongan</router-link>
            <router-link to="/cv-analyzer" class="text-on-dark-mute hover:text-on-dark text-[14px] transition-colors no-underline">Analisis CV</router-link>
            <router-link to="/cv-builder" class="text-on-dark-mute hover:text-on-dark text-[14px] transition-colors no-underline">Buat CV</router-link>
            <router-link to="/chatbot" class="text-on-dark-mute hover:text-on-dark text-[14px] transition-colors no-underline">AI Chatbot</router-link>
          </div>
          <div class="flex flex-col gap-sm">
            <span class="font-mono text-[12px] uppercase tracking-[1px] font-bold text-stone mb-xs">Sumber</span>
            <span class="text-on-dark-mute text-[14px]">LinkedIn</span>
            <span class="text-on-dark-mute text-[14px]">Glints</span>
            <span class="text-on-dark-mute text-[14px]">Jobstreet</span>
            <span class="text-on-dark-mute text-[14px]">Fastwork</span>
            <span class="text-on-dark-mute text-[14px]">Pintarnya</span>
          </div>
          <div class="flex flex-col gap-sm">
            <span class="font-mono text-[12px] uppercase tracking-[1px] font-bold text-stone mb-xs">Hubungi</span>
            <a href="mailto:hello@jobfinder.id" class="text-on-dark-mute hover:text-on-dark text-[14px] transition-colors no-underline">hello@jobfinder.id</a>
            <span class="font-mono text-[11px] uppercase tracking-[0.5px] font-semibold text-stone mt-auto">v2.0.0</span>
          </div>
        </div>
        <div class="flex justify-between items-center pt-lg border-t border-hairline-dark">
          <span class="text-[13px] font-normal leading-[1.5] text-on-dark-mute">&copy; {{ new Date().getFullYear() }} JobFinder. All rights reserved.</span>
          <span class="text-[13px] font-normal leading-[1.5] text-stone">Built with editorial precision</span>
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
