<template>
  <div class="page cv-wizard-container">
    <div class="no-print" style="margin-bottom: var(--spacing-xl);">
      <span class="mono-eyebrow stagger-1" style="color: var(--color-mute); margin-bottom: var(--spacing-sm); display: block;">Sistem Pembangun Dokumen ATS</span>
      <h1 class="display-md stagger-1">Pembuat CV</h1>
      <p class="subtitle stagger-2" style="margin-top: var(--spacing-sm); color: var(--color-ash); font-size: 14px;">Rakit bagian-bagian CV Anda langkah demi langkah. Tanda <span style="color:var(--color-error);">*</span> wajib diisi.</p>
    </div>

    <!-- Wizard Layout -->
    <div class="wizard-layout no-print">
      <!-- Sidebar Navigation -->
      <aside class="wizard-sidebar stagger-3">
        <div class="form-group" style="margin-bottom: 24px; padding: 0 16px;">
          <label style="font-size: 12px; margin-bottom: 4px;">Target Keahlian / Bidang</label>
          <select v-model="targetExpertise" style="width: 100%; font-size: 14px; padding: 6px 8px;">
            <option v-for="a in expertiseAreas" :key="a" :value="a">{{ a }}</option>
          </select>
        </div>
        
        <ul class="step-list">
          <li v-for="(section, index) in steps" :key="section.id" 
              class="step-item"
              :class="{ active: currentStep === index, completed: currentStep > index }"
              @click="goToStep(index)">
            <div class="step-indicator">{{ index + 1 }}</div>
            <div class="step-title">{{ section.title }}</div>
          </li>
          <li class="step-item"
              :class="{ active: currentStep === steps.length }" 
              @click="goToStep(steps.length)">
            <div class="step-indicator">✓</div>
            <div class="step-title">Preview & Export</div>
          </li>
        </ul>
      </aside>

      <!-- Main Content Panel -->
      <main class="wizard-content stagger-3 card">
        <!-- Active Form Section -->
        <div v-if="currentStep < steps.length" class="wizard-form-section">
          <h3 class="heading-md" style="margin-bottom: 24px;">
            {{ steps[currentStep].title }}
          </h3>
          
          <div class="section-fields">
            <div v-for="field in steps[currentStep].fields" :key="field.key" class="field-group">
              <label>
                {{ field.label }} 
                <span v-if="field.required" style="color: var(--color-error); font-weight: bold;">*</span>
                <button v-if="field.key === 'description' || field.key === 'summary' || field.key === 'technical_skills' || field.key === 'soft_skills'" class="suggestion-btn" @click.prevent="getSuggestion(field)" title="Minta saran AI">💡 AI Suggestion</button>
              </label>
              
              <input 
                v-if="field.key !== 'gpa' && field.key !== 'description' && field.key !== 'summary' && field.key !== 'email' && field.key !== 'linkedin'" 
                v-model="formData[field.key]" 
                :placeholder="field.placeholder" 
              />
              
              <input 
                v-else-if="field.key === 'email'"
                type="email"
                v-model="formData[field.key]" 
                :placeholder="field.placeholder" 
                @input="validateEmail"
              />

              <input 
                v-else-if="field.key === 'linkedin'"
                type="url"
                v-model="formData[field.key]" 
                :placeholder="field.placeholder" 
                @input="validateLinkedIn"
              />

              <input 
                v-else-if="field.key === 'gpa'"
                v-model="formData[field.key]" 
                :placeholder="field.placeholder" 
                @input="validateGPA"
              />

              <textarea 
                v-else 
                v-model="formData[field.key]" 
                :placeholder="field.placeholder"
                rows="4"
              ></textarea>
              
              <span class="hint">{{ field.hint }}</span>
              <div v-if="errors[field.key]" class="error-text">{{ errors[field.key] }}</div>
              
              <div v-if="suggestions[field.key]" class="suggestion-box">
                <span style="font-weight: 500; color: var(--text-primary);">Saran AI:</span> {{ suggestions[field.key] }}
              </div>
            </div>
          </div>

          <!-- Wizard Actions -->
          <div class="wizard-actions">
            <button class="btn btn-outline" :disabled="currentStep === 0" @click="prevStep">Sebelumnya</button>
            <button class="btn btn-primary" @click="nextStep">Selanjutnya</button>
          </div>
        </div>

        <!-- Preview Section -->
        <div v-else class="preview-step">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
            <h3 class="heading-md">Pratinjau Dokumen</h3>
            <div style="display: flex; gap: 12px;">
              <button class="btn btn-outline btn-sm" @click="analyzeBuiltCV" :disabled="analyzing">
                {{ analyzing ? 'Memindai...' : 'Scan ATS Score' }}
              </button>
              <button class="btn btn-primary btn-sm" @click="downloadPDF">
                Unduh PDF
              </button>
            </div>
          </div>
          
          <div v-if="analysisResult" style="margin-bottom: 24px; padding: 16px; border: 1px solid var(--border-color); border-radius: 8px; background: var(--bg-canvas);">
            <h4 class="heading-sm" style="margin-bottom: 12px;">Hasil Analisis AI</h4>
            <div v-html="analysisResult" class="analysis-content"></div>
          </div>

          <div class="ats-preview" v-if="formData.full_name || formData.summary">
            <!-- CV Visual Preview -->
            <div class="ats-header">
                <h2>{{ formData.full_name || '[Nama Anda]' }}</h2>
                <p>
                    {{ (!errors.email && formData.email) ? formData.email + ' | ' : '' }}
                    {{ formData.phone ? formData.phone + ' | ' : '' }}
                    {{ formData.address ? formData.address + ' | ' : '' }}
                    {{ (!errors.linkedin && formData.linkedin) ? formData.linkedin : '' }}
                </p>
            </div>
            
            <div class="ats-section" v-if="formData.summary">
                <h4>RINGKASAN PROFESIONAL</h4>
                <div class="ats-divider"></div>
                <p>{{ formData.summary }}</p>
            </div>
            
            <div class="ats-section" v-if="formData.degree || formData.institution">
                <h4>PENDIDIKAN</h4>
                <div class="ats-divider"></div>
                <div class="ats-item">
                    <div class="ats-item-header">
                        <strong>{{ formData.institution || '[Institusi]' }}</strong>
                        <span v-if="formData.gpa && !errors.gpa">IPK: {{ formData.gpa }}</span>
                    </div>
                    <div>{{ formData.degree || '[Gelar]' }}</div>
                </div>
            </div>
            
            <div class="ats-section" v-if="formData.company || formData.position || formData.description">
                <h4>PENGALAMAN</h4>
                <div class="ats-divider"></div>
                <div class="ats-item">
                    <div class="ats-item-header">
                        <strong>{{ formData.position || '[Posisi]' }}</strong>
                        <span>{{ formData.company || '[Perusahaan]' }}</span>
                    </div>
                    <ul class="ats-list" v-if="formData.description">
                        <li v-for="(point, idx) in formData.description.split('\n').filter(p => p.trim())" :key="idx">
                            {{ point }}
                        </li>
                    </ul>
                </div>
            </div>
            
            <div class="ats-section" v-if="formData.technical_skills || formData.soft_skills">
                <h4>KEAHLIAN</h4>
                <div class="ats-divider"></div>
                <p v-if="formData.technical_skills"><strong>Keahlian Teknis:</strong> {{ formData.technical_skills }}</p>
                <p v-if="formData.soft_skills"><strong>Soft Skills:</strong> {{ formData.soft_skills }}</p>
            </div>
            
            <div class="ats-section" v-if="formData.cert_name">
                <h4>SERTIFIKASI</h4>
                <div class="ats-divider"></div>
                <div class="ats-item">
                    <div class="ats-item-header">
                        <strong>{{ formData.cert_name }}</strong>
                        <span>{{ formData.issuer }}</span>
                    </div>
                </div>
            </div>
          </div>
          <div v-else class="preview-empty">
            Mulai isi data Anda pada tahapan sebelumnya untuk melihat pratinjau.
          </div>

          <div class="wizard-actions" style="margin-top: 32px; padding-top: 16px; border-top: 1px solid var(--border-color);">
            <button class="btn btn-outline" @click="prevStep">Sebelumnya</button>
          </div>
        </div>
      </main>
    </div>

    <!-- Hidden Print Container -->
    <div class="print-only print-area ats-preview">
        <div class="ats-header">
            <h2>{{ formData.full_name || '[Nama Anda]' }}</h2>
            <p>
                {{ (!errors.email && formData.email) ? formData.email + ' | ' : '' }}
                {{ formData.phone ? formData.phone + ' | ' : '' }}
                {{ formData.address ? formData.address + ' | ' : '' }}
                {{ (!errors.linkedin && formData.linkedin) ? formData.linkedin : '' }}
            </p>
        </div>
        
        <div class="ats-section" v-if="formData.summary">
            <h4>RINGKASAN PROFESIONAL</h4>
            <div class="ats-divider"></div>
            <p>{{ formData.summary }}</p>
        </div>
        
        <div class="ats-section" v-if="formData.degree || formData.institution">
            <h4>PENDIDIKAN</h4>
            <div class="ats-divider"></div>
            <div class="ats-item">
                <div class="ats-item-header">
                    <strong>{{ formData.institution || '[Institusi]' }}</strong>
                    <span v-if="formData.gpa && !errors.gpa">IPK: {{ formData.gpa }}</span>
                </div>
                <div>{{ formData.degree || '[Gelar]' }}</div>
            </div>
        </div>
        
        <div class="ats-section" v-if="formData.company || formData.position || formData.description">
            <h4>PENGALAMAN</h4>
            <div class="ats-divider"></div>
            <div class="ats-item">
                <div class="ats-item-header">
                    <strong>{{ formData.position || '[Posisi]' }}</strong>
                    <span>{{ formData.company || '[Perusahaan]' }}</span>
                </div>
                <ul class="ats-list" v-if="formData.description">
                    <li v-for="(point, idx) in formData.description.split('\n').filter(p => p.trim())" :key="idx">
                        {{ point }}
                    </li>
                </ul>
            </div>
        </div>
        
        <div class="ats-section" v-if="formData.technical_skills || formData.soft_skills">
            <h4>KEAHLIAN</h4>
            <div class="ats-divider"></div>
            <p v-if="formData.technical_skills"><strong>Keahlian Teknis:</strong> {{ formData.technical_skills }}</p>
            <p v-if="formData.soft_skills"><strong>Soft Skills:</strong> {{ formData.soft_skills }}</p>
        </div>
        
        <div class="ats-section" v-if="formData.cert_name">
            <h4>SERTIFIKASI</h4>
            <div class="ats-divider"></div>
            <div class="ats-item">
                <div class="ats-item-header">
                    <strong>{{ formData.cert_name }}</strong>
                    <span>{{ formData.issuer }}</span>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from "vue"
