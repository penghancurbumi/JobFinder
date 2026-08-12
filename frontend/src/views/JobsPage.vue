<template>
  <div class="pt-[50px] md:pt-[88px] min-h-screen bg-canvas-dark text-on-dark font-sans">
    <div class="w-full mx-auto px-[32px] md:px-[72px]">
      <div class="mb-xl pb-lg border-b border-hairline-dark">
        <div class="flex flex-col mb-lg">
          <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-stone mb-xs">Eksplorasi</span>
          <h1 class="text-[32px] md:text-[40px] font-medium leading-[1.2] tracking-[-0.4px] text-on-dark mb-0">Daftar Pekerjaan Yang Tersedia</h1>
        </div>

        <div class="flex flex-col md:flex-row items-center gap-md">          
          <div class="relative w-full md:flex-1">
            <Icon icon="material-symbols-light:search" class="absolute left-[16px] top-1/2 -translate-y-1/2 text-stone pointer-events-none" width="18" height="18" />
            <input type="text" v-model="searchQuery" placeholder="Cari posisi, kata kunci, teknologi..." class="w-full bg-surface-elevated border border-hairline-dark rounded-sm h-[44px] pl-[44px] pr-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone text-sm transition-all" />
          </div>

          <div class="relative w-full md:w-[280px]">
            <Icon icon="ion:location-outline" class="absolute left-[16px] top-1/2 -translate-y-1/2 text-stone pointer-events-none" width="18" height="18" />
            <input type="text" v-model="locationQuery" placeholder="Kota, lokasi, atau Remote..." class="w-full bg-surface-elevated border border-hairline-dark rounded-sm h-[44px] pl-[44px] pr-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone text-sm transition-all" />
          </div>

          <button @click="requestScrape" class="w-full md:w-auto shrink-0 inline-flex items-center justify-center font-medium rounded-sm transition-all duration-200 cursor-pointer bg-on-dark text-ink hover:bg-white/90 px-[24px] h-[44px] text-[14px] gap-[8px]" :disabled="backgroundRunning">
            <svg v-if="backgroundRunning" class="animate-[spin_1s_linear_infinite]" viewBox="0 0 24 24" width="16" height="16">
              <circle class="animate-[dash_1.5s_ease-in-out_infinite] [stroke-dasharray:60] [stroke-dashoffset:60]" cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"></circle>
            </svg>
            {{ buttonLabel }}
          </button>
        </div>

        <span class="text-[12px] text-stone mt-[8px] block">
          Total data {{ jobTotal.toLocaleString('id-ID') }} jobs • {{ (status.total_jobs_scraped || 0).toLocaleString('id-ID') }} data job ditambahkan
        </span>

      </div>

      <div v-if="statusMsg" class="mb-xl bg-surface-elevated rounded-md p-lg border border-hairline-dark">
        <span class="text-sm font-medium" :class="statusType === 'error' ? 'text-accent-danger' : 'text-accent-teal'">{{ statusMsg }}</span>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-[280px_1fr] items-start gap-lg">

        <!-- Filter Sidebar -->
        <aside class="bg-surface-elevated rounded-md p-xl static lg:sticky lg:top-[100px] mb-lg lg:mb-0 border border-hairline-dark">
          <div class="flex justify-between items-center mb-xl">
            <h3 class="text-base font-medium leading-[1.4] text-on-dark">Filter</h3>
            <button @click="resetFilters" class="p-0 h-auto bg-transparent text-white hover:text-stone font-semibold cursor-pointer text-sm">Reset</button>
          </div>

          <div class="mb-xl flex flex-col">
            <label class="block text-on-dark-mute mb-sm font-medium text-sm">Tipe Pekerjaan</label>
            <CustomSelect v-model="activeTipe" :options="tipeOptions" placeholder="Semua Tipe" />
          </div>

          <div class="mb-xl flex flex-col">
            <label class="block text-on-dark-mute mb-sm font-medium text-sm">Pengalaman</label>
            <CustomSelect v-model="experienceLevel" :options="experienceOptions" placeholder="Semua Pengalaman" />
          </div>

          <div class="mb-xl flex flex-col">
            <label class="block text-on-dark-mute mb-sm font-medium text-sm">Pendidikan</label>
            <CustomSelect v-model="educationlevel" :options="educationOptions" placeholder="Semua Pendidikan" />
          </div>

          <div class="mb-xl flex flex-col">
            <label class="block text-on-dark-mute mb-sm font-medium text-sm">Urutkan Berdasarkan</label>
            <CustomSelect v-model="sortBy" :options="sortOptions" placeholder="Terbaru" />
          </div>

          <div class="mt-xl flex flex-col">
            <label class="block text-on-dark-mute mb-sm font-medium text-sm">Rentang Gaji</label>
            <label class="flex items-center gap-[8px] font-normal text-[13px] normal-case cursor-pointer text-on-dark-mute">
              <input type="checkbox" v-model="hasSalary" class="w-[12px] h-[12px] min-h-[12px] cursor-pointer" />
              Hanya tampilkan yang mencantumkan gaji
            </label>
          </div>

          <div class="mt-xl flex flex-col">
            <label class="flex items-center gap-[8px] font-normal text-[13px] normal-case cursor-pointer text-on-dark-mute">
              <input type="checkbox" v-model="showClosed" class="w-[12px] h-[12px] min-h-[12px] cursor-pointer" />
              Tampilkan lowongan ditutup{{ closedCount ? ` (${closedCount})` : '' }}
            </label>
          </div>

        </aside>

        <!-- Main Content -->
        <main>
          <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-xl items-stretch">
            <div v-for="n in 6" :key="'skeleton-' + n" class="bg-surface-elevated rounded-md p-lg flex flex-col justify-between h-full border border-hairline-dark">
              <div class="flex flex-col gap-sm">
                <div class="h-[50px] w-[85%] bg-gradient-to-r from-surface-deep via-surface-elevated to-surface-deep bg-[length:200%_100%] animate-[loading-skeleton_1.5s_infinite] rounded-[4px] mb-xs"></div>
                <div class="flex gap-[6px]">
                  <div class="h-[24px] w-[70px] rounded-full bg-gradient-to-r from-surface-deep via-surface-elevated to-surface-deep bg-[length:200%_100%] animate-[loading-skeleton_1.5s_infinite]"></div>
                  <div class="h-[24px] w-[80px] rounded-full bg-gradient-to-r from-surface-deep via-surface-elevated to-surface-deep bg-[length:200%_100%] animate-[loading-skeleton_1.5s_infinite]"></div>
                </div>
                <div class="h-[16px] w-[60%] bg-gradient-to-r from-surface-deep via-surface-elevated to-surface-deep bg-[length:200%_100%] animate-[loading-skeleton_1.5s_infinite] rounded-[4px]"></div>
                <div class="h-[14px] w-[40%] bg-gradient-to-r from-surface-deep via-surface-elevated to-surface-deep bg-[length:200%_100%] animate-[loading-skeleton_1.5s_infinite] rounded-[4px]"></div>
                <div class="h-[76px] w-full rounded-[12px] mt-xs bg-gradient-to-r from-surface-deep via-surface-elevated to-surface-deep bg-[length:200%_100%] animate-[loading-skeleton_1.5s_infinite]"></div>
              </div>
              <div class="mt-md pt-sm border-t border-hairline-dark/40">
                <div class="h-[38px] w-full rounded-full bg-gradient-to-r from-surface-deep via-surface-elevated to-surface-deep bg-[length:200%_100%] animate-[loading-skeleton_1.5s_infinite]"></div>
              </div>
            </div>
          </div>

          <div v-else-if="jobs.length === 0" class="text-center p-[64px] border border-dashed border-hairline-dark rounded-[20px]">
            <p class="text-[18px] font-normal leading-[1.56] tracking-[-0.09px] text-stone italic">Tidak ada peluang yang sesuai dengan filter.</p>
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-lg items-stretch">
            <div 
              v-for="job in jobs" 
              :key="job.title + job.company + job.id" 
              class="bg-surface-elevated rounded-md p-lg flex flex-col justify-between h-full border border-hairline-dark hover:border-white/20 transition-all duration-200 shadow-sm"
              :class="{ 'opacity-60': job.isClosed }"
            >
              <!-- Top & Middle Info -->
              <div class="flex flex-col gap-sm">
                <!-- Title & Badges -->
                <div>
                  <h3 
                    class="text-[18px] font-medium leading-[1.4] text-on-dark line-clamp-2 min-h-[50px] mb-xs"
                    :title="job.title"
                  >
                    {{ job.title }}
                  </h3>
                  <div class="flex gap-[6px] shrink-0 flex-wrap items-center">
                    <span v-if="job.isClosed" class="bg-accent-danger/15 text-accent-danger border border-accent-danger/40 rounded-full px-[12px] py-[4px] text-[12px] font-semibold">
                      Ditutup
                    </span>
                    <span class="bg-surface-deep text-on-dark-mute border border-hairline-dark rounded-full px-[12px] py-[4px] text-[12px] font-medium">
                      {{ job.jobType ? (job.jobType.charAt(0).toUpperCase() + job.jobType.slice(1)) : 'Full-time' }}
                    </span>
                    <span v-if="job.expertise" class="bg-white/10 text-white border border-white/25 rounded-full px-[12px] py-[4px] text-[12px] font-medium truncate max-w-[150px]">
                      {{ job.expertise }}
                    </span>
                  </div>
                </div>
                
                <!-- Company & Location -->
                <div class="flex items-center gap-xs text-[12px] text-on-dark-mute truncate mt-xs">
                  <strong class="text-on-dark truncate max-w-[140px]" :title="job.company">{{ job.company }}</strong>
                  <span class="text-stone">•</span>
                  <span class="truncate" :title="job.location || 'Lokasi tidak disebutkan'">
                    {{ job.location || 'Lokasi tidak disebutkan' }}
                  </span>
                </div>
                
                <!-- Source -->
                <div class="text-stone text-[12px] font-normal leading-[1.5]">
                  Sumber: 
                  <a :href="job.url" target="_blank" rel="noopener noreferrer" class="text-white font-medium no-underline hover:underline">
                    {{ job.source }}
                  </a>
                </div>

                <!-- Info Meta Box (Uniform structure for all cards) -->
                <div class="flex flex-col gap-[4px] min-h-[76px] justify-center mt-xs">
                  <div class="flex justify-between items-center text-[12px]">
                    <span class="text-stone">Diposting</span>
                    <span class="text-on-dark-mute font-medium">
                      {{ formatPostedDate(job.postedDate) || 'Terbaru' }}
                    </span>
                  </div>
                  
                  <div class="flex justify-between items-center text-[12px]">
                    <span class="text-stone">Batas Waktu</span>
                    <span :class="job.deadlineDate ? 'text-accent-danger font-medium' : 'text-stone'">
                      {{ job.deadlineDate || '-' }}
                    </span>
                  </div>

                  <div class="flex justify-between items-center text-[12px]">
                    <span class="text-stone">Gaji</span>
                    <span :class="job.salary ? 'text-accent-teal font-medium' : 'text-stone'">
                      {{ job.salary || 'Tidak dicantumkan' }}
                    </span>
                  </div>
                </div>
              </div>
              
              <!-- Bottom Action Button -->
              <div class="mt-md pt-sm">
                <a 
                  :href="job.url" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  class="w-full inline-flex items-center justify-center font-medium rounded-sm transition-all duration-200 cursor-pointer bg-on-dark text-ink hover:bg-white/90 px-[20px] py-[8px] h-[38px] text-[13px] no-underline gap-xs"
                >
                  Lamar Sekarang
                </a>
              </div>
            </div>
          </div>

          <!-- Pagination Numbering -->
          <div v-if="!loading && totalPages > 1" class="mt-xl flex flex-col items-center gap-md">
            <div class="flex items-center gap-sm flex-wrap justify-center">
              <button 
                @click="goToPage(page - 1)" 
                :disabled="page === 1 || loading"
                aria-label="Halaman Sebelumnya"
                class="inline-flex items-center justify-center font-medium rounded-sm transition-all duration-200 w-[40px] h-[40px] text-[14px] bg-surface-elevated border border-hairline-dark text-on-dark hover:bg-body disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
              >
                <Icon icon="solar:arrow-left-outline" width="16" height="16" aria-hidden="true" />
              </button>

              <button 
                v-for="(p, idx) in visiblePages" 
                :key="'page-' + idx"
                @click="goToPage(p)"
                :disabled="p === '...'"
                :class="[
                  'inline-flex items-center justify-center font-medium rounded-sm transition-all duration-200 min-w-[40px] h-[40px] px-[12px] text-[14px]',
                  p === page 
                    ? 'bg-on-dark text-ink font-semibold' 
                    : p === '...' 
                      ? 'bg-transparent text-stone cursor-default border-none' 
                      : 'bg-surface-elevated border border-hairline-dark text-on-dark hover:bg-body cursor-pointer'
                ]"
              >
                {{ p }}
              </button>

              <button 
                @click="goToPage(page + 1)" 
                :disabled="page === totalPages || loading"
                aria-label="Halaman Selanjutnya"
                class="inline-flex items-center justify-center font-medium rounded-sm transition-all duration-200 w-[40px] h-[40px] text-[14px] bg-surface-elevated border border-hairline-dark text-on-dark hover:bg-body disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
              >
                <Icon icon="solar:arrow-right-outline" width="16" height="16" aria-hidden="true" />
              </button>
            </div>
          </div>
        </main>
        
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from "vue"
import { Icon } from '@iconify/vue'
import { io } from "socket.io-client"
import CustomSelect from "../components/CustomSelect.vue"
import { useHead } from "@vueuse/head"

