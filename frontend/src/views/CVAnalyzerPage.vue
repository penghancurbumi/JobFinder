<template>
  <div class="page">
    <div class="container" style="max-width: 1200px;">
      <span class="mono-eyebrow stagger-1" style="color: var(--color-mute); margin-bottom: var(--spacing-xs); display: block;">ATS Simulator</span>
      <h1 class="display-md stagger-1" style="margin-bottom: var(--spacing-sm);">CV Analyzer</h1>
      <p class="subtitle stagger-1" style="color: var(--color-mute); margin-bottom: var(--spacing-xl);">Unggah CV Anda untuk mendapatkan analisis mendalam berbasis AI dan simulasi sistem ATS.</p>

      <div class="card stagger-2" style="margin-bottom: var(--spacing-xl);">
        <div style="margin-bottom: var(--spacing-md);">
          <label style="margin-bottom: var(--spacing-xs); display: block; font-weight: 500;">Unggah Dokumen CV (PDF)</label>
          <div style="display: flex; gap: var(--spacing-md); align-items: center;">
            <input type="file" accept=".pdf" @change="onFileChange" style="flex: 1;" />
            
            <div style="flex: 1;">
              <select v-model="targetExpertise">
                <option value="Software Engineer">Software Engineer</option>
                <option value="Data Scientist">Data Scientist</option>
                <option value="Product Manager">Product Manager</option>
                <option value="UI/UX Designer">UI/UX Designer</option>
                <option value="Digital Marketing">Digital Marketing</option>
                <option value="General">General / Belum Yakin</option>
              </select>
            </div>

            <button class="btn btn-brand" @click="analyze" :disabled="analyzing || !file" style="white-space: nowrap; height: 44px;">
              {{ analyzing ? 'Menganalisis...' : 'Analisis Dokumen' }}
            </button>
          </div>
        </div>
      </div>

      <div v-if="result" class="stagger-3">
        <h2 class="heading-md" style="margin-bottom: var(--spacing-lg);">Laporan Analisis</h2>

        <!-- Error Handling -->
        <div v-if="result.analysis?.error" class="card" style="background: var(--color-error); color: white; margin-bottom: var(--spacing-lg);">
          Gagal menganalisis CV: {{ result.analysis.message }}
        </div>

        <template v-else>
          <!-- Score Summary -->
          <div class="grid grid-2" style="margin-bottom: var(--spacing-lg);">
            <div class="card" style="display: flex; align-items: center; gap: var(--spacing-lg);">
              <div style="width: 120px; height: 120px;">
                <Doughnut :data="overallChartData" :options="doughnutOptions" />
              </div>
              <div>
                <span class="mono-eyebrow">Overall Score</span>
                <h3 class="display-sm" style="margin: 0; color: var(--color-brand);">{{ result.analysis.overallScore || 0 }}<span style="font-size: 24px;">/100</span></h3>
                <p class="meta" style="color: var(--color-mute);">Kecocokan dengan posisi {{ targetExpertise }}</p>
              </div>
            </div>
            
            <div class="card" style="display: flex; align-items: center; gap: var(--spacing-lg);">
              <div style="width: 120px; height: 120px;">
                <Doughnut :data="atsChartData" :options="doughnutOptions" />
              </div>
              <div>
                <span class="mono-eyebrow">ATS Score</span>
                <h3 class="display-sm" style="margin: 0;" :style="{ color: result.ats.isATS ? 'var(--color-success)' : 'var(--color-error)' }">{{ result.ats.score }}<span style="font-size: 24px;">%</span></h3>
                <span class="badge-neutral" :style="{ background: result.ats.isATS ? 'rgba(55,205,132,0.1)' : 'rgba(221,0,0,0.1)', color: result.ats.isATS ? 'var(--color-success)' : 'var(--color-error)', border: 'none' }">
                  {{ result.ats.isATS ? 'Format ATS Valid' : 'Format ATS Kurang' }}
                </span>
                <p class="meta" style="color: var(--color-mute); margin-top: 4px;">{{ result.ats.matchedSections.length }} / {{ result.ats.totalSections }} bagian wajib ditemukan</p>
              </div>
            </div>
          </div>

          <!-- Summary -->
          <div class="card" style="margin-bottom: var(--spacing-lg);">
            <span class="mono-eyebrow">Resume Summary</span>
            <p class="body" style="color: var(--color-graphite);">{{ result.analysis.summary }}</p>
          </div>

          <!-- Charts Dashboard -->
          <div class="grid grid-2" style="margin-bottom: var(--spacing-lg);">
            <div class="card">
              <span class="mono-eyebrow" style="margin-bottom: var(--spacing-lg); display: block;">Analisis Kategori (Radar)</span>
              <div style="position: relative; height: 300px; width: 100%; display: flex; justify-content: center;">
                <Radar :data="radarChartData" :options="radarOptions" />
              </div>
            </div>
            <div class="card">
              <span class="mono-eyebrow" style="margin-bottom: var(--spacing-lg); display: block;">Performa per Aspek (Bar)</span>
              <div style="position: relative; height: 300px; width: 100%;">
                <Bar :data="barChartData" :options="barOptions" />
              </div>
            </div>
          </div>

          <!-- Detailed Insights -->
          <div class="bento-grid" style="margin-bottom: var(--spacing-lg);">
            <div class="card" style="border-top: 4px solid var(--color-success);">
              <span class="mono-eyebrow" style="color: var(--color-success);">Kekuatan (Strengths)</span>
              <ul style="padding-left: 20px; color: var(--color-graphite);" class="body-sm">
                <li v-for="(item, idx) in result.analysis.strengths" :key="'s'+idx" style="margin-bottom: 8px;">{{ item }}</li>
              </ul>
            </div>
            
            <div class="card" style="border-top: 4px solid var(--color-error);">
              <span class="mono-eyebrow" style="color: var(--color-error);">Kelemahan (Weaknesses)</span>
              <ul style="padding-left: 20px; color: var(--color-graphite);" class="body-sm">
                <li v-for="(item, idx) in result.analysis.weaknesses" :key="'w'+idx" style="margin-bottom: 8px;">{{ item }}</li>
              </ul>
            </div>
          </div>

          <div class="grid grid-2" style="margin-bottom: var(--spacing-lg);">
            <div class="card">
              <span class="mono-eyebrow">Keyword Match</span>
              <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px;">
                <span v-for="(kw, idx) in result.analysis.keywordMatch" :key="'kw'+idx" class="badge-neutral" style="background: rgba(55,205,132,0.1); color: var(--color-success); border: 1px solid rgba(55,205,132,0.3);">
                  ✓ {{ kw }}
                </span>
                <span v-if="!result.analysis.keywordMatch || result.analysis.keywordMatch.length === 0" class="meta" style="color: var(--color-mute);">Tidak ada keyword yang cocok.</span>
              </div>
            </div>
            
            <div class="card">
              <span class="mono-eyebrow">Missing Skills</span>
              <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px;">
                <span v-for="(kw, idx) in result.analysis.missingSkills" :key="'mk'+idx" class="badge-neutral" style="background: rgba(221,0,0,0.05); color: var(--color-error); border: 1px solid rgba(221,0,0,0.2);">
                  ✗ {{ kw }}
                </span>
                <span v-if="!result.analysis.missingSkills || result.analysis.missingSkills.length === 0" class="meta" style="color: var(--color-mute);">Tidak ada skill yang terlewat. Bagus!</span>
              </div>
            </div>
          </div>

          <!-- Recommendations -->
          <div class="card" style="background: var(--color-canvas); color: var(--color-on-primary);">
            <span class="mono-eyebrow" style="color: var(--color-mute);">Rekomendasi AI</span>
            <ul style="padding-left: 20px; margin-top: 16px;" class="body">
              <li v-for="(rec, idx) in result.analysis.recommendations" :key="'r'+idx" style="margin-bottom: 12px; color: var(--color-ash);">
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
import { ref, computed } from "vue"
import axios from "axios"
import { Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend, Title, BarElement, CategoryScale, LinearScale, ArcElement } from 'chart.js'
import { Radar, Bar, Doughnut } from 'vue-chartjs'

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend, Title, BarElement, CategoryScale, LinearScale, ArcElement)