import axios from "axios"

const steps = ref([])
const expertiseAreas = ref([])
const targetExpertise = ref("Software Development")
const formData = reactive({})
const suggestions = reactive({})
const errors = reactive({
  gpa: "",
  email: "",
  linkedin: ""
})
const analysisResult = ref("")
const analyzing = ref(false)

const currentStep = ref(0)

const FIELDS = [
  "full_name", "email", "phone", "address", "linkedin",
  "summary", "degree", "institution", "gpa",
  "company", "position", "description",
  "technical_skills", "soft_skills", "ponytail", "superpowers",
  "cert_name", "issuer",
]

FIELDS.forEach(k => formData[k] = "")

// Auto Save / Load feature
onMounted(async () => {
  // Load saved data from localStorage
  const savedData = localStorage.getItem('jobfinder_cv_data')
  if (savedData) {
    try {
      const parsed = JSON.parse(savedData)
      Object.keys(parsed).forEach(k => {
        if (FIELDS.includes(k)) formData[k] = parsed[k]
      })
    } catch(e) {}
  }

  try {
    const [secRes, areaRes] = await Promise.all([
      axios.get("/api/cv/builder-sections"),
      axios.get("/api/expertise-areas"),
    ])
    steps.value = secRes.data
    expertiseAreas.value = areaRes.data
  } catch (e) {
    console.error(e)
    expertiseAreas.value = ["Software Development", "IT Infra", "Graphic Design", "Data Science"]
  }
})