useHead({
  title: 'Cari Lowongan Kerja & Magang — JobFinder',
  meta: [
    { name: 'description', content: 'Temukan ribuan lowongan kerja dan magang dari LinkedIn, Glints, Jobstreet, Pintarnya, KitaLulus, dan sumber terpercaya lainnya. Filter berdasarkan tipe, lokasi, pengalaman, dan gaji.' },
    { property: 'og:title', content: 'Cari Lowongan Kerja & Magang — JobFinder' },
    { property: 'og:description', content: 'Ribuan lowongan kerja dan magang dari seluruh sumber terpercaya di Indonesia dalam satu platform.' },
  ]
})


const jobs = ref([])
const loading = ref(true)
const backgroundRunning = ref(false)
const status = ref({})
const jobTotal = ref(0)
const statusMsg = ref("")
const statusType = ref("ok")
const page = ref(1)
const limit = 24
const total = ref(0)
const totalPages = ref(0)
const loadingMore = ref(false)

let statusTimer = null

// Filters
const activeTipe = ref("all")
const searchQuery = ref("")
const locationQuery = ref("")
const experienceLevel = ref("all")
const educationlevel = ref("all")

const tipeOptions = [
  { value: 'all', label: 'Semua Tipe' },
  { value: 'fulltime', label: 'Full-time' },
  { value: 'parttime', label: 'Part-time' },
  { value: 'contract', label: 'Contract' },
  { value: 'freelance', label: 'Freelance' },
  { value: 'intern', label: 'Internship' },
  { value: 'remote', label: 'Remote' },
  { value: 'hybrid', label: 'Hybrid' },
  { value: 'onsite', label: 'On-site' }
]

