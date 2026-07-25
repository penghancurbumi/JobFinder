<template>
  <div class="min-h-screen pt-[88px] bg-canvas-dark text-on-dark font-sans w-full max-w-[1200px] mx-auto px-xl">
    <div class="print:hidden mb-xl">
      <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-stone mb-sm block">Sistem Pembangun Dokumen ATS</span>
      <h1 class="text-[32px] md:text-[40px] font-medium leading-[1.2] tracking-[-0.4px] text-on-dark">Pembuat CV</h1>
      <p class="mt-sm text-on-dark-mute text-[14px] font-normal leading-[1.5]">Rakit bagian-bagian CV Anda langkah demi langkah. Tanda <span class="text-accent-danger">*</span> wajib diisi.</p>
    </div>

    <!-- Wizard Layout -->
    <div class="flex flex-col md:flex-row gap-xl print:hidden items-start">
      <!-- Sidebar Navigation -->
      <aside class="w-full md:w-[280px] shrink-0 md:sticky top-[100px] bg-surface-elevated rounded-[20px] py-xl">
        <div class="mb-[24px] px-[16px]">
          <label class="text-[12px] mb-[4px] text-on-dark-mute block font-semibold">Target Keahlian / Bidang</label>
          <select v-model="targetExpertise" class="w-full text-[14px] bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-primary focus:outline-none appearance-none">
            <option v-for="a in expertiseAreas" :key="a" :value="a" class="bg-surface-elevated text-on-dark">{{ a }}</option>
          </select>
        </div>
        
        <ul class="list-none m-0 p-0 flex md:block overflow-x-auto md:overflow-visible pb-[12px] md:pb-0">
          <li v-for="(section, index) in steps" :key="section.id" 
              class="flex shrink-0 items-center px-[16px] py-[12px] cursor-pointer rounded-none transition-all duration-200 text-on-dark-mute hover:bg-surface-deep border-b-[3px] md:border-b-0 md:border-l-[3px] border-transparent"
              :class="{ 'bg-surface-deep !text-on-dark font-medium !border-primary': currentStep === index, 'completed': currentStep > index }"
              @click="goToStep(index)">
            <div class="w-[28px] h-[28px] rounded-full border border-hairline-dark flex items-center justify-center text-[12px] mr-[12px] shrink-0 transition-colors" :class="{ 'bg-primary text-on-primary border-primary': currentStep > index }">{{ index + 1 }}</div>
            <div class="text-[14px]">{{ section.title }}</div>
          </li>
          <li class="flex shrink-0 items-center px-[16px] py-[12px] cursor-pointer rounded-none transition-all duration-200 text-on-dark-mute hover:bg-surface-deep border-b-[3px] md:border-b-0 md:border-l-[3px] border-transparent"
              :class="{ 'bg-surface-deep !text-on-dark font-medium !border-primary': currentStep === steps.length }" 
              @click="goToStep(steps.length)">
            <div class="w-[28px] h-[28px] rounded-full border border-hairline-dark flex items-center justify-center text-[12px] mr-[12px] shrink-0 transition-colors">✓</div>
            <div class="text-[14px]">Preview &amp; Export</div>
          </li>
        </ul>
      </aside>

      <!-- Main Content Panel -->
      <main class="flex-grow min-w-0 bg-surface-elevated rounded-[20px] p-xl md:p-xxl w-full">
        <!-- Active Form Section -->
        <div v-if="currentStep < steps.length">
          <h3 class="text-[24px] font-medium leading-[1.33] mb-[24px] text-on-dark">
            {{ steps[currentStep].title }}
          </h3>
          
          <div class="flex flex-col gap-[20px]">
            <div v-for="field in steps[currentStep].fields" :key="field.key" class="flex flex-col">
              <label class="mb-[8px] font-semibold text-on-dark-mute">
                {{ field.label }} 
                <span v-if="field.required" class="text-accent-danger font-bold">*</span>
                <button v-if="field.key === 'description' || field.key === 'summary' || field.key === 'technical_skills' || field.key === 'soft_skills'" class="bg-transparent border-none text-primary cursor-pointer text-[12px] ml-[12px] px-[8px] py-[2px] rounded-full transition-colors duration-200 hover:bg-primary/12" @click.prevent="getSuggestion(field)" title="Minta saran AI">💡 AI Suggestion</button>
              </label>
              
              <input 
                v-if="field.key !== 'gpa' && field.key !== 'description' && field.key !== 'summary' && field.key !== 'email' && field.key !== 'linkedin'" 
                v-model="formData[field.key]" 
                :placeholder="field.placeholder" 
                class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-primary focus:outline-none placeholder:text-stone"
              />
              
              <input 
                v-else-if="field.key === 'email'"
                type="email"
                v-model="formData[field.key]" 
                :placeholder="field.placeholder" 
                @input="validateEmail"
                class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-primary focus:outline-none placeholder:text-stone"
              />

              <input 
                v-else-if="field.key === 'linkedin'"
                type="url"
                v-model="formData[field.key]" 
                :placeholder="field.placeholder" 
                @input="validateLinkedIn"
                class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-primary focus:outline-none placeholder:text-stone"
              />

              <input 
                v-else-if="field.key === 'gpa'"
                v-model="formData[field.key]" 
                :placeholder="field.placeholder" 
                @input="validateGPA"
                class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-primary focus:outline-none placeholder:text-stone"
              />

              <textarea 
                v-else 
                v-model="formData[field.key]" 
                :placeholder="field.placeholder"
                rows="4"
                class="w-full bg-transparent border border-hairline-dark rounded-[12px] p-[16px] text-on-dark focus:border-primary focus:outline-none placeholder:text-stone resize-y"
              ></textarea>
              
              <span class="text-[12px] text-stone mt-[6px]">{{ field.hint }}</span>
              <div v-if="errors[field.key]" class="text-accent-danger text-[12px] mt-[6px]">{{ errors[field.key] }}</div>
              
              <div v-if="suggestions[field.key]" class="bg-surface-deep px-[16px] py-[12px] rounded-md text-[13px] text-on-dark-mute mt-[8px] border-l-[3px] border-primary">
                <span class="font-semibold text-primary">Saran AI:</span> {{ suggestions[field.key] }}
              </div>
            </div>
          </div>

          <!-- Wizard Actions -->
          <div class="flex justify-between mt-[32px] pt-[24px] border-t border-hairline-dark">
            <button class="inline-flex items-center justify-center font-semibold rounded-full transition-all duration-200 cursor-pointer text-[14px] px-[20px] h-[40px] bg-transparent border border-hairline-dark text-on-dark hover:bg-surface-elevated disabled:opacity-50 disabled:cursor-not-allowed" :disabled="currentStep === 0" @click="prevStep">Sebelumnya</button>
            <button class="inline-flex items-center justify-center font-semibold rounded-full transition-all duration-200 cursor-pointer text-[14px] px-[20px] h-[40px] bg-on-dark text-ink hover:bg-white/90" @click="nextStep">Selanjutnya</button>
          </div>
        </div>

        <!-- Preview Section -->
        <div v-else>
          <div class="flex justify-between items-center mb-[24px] flex-wrap gap-[12px]">
            <h3 class="text-[24px] font-medium leading-[1.33] text-on-dark">Pratinjau Dokumen</h3>
            <div class="flex gap-[12px]">
              <button class="inline-flex items-center justify-center font-semibold rounded-full transition-all duration-200 cursor-pointer text-[13px] px-[16px] h-[32px] bg-transparent border border-hairline-dark text-on-dark hover:bg-surface-elevated disabled:opacity-50 disabled:cursor-not-allowed" @click="analyzeBuiltCV" :disabled="analyzing">
                {{ analyzing ? 'Memindai...' : 'Scan ATS Score' }}
              </button>
              <button class="inline-flex items-center justify-center font-semibold rounded-full transition-all duration-200 cursor-pointer text-[13px] px-[16px] h-[32px] bg-on-dark text-ink hover:bg-white/90" @click="downloadPDF">
                Unduh PDF
              </button>
            </div>
          </div>
          
          <div v-if="analysisResult" class="mb-[24px] p-xl border border-hairline-dark rounded-[20px] bg-surface-deep">
            <h4 class="text-[20px] font-medium leading-[1.4] mb-[12px] text-on-dark">Hasil Analisis AI</h4>
            <div v-html="analysisResult" class="analysis-content"></div>
          </div>

          <div class="bg-white text-black p-[40px] rounded-[20px] leading-[1.5] max-w-[800px] mx-auto" v-if="formData.full_name || formData.summary">
            <!-- CV Visual Preview -->
            <div class="text-center mb-[24px]">
                <h2 class="text-[24px] mb-[4px] uppercase tracking-[1px] font-bold">{{ formData.full_name || '[Nama Anda]' }}</h2>
                <p class="text-[14px]">
                    {{ (!errors.email && formData.email) ? formData.email + ' | ' : '' }}
                    {{ formData.phone ? formData.phone + ' | ' : '' }}
                    {{ formData.address ? formData.address + ' | ' : '' }}
                    {{ (!errors.linkedin && formData.linkedin) ? formData.linkedin : '' }}
                </p>
            </div>
            
            <div class="mb-[20px]" v-if="formData.summary">
                <h4 class="text-[14px] uppercase mb-[4px] font-bold">RINGKASAN PROFESIONAL</h4>
                <div class="border-b border-black mb-[12px]"></div>
                <p class="text-[14px]">{{ formData.summary }}</p>
            </div>
            
            <div class="mb-[20px]" v-if="formData.degree || formData.institution">
                <h4 class="text-[14px] uppercase mb-[4px] font-bold">PENDIDIKAN</h4>
                <div class="border-b border-black mb-[12px]"></div>
                <div class="mb-[12px]">
                    <div class="flex justify-between">
                        <strong>{{ formData.institution || '[Institusi]' }}</strong>
                        <span v-if="formData.gpa && !errors.gpa">IPK: {{ formData.gpa }}</span>
                    </div>
                    <div class="text-[14px]">{{ formData.degree || '[Gelar]' }}</div>
                </div>
            </div>
            
            <div class="mb-[20px]" v-if="formData.company || formData.position || formData.description">
                <h4 class="text-[14px] uppercase mb-[4px] font-bold">PENGALAMAN</h4>
                <div class="border-b border-black mb-[12px]"></div>
                <div class="mb-[12px]">
                    <div class="flex justify-between">
                        <strong>{{ formData.position || '[Posisi]' }}</strong>
                        <span>{{ formData.company || '[Perusahaan]' }}</span>
                    </div>
                    <ul class="mt-[6px] pl-[24px] list-disc" v-if="formData.description">
                        <li v-for="(point, idx) in formData.description.split('\n').filter(p => p.trim())" :key="idx" class="text-[14px] mb-[4px]">
                            {{ point }}
                        </li>
                    </ul>
                </div>
            </div>
            
            <div class="mb-[20px]" v-if="formData.technical_skills || formData.soft_skills">
                <h4 class="text-[14px] uppercase mb-[4px] font-bold">KEAHLIAN</h4>
                <div class="border-b border-black mb-[12px]"></div>
                <p v-if="formData.technical_skills" class="text-[14px]"><strong>Keahlian Teknis:</strong> {{ formData.technical_skills }}</p>
                <p v-if="formData.soft_skills" class="text-[14px]"><strong>Soft Skills:</strong> {{ formData.soft_skills }}</p>
            </div>
            
            <div class="mb-[20px]" v-if="formData.cert_name">
                <h4 class="text-[14px] uppercase mb-[4px] font-bold">SERTIFIKASI</h4>
                <div class="border-b border-black mb-[12px]"></div>
                <div class="mb-[12px]">
                    <div class="flex justify-between text-[14px]">
                        <strong>{{ formData.cert_name }}</strong>
                        <span>{{ formData.issuer }}</span>
                    </div>
                </div>
            </div>
          </div>
          <div v-else class="text-stone text-center p-[40px] italic border border-dashed border-hairline-dark rounded-[20px]">
            Mulai isi data Anda pada tahapan sebelumnya untuk melihat pratinjau.
          </div>

          <div class="flex justify-between mt-[32px] pt-[16px] border-t border-hairline-dark">
            <button class="inline-flex items-center justify-center font-semibold rounded-full transition-all duration-200 cursor-pointer text-[14px] px-[20px] h-[40px] bg-transparent border border-hairline-dark text-on-dark hover:bg-surface-elevated" @click="prevStep">Sebelumnya</button>
          </div>
        </div>
      </main>
    </div>

    <!-- Hidden Print Container -->
    <div class="hidden print:block absolute left-0 top-0 w-full m-0 p-[40px] border-none shadow-none rounded-none bg-white text-black leading-[1.5]">
        <div class="text-center mb-[24px]">
            <h2 class="text-[24px] mb-[4px] uppercase tracking-[1px] font-bold">{{ formData.full_name || '[Nama Anda]' }}</h2>
            <p class="text-[14px]">
                {{ (!errors.email && formData.email) ? formData.email + ' | ' : '' }}
                {{ formData.phone ? formData.phone + ' | ' : '' }}
                {{ formData.address ? formData.address + ' | ' : '' }}
                {{ (!errors.linkedin && formData.linkedin) ? formData.linkedin : '' }}
            </p>
        </div>
        
        <div class="mb-[20px]" v-if="formData.summary">
            <h4 class="text-[14px] uppercase mb-[4px] font-bold">RINGKASAN PROFESIONAL</h4>
            <div class="border-b border-black mb-[12px]"></div>
            <p class="text-[14px]">{{ formData.summary }}</p>
        </div>
        
        <div class="mb-[20px]" v-if="formData.degree || formData.institution">
            <h4 class="text-[14px] uppercase mb-[4px] font-bold">PENDIDIKAN</h4>
            <div class="border-b border-black mb-[12px]"></div>
            <div class="mb-[12px]">
                <div class="flex justify-between text-[14px]">
                    <strong>{{ formData.institution || '[Institusi]' }}</strong>
                    <span v-if="formData.gpa && !errors.gpa">IPK: {{ formData.gpa }}</span>
                </div>
                <div class="text-[14px]">{{ formData.degree || '[Gelar]' }}</div>
            </div>
        </div>
        
        <div class="mb-[20px]" v-if="formData.company || formData.position || formData.description">
            <h4 class="text-[14px] uppercase mb-[4px] font-bold">PENGALAMAN</h4>
            <div class="border-b border-black mb-[12px]"></div>
            <div class="mb-[12px]">
                <div class="flex justify-between text-[14px]">
                    <strong>{{ formData.position || '[Posisi]' }}</strong>
                    <span>{{ formData.company || '[Perusahaan]' }}</span>
                </div>
                <ul class="mt-[6px] pl-[24px] list-disc" v-if="formData.description">
                    <li v-for="(point, idx) in formData.description.split('\n').filter(p => p.trim())" :key="idx" class="text-[14px] mb-[4px]">
                        {{ point }}
                    </li>
                </ul>
            </div>
        </div>
        
        <div class="mb-[20px]" v-if="formData.technical_skills || formData.soft_skills">
            <h4 class="text-[14px] uppercase mb-[4px] font-bold">KEAHLIAN</h4>
            <div class="border-b border-black mb-[12px]"></div>
            <p v-if="formData.technical_skills" class="text-[14px]"><strong>Keahlian Teknis:</strong> {{ formData.technical_skills }}</p>
            <p v-if="formData.soft_skills" class="text-[14px]"><strong>Soft Skills:</strong> {{ formData.soft_skills }}</p>
        </div>
        
        <div class="mb-[20px]" v-if="formData.cert_name">
            <h4 class="text-[14px] uppercase mb-[4px] font-bold">SERTIFIKASI</h4>
            <div class="border-b border-black mb-[12px]"></div>
            <div class="mb-[12px]">
                <div class="flex justify-between text-[14px]">
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
.analysis-content :deep(table) { margin: 16px 0; width: 100%; border-collapse: collapse; }
.analysis-content :deep(th), .analysis-content :deep(td) { padding: 8px 12px; border: 1px solid var(--color-hairline-dark); }
.analysis-content :deep(th) { background: var(--color-surface-deep); text-align: left; color: var(--color-on-dark); }

@media print {
  @page { margin: 0; }
  body * {
    visibility: hidden;
  }
  .print\:block {
    visibility: visible !important;
  }
  .print\:block * {
    visibility: visible;
  }
}
</style>
