<template>
  <div class="page">
    <h1 class="page-title stagger-1">CV Analyzer</h1>

    <div class="card stagger-2" style="margin-bottom: 24px;">
      <div class="form-group" style="margin-bottom: 0;">
        <label>Upload CV (PDF Only)</label>
        <div style="display: flex; gap: 12px; align-items: center; margin-top: 8px;">
          <input type="file" accept=".pdf" @change="onFileChange" style="flex: 1;" />
          <button class="btn btn-primary" @click="analyze" :disabled="analyzing || !file" style="padding: 12px 24px;">
            {{ analyzing ? 'Analyzing...' : 'Analyze Document' }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="result" class="card result-card stagger-3">
      <h2 style="font-family: 'Newsreader', serif; font-weight: 400; font-size: 1.5rem; margin-bottom: 24px;">Analysis Report</h2>

      <div class="ats-status" :style="{ background: result.ats.isATS ? 'var(--pastel-green-bg)' : 'var(--pastel-red-bg)', color: result.ats.isATS ? 'var(--pastel-green-text)' : 'var(--pastel-red-text)' }">
        <span style="font-weight: 600;">{{ result.ats.isATS ? 'ATS Compatible' : 'Not ATS Compatible' }}</span>
        <span class="mono" style="font-size: 12px;">Score: {{ result.ats.score }}% ({{ result.ats.matchedSections.length }}/{{ result.ats.totalSections }})</span>
      </div>

      <div v-if="!result.eligible" class="warning" style="background: var(--pastel-yellow-bg); color: var(--pastel-yellow-text); padding: 16px; border-radius: 4px; margin-bottom: 24px; font-size: 14px;">
        {{ result.message || 'CV is not ATS compatible. Please reformat your document to proceed with deep analysis.' }}
      </div>

      <div v-if="result.analysis && result.eligible" class="analysis-content">
        <div v-html="result.analysis"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import axios from "axios"

const file = ref(null)
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
    // No expertise selected by user, sending generic to let AI figure it out or just general analysis
    form.append("expertise", "General/Specific to the CV content")
    form.append("cv", file.value)
    
    const { data } = await axios.post("/api/cv/analyze", form)
    
    if (data.analysis) {
        let cleanHtml = data.analysis
            .replace(/```html\n?/g, "")
            .replace(/```\n?/g, "")
            .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
        data.analysis = cleanHtml
    }
    
    result.value = data
  } catch (e) {
    const msg = e.response?.data?.error || e.message
    result.value = { 
      ats: { isATS: false, score: 0, matchedSections: [], totalSections: 0 }, 
      eligible: false, 
      message: msg 
    }
  } finally {
    analyzing.value = false
  }
}
</script>

<style scoped>
.ats-status { padding: 16px 20px; border-radius: 4px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; border: 1px solid var(--border-color); }
.analysis-content { font-family: inherit; font-size: 14px; line-height: 1.7; color: var(--text-primary); }
.analysis-content :deep(table) { margin: 32px 0; }
.analysis-content :deep(h1), .analysis-content :deep(h2), .analysis-content :deep(h3) { margin-top: 32px; margin-bottom: 16px; font-family: 'Newsreader', serif; font-weight: 400; color: #000; }
.analysis-content :deep(p) { margin-bottom: 16px; }
.analysis-content :deep(ul), .analysis-content :deep(ol) { margin-bottom: 16px; padding-left: 20px; }
.analysis-content :deep(li) { margin-bottom: 8px; }
</style>
