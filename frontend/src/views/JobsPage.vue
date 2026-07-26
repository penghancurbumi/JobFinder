<template>
  <div class="pt-[88px] min-h-screen bg-canvas-dark text-on-dark font-sans">
    <div class="w-full max-w-[1200px] mx-auto px-xl">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-end mb-xl pb-lg border-b border-hairline-dark gap-md md:gap-0">
        <div>
          <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-stone">Eksplorasi</span>
          <h1 class="text-[32px] md:text-[40px] font-medium leading-[1.2] tracking-[-0.4px] text-on-dark mb-0">Daftar Pekerjaan Yang Tersedia</h1>
        </div>
        <button @click="requestScrape" class="inline-flex items-center justify-center font-medium rounded-full transition-all duration-200 cursor-pointer bg-on-dark text-ink hover:bg-white/90 px-[20px] py-[8px] h-[40px] text-[14px] gap-[8px]" :disabled="isScraping">
          <svg v-if="isScraping" class="animate-[spin_1s_linear_infinite]" viewBox="0 0 24 24" width="16" height="16">
            <circle class="animate-[dash_1.5s_ease-in-out_infinite] [stroke-dasharray:60] [stroke-dashoffset:60]" cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"></circle>
          </svg>
          {{ isScraping ? 'Mencari Data Baru...' : 'Perbarui Data' }}
        </button>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-[280px_1fr] items-start gap-lg">
        <!-- Filter Sidebar -->
        <aside class="bg-surface-elevated rounded-md p-xl static lg:sticky lg:top-[100px] mb-lg lg:mb-0">
          <div class="flex justify-between items-center mb-xl">
            <h3 class="text-base font-medium leading-[1.4] text-on-dark">Filter</h3>
            <button @click="resetFilters" class="p-0 h-auto bg-transparent text-white hover:text-stone font-semibold cursor-pointer text-sm">Reset</button>
          </div>

          <div class="mb-xl flex flex-col">
            <label class="block text-on-dark-mute mb-sm font-semibold text-sm">Pencarian Kata Kunci</label>
            <input type="text" v-model="searchQuery" placeholder="Software, UI/UX, Sales..." class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[40px] px-[12px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone text-sm" />
          </div>
          
          <div class="mb-xl flex flex-col">
            <label class="block text-on-dark-mute mb-sm font-semibold text-sm">Lokasi</label>
            <input type="text" v-model="locationQuery" placeholder="Jakarta, Remote, Bali..." class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[40px] px-[12px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone text-sm" />
          </div>

          <div class="mb-xl flex flex-col">
            <label class="block text-on-dark-mute mb-sm font-semibold text-sm">Tipe Pekerjaan</label>
            <select v-model="activeTipe" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[40px] px-[12px] text-on-dark focus:border-white focus:outline-none appearance-none text-sm">
              <option class="bg-surface-elevated text-on-dark" value="all">Semua Tipe</option>
              <option class="bg-surface-elevated text-on-dark" value="fulltime">Full-time</option>
              <option class="bg-surface-elevated text-on-dark" value="parttime">Part-time</option>
              <option class="bg-surface-elevated text-on-dark" value="contract">Contract</option>
              <option class="bg-surface-elevated text-on-dark" value="freelance">Freelance</option>
              <option class="bg-surface-elevated text-on-dark" value="intern">Internship</option>
              <option class="bg-surface-elevated text-on-dark" value="remote">Remote</option>
              <option class="bg-surface-elevated text-on-dark" value="hybrid">Hybrid</option>
              <option class="bg-surface-elevated text-on-dark" value="onsite">On-site</option>
            </select>
          </div>

          <div class="mb-xl flex flex-col">
            <label class="block text-on-dark-mute mb-sm font-semibold text-sm">Tingkat Pengalaman</label>
            <select v-model="experienceLevel" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[40px] px-[12px] text-on-dark focus:border-white focus:outline-none appearance-none text-sm">
              <option class="bg-surface-elevated text-on-dark" value="all">Semua Pengalaman</option>
              <option class="bg-surface-elevated text-on-dark" value="entry">Entry Level / Junior</option>
              <option class="bg-surface-elevated text-on-dark" value="mid">Mid Level</option>
              <option class="bg-surface-elevated text-on-dark" value="senior">Senior Level</option>
              <option class="bg-surface-elevated text-on-dark" value="manager">Manager / Director</option>
            </select>
          </div>

          <div class="mb-xl flex flex-col">
            <label class="block text-on-dark-mute mb-sm font-semibold text-sm">Rentang Gaji</label>
            <label class="flex items-center gap-[8px] font-normal text-[14px] normal-case cursor-pointer text-on-dark-mute">
              <input type="checkbox" v-model="hasSalary" class="w-[16px] h-[16px] min-h-[16px] cursor-pointer" />
              Hanya tampilkan yang mencantumkan gaji
            </label>
          </div>

          <div class="mt-xl flex flex-col">
            <label class="block text-on-dark-mute mb-sm font-semibold text-sm">Urutkan Berdasarkan</label>
            <select v-model="sortBy" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[40px] px-[12px] text-on-dark focus:border-white focus:outline-none appearance-none text-sm">
              <option class="bg-surface-elevated text-on-dark text-sm" value="newest">Terbaru</option>
              <option class="bg-surface-elevated text-on-dark text-sm" value="oldest">Terlama</option>
              <option class="bg-surface-elevated text-on-dark text-sm" value="az">Abjad (A - Z)</option>
              <option class="bg-surface-elevated text-on-dark text-sm" value="za">Abjad (Z - A)</option>
            </select>
          </div>
        </aside>

        <!-- Main Content -->
        <main>
          <div v-if="loading || isScraping" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-lg">
            <div v-for="n in 6" :key="'skeleton-' + n" class="bg-surface-elevated rounded-sm p-lg flex flex-col gap-0 min-h-[200px]">
              <div class="h-[24px] w-[70%] mb-[12px] bg-gradient-to-r from-surface-deep via-surface-elevated to-surface-deep bg-[length:200%_100%] animate-[loading-skeleton_1.5s_infinite] rounded-[4px]"></div>
              <div class="flex gap-[6px] mb-[12px]">
                <div class="h-[20px] w-[60px] rounded-[12px] bg-gradient-to-r from-surface-deep via-surface-elevated to-surface-deep bg-[length:200%_100%] animate-[loading-skeleton_1.5s_infinite]"></div>
                <div class="h-[20px] w-[60px] rounded-[12px] bg-gradient-to-r from-surface-deep via-surface-elevated to-surface-deep bg-[length:200%_100%] animate-[loading-skeleton_1.5s_infinite]"></div>
              </div>
              <div class="h-[16px] w-[50%] mb-[12px] bg-gradient-to-r from-surface-deep via-surface-elevated to-surface-deep bg-[length:200%_100%] animate-[loading-skeleton_1.5s_infinite] rounded-[4px]"></div>
              <div class="h-[12px] w-[80%] mb-[12px] bg-gradient-to-r from-surface-deep via-surface-elevated to-surface-deep bg-[length:200%_100%] animate-[loading-skeleton_1.5s_infinite] rounded-[4px]"></div>
              <div class="h-[32px] w-full rounded-[4px] mb-[16px] bg-gradient-to-r from-surface-deep via-surface-elevated to-surface-deep bg-[length:200%_100%] animate-[loading-skeleton_1.5s_infinite]"></div>
              <div class="h-[14px] w-full mb-[8px] bg-gradient-to-r from-surface-deep via-surface-elevated to-surface-deep bg-[length:200%_100%] animate-[loading-skeleton_1.5s_infinite] rounded-[4px]"></div>
              <div class="h-[14px] w-full mb-[8px] bg-gradient-to-r from-surface-deep via-surface-elevated to-surface-deep bg-[length:200%_100%] animate-[loading-skeleton_1.5s_infinite] rounded-[4px]"></div>
              <div class="h-[14px] w-[80%] mb-[8px] bg-gradient-to-r from-surface-deep via-surface-elevated to-surface-deep bg-[length:200%_100%] animate-[loading-skeleton_1.5s_infinite] rounded-[4px]"></div>
              <div class="h-[32px] w-[120px] rounded-full mt-auto bg-gradient-to-r from-surface-deep via-surface-elevated to-surface-deep bg-[length:200%_100%] animate-[loading-skeleton_1.5s_infinite]"></div>
            </div>
          </div>

          <div v-else-if="jobs.length === 0" class="text-center p-[64px] border border-dashed border-hairline-dark rounded-[20px]">
            <p class="text-[18px] font-normal leading-[1.56] tracking-[-0.09px] text-stone italic">Tidak ada peluang yang sesuai dengan filter.</p>
            <button @click="resetFilters" class="mt-lg inline-flex items-center justify-center font-semibold rounded-full transition-all duration-200 cursor-pointer text-[16px] px-[24px] h-[48px] bg-transparent border border-hairline-dark text-on-dark hover:bg-surface-elevated">Reset Filter</button>
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-lg">
            <div v-for="job in jobs" :key="job.title + job.company + job.id" class="bg-surface-elevated rounded-sm p-lg flex flex-col gap-[8px]">
              <div>
                <h3 class="text-[18px] font-medium leading-[1.4] text-on-dark">{{ job.title }}</h3>
                <div class="flex gap-[6px] shrink-0 flex-wrap mt-[8px]">
                  <span class="bg-surface-deep text-on-dark-mute border border-hairline-dark rounded-full px-[12px] py-[4px] text-[12px]">
                    {{ job.jobType.charAt(0).toUpperCase() + job.jobType.slice(1) }}
                  </span>
                  <span class="bg-white/10 text-white border border-white/25 rounded-full px-[12px] py-[4px] text-[12px]">{{ job.expertise }}</span>
                </div>
              </div>
              
              <div class="flex gap-sm text-[12px] flex-wrap">
                <strong class="text-on-dark">{{ job.company }}</strong>
                <span class="text-stone">•</span>
                <span class="text-on-dark-mute">{{ job.location || 'Lokasi tidak disebutkan' }}</span>
              </div>
              
              <div class="text-stone text-[12px] font-normal leading-[1.5]">
                Sumber: <a :href="job.url" target="_blank" class="text-white no-underline hover:underline">{{ job.source }}</a>
              </div>

              <div class="flex flex-wrap gap-sm bg-surface-deep p-sm rounded-[12px] mt-xs" v-if="job.postedDate || job.deadlineDate || job.salary">
                 <span v-if="job.postedDate" class="text-[12px] font-normal leading-[1.5] text-on-dark-mute">Diposting: {{ job.postedDate }}</span>
                 <span v-if="job.deadlineDate" class="text-[12px] leading-[1.5] text-accent-danger font-medium">Batas Waktu: {{ job.deadlineDate }}</span>
                 <span v-if="job.salary" class="text-[12px] leading-[1.5] text-accent-teal font-medium w-full">Gaji: {{ job.salary }}</span>
              </div>
              
              <div class="flex flex-col">
                <p :class="['text-[12px] font-normal leading-[1.5] text-on-dark-mute whitespace-pre-wrap mb-xs', { 'line-clamp-3 overflow-hidden text-ellipsis': !isExpanded(job) }]">{{ job.description }}</p>
              </div>
              
              <a :href="job.url" target="_blank" class="self-start inline-flex items-center justify-center font-medium rounded-full transition-all duration-200 cursor-pointer bg-on-dark text-ink hover:bg-white/90 px-[20px] py-[8px] h-[36px] text-[12px] no-underline">Lamar Sekarang</a>
            </div>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from "vue"
import { io } from "socket.io-client"

const jobs = ref([])
const loading = ref(true)
const isScraping = ref(false)

// Filters
const activeTipe = ref("all")
const searchQuery = ref("")
const locationQuery = ref("")
const experienceLevel = ref("all")
const hasSalary = ref(false)
const sortBy = ref("newest")

const expandedJobs = ref({})
let socket = null

function isExpanded(job) {
  return !!expandedJobs.value[job.id || (job.title + job.company)]
}

function toggleExpand(job) {
  const id = job.id || (job.title + job.company)
  expandedJobs.value[id] = !expandedJobs.value[id]
}

function needsTruncation(desc) {
  if (!desc) return false
  return desc.length > 200 // Truncate longer descriptions
}

onMounted(async () => {
  // Fetch existing jobs from REST API as primary data source (no scraping triggered)
  try {
    const res = await fetch("http://localhost:3000/api/jobs")
    if (res.ok) {
      jobs.value = await res.json()
      loading.value = false
    }
  } catch { /* socket will be fallback */ }

  socket = io("http://localhost:3000")
  
  socket.on("jobs-updated", (data) => {
    jobs.value = data
    loading.value = false
  })
  
  socket.on("scrape-status", (data) => {
    isScraping.value = data.status === "scraping"
  })

  socket.on("connect", () => {
    loading.value = false
    // Don't auto-scrape - just show existing data
  })
})

onUnmounted(() => {
  if (socket) socket.disconnect()
})

let searchTimeout;
watch([activeTipe, searchQuery, locationQuery, experienceLevel, hasSalary, sortBy], () => {
  loading.value = true
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    if (socket) {
      socket.emit("filter-jobs", { 
        search: searchQuery.value, 
        bidang: "all", 
        tipe: activeTipe.value,
        sortBy: sortBy.value,
        location: locationQuery.value,
        experience: experienceLevel.value,
        hasSalary: hasSalary.value
      })
    }
  }, 400) // debounce
})

function resetFilters() {
  activeTipe.value = "all"
  sortBy.value = "newest"
  searchQuery.value = ""
  locationQuery.value = ""
  experienceLevel.value = "all"
  hasSalary.value = false
}

function requestScrape() {
  if (socket && !isScraping.value) {
    isScraping.value = true
    socket.emit("request-scrape")
  }
}
</script>
