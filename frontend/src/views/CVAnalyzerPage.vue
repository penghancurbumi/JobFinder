<template>
  <div class="min-h-screen pt-[50px] md:pt-[88px] bg-canvas-dark text-on-dark font-sans">
    <div class="w-full mx-auto px-[32px] md:px-[72px]">
      <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-stone mb-xs block">ATS Simulator</span>
      <h1 class="text-[32px] md:text-[40px] font-medium leading-[1.2] tracking-[-0.4px] mb-sm text-on-dark">CV Analyzer</h1>
      <p class="text-[12px] md:text-[16px] font-normal leading-[1.56] tracking-[-0.09px] text-on-dark-mute mb-xl">Unggah CV Anda untuk mendapatkan analisis mendalam berbasis AI dan simulasi sistem ATS.</p>

      <div class="bg-surface-elevated border border-hairline-dark rounded-[20px] p-xxl mb-xl">
        <div class="mb-md gap-sm">
          <label class="mb-lg block text-on-dark font-medium text-lg">Unggah Dokumen CV (PDF)</label>
          <div class="flex gap-md items-center flex-wrap">
            
            <div class="relative flex-1 min-w-[200px] h-[200px]">
              <label
                class="absolute inset-0 bg-surface-elevated border-2 border-dashed border-hairline-dark rounded-sm flex items-center justify-center px-4 cursor-pointer hover:bg-surface-elevated"
              >
                <input
                  ref="fileInput"
                  type="file"
                  accept=".pdf"
                  @change="onFileChange"
                  class="hidden"
                />

                <div class="flex flex-col gap-2 items-center">
                  <Icon icon="material-symbols:upload-file" width="35"/>

                  <div class="flex flex-col items-center gap-0">
                    <span class="text-sm text-on-dark">
                      Pilih file PDF
                    </span>

                    <span class="text-[10px] text-on-dark-mute font-normal">Drag & drop atau klik untuk memilih file</span>
                  </div>
                </div>

              </label>
            </div>

            <div v-if="file" class="flex-1 min-w-[200px] border border-hairline-dark rounded-sm">
              <div class="flex flex-row gap-2 items-center p-md">
                <Icon icon="mdi:file" width="30" class="text-on-dark-mute"/>
                
               <div class="flex flex-col flex-1 justify-center min-w-0">
                <div class="w-full flex items-center justify-between">
                  <span class="text-[12px] font-medium text-on-dark truncate"
                  :title="file.name">
                    {{ file.name }}
                  </span>

                  <button
                    type="button"
                    @click="removeFile"
                    class="flex items-center justify-center text-on-dark-mute hover:text-white transition"
                  >
                    <Icon icon="lucide:x" width="15" />
                  </button>
                </div>

                <span class="text-[10px] text-on-dark-mute font-mono">
                  <template v-if="uploadProgress < 100">
                    {{ formatFileSize(uploadedBytes) }} of {{ formatFileSize(file.size) }}
                  </template>

                  <template v-else>
                    {{ formatFileSize(file.size) }}
                  </template>
                </span>

                <div v-if="uploadProgress < 100" class="w-full bg-white/10 h-[2px] rounded-full overflow-hidden mt-1">
                  <div 
                    class="bg-white h-full transition-all duration-100 ease-out"
                    :style="{ width: `${uploadProgress}%` }"
                  ></div>
                </div>   
                          
               </div>
              </div>
            </div>

            <CustomSelect
              label="Pilih Bidang Keahlian"
              :options="ExpertiseOptions"
              v-model="targetExpertise"
              class="flex-1 min-w-[200px]"
              />

            <button class="inline-flex items-center justify-center font-medium rounded-full transition-all duration-200 cursor-pointer bg-on-dark text-ink hover:bg-white/90 px-[24px] h-[48px] text-[14px] md:text-[16px] whitespace-nowrap disabled:opacity-50 disabled:cursor-not-allowed" @click="analyze" :disabled="analyzing || !file">
              {{ analyzing ? 'Menganalisis...' : 'Analisis Dokumen' }}
            </button>
          </div>
        </div>
      </div>

      <div v-if="result" class="animate-fade-in">
        <h2 class="text-[24px] font-medium leading-[1.33] tracking-[0] mb-xl text-on-dark">Laporan Analisis</h2>

        <!-- Error Handling -->
        <div v-if="result.analysis?.error" class="bg-accent-danger text-white rounded-[20px] p-xxl mb-xl">
          Gagal menganalisis CV: {{ result.analysis.message }}
        </div>

        <template v-else>
          <!-- Score Summary -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-xl mb-xl">
            <div class="bg-surface-elevated rounded-[20px] p-xxl flex items-center gap-xl">
              <div class="w-[120px] h-[120px] shrink-0 relative">
                <Doughnut :data="overallChartData" :options="doughnutOptions" />
              </div>
              <div>
                <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-stone">Overall Score</span>
                <h3 class="text-[32px] font-medium leading-[1.19] tracking-[-0.32px] m-0 text-white">{{ result.analysis.overallScore || 0 }}<span class="text-[20px] text-on-dark-mute">/100</span></h3>
                <p class="text-[14px] font-normal leading-[1.5] text-on-dark-mute mt-[4px]">Kecocokan dengan posisi {{ targetExpertise }}</p>
              </div>
            </div>
            
            <div class="bg-surface-elevated rounded-[20px] p-xxl flex items-center gap-xl">
              <div class="w-[120px] h-[120px] shrink-0 relative">
                <Doughnut :data="atsChartData" :options="doughnutOptions" />
              </div>
              
              <div>
                <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-stone">ATS Score</span>
                <h3 class="text-[32px] font-medium leading-[1.19] tracking-[-0.32px] m-0" :class="result.ats.isATS ? 'text-accent-teal' : 'text-accent-danger'">{{ result.ats.score }}<span class="text-[20px] text-on-dark-mute">%</span></h3>
                <span class="inline-block rounded-full text-[13px] font-medium mt-[4px]" :class="result.ats.isATS ? 'text-accent-teal' : 'text-accent-danger'">
                  {{ result.ats.isATS ? 'Format ATS Valid' : 'Format ATS Kurang' }}
                </span>
                <p class="text-[14px] font-normal leading-[1.5] text-on-dark-mute mt-[4px]">{{ result.ats.matchedSections.length }} / {{ result.ats.totalSections }} bagian wajib ditemukan</p>
              </div>
            </div>
          </div>

          <!-- Charts Dashboard -->
          <div class="bg-surface-elevated rounded-[20px] p-xxl mb-xl">
            <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] mb-lg block text-stone">Analisis Kategori (Line Chart)</span>
            <div class="relative h-[300px] w-full">
              <Line :data="lineChartData" :options="lineOptions" />
            </div>
          </div>

          <!-- Summary -->
          <div class="bg-surface-elevated rounded-[20px] p-xxl mb-xl">
            <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-stone">Resume Summary</span>
            <p class="text-[16px] font-normal leading-[1.6] text-on-dark-mute mt-sm">{{ result.analysis.summary }}</p>
          </div>
          
          <!-- Detailed Insights -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-xl mb-xl">
            <div class="bg-surface-elevated rounded-[20px] p-xxl border-t-3 border-accent-teal">
              <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-stone">Kekuatan (Strengths)</span>
              <ul class="pl-[20px] mt-md text-[14px] font-normal leading-[1.5] list-disc">
                <li v-for="(item, idx) in result.analysis.strengths" :key="'s'+idx" class="mb-[8px] text-on-dark-mute">{{ item }}</li>
              </ul>
            </div>
            
            <div class="bg-surface-elevated rounded-[20px] p-xxl border-t-3 border-accent-danger">
              <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-stone">Kelemahan (Weaknesses)</span>
              <ul class="pl-[20px] mt-md text-[14px] font-normal leading-[1.5] list-disc">
                <li v-for="(item, idx) in result.analysis.weaknesses" :key="'w'+idx" class="mb-[8px] text-on-dark-mute">{{ item }}</li>
              </ul>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-xl mb-xl">
            <div class="bg-surface-elevated rounded-[20px] p-xxl">
              <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-stone">Keyword Match</span>
              <div class="flex flex-wrap gap-[8px] mt-[12px]">
                <span v-for="(kw, idx) in result.analysis.keywordMatch" :key="'kw'+idx" class="inline-flex items-center gap-[6px] bg-gray/10 text-white border border-white/25 rounded-full px-[12px] py-[4px] text-[13px]">
                  <span class="inline-block rounded-full bg-white w-[4px] h-[4px]"></span> {{ kw }}
                </span>
                <span v-if="!result.analysis.keywordMatch || result.analysis.keywordMatch.length === 0" class="text-[14px] font-normal leading-[1.5] text-stone">Tidak ada keyword yang cocok.</span>
              </div>
            </div>
            
            <div class="bg-surface-elevated rounded-[20px] p-xxl">
              <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-stone">Missing Skills</span>
              <div class="flex flex-wrap gap-[8px] mt-[12px]">
                <span v-for="(kw, idx) in result.analysis.missingSkills" :key="'mk'+idx" class="inline-flex items-center gap-[6px] bg-gray/10 text-white border border-white/25 rounded-full px-[12px] py-[4px] text-[13px]">
                  <span class="inline-block rounded-full bg-white w-[4px] h-[4px]"></span> {{ kw }}
                </span>
                <span v-if="!result.analysis.missingSkills || result.analysis.missingSkills.length === 0" class="text-[14px] font-normal leading-[1.5] text-stone">Tidak ada skill yang terlewat. Bagus!</span>
              </div>
            </div>
          </div>

          <!-- Recommendations -->
          <div class="bg-surface-elevated rounded-[20px] p-xxl border-l-3 border-primary">
            <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-stone">Rekomendasi AI</span>
            <ul class="pl-[20px] mt-md text-[14px] font-normal leading-[1.6] list-disc">
              <li v-for="(rec, idx) in result.analysis.recommendations" :key="'r'+idx" class="mb-[12px] text-on-dark-mute">
                {{ rec }}
              </li>
            </ul>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import axios from "axios"
import { Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend, Title, BarElement, CategoryScale, LinearScale, ArcElement } from 'chart.js'
import { Line, Doughnut } from 'vue-chartjs'
import CustomSelect from "../components/CustomSelect.vue"
import { useHead } from "@vueuse/head"
import { Icon } from "@iconify/vue"

useHead({
  title: 'Analisis CV & ATS Score — JobFinder',
  meta: [
    { name: 'description', content: 'Unggah CV Anda dan dapatkan analisis mendalam berbasis AI. Simulasikan skor ATS, temukan kelemahan CV, dan dapatkan rekomendasi perbaikan yang spesifik untuk bidang keahlianmu.' },
    { property: 'og:title', content: 'Analisis CV & ATS Score — JobFinder' },
    { property: 'og:description', content: 'Simulasi ATS dan analisis CV berbasis AI untuk pencari kerja Indonesia.' },
  ]
})

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend, Title, BarElement, CategoryScale, LinearScale, ArcElement)

// Expertise areas diambil dari API agar selalu sinkron dengan backend
const expertiseAreas = ref([])
const ExpertiseOptions = computed(() => [
  { value: '', label: 'Pilih Bidang Keahlian' },
  ...expertiseAreas.value.map(a => ({ value: a, label: a }))
])

const file = ref(null)
const targetExpertise = ref('')
const analyzing = ref(false)
const result = ref(null)