watch(formData, (newVal) => {
  localStorage.setItem('jobfinder_cv_data', JSON.stringify(newVal))
}, { deep: true })

function isStepValid(stepIndex) {
  if (stepIndex >= steps.value.length) return true
  const section = steps.value[stepIndex]
  let valid = true
  for (const field of section.fields) {
    if (field.required && !formData[field.key]) {
      valid = false
    }
    if (errors[field.key]) {
      valid = false
    }
  }
  return valid
}

function nextStep() {
  if (isStepValid(currentStep.value)) {
    if (currentStep.value < steps.value.length) {
      currentStep.value++
    }
  } else {
    alert("Harap lengkapi semua field yang wajib (*).")
  }
}

function prevStep() {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

function goToStep(index) {
  // Allow going to previous steps freely
  if (index < currentStep.value) {
    currentStep.value = index
    return
  }
  // Allow going to next step only if current is valid
  if (index === currentStep.value + 1 && isStepValid(currentStep.value)) {
    currentStep.value = index
    return
  }
}

function validateGPA() {
    const val = formData.gpa;
    if (!val) {
        errors.gpa = "";
        return;
    }
    const isValid = /^([0-4](\.\d+)?)(?:\/4(?:\.0+)?)?$/.test(val);
    if (!isValid) {
        errors.gpa = "Format harus desimal (misal 3.8 atau 3.8/4.0). Maksimal 4.0.";
    } else {
        const num = parseFloat(val.split('/')[0]);
        if (num < 3.0) {
            errors.gpa = "Saran: Sebaiknya hanya cantumkan IPK jika di atas 3.0.";
        } else {
            errors.gpa = "";
        }
    }
}

function validateEmail() {
    const val = formData.email;
    if (!val) {
        errors.email = "";
        return;
    }
    const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val);
    if (!isValid) {
        errors.email = "Format email tidak valid.";
    } else {
        errors.email = "";
    }
}

