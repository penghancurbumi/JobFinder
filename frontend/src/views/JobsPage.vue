<template>
  <div class="pt-[50px] md:pt-[88px] min-h-screen bg-canvas-dark text-on-dark font-sans">
    <div class="w-full mx-auto px-[32px] md:px-[72px]">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-end mb-xl pb-lg border-b border-hairline-dark gap-md md:gap-0">
        <div>
          <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-stone">Eksplorasi</span>
          <h1 class="text-[32px] md:text-[40px] font-medium leading-[1.2] tracking-[-0.4px] text-on-dark mb-0">Daftar Pekerjaan Yang Tersedia</h1>
        </div>
        <button @click="requestScrape" class="inline-flex items-center justify-center font-medium rounded-full transition-all duration-200 cursor-pointer bg-on-dark text-ink hover:bg-white/90 px-[20px] py-[8px] h-[40px] text-[14px] gap-[8px]" :disabled="isScraping || !!cooldownMsg">
          <svg v-if="isScraping" class="animate-[spin_1s_linear_infinite]" viewBox="0 0 24 24" width="16" height="16">
            <circle class="animate-[dash_1.5s_ease-in-out_infinite] [stroke-dasharray:60] [stroke-dashoffset:60]" cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"></circle>
          </svg>
          {{ isScraping ? 'Memperbarui Data...' : 'Perbarui Data' }}
        </button>
      </div>

      <div v-if="cooldownMsg" class="mb-xl bg-surface-elevated rounded-md p-lg border border-hairline-dark">
        <span class="text-sm font-medium">{{ cooldownMsg }}</span>
      </div>

      <!-- Live scrape progress -->
      <div v-if="isScraping" class="mb-xl bg-surface-elevated rounded-md p-lg border border-hairline-dark">
        <div class="flex items-center gap-sm mb-sm">
          <svg class="animate-[spin_1s_linear_infinite]" viewBox="0 0 24 24" width="16" height="16">
            <circle class="animate-[dash_1.5s_ease-in-out_infinite] [stroke-dasharray:60] [stroke-dashoffset:60]" cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"></circle>
          </svg>
          <span class="text-sm font-medium">Memperbarui data dari semua sumber...</span>
          <span class="ml-auto font-mono text-[12px] text-stone">{{ scrapeElapsed }}s</span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-sm">
          <div v-for="c in scrapeCategories" :key="c" class="bg-surface-deep rounded-sm p-sm border border-hairline-dark">
            <div class="flex items-center justify-between mb-xs">
              <span class="text-[12px] font-medium capitalize">{{ c }}</span>
              <span class="text-[11px] font-mono text-stone">{{ spiderCount(c) }}/7</span>
            </div>
            <div class="flex flex-wrap gap-[4px]">
              <span v-for="(s, name) in (scrapeStatus[c] || {}).spiders || {}" :key="name"
                :class="['text-[10px] px-[6px] py-[2px] rounded-full border', s.status === 'done' ? 'text-accent-teal border-white/20' : 'text-stone border-white/10']">
                {{ name }}{{ s.status === 'done' ? ' ✓' : '' }}
              </span>
              <span v-if="!Object.keys((scrapeStatus[c] || {}).spiders || {}).length" class="text-[10px] text-stone italic">menunggu...</span>
            </div>
          </div>
        </div>

        <div v-if="scrapeLog.length" class="mt-sm max-h-[110px] overflow-y-auto font-mono text-[11px] text-stone space-y-[2px]">
          <div v-for="(l, i) in scrapeLog" :key="i">{{ l }}</div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-[280px_1fr] items-start gap-lg">
        <!-- Filter Sidebar -->
        <aside class="bg-surface-elevated rounded-md p-xl static lg:sticky lg:top-[100px] mb-lg lg:mb-0">
          <div class="flex justify-between items-center mb-lg">
            <h3 class="text-base font-medium leading-[1.4] text-on-dark">Filter</h3>
            <button @click="resetFilters" class="p-0 h-auto bg-transparent text-white hover:text-stone font-semibold cursor-pointer text-sm">Reset</button>
          </div>

          <div class="mb-lg flex flex-col">
            <label class="block text-on-dark-mute mb-sm font-semibold text-sm">Pencarian Kata Kunci</label>
            <input type="text" v-model="searchQuery" placeholder="Software, UI/UX, Sales..." class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[40px] px-[12px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone text-sm" />
          </div>
          
          <div class="mb-lg flex flex-col">
            <label class="block text-on-dark-mute mb-sm font-semibold text-sm">Lokasi</label>
            <input type="text" v-model="locationQuery" placeholder="Jakarta, Remote, Bali..." class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[40px] px-[12px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone text-sm" />
          </div>

          <div class="mb-lg flex flex-col">
            <label class="block text-on-dark-mute mb-sm font-semibold text-sm">Tipe Pekerjaan</label>
            <CustomSelect v-model="activeTipe" :options="tipeOptions" placeholder="Semua Tipe" />
          </div>

          <div class="mb-lg flex flex-col">
            <label class="block text-on-dark-mute mb-sm font-semibold text-sm">Tingkat Pengalaman</label>
            <CustomSelect v-model="experienceLevel" :options="experienceOptions" placeholder="Semua Pengalaman" />
          </div>

          <div class="mb-lg flex flex-col">
            <label class="block text-on-dark-mute mb-sm font-semibold text-sm">Urutkan Berdasarkan</label>
            <CustomSelect v-model="sortBy" :options="sortOptions" placeholder="Terbaru" />
          </div>

          <div class="mt-lg flex flex-col">
            <label class="block text-on-dark-mute mb-sm font-semibold text-sm">Rentang Gaji</label>
            <label class="flex items-center gap-[8px] font-normal text-[13px] normal-case cursor-pointer text-on-dark-mute">
              <input type="checkbox" v-model="hasSalary" class="w-[12px] h-[12px] min-h-[12px] cursor-pointer" />
              Hanya tampilkan yang mencantumkan gaji
            </label>
          </div>

        </aside>

        <!-- Main Content -->
        <main>
          <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-lg">
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
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-xl">
            <div v-for="job in jobs" :key="job.title + job.company + job.id" class="bg-surface-elevated rounded-sm p-[15px] flex flex-col gap-[8px]">
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

              <div class="flex flex-wrap gap-sm bg-surface-deep p-sm rounded-[12px] mt-xs" v-if="formatPostedDate(job.postedDate) || job.deadlineDate || job.salary">
                 <span v-if="formatPostedDate(job.postedDate)" class="text-[12px] font-normal leading-[1.5] text-on-dark-mute">Diposting: {{ formatPostedDate(job.postedDate) }}</span>
                 <span v-if="job.deadlineDate" class="text-[12px] leading-[1.5] text-accent-danger font-medium">Batas Waktu: {{ job.deadlineDate }}</span>
                 <span v-if="job.salary" class="text-[12px] leading-[1.5] text-accent-teal font-medium w-full">Gaji: {{ job.salary }}</span>
              </div>
              
              <div class="flex flex-col">
                <p :class="['text-[12px] font-normal leading-[1.5] text-on-dark-mute whitespace-pre-wrap mb-xs', { 'line-clamp-3 overflow-hidden text-ellipsis': !isExpanded(job) }]">{{ job.description }}</p>
              </div>
              
              <a :href="job.url" target="_blank" class="self-start inline-flex items-center justify-center font-medium rounded-full transition-all duration-200 cursor-pointer bg-on-dark text-ink hover:bg-white/90 px-[20px] py-[8px] h-[36px] text-[12px] no-underline">Lamar Sekarang</a>
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
const isScraping = ref(false)
const page = ref(1)
const limit = 24
const total = ref(0)
const totalPages = ref(0)
const loadingMore = ref(false)

const scrapeCategories = ['fulltime', 'parttime', 'internship', 'hybrid', 'contract']
const scrapeStatus = ref({})
const scrapeLog = ref([])
const scrapeElapsed = ref(0)
const cooldownMsg = ref("")
let scrapeTimer = null
let cooldownTimer = null

// Filters
const activeTipe = ref("all")
const searchQuery = ref("")
const locationQuery = ref("")
const experienceLevel = ref("all")

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

onMounted(async () => {
  await fetchPage(1, false)

  socket = io("http://localhost:3000")
  
  socket.on("jobs-updated", (data) => {
    applyJobsPayload(data)
  })
  
  socket.on("scrape-status", (data) => {
    if (data.status === "cooldown") {
      isScraping.value = false
      startCooldown(data.waitSeconds || 300)
      return
    }
    clearTimeout(cooldownTimer)
    cooldownMsg.value = ""
    isScraping.value = data.status === "scraping"
    if (isScraping.value) {
      scrapeElapsed.value = 0
      scrapeLog.value = []
      scrapeStatus.value = {}
      if (!scrapeTimer) scrapeTimer = setInterval(() => scrapeElapsed.value++, 1000)
    } else {
      clearInterval(scrapeTimer)
      scrapeTimer = null
    }
  })

  socket.on("scrape-progress", (evt) => {
    if (evt.status === "done") {
      clearInterval(scrapeTimer)
      scrapeTimer = null
    }
    if (evt.status === "category-start") {
      scrapeStatus.value[evt.category] = { running: true, spiders: {} }
    } else if (evt.category && evt.spider) {
      const cat = scrapeStatus.value[evt.category] || (scrapeStatus.value[evt.category] = { running: true, spiders: {} })
      cat.spiders = cat.spiders || {}
      cat.spiders[evt.spider] = { status: evt.status, items: evt.items || 0 }
    }
    if (evt.message) {
      scrapeLog.value.push(`${new Date().toLocaleTimeString('id-ID', { hour12: false })} ${evt.message}`)
      if (scrapeLog.value.length > 12) scrapeLog.value.shift()
    }
  })

  socket.on("connect", () => {
    loading.value = false
    // Don't auto-scrape - just show existing data
  })
})

onUnmounted(() => {
  clearInterval(scrapeTimer)
  scrapeTimer = null
  clearInterval(cooldownTimer)
  cooldownTimer = null
  if (socket) socket.disconnect()
})

function spiderCount(c) {
  const cat = scrapeStatus.value[c]
  if (!cat || !cat.spiders) return 0
  return Object.values(cat.spiders).filter((s) => s.status === 'done').length
}

function applyJobsPayload(data) {
  if (!data) return
  jobs.value = data.jobs || []
  total.value = data.total || 0
  totalPages.value = data.totalPages || 0
  page.value = data.page || 1
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
    hasSalary: hasSalary.value ? 'true' : 'false',
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
watch([activeTipe, searchQuery, locationQuery, experienceLevel, hasSalary, sortBy], () => {
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
  hasSalary.value = false
}

function startCooldown(seconds) {
  cooldownMsg.value = `Tunggu ${seconds} detik sebelum memperbarui lagi`
  clearInterval(cooldownTimer)
  cooldownTimer = setInterval(() => {
    seconds--
    if (seconds <= 0) {
      clearInterval(cooldownTimer)
      cooldownTimer = null
      cooldownMsg.value = ""
    } else {
      cooldownMsg.value = `Tunggu ${seconds} detik sebelum memperbarui lagi`
    }
  }, 1000)
}

function requestScrape() {
  if (socket && !isScraping.value && !cooldownMsg.value) {
    socket.emit("request-scrape")
  }
}
</script>
