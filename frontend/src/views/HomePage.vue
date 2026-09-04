<template>
  <div class="home bg-transparent text-on-dark font-sans">
    <!-- Hero Section (Dark Canvas) -->
    <section class="bg-transparent py-[110px]">
      <div class="w-full mx-auto px-[32px] md:px-[72px]">
        <div class="flex flex-col gap-[30px] md:gap-[40px] items-center">
          <h1 class="font-medium leading-[1.0] tracking-[-0.8px]">
            <span class="text-[42px] md:text-[64px] lg:text-[72px] block">Temukan Karier</span>
            <span class="text-[42px] md:text-[64px] lg:text-[72px] block">Masa Depanmu</span>
          </h1>

          <p class="text-sm md:text-[15px] font-normal leading-[1.56] tracking-[-0.09px] text-on-dark-mute max-w-[640px] text-center">
            Platform agregasi lowongan kerja dan magang dari seluruh sumber terpercaya.
            Lengkap dengan analisis CV dan pembuatan dokumen ATS berstandar industri.
          </p>

          <div class="flex gap-[20px] flex-wrap items-center">
            <router-link to="/jobs" class="inline-flex items-center gap-[8px] justify-center font-medium rounded-full transition-all duration-200 cursor-pointer text-sm md:text-[18px] px-[20px] h-[44px] bg-on-dark text-ink hover:bg-white/90">
              Get Started
              <Icon icon="mdi-light:arrow-right" width="25"/>
            </router-link>            

            <a href="https://github.com/penghancurbumi/JobFinder" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-[8px] justify-center font-medium rounded-full transition-all duration-200 cursor-pointer text-sm md:text-[18px] px-[24px] h-[44px] bg-surface-elevated hover:bg-body border border-hairline-dark text-on-dark">
              <Icon icon="mdi:github" width="25"/>
              GitHub</a>
          </div>
        </div>
      </div>

      <div class="w-full mx-auto px-[32px] md:px-[120px] flex items-center justify-center mt-20 overflow-hidden">
        <div class="hero-border-gradient w-full overflow-hidden">
          <img src="../assets/images/image-hero.png" alt="image hero" class="rounded-sm w-full h-full object-cover object-center block">
        </div>
      </div>

      <!-- Logo Slider — full width, label kiri -->
      <div class="flex flex-col md:flex-row md:items-center gap-[16px] md:gap-[24px] mt-[80px]">

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
          <h2 class="text-[40px] md:text-[50px] font-medium leading-[1.2] tracking-[-0.4px] text-on-dark">Satu Platform, Semua Kebutuhan Kariermu</h2>
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
      fetch("/api/jobs?limit=500"),
      fetch("/api/expertise-areas"),
    ])

    if (jobsRes.ok) {
      const data = await jobsRes.json()
      const jobs = Array.isArray(data) ? data : (data.jobs || [])
      totalJobs.value = data.total || jobs.length
      const sources = new Set()
      jobs.forEach((j) => {
        if (j.source) sources.add(j.source)
      })
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
/* Gradient border: putih -> hairline-dark */
.hero-border-gradient {
  padding: 4px;
  background: linear-gradient(to right, rgba(255, 255, 255, 0.12),#545252, rgba(255, 255, 255, 0.12), #545252, rgba(255, 255, 255, 0.12));
  border-radius: 12px;
}

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