const sortOptions = [
  { value: 'newest', label: 'Terbaru' },
  { value: 'oldest', label: 'Terlama' },
  { value: 'az', label: 'Abjad (A - Z)' },
  { value: 'za', label: 'Abjad (Z - A)' }
]

const experienceOptions = [
  { value: 'all', label: 'Semua Pengalaman' },
  { value: 'entry', label: 'Entry Level / Junior' },
  { value: 'mid', label: 'Mid Level' },
  { value: 'senior', label: 'Senior Level' },
  { value: 'manager', label: 'Manager / Director' }
]

const educationOptions = [
  { value: 'all', label: 'Semua Pendidikan' },
  { value: 's3', label: 'S3 / Doktor' },
  { value: 's2', label: 'S2 / Magister' },
  { value: 's1', label: 'S1 / Sarjana' },
  { value: 'd4', label: 'D4 / Sarjana Terapan' },
  { value: 'd3', label: 'D3 / Diploma 3' },
  { value: 'sma', label: 'SMA / SMK Sederajat' }
]


const hasSalary = ref(false)
const showClosed = ref(false)
const closedCount = ref(0)
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
  return desc.length > 200
}

function formatPostedDate(raw) {
  if (!raw) return null
  // Cek apakah format ISO/YYYY-MM-DD
  const isoMatch = raw.match(/^(\d{4})-(\d{2})-(\d{2})/)
  if (isoMatch) {
    const date = new Date(raw)
    if (!isNaN(date)) {
      return date.toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' })
    }
  }
  // Jika teks tidak valid / relatif ("Terakhir d...") — sembunyikan
  return null
}

