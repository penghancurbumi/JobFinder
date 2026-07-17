<template>
  <div class="page" style="padding-top: var(--spacing-section);">
    <div class="container">
      <div class="header-action stagger-1" style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: var(--spacing-xl); padding-bottom: var(--spacing-lg); border-bottom: 1px solid var(--color-hairline-soft);">
        <div>
          <span class="mono-eyebrow">Eksplorasi</span>
          <h1 class="display-md" style="margin-bottom: 0;">Daftar Pekerjaan & Magang</h1>
        </div>
        <button @click="requestScrape" class="btn btn-primary-on-light" :disabled="isScraping" style="display: flex; align-items: center; gap: 8px;">
          <svg v-if="isScraping" class="spinner" viewBox="0 0 24 24" width="16" height="16">
            <circle class="spinner-circle" cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"></circle>
          </svg>
          {{ isScraping ? 'Mencari Data Baru...' : 'Perbarui Data (Scrape)' }}
        </button>
      </div>

      <div class="grid stagger-2" style="grid-template-columns: 280px 1fr; align-items: start;">
        <!-- Filter Sidebar -->
        <aside class="card" style="position: sticky; top: 100px; padding: var(--spacing-lg);">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--spacing-lg);">
            <h3 class="heading-sm">Filter</h3>
            <button @click="resetFilters" class="btn btn-ghost-dark" style="color: var(--color-brand); padding: 0;">Reset</button>
          </div>

          <div class="filter-group">
            <label>Pencarian Kata Kunci</label>
            <input type="text" v-model="searchQuery" placeholder="Software, UI/UX, Sales..." style="margin-bottom: var(--spacing-lg);" />
          </div>
          
          <div class="filter-group">
            <label>Lokasi</label>
            <input type="text" v-model="locationQuery" placeholder="Jakarta, Remote, Bali..." style="margin-bottom: var(--spacing-lg);" />
          </div>

          <div class="filter-group">
            <label>Tipe Pekerjaan</label>
            <select v-model="activeTipe" style="margin-bottom: var(--spacing-lg);">
              <option value="all">Semua Tipe</option>
              <option value="fulltime">Full-time</option>
              <option value="parttime">Part-time</option>
              <option value="contract">Contract</option>
              <option value="freelance">Freelance</option>
              <option value="intern">Internship</option>
              <option value="remote">Remote</option>
              <option value="hybrid">Hybrid</option>
              <option value="onsite">On-site</option>
            </select>
          </div>

          <div class="filter-group">
            <label>Tingkat Pengalaman</label>
            <select v-model="experienceLevel" style="margin-bottom: var(--spacing-lg);">
              <option value="all">Semua Pengalaman</option>
              <option value="entry">Entry Level / Junior</option>
              <option value="mid">Mid Level</option>
              <option value="senior">Senior Level</option>
              <option value="manager">Manager / Director</option>
            </select>
          </div>

          <div class="filter-group">
            <label>Rentang Gaji</label>
            <label style="display: flex; align-items: center; gap: 8px; font-weight: normal; font-size: 14px; text-transform: none; cursor: pointer;">
              <input type="checkbox" v-model="hasSalary" style="width: 16px; height: 16px;" />
              Hanya tampilkan yang mencantumkan gaji
            </label>
          </div>

          <div class="filter-group" style="margin-top: var(--spacing-xl);">
            <label>Urutkan Berdasarkan</label>
            <select v-model="sortBy">
              <option value="newest">Terbaru</option>
              <option value="oldest">Terlama</option>
              <option value="az">Abjad (A - Z)</option>
              <option value="za">Abjad (Z - A)</option>
            </select>
          </div>
        </aside>

        <!-- Main Content -->
        <main>
          <div v-if="loading" class="grid grid-2 stagger-3">
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

          <div v-else-if="jobs.length === 0" class="card stagger-3" style="text-align:center; padding: 64px; border: 1px dashed var(--color-hairline);">
            <p class="subtitle" style="color: var(--color-mute); font-style: italic;">Tidak ada peluang yang sesuai dengan filter.</p>
            <button @click="resetFilters" class="btn btn-outline" style="margin-top: var(--spacing-lg);">Reset Filter</button>
          </div>

          <div v-else class="grid grid-2 stagger-3">
            <div v-for="job in jobs" :key="job.title + job.company + job.id" class="card job-card" style="display: flex; flex-direction: column; gap: var(--spacing-sm);">
              <div class="job-header">
                <h3 class="heading-sm">{{ job.title }}</h3>
                <div class="job-badges">
                  <span class="badge-filled" style="background: var(--color-canvas-soft); color: var(--color-on-primary);">
                    {{ job.jobType.charAt(0).toUpperCase() + job.jobType.slice(1) }}
                  </span>
                  <span class="badge-neutral" style="background: rgba(243, 100, 88, 0.1); color: var(--color-brand); border: 1px solid rgba(243, 100, 88, 0.2);">{{ job.expertise }}</span>
                </div>
              </div>
              
              <div class="job-meta" style="display: flex; gap: var(--spacing-sm); font-size: 14px; flex-wrap: wrap;">
                <strong style="color: var(--color-on-primary);">{{ job.company }}</strong>
                <span style="color: var(--color-mute);">•</span>
                <span style="color: var(--color-ash);">{{ job.location || 'Lokasi tidak disebutkan' }}</span>
              </div>
              
              <div class="meta" style="color: var(--color-mute); word-break: break-all;">
                Sumber: <a :href="job.url" target="_blank" style="color: var(--color-link-blue); text-decoration: none;">{{ job.source }}</a>
              </div>

              <div class="job-dates" v-if="job.postedDate || job.deadlineDate || job.salary" style="display: flex; flex-wrap: wrap; gap: var(--spacing-sm); background: var(--color-canvas); padding: var(--spacing-sm); border-radius: var(--rounded-app-md); margin-top: var(--spacing-xs);">
                 <span v-if="job.postedDate" class="meta" style="color: var(--color-ash);">Diposting: {{ job.postedDate }}</span>
                 <span v-if="job.deadlineDate" class="meta" style="color: var(--color-error); font-weight: 500;">Batas Waktu: {{ job.deadlineDate }}</span>
                 <span v-if="job.salary" class="meta" style="color: var(--color-success); font-weight: 500; width: 100%;">Gaji: {{ job.salary }}</span>
              </div>
              
              <div class="job-desc-container" style="margin-top: var(--spacing-sm); flex: 1; display: flex; flex-direction: column;">
                <p :class="['job-desc', { 'collapsed': !isExpanded(job) }]" class="body-sm" style="color: var(--color-ash); white-space: pre-wrap; margin-bottom: var(--spacing-xs);">{{ job.description }}</p>
                <button v-if="needsTruncation(job.description)" 
                        @click="toggleExpand(job)" 
                        class="meta" style="padding: 0; color: var(--color-link-blue); font-weight: 500; cursor: pointer; background: none; border: none; text-align: left; margin-bottom: var(--spacing-md);">
                  {{ isExpanded(job) ? 'Tampilkan Lebih Sedikit' : 'Selengkapnya' }}
                </button>
              </div>
              
              <a :href="job.url" target="_blank" class="btn btn-primary-on-light" style="align-self: flex-start; margin-top: auto; padding: 0 var(--spacing-lg); height: 36px; font-size: 14px;">Lamar Sekarang</a>
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

<style scoped>
.filter-group label {
  color: var(--color-mute);
}

.job-badges { display: flex; gap: 6px; flex-shrink: 0; flex-wrap: wrap; margin-top: 8px; }

.job-card {
  height: 420px;
}

.job-desc.collapsed { 
  display: -webkit-box; 
  -webkit-line-clamp: 3; 
  -webkit-box-orient: vertical; 
  overflow: hidden; 
  text-overflow: ellipsis; 
}

/* Skeleton */
.skeleton {
  background: linear-gradient(90deg, var(--color-hairline) 25%, var(--color-canvas-light) 50%, var(--color-hairline) 75%);
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

@media (max-width: 960px) {
  .grid[style*="grid-template-columns: 280px"] {
    grid-template-columns: 1fr !important;
  }
  aside {
    position: static !important;
    margin-bottom: var(--spacing-lg);
  }
}
@media (max-width: 768px) {
  .header-action {
    flex-direction: column;
    align-items: flex-start !important;
    gap: var(--spacing-md);
  }
}
</style>