function validateLinkedIn() {
    const val = formData.linkedin;
    if (!val) {
        errors.linkedin = "";
        return;
    }
    const isValid = /linkedin\.com\/(in|pub|profile)/i.test(val);
    if (!isValid) {
        errors.linkedin = "Format harus tautan profil LinkedIn (misal: linkedin.com/in/nama).";
    } else {
        errors.linkedin = "";
    }
}

async function getSuggestion(field) {
  try {
    const { data } = await axios.post("/api/cv/suggestion", {
      fieldLabel: field.label,
      expertise: targetExpertise.value,
    })
    suggestions[field.key] = data.suggestion
  } catch {
    suggestions[field.key] = `Saran: Buat agar relevan dengan posisi ${targetExpertise.value}.`
  }
}

async function analyzeBuiltCV() {
  analyzing.value = true;
  analysisResult.value = "";
  
  const cvText = `
    Name: ${formData.full_name}
    Contact: ${formData.email} | ${formData.phone} | ${formData.address}
    LinkedIn: ${formData.linkedin}
    Summary: ${formData.summary}
    Education: ${formData.degree} at ${formData.institution} (GPA: ${formData.gpa})
    Experience: ${formData.position} at ${formData.company}. Description: ${formData.description}
    Skills: Technical (${formData.technical_skills}), Soft (${formData.soft_skills})
    Certifications: ${formData.cert_name} from ${formData.issuer}
  `;
  
  try {
    const form = new FormData();
    form.append("expertise", targetExpertise.value);
    const blob = new Blob([cvText], { type: 'text/plain' });
    form.append("cv", blob, "cv.txt");
    
    const { data } = await axios.post("/api/cv/analyze", form);
    
    if (data.analysis) {
        analysisResult.value = data.analysis
            .replace(/```html\n?/g, "")
            .replace(/```\n?/g, "")
            .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
    } else {
        analysisResult.value = "Analisis gagal atau kosong.";
    }
  } catch (e) {
    console.error(e);
    analysisResult.value = "Gagal memindai CV. Silakan coba lagi.";
  } finally {
    analyzing.value = false;
  }
}

function downloadPDF() {
    window.print();
}
</script>

<style scoped>
.cv-wizard-container {
  max-width: 1200px;
  margin: 0 auto;
}