const lastUpdatedText = computed(() => {
  const iso = status.value.last_run_at
  if (!iso) return "belum pernah"
  const diff = Date.now() - new Date(iso).getTime()
  const min = Math.floor(diff / 60000)
  if (min < 1) return "baru saja"
  if (min < 60) return `${min} menit lalu`
  const h = Math.floor(min / 60)
  if (h < 24) return `${h} jam lalu`
  return `${Math.floor(h / 24)} hari lalu`
})

function cap(s) {
  return s ? String(s).charAt(0).toUpperCase() + String(s).slice(1) : ""
}

const buttonLabel = computed(() => {
  if (backgroundRunning.value) return `Memperbarui Data...`
  return `Perbarui Data`
})

async function refreshStatus() {
  try {
    const res = await fetch("http://localhost:3000/api/status")
    if (res.ok) status.value = await res.json()
  } catch { /* ignore */ }
}

function setStatusMsg(msg, type = "ok") {
  statusMsg.value = msg
  statusType.value = type
  clearTimeout(statusTimer)
  statusTimer = setTimeout(() => { statusMsg.value = "" }, 5000)
}

onMounted(async () => {
  await fetchPage(1, false)
  refreshStatus()

  socket = io("http://localhost:3000")
  
  socket.on("jobs-updated", (data) => {
    applyJobsPayload(data)
    refreshStatus()
  })
  
  socket.on("scrape-status", (data) => {
    if (data.status === "started" || data.status === "running") {
      backgroundRunning.value = true
      if (data.message) setStatusMsg(data.message, "ok")
      return
    }
    if (data.status === "completed") {
      backgroundRunning.value = false
      if (data.message) setStatusMsg(data.message, "ok")
      refreshStatus()
      return
    }
    if (data.status === "failed") {
      backgroundRunning.value = false
      setStatusMsg(data.message || "Scraping gagal", "error")
      refreshStatus()
      return
    }
    if (data.status === "idle") {
      backgroundRunning.value = false
      refreshStatus()
    }
  })

  socket.on("connect", () => {
    loading.value = false
  })
})

