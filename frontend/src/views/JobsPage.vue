<template>
  <div class="page">
    <div class="header-action stagger-1">
      <h1 class="page-title" style="margin-bottom: 0;">Daftar Pekerjaan & Magang</h1>
      <button @click="requestScrape" class="btn btn-outline btn-sm" :disabled="isScraping" style="display: flex; align-items: center; gap: 8px;">
        <svg v-if="isScraping" class="spinner" viewBox="0 0 24 24" width="16" height="16">
          <circle class="spinner-circle" cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"></circle>
        </svg>
        {{ isScraping ? 'Mencari Data...' : 'Perbarui Data' }}
      </button>
    </div>

    <div class="card stagger-2" style="margin-bottom: 32px; padding: 24px;">
      <div class="filter-row">
        <div class="filter-group">
          <label>Filter Tipe</label>
          <select v-model="activeTipe" class="form-select" style="width: 100%; padding: 10px 12px; border-radius: 6px; border: 1px solid var(--border-color); background: var(--bg-canvas); color: var(--text-primary); font-size: 14px;">
            <option value="all">Semua Tipe</option>
            <option value="fulltime">Fulltime</option>
            <option value="hybrid">Hybrid</option>
            <option value="freelance">Freelance</option>
            <option value="parttime">Parttime</option>
            <option value="intern">Internship</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label>Urutkan</label>
          <select v-model="sortBy" class="form-select" style="width: 100%; padding: 10px 12px; border-radius: 6px; border: 1px solid var(--border-color); background: var(--bg-canvas); color: var(--text-primary); font-size: 14px;">
            <option value="all">Semua</option>
            <option value="newest">Terbaru</option>
            <option value="oldest">Terlama</option>
            <option value="az">Abjad (A - Z)</option>
            <option value="za">Abjad (Z - A)</option>
          </select>
        </div>

        <div class="filter-group" style="flex: 2;">
          <label>Cari Keahlian atau Jabatan</label>
          <input type="text" v-model="searchQuery" placeholder="Contoh: Software Development, UI/UX..." />
        </div>

        <div class="filter-group" style="flex: 0; align-self: flex-end;">
          <button @click="resetFilters" class="btn btn-outline" style="height: 42px; padding: 0 16px;">Reset</button>
        </div>
      </div>
    </div>

    <div v-if="loading" class="bento-grid stagger-3">
      <div v-for="n in 6" :key="'skeleton-' + n" class="card job-card skeleton-card">
        <div class="skeleton skeleton-title"></div>
        <div class="skeleton-badge-row">
          <div class="skeleton skeleton-badge"></div>
          <div class="skeleton skeleton-badge"></div>
        </div>
        <div class="skeleton skeleton-meta"></div>
        <div class="skeleton skeleton-source"></div>
        <div class="skeleton skeleton-dates"></div>
        <div class="skeleton skeleton-desc"></div>
        <div class="skeleton skeleton-desc"></div>
        <div class="skeleton skeleton-desc" style="width: 80%;"></div>
        <div class="skeleton skeleton-button"></div>
      </div>
    </div>
    <div v-else-if="jobs.length === 0" class="card stagger-3" style="text-align:center;padding:64px; border-style: dashed;">
      <p style="color: var(--text-muted); font-family: 'Newsreader', serif; font-style: italic; font-size: 1.2rem;">Tidak ada peluang yang sesuai dengan filter.</p>
    </div>
    <div v-else class="bento-grid stagger-3">
      <div v-for="job in jobs" :key="job.title + job.company" class="card job-card">
        <div class="job-header">
          <h3 style="font-family: 'Newsreader', serif; font-size: 1.25rem;">{{ job.title }}</h3>
          <div class="job-badges">
            <span :class="['badge', 'badge-' + job.jobType.toLowerCase()]">
              {{ job.jobType.charAt(0).toUpperCase() + job.jobType.slice(1) }}
            </span>
            <span class="badge badge-expertise">{{ job.expertise }}</span>
          </div>
        </div>
        
        <div class="job-meta">
          <span style="font-weight: 500;">{{ job.company }}</span>
          <span style="color: var(--text-muted);">{{ job.location }}</span>
        </div>
        
        <div style="font-size: 12px; margin-bottom: 12px; color: var(--text-muted); word-break: break-all;">
          Sumber: <a :href="job.url" target="_blank" style="color: inherit; text-decoration: underline;">{{ job.source }} ({{ job.url === '#' ? job.source.toLowerCase() + '.com' : job.url }})</a>
        </div>

        <div class="job-dates" v-if="job.postedDate || job.deadlineDate || job.salary">
           <span v-if="job.postedDate">Diposting: {{ job.postedDate }}</span>
           <span v-if="job.deadlineDate" class="deadline-text">Batas Waktu: {{ job.deadlineDate }}</span>
           <span v-if="job.salary" class="salary-text" style="color: var(--pastel-green-text); font-weight: 500;">Gaji: {{ job.salary }}</span>
        </div>
        
        <div class="job-desc-container">
          <p :class="['job-desc', { 'collapsed': !isExpanded(job) }]" style="white-space: pre-wrap;">{{ job.description }}</p>
          <button v-if="needsTruncation(job.description)" 
                  @click="toggleExpand(job)" 
                  style="padding: 0; color: var(--text-primary); font-weight: 600; cursor: pointer; background: none; border: none; text-decoration: underline; margin-bottom: 16px; font-size: 14px;">
            {{ isExpanded(job) ? 'Tampilkan Lebih Sedikit' : 'Selengkapnya' }}
          </button>
        </div>
        
        <a :href="job.url" target="_blank" class="btn btn-sm btn-primary" style="align-self: flex-start; margin-top: auto;">Lamar Sekarang</a>
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
const activeTipe = ref("all")
const searchQuery = ref("")
const sortBy = ref("all")
const expandedJobs = ref({})
let socket = null

