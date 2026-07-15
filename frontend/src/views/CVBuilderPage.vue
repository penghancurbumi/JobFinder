<template>
  <div class="page">
    <div class="no-print">
      <h1 class="page-title stagger-1">Pembuat CV</h1>
      <p class="hint stagger-2" style="margin-bottom: 32px; font-size: 14px;">Rakit bagian-bagian CV Anda. Tanda <span style="color:var(--pastel-red-text);">*</span> wajib diisi. Klik ikon 💡 untuk meminta saran dari asisten AI.</p>

      <div class="card stagger-3" style="margin-bottom: 24px;">
        <div class="form-group" style="margin-bottom: 0;">
          <label>Target Keahlian / Bidang</label>
          <select v-model="targetExpertise">
            <option v-for="a in expertiseAreas" :key="a" :value="a">{{ a }}</option>
          </select>
        </div>
      </div>

      <div class="bento-grid stagger-3">
        <div v-for="section in sections" :key="section.id" class="card section-card">
          <h3 style="font-family: 'Newsreader', serif; margin-bottom: 24px; font-size: 1.25rem;">{{ section.title }}</h3>
          <div class="section-fields">
            <div v-for="field in section.fields" :key="field.key" class="field-group">
              <label>
                {{ field.label }} 
                <span v-if="field.required" style="color: var(--pastel-red-text); font-weight: bold;">*</span>
                <span v-if="field.key === 'description'" class="suggestion-btn" @click="getSuggestion(field)" title="Minta saran AI">💡</span>
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
                rows="3"
              ></textarea>
              
              <span class="hint">{{ field.hint }}</span>
              <div v-if="errors[field.key]" class="error-text">{{ errors[field.key] }}</div>
              
              <div v-if="suggestions[field.key]" class="suggestion-box">
                <span style="font-weight: 500; color: var(--text-primary);">Saran AI:</span> {{ suggestions[field.key] }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Print / Download Area -->
    <div class="card preview-card stagger-3 no-print-shadow" style="margin-top: 32px;">
      <div class="no-print" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
        <h3 style="font-family: 'Newsreader', serif; font-size: 1.5rem;">Pratinjau Dokumen</h3>
        <div style="display: flex; gap: 12px;">
          <button class="btn btn-outline btn-sm" @click="analyzeBuiltCV" :disabled="analyzing">
            {{ analyzing ? 'Memindai...' : 'Scan Kecocokan %' }}
          </button>
          <button class="btn btn-primary btn-sm" @click="downloadPDF">
            Unduh PDF
          </button>
        </div>
      </div>
      
      <div class="no-print" v-if="analysisResult" style="margin-bottom: 24px; padding: 16px; border: 1px solid var(--border-color); border-radius: 4px; background: var(--bg-canvas);">
        <h4 style="margin-bottom: 12px; font-family: 'Newsreader', serif;">Laporan Pemindaian AI</h4>
        <div v-html="analysisResult" class="analysis-content"></div>
      </div>

      <div v-if="formData.full_name || formData.summary" class="ats-preview print-area">
        <div class="ats-header">
            <h2 style="font-family: 'Times New Roman', serif;">{{ formData.full_name || '[Nama Anda]' }}</h2>
            <p style="font-family: 'Times New Roman', serif;">
                {{ (!errors.email && formData.email) ? formData.email + ' | ' : '' }}
                {{ formData.phone ? formData.phone + ' | ' : '' }}
                {{ formData.address ? formData.address + ' | ' : '' }}
                {{ (!errors.linkedin && formData.linkedin) ? formData.linkedin : '' }}
            </p>
        </div>
        
        <div class="ats-section" v-if="formData.summary">
            <h4 style="font-family: 'Times New Roman', serif;">RINGKASAN PROFESIONAL</h4>
            <div class="ats-divider"></div>
            <p style="font-family: 'Times New Roman', serif;">{{ formData.summary }}</p>
        </div>
        
        <div class="ats-section" v-if="formData.degree || formData.institution">
            <h4 style="font-family: 'Times New Roman', serif;">PENDIDIKAN</h4>
            <div class="ats-divider"></div>
            <div class="ats-item">
                <div class="ats-item-header">
                    <strong style="font-family: 'Times New Roman', serif;">{{ formData.institution || '[Institusi]' }}</strong>
                    <span v-if="formData.gpa && !errors.gpa" style="font-family: 'Times New Roman', serif;">IPK: {{ formData.gpa }}</span>
                </div>
                <div style="font-family: 'Times New Roman', serif;">{{ formData.degree || '[Gelar]' }}</div>
            </div>
        </div>
        
        <div class="ats-section" v-if="formData.company || formData.position || formData.description">
            <h4 style="font-family: 'Times New Roman', serif;">PENGALAMAN</h4>
            <div class="ats-divider"></div>
            <div class="ats-item">
                <div class="ats-item-header">
                    <strong style="font-family: 'Times New Roman', serif;">{{ formData.position || '[Posisi]' }}</strong>
                    <span style="font-family: 'Times New Roman', serif;">{{ formData.company || '[Perusahaan]' }}</span>
                </div>
                <ul class="ats-list" v-if="formData.description">
                    <li v-for="(point, idx) in formData.description.split('\\n').filter(p => p.trim())" :key="idx" style="font-family: 'Times New Roman', serif;">
                        {{ point }}
                    </li>
                </ul>
            </div>
        </div>
        
        <div class="ats-section" v-if="formData.technical_skills || formData.soft_skills">
            <h4 style="font-family: 'Times New Roman', serif;">KEAHLIAN</h4>
            <div class="ats-divider"></div>
            <p v-if="formData.technical_skills" style="font-family: 'Times New Roman', serif;"><strong>Keahlian Teknis:</strong> {{ formData.technical_skills }}</p>
            <p v-if="formData.soft_skills" style="font-family: 'Times New Roman', serif;"><strong>Soft Skills:</strong> {{ formData.soft_skills }}</p>
        </div>
        
        <div class="ats-section" v-if="formData.cert_name">
            <h4 style="font-family: 'Times New Roman', serif;">SERTIFIKASI</h4>
            <div class="ats-divider"></div>
            <div class="ats-item">
                <div class="ats-item-header">
                    <strong style="font-family: 'Times New Roman', serif;">{{ formData.cert_name }}</strong>
                    <span style="font-family: 'Times New Roman', serif;">{{ formData.issuer }}</span>
                </div>
            </div>
        </div>
      </div>
      <div v-else class="preview-empty no-print">
        Mulai isi data Anda untuk melihat pratinjau dokumen ATS secara langsung.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue"
import axios from "axios"

const sections = ref([])
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

const FIELDS = [
  "full_name", "email", "phone", "address", "linkedin",
  "summary", "degree", "institution", "gpa",
  "company", "position", "description",
  "technical_skills", "soft_skills",
  "cert_name", "issuer",
]

FIELDS.forEach(k => formData[k] = "")

onMounted(async () => {
  try {
    const [secRes, areaRes] = await Promise.all([
      axios.get("/api/cv/builder-sections"),
      axios.get("/api/expertise-areas"),
    ])
    sections.value = secRes.data
    expertiseAreas.value = areaRes.data
  } catch (e) {
    console.error(e)
    expertiseAreas.value = ["Software Development", "IT Infra", "Graphic Design", "Data Science"]
  }
})

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
.section-fields { display: flex; flex-direction: column; gap: 16px; }
.field-group { margin-bottom: 4px; }
.suggestion-btn { cursor: pointer; font-size: 14px; margin-left: 6px; opacity: 0.5; transition: opacity 0.2s; }
.suggestion-btn:hover { opacity: 1; }
.suggestion-box { background: var(--bg-canvas); padding: 12px 16px; border-radius: 4px; font-size: 13px; color: var(--text-muted); margin-top: 8px; border: 1px solid var(--border-color); }
.error-text { color: var(--pastel-red-text); font-size: 12px; margin-top: 6px; }

/* ATS Format Styling */
.ats-preview {
    background: #ffffff;
    padding: 60px;
    border: 1px solid var(--border-color);
    font-family: "Times New Roman", Times, serif;
    color: #000;
    line-height: 1.5;
    max-width: 800px;
    margin: 0 auto;
}

.ats-header {
    text-align: center;
    margin-bottom: 24px;
}
.ats-header h2 {
    font-size: 24px;
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.ats-header p {
    font-size: 14px;
}

.ats-section {
    margin-bottom: 20px;
}
.ats-section h4 {
    font-size: 14px;
    text-transform: uppercase;
    margin-bottom: 4px;
    font-weight: bold;
}
.ats-divider {
    border-bottom: 1px solid #000;
    margin-bottom: 12px;
}

.ats-item {
    margin-bottom: 12px;
}
.ats-item-header {
    display: flex;
    justify-content: space-between;
}
.ats-list {
    margin-top: 6px;
    padding-left: 24px;
}
.ats-list li {
    font-size: 14px;
    margin-bottom: 4px;
}

.preview-empty { color: var(--text-muted); text-align: center; padding: 40px; font-family: 'Newsreader', serif; font-style: italic; border: 1px dashed var(--border-color); }

.analysis-content :deep(table) { margin: 16px 0; width: 100%; border-collapse: collapse; }
.analysis-content :deep(th), .analysis-content :deep(td) { padding: 8px 12px; border: 1px solid var(--border-color); }
.analysis-content :deep(th) { background: #f9f9f9; text-align: left; }

/* Printing Styles */
@media print {
  @page { margin: 0; } /* Removes header/footer like localhost url */
  body * {
    visibility: hidden;
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
  .no-print-shadow {
    box-shadow: none !important;
    border: none !important;
    background: transparent !important;
    padding: 0 !important;
    margin: 0 !important;
  }
  .page { padding: 0 !important; }
}
</style>