onUnmounted(() => {
  clearTimeout(statusTimer)
  statusTimer = null
  if (socket) socket.disconnect()
})

function applyJobsPayload(data) {
  if (!data) return
  jobs.value = data.jobs || []
  total.value = data.total || 0
  totalPages.value = data.totalPages || 0
  closedCount.value = data.closedCount || 0
  page.value = data.page || 1
  jobTotal.value = data.total || 0
  loading.value = false
  loadingMore.value = false
}

async function fetchPage(p, append = false) {
  if (append) loadingMore.value = true
  else loading.value = true
  const params = new URLSearchParams({
    search: searchQuery.value,
    tipe: activeTipe.value,
    sortBy: sortBy.value,
    location: locationQuery.value,
    experience: experienceLevel.value,
    education: educationlevel.value,
    hasSalary: hasSalary.value ? 'true' : 'false',
    showClosed: showClosed.value ? 'true' : 'false',
    page: String(p),
    limit: String(limit)
  })
  try {
    const res = await fetch(`http://localhost:3000/api/jobs?${params}`)
    if (res.ok) {
      const data = await res.json()
      if (append) jobs.value = [...jobs.value, ...(data.jobs || [])]
      else jobs.value = data.jobs || []
      total.value = data.total || 0
      totalPages.value = data.totalPages || 0
      closedCount.value = data.closedCount || 0
      page.value = p
    }
  } catch { /* socket will be fallback */ }
  loading.value = false
  loadingMore.value = false
}

function goToPage(p) {
  if (typeof p !== 'number' || p < 1 || p > totalPages.value || p === page.value || loading.value) return
  fetchPage(p, false)
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const visiblePages = computed(() => {
  const current = page.value
  const totalP = totalPages.value
  if (totalP <= 7) {
    return Array.from({ length: totalP }, (_, i) => i + 1)
  }
  const pages = []
  if (current <= 4) {
    for (let i = 1; i <= 5; i++) pages.push(i)
    pages.push('...')
    pages.push(totalP)
  } else if (current >= totalP - 3) {
    pages.push(1)
    pages.push('...')
    for (let i = totalP - 4; i <= totalP; i++) pages.push(i)
  } else {
    pages.push(1)
    pages.push('...')
    for (let i = current - 1; i <= current + 1; i++) pages.push(i)
    pages.push('...')
    pages.push(totalP)
  }
  return pages
})

let searchTimeout;
watch([activeTipe, searchQuery, locationQuery, experienceLevel, educationlevel, hasSalary, sortBy, showClosed], () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    fetchPage(1, false)
  }, 400) // debounce
})

function resetFilters() {
  activeTipe.value = "all"
  sortBy.value = "newest"
  searchQuery.value = ""
  locationQuery.value = ""
  experienceLevel.value = "all"
  educationlevel.value = "all"
  hasSalary.value = false
  showClosed.value = false
  closedCount.value = 0
}

function requestScrape() {
  if (socket && !backgroundRunning.value) {
    socket.emit("request-scrape")
  }
}
</script>