function isExpanded(job) {
  return !!expandedJobs.value[job.title + job.company]
}

function toggleExpand(job) {
  const id = job.title + job.company
  expandedJobs.value[id] = !expandedJobs.value[id]
}

function needsTruncation(desc) {
  if (!desc) return false
  return desc.length > 250 // Roughly 4 lines of text
}

onMounted(() => {
  socket = io("http://localhost:3000")
  
  socket.on("jobs-updated", (data) => {
    jobs.value = data
    loading.value = false
  })
  
  socket.on("scrape-status", (data) => {
    isScraping.value = data.status === "scraping"
  })

  // Automatically request a scrape when page loads and socket connects
  socket.on("connect", () => {
    requestScrape()
  })
})

onUnmounted(() => {
  if (socket) socket.disconnect()
})

let searchTimeout;
watch([activeTipe, searchQuery, sortBy], () => {
  loading.value = true
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    if (socket) {
      socket.emit("filter-jobs", { 
        search: searchQuery.value, 
        bidang: "all", 
        tipe: activeTipe.value,
        sortBy: sortBy.value 
      })
    }
  }, 300) // debounce
})

function resetFilters() {
  activeTipe.value = "all"
  sortBy.value = "all"
  searchQuery.value = ""
}

function requestScrape() {
  if (socket && !isScraping.value) {
    isScraping.value = true
    socket.emit("request-scrape")
  }
}
</script>

<style scoped>
.header-action { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 40px; }
.filter-row { display: flex; gap: 24px; flex-wrap: wrap; align-items: end; }
.filter-group { flex: 1; min-width: 200px; }
.tab-group { display: flex; gap: 4px; background: var(--bg-canvas); padding: 4px; border-radius: 6px; border: 1px solid var(--border-color); }
.tab { flex: 1; padding: 8px 16px; border: none; border-radius: 4px; font-size: 13px; cursor: pointer; background: transparent; transition: all 0.2s; color: var(--text-muted); }
.tab.active { background: var(--bg-surface); font-weight: 500; color: var(--text-primary); box-shadow: 0 1px 2px rgba(0,0,0,0.04); }
.job-card { display: flex; flex-direction: column; gap: 12px; }
.job-header { display: flex; flex-direction: column; gap: 12px; }
.job-badges { display: flex; gap: 6px; flex-shrink: 0; flex-wrap: wrap; }
.job-meta { display: flex; gap: 12px; font-size: 13px; color: var(--text-primary); margin-bottom: -4px; flex-wrap: wrap; }
.job-dates { display: flex; gap: 16px; color: var(--text-muted); font-size: 12px; background: var(--bg-canvas); padding: 8px 12px; border-radius: 4px; border: 1px solid var(--border-color); flex-wrap: wrap;}
.deadline-text { color: var(--pastel-red-text); font-weight: 500; }
.job-desc { color: var(--text-primary); font-size: 14px; line-height: 1.6; margin-bottom: 16px; flex: 1; }
.job-desc.collapsed { display: -webkit-box; -webkit-line-clamp: 4; -webkit-box-orient: vertical; overflow: hidden; text-overflow: ellipsis; }
.loading { text-align: center; padding: 64px; color: var(--text-muted); font-family: 'Newsreader', serif; font-style: italic; font-size: 1.2rem; }

/* Skeleton */
.skeleton {
  background: linear-gradient(90deg, var(--border-color) 25%, var(--bg-surface) 50%, var(--border-color) 75%);
  background-size: 200% 100%;
  animation: loading-skeleton 1.5s infinite;
  border-radius: 4px;
}
@keyframes loading-skeleton {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.skeleton-title { height: 24px; width: 70%; margin-bottom: 12px; }
.skeleton-badge-row { display: flex; gap: 6px; margin-bottom: 12px; }
.skeleton-badge { height: 20px; width: 60px; border-radius: 12px; }
.skeleton-meta { height: 16px; width: 50%; margin-bottom: 12px; }
.skeleton-source { height: 12px; width: 80%; margin-bottom: 12px; }
.skeleton-dates { height: 32px; width: 100%; border-radius: 4px; margin-bottom: 16px; }
.skeleton-desc { height: 14px; width: 100%; margin-bottom: 8px; }
.skeleton-button { height: 32px; width: 120px; border-radius: 6px; margin-top: auto; }
.skeleton-card { gap: 0; min-height: 380px; }

/* Spinner */
.spinner {
  animation: spin 1s linear infinite;
}
.spinner-circle {
  stroke-dasharray: 60;
  stroke-dashoffset: 60;
  animation: dash 1.5s ease-in-out infinite;
}
@keyframes spin {
  100% { transform: rotate(360deg); }
}
@keyframes dash {
  0% { stroke-dasharray: 1, 200; stroke-dashoffset: 0; }
  50% { stroke-dasharray: 40, 200; stroke-dashoffset: -20px; }
  100% { stroke-dasharray: 40, 200; stroke-dashoffset: -60px; }
}
</style>