const FALLBACK_AREAS = ['IT Infra', 'Graphic Design', 'Software Development', 'Data Science', 'UI/UX Design', 'Digital Marketing', 'Content Writing', 'Mobile Development', 'DevOps', 'Cyber Security', 'AI / Machine Learning', 'Product Management', 'Others']

onMounted(async () => {
  try {
    const { data } = await axios.get('/api/expertise-areas')
    expertiseAreas.value = data
  } catch {
    expertiseAreas.value = FALLBACK_AREAS
  }
})

function onFileChange(e) {
  const selected = e.target.files[0]
  if (selected) {
    file.value = selected
    simulateUpload(selected.size)
  }
}

async function analyze() {
  if (!file.value) return
  analyzing.value = true
  result.value = null
  try {
    const form = new FormData()
    form.append("expertise", targetExpertise.value)
    form.append("cv", file.value)
    
    const { data } = await axios.post("/api/cv/analyze", form)
    result.value = data
  } catch (e) {
    const msg = e.response?.data?.error || e.message
    result.value = { 
      ats: { isATS: false, score: 0, matchedSections: [], totalSections: 0 }, 
      eligible: false, 
      analysis: { error: true, message: msg }
    }
  } finally {
    analyzing.value = false
  }
}

// Chart Configurations — cobalt violet palette
const doughnutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '75%',
  plugins: { legend: { display: false }, tooltip: { enabled: false } }
}

