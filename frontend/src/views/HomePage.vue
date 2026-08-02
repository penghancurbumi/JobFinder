<template>
  <div class="home bg-transparent text-on-dark font-sans">
    <!-- Hero Section (Dark Canvas) -->
    <section class="bg-transparent py-[110px]">
      <div class="w-full mx-auto px-[32px] md:px-[72px]">
        <div class="flex flex-col gap-[40px]">
          <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] block text-stone">Job Aggregator Indonesia</span>
          <h1 class="font-medium leading-[1.0] tracking-[-0.8px]">
            <span class="text-[48px] md:text-[64px] lg:text-[72px] block">Temukan Karier</span>
            <span class="text-[48px] md:text-[64px] lg:text-[72px] block">Masa Depanmu</span>
          </h1>

          <p class="text-sm md:text-[18px] font-normal leading-[1.56] tracking-[-0.09px] text-on-dark-mute max-w-[640px]">
            Platform agregasi lowongan kerja dan magang dari seluruh sumber terpercaya.
            Lengkap dengan analisis CV dan pembuatan dokumen ATS berstandar industri.
          </p>

          <div class="flex gap-[20px] flex-wrap items-center">
            <router-link to="/jobs" class="inline-flex items-center gap-[8px] justify-center font-medium rounded-full transition-all duration-200 cursor-pointer text-sm md:text-[18px] px-[24px] h-[48px] bg-on-dark text-ink hover:bg-white/90">
              Get Started
              <Icon icon="mdi-light:arrow-right" width="20"/>
            </router-link>            

            <a href="https://github.com/penghancurbumi/JobFinder" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-[8px] justify-center font-medium rounded-full transition-all duration-200 cursor-pointer text-sm md:text-[18px] px-[24px] h-[48px] bg-surface-elevated hover:bg-body border border-hairline-dark text-on-dark">
              <Icon icon="mdi:github" width="20"/>
              GitHub</a>
          </div>
        </div>
      </div>

      <!-- Logo Slider — full width, label kiri -->
      <div class="flex items-center gap-[24px] mt-[90px]">
        <div class="flex flex-row items-center gap-2 px-[32px] md:px-[72px]">
          <div class="h-1 w-1 rounded-full bg-white"></div>
          <p class="font-mono uppercase text-[14px] font-bold tracking-[1.5px] text-white shrink-0">Powered by Trusted Sources</p>
        </div>

        <div class="logo-track-wrapper flex-1 min-w-0">
          <div class="logo-track">
            <div v-for="n in 2" :key="n" class="logo-group">

              <!-- LinkedIn -->
              <div class="logo-chip">
                <img src="../assets/images/linkedin logo.png" alt="LinkedIn Logo">
              </div>

              <!-- Glints -->
              <div class="logo-chip">
                <img src="../assets/images/glints logo.png" alt="Glints Logo">
              </div>
              
              <!-- Jobstreet -->
              <div class="logo-chip">
                <img src="../assets/images/jobstreet logo.png" alt="Jobstreet Logo">
              </div>

              <!-- pintarnya -->
              <div class="logo-chip">
                <img src="../assets/images/pintarnya logo.png" alt="Pintarnya Logo">
              </div>

              <!-- Techinasia -->
              <div class="logo-chip">
                <img src="../assets/images/techinasia logo.png" alt="Techinasia Logo">
              </div>

              <!-- KitaLulus -->
              <div class="logo-chip">
                <img src="../assets/images/kitalulus logo.png" alt="Kitalulus Logo">
              </div>

              <!-- Kalibrr -->
              <div class="logo-chip">
                <img src="../assets/images/kalibrr logo.png" alt="Kalibrr Logo">
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>


    <!-- Features Section (Dark Canvas) -->
    <section class="bg-transparent pt-[80px] pb-[80px]">
      <div class="w-full mx-auto px-[32px] md:px-[72px]">
        <div class="mb-xxl">
          <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-stone mb-lg block">Fitur Unggulan</span>
          <h2 class="text-[32px] md:text-[40px] font-medium leading-[1.2] tracking-[-0.4px] text-on-dark">Satu Platform, Semua Kebutuhan Kariermu</h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-xl">
          <div class="bg-surface-elevated rounded-[20px] p-xxl flex flex-col">
            <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] mb-xs text-stone">Multi-Source</span>
            <h3 class="text-[20px] font-medium leading-[1.4] mb-sm text-on-dark">Agregasi Lowongan</h3>
            <p class="md:text-[16px] text-sm font-normal leading-[1.6] text-on-dark-mute mb-lg flex-1">Kumpulan lowongan kerja dan magang dari LinkedIn, Glints, Jobstreet, Fastwork, dan Pintarnya dalam satu tampilan.</p>
            <router-link to="/jobs" class="inline-flex items-center font-semibold transition-all duration-200 cursor-pointer text-[16px] bg-transparent text-on-dark hover:text-white pl-0">Lihat Lowongan →</router-link>
          </div>

          <div class="bg-surface-elevated rounded-[20px] p-xxl flex flex-col">
            <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] mb-xs text-stone">ATS Check</span>
            <h3 class="text-[20px] font-medium leading-[1.4] mb-sm text-on-dark">Analisis CV</h3>
            <p class="md:text-[16px] text-sm font-normal leading-[1.6] text-on-dark-mute mb-lg flex-1">Evaluasi kompatibilitas CV-mu terhadap sistem ATS dan dapatkan skor kecocokan dengan bidang keahlian spesifik.</p>
            <router-link to="/cv-analyzer" class="inline-flex items-center font-semibold transition-all duration-200 cursor-pointer text-[16px] bg-transparent text-on-dark hover:text-white pl-0">Analisis Sekarang →</router-link>
          </div>

          <div class="bg-surface-elevated rounded-[20px] p-xxl flex flex-col">
            <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] mb-xs text-stone">Builder</span>
            <h3 class="text-[20px] font-medium leading-[1.4] mb-sm text-on-dark">Pembuat CV</h3>
            <p class="md:text-[16px] text-sm font-normal leading-[1.6] text-on-dark-mute mb-lg flex-1">Buat dokumen CV ATS-minimalis dengan panduan pengisian dari asisten AI. Format rapi dan siap pakai.</p>
            <router-link to="/cv-builder" class="inline-flex items-center font-semibold transition-all duration-200 cursor-pointer text-[16px] bg-transparent text-on-dark hover:text-white pl-0">Buat CV →</router-link>
          </div>

          <!-- Featured card — cobalt violet inversion -->
          <div class="bg-surface-elevated rounded-[20px] p-xxl flex flex-col">
            <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] mb-xs text-stone">AI-Powered</span>
            <h3 class="text-[20px] font-medium leading-[1.4] mb-sm text-on-dark">Diskusi Karier</h3>
            <p class="md:text-[16px] text-sm font-normal leading-[1.6] text-on-dark-mute mb-lg flex-1">Tanya apapun seputar karier, lowongan, atau penyusunan CV. Dapatkan saran personal dari asisten AI.</p>
            <router-link to="/chatbot" class="inline-flex items-center font-semibold transition-all duration-200 cursor-pointer text-[16px] bg-transparent text-on-dark hover:text-white pl-0">Mulai Chat →</router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Documentation Section -->
    <section class="bg-transparent py-[80px]">
      <div class="w-full mx-auto px-[32px] md:px-[72px]">
        <div class="mb-xxl">
          <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-stone mb-lg block">Panduan</span>
          <h2 class="text-[32px] md:text-[40px] font-medium leading-[1.2] tracking-[-0.4px] text-on-dark">Mulai dengan JobFinder</h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-xl">
          <div class="bg-surface-elevated rounded-[20px] p-xxl flex flex-col border border-hairline-dark shadow-sm">
            <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-white mb-sm block">Langkah 1</span>
            <h3 class="text-[20px] font-medium leading-[1.4] mb-sm text-on-dark">Jelajahi Lowongan</h3>
            <p class="text-[14px] font-normal leading-[1.5] text-on-dark-mute">Gunakan filter canggih untuk menemukan posisi yang sesuai dengan keahlian dan preferensimu.</p>
          </div>
          <div class="bg-surface-elevated rounded-[20px] p-xxl flex flex-col border border-hairline-dark shadow-sm">
            <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-white mb-sm block">Langkah 2</span>
            <h3 class="text-[20px] font-medium leading-[1.4] mb-sm text-on-dark">Analisis CV</h3>
            <p class="text-[14px] font-normal leading-[1.5] text-on-dark-mute">Uji CV-mu terhadap standar ATS dan dapatkan rekomendasi perbaikan yang spesifik.</p>
          </div>
          <div class="bg-surface-elevated rounded-[20px] p-xxl flex flex-col border border-hairline-dark shadow-sm">
            <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-white mb-sm block">Langkah 3</span>
            <h3 class="text-[20px] font-medium leading-[1.4] mb-sm text-on-dark">Buat &amp; Lamar</h3>
            <p class="text-[14px] font-normal leading-[1.5] text-on-dark-mute">Bangun CV yang dioptimalkan untuk ATS dan lamar pekerjaan impianmu dengan percaya diri.</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>



