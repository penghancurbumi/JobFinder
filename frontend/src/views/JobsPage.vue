<template>
  <div class="page">
    <div class="header-action stagger-1">
      <h1 class="page-title" style="margin-bottom: 0;">Daftar Pekerjaan & Magang</h1>
      <button @click="requestScrape" class="btn btn-outline btn-sm" :disabled="isScraping">
        {{ isScraping ? 'Mencari Data...' : 'Perbarui Data' }}
      </button>
    </div>

    <div class="card stagger-2" style="margin-bottom: 32px; padding: 24px;">
      <div class="filter-row">
        <div class="filter-group">
          <label>Tipe</label>
          <div class="tab-group">
            <button :class="['tab', { active: activeTab === 'all' }]" @click="activeTab = 'all'">Semua</button>
            <button :class="['tab', { active: activeTab === 'intern' }]" @click="activeTab = 'intern'">Magang</button>
            <button :class="['tab', { active: activeTab === 'job' }]" @click="activeTab = 'job'">Pekerjaan</button>
          </div>
        </div>
        <div class="filter-group" style="flex: 2;">
          <label>Cari Keahlian atau Jabatan</label>
          <input type="text" v-model="searchQuery" placeholder="Contoh: Software Development, UI/UX..." />
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading stagger-3">Mengumpulkan peluang...</div>
    <div v-else-if="jobs.length === 0" class="card stagger-3" style="text-align:center;padding:64px; border-style: dashed;">
      <p style="color: var(--text-muted); font-family: 'Newsreader', serif; font-style: italic; font-size: 1.2rem;">Tidak ada peluang yang sesuai dengan filter.</p>
    </div>
    <div v-else class="bento-grid stagger-3">
      <div v-for="job in jobs" :key="job.title + job.company" class="card job-card">
        <div class="job-header">
          <h3 style="font-family: 'Newsreader', serif; font-size: 1.25rem;">{{ job.title }}</h3>
          <div class="job-badges">
            <span :class="['badge', job.jobType === 'intern' ? 'badge-intern' : 'badge-job']">
              {{ job.jobType === 'intern' ? 'Magang' : 'Pekerjaan' }}
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

        <div class="job-dates" v-if="job.postedDate || job.deadlineDate">
           <span v-if="job.postedDate">Diposting: {{ job.postedDate }}</span>
           <span v-if="job.deadlineDate" class="deadline-text">Batas Waktu: {{ job.deadlineDate }}</span>
        </div>
        
        <p class="job-desc">{{ job.description }}</p>
        
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
const activeTab = ref("all")
const searchQuery = ref("")
let socket = null

onMounted(() => {
  socket = io("http://localhost:3000")
  
  socket.on("jobs-updated", (data) => {
    jobs.value = data
    loading.value = false
  })
  
  socket.on("scrape-status", (data) => {
    isScraping.value = data.status === "scraping"
  })
})

onUnmounted(() => {
  if (socket) socket.disconnect()
})

let searchTimeout;
watch([activeTab, searchQuery], () => {
  loading.value = true
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    if (socket) {
      socket.emit("filter-jobs", { search: searchQuery.value, jobType: activeTab.value })
    }
  }, 300) // debounce
})

function requestScrape() {
  if (socket && !isScraping.value) {
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
.loading { text-align: center; padding: 64px; color: var(--text-muted); font-family: 'Newsreader', serif; font-style: italic; font-size: 1.2rem; }
</style>