const file = ref(null)
const targetExpertise = ref("Software Engineer")
const analyzing = ref(false)
const result = ref(null)

function onFileChange(e) {
  file.value = e.target.files[0]
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

// Chart Configurations
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
      backgroundColor: ['#f36458', '#ededed'],
      borderWidth: 0
    }]
  }
})

const atsChartData = computed(() => {
  const score = result.value?.ats?.score || 0
  const color = score >= 25 ? '#37cd84' : '#dd0000'
  return {
    labels: ['Score', 'Remaining'],
    datasets: [{
      data: [score, 100 - score],
      backgroundColor: [color, '#ededed'],
      borderWidth: 0
    }]
  }
})

const radarOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    r: {
      min: 0, max: 100,
      ticks: { display: false },
      pointLabels: { font: { family: 'IBM Plex Mono', size: 11 } }
    }
  },
  plugins: { legend: { display: false } }
}

const radarChartData = computed(() => {
  const cats = result.value?.analysis?.categories || {}
  return {
    labels: ['Skills', 'Experience', 'Education', 'Projects', 'Certificates', 'Soft Skills'],
    datasets: [{
      label: 'Kategori',
      data: [cats.Skills||0, cats.Experience||0, cats.Education||0, cats.Projects||0, cats.Certificates||0, cats.SoftSkills||0],
      backgroundColor: 'rgba(243, 100, 88, 0.2)',
      borderColor: '#f36458',
      pointBackgroundColor: '#dd0000',
    }]
  }
})

const barOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: { y: { min: 0, max: 100 } },
  plugins: { legend: { display: false } }
}

const barChartData = computed(() => {
  const cats = result.value?.analysis?.categories || {}
  return {
    labels: ['Skills', 'Exp', 'Edu', 'Proj', 'Cert', 'Soft'],
    datasets: [{
      data: [cats.Skills||0, cats.Experience||0, cats.Education||0, cats.Projects||0, cats.Certificates||0, cats.SoftSkills||0],
      backgroundColor: '#0b0b0b',
      borderRadius: 4
    }]
  }
})
</script>

<style scoped>
</style>