<script setup>
import { Icon } from '@iconify/vue'
import { ref, onMounted } from "vue"
import { useHead } from "@vueuse/head"

useHead({
  title: 'JobFinder — Temukan Karier Masa Depanmu',
  meta: [
    {
      name: 'description',
      content: 'Platform agregasi lowongan kerja dan magang terlengkap di Indonesia. Temukan ribuan peluang dari LinkedIn, Glints, Jobstreet, dan sumber terpercaya lainnya — dilengkapi analisis CV berbasis AI dan pembuat CV ATS-friendly.'
    },
    { property: 'og:title', content: 'JobFinder — Temukan Karier Masa Depanmu' },
    { property: 'og:description', content: 'Agregasi lowongan kerja dan magang dari seluruh sumber terpercaya Indonesia, lengkap dengan analisis CV AI dan pembuat dokumen ATS.' },
  ]
})


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
/* Track wrapper — overflow + fade mask */
.logo-track-wrapper {
  position: relative;
  overflow: hidden;
  -webkit-mask-image: linear-gradient(to right, transparent 0%, black 12%, black 88%, transparent 100%);
  mask-image: linear-gradient(to right, transparent 0%, black 12%, black 88%, transparent 100%);
}

/* Scrolling track */
.logo-track {
  display: flex;
  width: max-content;
  animation: marquee-hero 25s linear infinite;
}

.logo-track:hover {
  animation-play-state: paused;
}

/* Logo group (one full set) */
.logo-group {
  display: flex;
  align-items: center;
  gap: 8px;
  padding-right: 8px;
}

/* Individual pill chip */
.logo-chip {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 16px;
  opacity: 0.6;
  transition: opacity 0.2s ease;
  flex-shrink: 0;
  cursor: default;
}

.logo-chip:hover {
  opacity: 1;
}

.logo-chip img {
  height: 36px;
  width: auto;
  object-fit: contain;
}

@keyframes marquee-hero {
  0%   { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
</style>