.wizard-layout {
  display: flex;
  gap: 32px;
  align-items: flex-start;
}

.wizard-sidebar {
  width: 280px;
  flex-shrink: 0;
  position: sticky;
  top: 100px;
}

.step-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.step-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  cursor: pointer;
  border-radius: 8px;
  margin-bottom: 8px;
  transition: all 0.2s;
  color: var(--text-muted);
}

.step-item:hover {
  background: var(--bg-canvas-soft, #f0f0f0);
}

.step-item.active {
  background: var(--bg-card, #fff);
  color: var(--text-primary);
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  border: 1px solid var(--border-color);
}

.step-item.completed .step-indicator {
  background: var(--primary-color, #f36458);
  color: white;
  border-color: var(--primary-color, #f36458);
}

.step-indicator {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 1px solid currentColor;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  margin-right: 12px;
}

.wizard-content {
  flex-grow: 1;
  min-width: 0;
  padding: 32px;
}

.section-fields { display: flex; flex-direction: column; gap: 20px; }
.field-group { display: flex; flex-direction: column; }
.field-group label { margin-bottom: 8px; font-weight: 500; }

.suggestion-btn { 
  background: none; 
  border: none;
  color: var(--primary-color, #f36458);
  cursor: pointer; 
  font-size: 12px; 
  margin-left: 12px; 
  padding: 2px 6px;
  border-radius: 4px;
  transition: background 0.2s; 
}
.suggestion-btn:hover { background: rgba(243, 100, 88, 0.1); }

.suggestion-box { background: var(--bg-canvas); padding: 12px 16px; border-radius: 4px; font-size: 13px; color: var(--text-muted); margin-top: 8px; border: 1px solid var(--border-color); }
.error-text { color: var(--color-error); font-size: 12px; margin-top: 6px; }

.wizard-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--border-color);
}

/* Inputs inherit from global style.css */

/* ATS Format Styling for both Screen and Print */
.ats-preview {
    background: white;
    color: black;
    padding: 40px;
    border: 1px solid var(--border-color);
    line-height: 1.5;
    max-width: 800px;
    margin: 0 auto;
}

.ats-header { text-align: center; margin-bottom: 24px; }
.ats-header h2 { font-size: 24px; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 1px; }
.ats-header p { font-size: 14px; }
.ats-section { margin-bottom: 20px; }
.ats-section h4 { font-size: 14px; text-transform: uppercase; margin-bottom: 4px; font-weight: bold; }
.ats-divider { border-bottom: 1px solid #000; margin-bottom: 12px; }
.ats-item { margin-bottom: 12px; }
.ats-item-header { display: flex; justify-content: space-between; }
.ats-list { margin-top: 6px; padding-left: 24px; }
.ats-list li { font-size: 14px; margin-bottom: 4px; }

.preview-empty { color: var(--color-mute); text-align: center; padding: 40px; font-style: italic; border: 1px dashed var(--color-hairline); }

.analysis-content :deep(table) { margin: 16px 0; width: 100%; border-collapse: collapse; }
.analysis-content :deep(th), .analysis-content :deep(td) { padding: 8px 12px; border: 1px solid var(--border-color); }
.analysis-content :deep(th) { background: #f9f9f9; text-align: left; }

.print-only {
  display: none;
}

/* Printing Styles */
@media print {
  @page { margin: 0; }
  body * {
    visibility: hidden;
  }
  .print-only {
    display: block !important;
  }
  .print-area, .print-area * {
    visibility: visible;
  }
  .print-area {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    margin: 0;
    padding: 40px !important;
    border: none !important;
    box-shadow: none !important;
  }
  .no-print {
    display: none !important;
  }
  .page { padding: 0 !important; }
}

@media (max-width: 768px) {
  .wizard-layout {
    flex-direction: column;
  }
  .wizard-sidebar {
    width: 100%;
    position: static;
  }
  .wizard-content {
    width: 100%;
    padding: 20px;
  }
  .step-list {
    display: flex;
    overflow-x: auto;
    gap: 8px;
    padding-bottom: 12px;
  }
  .step-item {
    flex-shrink: 0;
    margin-bottom: 0;
  }
}
</style>