const overallChartData = computed(() => {
  const score = result.value?.analysis?.overallScore || 0
  return {
    labels: ['Score', 'Remaining'],
    datasets: [{
      data: [score, 100 - score],
      backgroundColor: ['#ffffff', 'rgba(255,255,255,0.08)'],
      borderWidth: 0
    }]
  }
})

const atsChartData = computed(() => {
  const score = result.value?.ats?.score || 0
  const color = score >= 25 ? '#00a87e' : '#e23b4a'
  return {
    labels: ['Score', 'Remaining'],
    datasets: [{
      data: [score, 100 - score],
      backgroundColor: [color, 'rgba(255,255,255,0.08)'],
      borderWidth: 0
    }]
  }
})

const lineOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: { 
    y: { min: 0, max: 100, ticks: { color: '#8d969e' }, grid: { color: 'rgba(255,255,255,0.06)' } },
    x: { ticks: { color: '#8d969e' }, grid: { display: false } }
  },
  plugins: { legend: { display: false } }
}

const lineChartData = computed(() => {
  const cats = result.value?.analysis?.categories || {}
  return {
    labels: ['Skills', 'Experience', 'Education', 'Projects', 'Certificates', 'Soft Skills'],
    datasets: [{
      label: 'Skor Kategori',
      data: [cats.Skills||0, cats.Experience||0, cats.Education||0, cats.Projects||0, cats.Certificates||0, cats.SoftSkills||0],
      borderColor: '#ffffff',
      backgroundColor: 'rgba(90, 90, 90, 0.3)',
      pointBackgroundColor: '#ffffff',
      fill: true,
      tension: 0.4
    }]
  }
})

const fileInput = ref(null)
const uploadProgress = ref(0)
const uploadedBytes = ref(0)
let uploadTimer = null

function simulateUpload(totalSize) {
  if (uploadTimer) clearInterval(uploadTimer)
  uploadProgress.value = 0
  uploadedBytes.value = 0
  
  const duration = 750 // 750ms animasi halus
  const interval = 25  // pembaruan tiap 25ms
  const steps = duration / interval
  const byteIncrement = totalSize / steps
  const percentIncrement = 100 / steps
  
  uploadTimer = setInterval(() => {
    if (uploadProgress.value < 100) {
      uploadProgress.value = Math.min(100, Math.round(uploadProgress.value + percentIncrement))
      uploadedBytes.value = Math.min(totalSize, Math.round(uploadedBytes.value + byteIncrement))
    } else {
      uploadProgress.value = 100
      uploadedBytes.value = totalSize
      clearInterval(uploadTimer)
    }
  }, interval)
}

function removeFile() {
  if (uploadTimer) clearInterval(uploadTimer)
  file.value = null
  uploadProgress.value = 0
  uploadedBytes.value = 0
  if (fileInput.value) {
    fileInput.value.value = ''
  }
  result.value = null
}

function formatFileSize(bytes, decimals = 2) {
  if (!bytes || bytes <= 0) return "0 KB"
  const mb = bytes / (1024 * 1024)
  if (mb < 0.1){
    return (bytes / 1024).toFixed(0) + " KB"
  }
  return mb.toFixed(1) + " MB"
}

</script>

<style scoped>
/* Scoped styles removed because we used Tailwind */
</style>
