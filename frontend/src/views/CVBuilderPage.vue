<template>
  <div class="min-h-screen pt-[88px] bg-canvas-dark text-on-dark font-sans">
    <div class="w-full mx-auto px-[32px] md:px-[72px]">
      <div class="print:hidden mb-xl">
        <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-stone mb-sm block">Sistem Pembangun Dokumen ATS</span>
        <h1 class="text-[32px] md:text-[40px] font-medium leading-[1.2] tracking-[-0.4px] text-on-dark">Pembuat CV</h1>
        <p class="mt-sm text-on-dark-mute text-[16px] font-normal leading-[1.5]">Rakit bagian-bagian CV Anda langkah demi langkah. Tanda <span class="text-accent-danger">*</span> wajib diisi.</p>
      </div>

      <!-- Wizard Layout -->
      <div class="flex flex-col md:flex-row gap-xl print:hidden items-start">

        <!-- Sidebar Navigation -->
        <aside class="w-full md:w-[280px] shrink-0 md:sticky top-[100px] bg-surface-elevated rounded-[20px] py-xl border border-hairline-dark">
          <!-- Target Expertise -->
          <div class="mb-[24px] px-[16px]">
            <label class="text-[12px] mb-md text-on-dark-mute block font-semibold">Target Keahlian / Bidang</label>
            <CustomSelect
              :options="ExpertiseOptions"
              v-model="targetExpertise"
            />
          </div>

          <ul class="list-none m-0 p-0 flex md:block overflow-x-auto md:overflow-visible pb-[12px] md:pb-0">
            <!-- Step 0: Template Select -->
            <li class="flex shrink-0 items-center px-[16px] py-[12px] rounded-none transition-all duration-200 text-on-dark-mute hover:bg-surface-deep border-b-[3px] md:border-b-0 md:border-l-[3px] border-transparent cursor-pointer"
                :class="{ 'bg-surface-deep !text-on-dark font-medium !border-white': currentStep === 0 }"
                @click="goToStep(0)">
              <div class="w-[28px] h-[28px] rounded-full border border-hairline-dark flex items-center justify-center text-[12px] mr-[12px] shrink-0 transition-colors" :class="{ 'bg-white text-ink border-white': currentStep > 0 }">1</div>
              <div class="text-[14px]">Pilih Template</div>
            </li>

            <!-- Template-specific steps -->
            <li v-for="(section, index) in activeSteps" :key="section.id"
                class="flex shrink-0 items-center px-[16px] py-[12px] rounded-none transition-all duration-200 text-on-dark-mute hover:bg-surface-deep border-b-[3px] md:border-b-0 md:border-l-[3px] border-transparent"
                :class="{
                  'bg-surface-deep !text-on-dark font-medium !border-white': currentStep === index + 1,
                  'cursor-pointer': index + 1 <= maxStepReached,
                  'opacity-50 cursor-not-allowed': index + 1 > maxStepReached
                }"
                @click="goToStep(index + 1)">
              <div class="w-[28px] h-[28px] rounded-full border border-hairline-dark flex items-center justify-center text-[12px] mr-[12px] shrink-0 transition-colors" :class="{ 'bg-white text-ink border-white': index + 1 < currentStep }">{{ index + 2 }}</div>
              <div class="text-[14px]">{{ section.title }}</div>
            </li>

            <!-- Preview Step -->
            <li class="flex shrink-0 items-center px-[16px] py-[12px] rounded-none transition-all duration-200 text-on-dark-mute hover:bg-surface-deep border-b-[3px] md:border-b-0 md:border-l-[3px] border-transparent"
                :class="{
                  'bg-surface-deep !text-on-dark font-medium !border-white': currentStep === totalSteps - 1,
                  'cursor-pointer': totalSteps - 1 <= maxStepReached,
                  'opacity-50 cursor-not-allowed': totalSteps - 1 > maxStepReached
                }"
                @click="goToStep(totalSteps - 1)">
              <div class="w-[28px] h-[28px] rounded-full border border-hairline-dark flex items-center justify-center text-[12px] mr-[12px] shrink-0 transition-colors" :class="{ 'bg-white text-ink border-white': maxStepReached >= totalSteps - 1 }">✓</div>
              <div class="text-[14px]">Preview & Export</div>
            </li>
          </ul>
        </aside>

        <!-- Main Content -->
        <main class="flex-grow min-w-0 bg-surface-elevated rounded-[20px] p-xl md:p-xxl w-full border border-hairline-dark">

          <!-- ===== STEP 0: TEMPLATE SELECT ===== -->
          <div v-if="currentStep === 0">
            <h3 class="text-[24px] font-medium leading-[1.33] mb-[24px] text-on-dark">Pilih Template</h3>
            <p class="text-[14px] text-on-dark-mute mb-[24px]">Pilih template CV. Setiap template memiliki desain preview dan bagian input yang berbeda.</p>

            <div class="grid grid-cols-1 sm:grid-cols-3 gap-[16px]">
              <label v-for="tpl in CV_TEMPLATES" :key="tpl.id"
                class="relative cursor-pointer rounded-[16px] border-2 p-[4px] transition-all duration-200 hover:border-white/60"
                :class="selectedTemplate === tpl.id ? 'border-white shadow-[0_0_20px_rgba(255,255,255,0.15)]' : 'border-hairline-dark'">
                <input type="radio" :value="tpl.id" v-model="selectedTemplate" class="sr-only" />
                <div class="w-full aspect-[3/4] bg-white rounded-[12px] overflow-hidden flex items-center justify-center">
                </div>
                
                <div class="flex items-center gap-[8px] mt-[12px] px-[8px] pb-[8px]">
                  <div class="w-[18px] h-[18px] rounded-full border-2 flex items-center justify-center shrink-0 transition-colors" :class="selectedTemplate === tpl.id ? 'border-white' : 'border-stone'">
                    <div v-if="selectedTemplate === tpl.id" class="w-[10px] h-[10px] rounded-full bg-white"></div>
                  </div>
                  <div>
                    <div class="text-[14px] font-semibold text-on-dark">{{ tpl.name }}</div>
                    <div class="text-[12px] text-stone">{{ tpl.desc }}</div>
                  </div>
                </div>
                <span v-if="tpl.isDefault" class="absolute top-[12px] right-[12px] bg-white text-ink text-[10px] font-bold uppercase tracking-[0.5px] px-[8px] py-[2px] rounded-full">Default</span>
              </label>
            </div>

            <!-- Font Selector -->
            <div class="mt-[32px] pt-[24px] border-t border-hairline-dark">
              <label class="block text-[14px] font-semibold text-on-dark-mute mb-[12px]">Font CV</label>
              <div class="relative flex-1 mb-[12px]">
                <Icon icon="mdi:magnify" class="absolute left-[12px] top-1/2 -translate-y-1/2 text-stone text-[18px] pointer-events-none" />
                <input v-model="fontSearch" type="text" placeholder="Cari font..." class="w-full bg-transparent border border-hairline-dark rounded-[10px] h-[40px] pl-[36px] pr-[12px] text-[14px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
              </div>

              <!-- Selected font indicator -->
              <div v-if="selectedFont" class="mb-[12px] flex items-center justify-between px-[14px] py-[10px] rounded-[10px] bg-white/5 border border-white/20">
                <span class="text-[15px] text-on-dark" :style="{ fontFamily: `'${selectedFont}', sans-serif` }">{{ selectedFont }}</span>
                <button type="button" @click="selectedFont = ''; selectedFontName = ''" class="text-stone hover:text-on-dark transition-colors shrink-0 ml-[12px]">
                  <Icon icon="mdi:close" class="text-[16px]" />
                </button>
              </div>

              <div v-if="fontLoading" class="flex items-center justify-center py-[32px] gap-[8px] text-stone text-[14px]">
                <Icon icon="mdi:loading" class="animate-spin text-[20px]" /> Memuat daftar font...
              </div>

              <div v-else ref="fontListRef" class="h-[280px] overflow-y-auto rounded-[12px] border border-hairline-dark divide-y divide-hairline-dark" tabindex="0" @wheel.stop>
                <!-- System Fonts Section -->
                <div v-if="filteredSystemFonts.length > 0">
                  <div class="px-[14px] py-[6px] text-[10px] font-bold uppercase tracking-widest text-stone bg-white/3 sticky top-0">System Fonts</div>
                  <button v-for="f in filteredSystemFonts" :key="'sys-' + f.family" type="button"
                    @click="selectFont(f)"
                    class="w-full flex items-center gap-[10px] px-[14px] py-[10px] transition-colors hover:bg-white/5 text-left"
                    :class="selectedFont === f.family ? 'bg-white/8' : ''">
                    <div class="w-[16px] h-[16px] rounded-full border-2 flex items-center justify-center shrink-0 transition-colors" :class="selectedFont === f.family ? 'border-white' : 'border-stone'">
                      <div v-if="selectedFont === f.family" class="w-[8px] h-[8px] rounded-full bg-white"></div>
                    </div>
                    <span class="text-[15px] transition-colors" :class="selectedFont === f.family ? 'text-on-dark' : 'text-on-dark-mute'" :style="{ fontFamily: `'${f.family}', ${f.category}` }">{{ f.family }}</span>
                    <span class="text-[11px] text-stone capitalize ml-[2px]">{{ f.category }}</span>
                  </button>
                </div>

                <!-- Google Fonts Section -->
                <div v-if="filteredGoogleFonts.length > 0 && !fontSearch.trim()">
                  <div class="px-[14px] py-[6px] text-[10px] font-bold uppercase tracking-widest text-stone bg-white/3 sticky top-0">Google Fonts</div>
                </div>
                <button v-for="f in filteredGoogleFonts" :key="f.family" type="button"
                  @click="selectFont(f)" @mouseenter="onFontHover(f.family)"
                  class="w-full flex items-center gap-[10px] px-[14px] py-[10px] transition-colors hover:bg-white/5 text-left"
                  :class="selectedFont === f.family ? 'bg-white/8' : ''">
                  <div class="w-[16px] h-[16px] rounded-full border-2 flex items-center justify-center shrink-0 transition-colors" :class="selectedFont === f.family ? 'border-white' : 'border-stone'">
                    <div v-if="selectedFont === f.family" class="w-[8px] h-[8px] rounded-full bg-white"></div>
                  </div>

                  <!-- Font name rendered in its own typeface -->
                  <span
                    class="text-[15px] transition-colors"
                    :class="selectedFont === f.family ? 'text-on-dark' : 'text-on-dark-mute'"
                    :style="loadedFonts.includes(f.family) ? { fontFamily: `'${f.family}', sans-serif` } : {}"
                  >{{ f.family }}</span>
                  <span class="text-[11px] text-stone capitalize ml-[2px]">{{ f.category }}</span>
                </button>
                <div v-if="filteredGoogleFonts.length === 0 && filteredSystemFonts.length === 0" class="text-center text-stone text-[13px] py-[24px]">Tidak ada font ditemukan.</div>
              </div>

              <p class="text-[12px] text-stone mt-[10px]">{{ googleFonts.length.toLocaleString() }} font tersedia </p>
            </div>
          </div>

          <!-- ===== TEMPLATE FORM STEPS ===== -->
          <div v-else-if="currentStep < totalSteps - 1">
            <h3 class="text-[24px] font-medium leading-[1.33] mb-[24px] text-on-dark">{{ activeSteps[currentStep - 1]?.title }}</h3>
            <component
              :is="activeTemplateComponent"
              ref="templateRef"
              :step-index="currentStep - 1"
              :is-preview="false"
              :template-font="templateFont"
              :target-expertise="targetExpertise"
            />
          </div>

          <!-- ===== PREVIEW & EXPORT STEP ===== -->
          <div v-else>
            <div class="flex justify-between items-center mb-[24px] flex-wrap gap-[12px]">
              <h3 class="text-[24px] font-medium leading-[1.33] text-on-dark">Pratinjau Dokumen</h3>
              <div class="flex gap-[12px]">
                <button class="inline-flex items-center justify-center font-medium rounded-full transition-all duration-200 cursor-pointer text-[13px] px-[16px] h-[32px] bg-transparent border border-hairline-dark text-on-dark hover:bg-surface-elevated disabled:opacity-50 disabled:cursor-not-allowed" @click="analyzeBuiltCV" :disabled="analyzing">
                  {{ analyzing ? 'Memindai...' : 'Scan ATS Score' }}
                </button>
                <button class="inline-flex items-center justify-center font-medium rounded-full transition-all duration-200 cursor-pointer text-[13px] px-[16px] h-[32px] bg-on-dark text-ink hover:bg-white/90" @click="downloadPDF">
                  Unduh PDF
                </button>
              </div>
            </div>

            <!-- ATS Analysis Result -->
            <div v-if="analysisResult" class="mb-[32px] animate-fade-in">
              <h2 class="text-[24px] font-medium leading-[1.33] tracking-[0] mb-xl text-on-dark">Laporan Analisis</h2>
              <div v-if="analysisResult.analysis?.error" class="bg-accent-danger text-white rounded-[20px] p-xxl mb-xl">
                Gagal menganalisis CV: {{ analysisResult.analysis.message }}
              </div>
              <template v-else>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-xl mb-xl">
                  <div class="bg-surface-elevated rounded-[20px] p-xxl flex items-center gap-xl border border-hairline-dark">
                    <div class="w-[100px] h-[100px] shrink-0 relative"><Doughnut :data="overallChartData" :options="doughnutOptions" /></div>
                    <div>
                      <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-stone">Overall Score</span>
                      <h3 class="text-[32px] font-medium leading-[1.19] tracking-[-0.32px] m-0 text-white">{{ analysisResult.analysis?.overallScore || 0 }}<span class="text-[20px] text-on-dark-mute">/100</span></h3>
                      <p class="text-[14px] font-normal leading-[1.5] text-on-dark-mute mt-[4px]">Kecocokan dengan {{ targetExpertise }}</p>
                    </div>
                  </div>
                  <div class="bg-surface-elevated rounded-[20px] p-xxl flex items-center gap-xl border border-hairline-dark">
                    <div class="w-[100px] h-[100px] shrink-0 relative"><Doughnut :data="atsChartData" :options="doughnutOptions" /></div>
                    <div>
                      <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-stone">ATS Score</span>
                      <h3 class="text-[32px] font-medium leading-[1.19] tracking-[-0.32px] m-0" :class="analysisResult.ats?.isATS ? 'text-accent-teal' : 'text-accent-danger'">{{ analysisResult.ats?.score || 0 }}<span class="text-[20px] text-on-dark-mute">%</span></h3>
                      <span class="inline-block rounded-full text-[13px] font-medium mt-[4px]" :class="analysisResult.ats?.isATS ? 'text-accent-teal' : 'text-accent-danger'">{{ analysisResult.ats?.isATS ? 'Format ATS Valid' : 'Format ATS Kurang' }}</span>
                    </div>
                  </div>
                </div>

                <div class="bg-surface-elevated rounded-[20px] p-xxl mb-xl border border-hairline-dark">
                  <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] mb-lg block text-stone">Analisis Kategori</span>
                  <div class="relative h-[280px] w-full"><Line :data="lineChartData" :options="lineOptions" /></div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-xl mb-xl">
                  <div v-if="analysisResult.analysis?.strengths?.length" class="bg-surface-elevated rounded-[20px] p-xxl border-t-3 border-accent-teal">
                    <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-stone">Kekuatan</span>
                    <ul class="pl-[20px] mt-md text-[14px] list-disc"><li v-for="(item, i) in analysisResult.analysis.strengths" :key="i" class="mb-[8px] text-on-dark-mute">{{ item }}</li></ul>
                  </div>
                  <div v-if="analysisResult.analysis?.weaknesses?.length" class="bg-surface-elevated rounded-[20px] p-xxl border-t-3 border-accent-danger">
                    <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-stone">Kelemahan</span>
                    <ul class="pl-[20px] mt-md text-[14px] list-disc"><li v-for="(item, i) in analysisResult.analysis.weaknesses" :key="i" class="mb-[8px] text-on-dark-mute">{{ item }}</li></ul>
                  </div>
                </div>

                <div v-if="analysisResult.analysis?.recommendations?.length" class="bg-surface-elevated rounded-[20px] p-xxl border-l-3 border-primary mb-xl">
                  <span class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-stone">Rekomendasi AI</span>
                  <ul class="pl-[20px] mt-md text-[14px] list-disc"><li v-for="(rec, i) in analysisResult.analysis.recommendations" :key="i" class="mb-[12px] text-on-dark-mute">{{ rec }}</li></ul>
                </div>
              </template>
            </div>

            <!-- CV Preview via template component -->
            <div class="rounded-[20px] overflow-hidden shadow-2xl max-w-[800px] mx-auto">
              <component
                :is="activeTemplateComponent"
                ref="previewTemplateRef"
                :key="`preview-${currentStep}`"
                :step-index="0"
                :is-preview="true"
                :template-font="templateFont"
                :target-expertise="targetExpertise"
              />
            </div>

            <div v-if="!hasPreviewData" class="text-stone text-center p-[40px] italic border border-dashed border-hairline-dark rounded-[20px]">
              Mulai isi data Anda pada tahapan sebelumnya untuk melihat pratinjau.
            </div>

            <div class="flex justify-between mt-[32px] pt-[16px] border-t border-hairline-dark">
              <button class="inline-flex items-center justify-center font-medium rounded-full transition-all duration-200 cursor-pointer text-[14px] px-[20px] h-[40px] bg-transparent border border-hairline-dark text-on-dark hover:bg-surface-elevated" @click="prevStep">Sebelumnya</button>
            </div>
          </div>

          <!-- Wizard Navigation Buttons (form steps) -->
          <div v-if="currentStep > 0 && currentStep < totalSteps - 1" class="flex justify-between mt-[32px] pt-[24px] border-t border-hairline-dark">
            <button class="inline-flex items-center justify-center font-medium rounded-full transition-all duration-200 cursor-pointer text-[14px] px-[20px] h-[40px] bg-transparent border border-hairline-dark text-on-dark hover:bg-surface-elevated disabled:opacity-50 disabled:cursor-not-allowed" :disabled="currentStep === 0" @click="prevStep">Sebelumnya</button>
            <button class="inline-flex items-center justify-center font-medium rounded-full transition-all duration-200 cursor-pointer text-[14px] px-[20px] h-[40px] bg-on-dark text-ink hover:bg-white/90" @click="nextStep">Selanjutnya</button>
          </div>
          <!-- Template select next button -->
          <div v-if="currentStep === 0" class="flex justify-end mt-[32px] pt-[24px] border-t border-hairline-dark">
            <button class="inline-flex items-center justify-center font-medium rounded-full transition-all duration-200 cursor-pointer text-[14px] px-[20px] h-[40px] bg-on-dark text-ink hover:bg-white/90" @click="nextStep">Selanjutnya</button>
          </div>

        </main>
      </div>
    </div>

    <!-- Print container -->
    <div class="hidden print:block absolute left-0 top-0 w-full m-0 p-0 border-none shadow-none rounded-none bg-white">
      <component
        :is="activeTemplateComponent"
        :step-index="0"
        :is-preview="true"
        :template-font="templateFont"
        :target-expertise="targetExpertise"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import CustomSelect from '../components/CustomSelect.vue'
import axios from 'axios'
import { Icon } from '@iconify/vue'
import { Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend, Title, BarElement, CategoryScale, LinearScale, ArcElement } from 'chart.js'
import { Line, Doughnut } from 'vue-chartjs'
import { useHead } from '@vueuse/head'

import ModernATSTemplate from '@/components/cv-templates/ModernATSTemplate.vue'
import ClassicATSTemplate from '@/components/cv-templates/ClassicATSTemplate.vue'
import ExecutiveATSTemplate from '@/components/cv-templates/ExecutiveATSTemplate.vue'

useHead({
  title: 'Pembuat CV ATS-Friendly — JobFinder',
  meta: [
    { name: 'description', content: 'Buat CV profesional berstandar ATS langkah demi langkah dengan panduan asisten AI. Template minimalis yang dioptimalkan untuk sistem perekrutan otomatis di Indonesia.' },
    { property: 'og:title', content: 'Pembuat CV ATS-Friendly — JobFinder' },
    { property: 'og:description', content: 'Buat CV ATS-friendly dengan panduan AI. Template profesional dan siap lamar.' },
  ]
})

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend, Title, BarElement, CategoryScale, LinearScale, ArcElement)

// ===== TEMPLATES =====
const CV_TEMPLATES = [
  { id: 'modern_ats', name: 'Modern ATS', desc: 'Single column, minimalis & bersih.', isDefault: true },
  { id: 'classic_ats', name: 'Classic ATS', desc: 'Format akademis formal + Referensi.', isDefault: false },
  { id: 'executive_ats', name: 'Executive ATS', desc: 'Dua kolom premium untuk posisi senior.', isDefault: false },
]

const TEMPLATE_COMPONENT_MAP = {
  modern_ats: ModernATSTemplate,
  classic_ats: ClassicATSTemplate,
  executive_ats: ExecutiveATSTemplate,
}

const TEMPLATE_DEFAULT_FONT = {
  modern_ats: "'Calibri', sans-serif",
  classic_ats: "'Times New Roman', serif",
  executive_ats: "'Cambria', serif",
}

// Steps didefinisikan statis agar sidebar muncul langsung tanpa harus menunggu komponen di-mount
const TEMPLATE_STEPS = {
  modern_ats: [
    { id: 'personal_info', title: 'Informasi Pribadi' },
    { id: 'summary', title: 'Ringkasan Profesional' },
    { id: 'education', title: 'Pendidikan' },
    { id: 'organization', title: 'Pengalaman Organisasi' },
    { id: 'experience', title: 'Pengalaman Kerja' },
    { id: 'skills', title: 'Keahlian' },
    { id: 'certifications', title: 'Sertifikasi' },
  ],
  classic_ats: [
    { id: 'personal_info', title: 'Informasi Pribadi' },
    { id: 'objective', title: 'Tujuan Karir' },
    { id: 'education', title: 'Pendidikan' },
    { id: 'experience', title: 'Pengalaman Kerja' },
    { id: 'skills', title: 'Keahlian' },
    { id: 'references', title: 'Referensi' },
  ],
  executive_ats: [
    { id: 'personal_info', title: 'Informasi Pribadi' },
    { id: 'exec_summary', title: 'Executive Summary' },
    { id: 'competencies', title: 'Core Competencies' },
    { id: 'experience', title: 'Pengalaman Profesional' },
    { id: 'education', title: 'Pendidikan' },
    { id: 'achievements', title: 'Key Achievements' },
  ],
}

// ===== STATE =====
const selectedTemplate = ref('modern_ats')
const currentStep = ref(0)
const maxStepReached = ref(0)
const targetExpertise = ref('Software Development')
const expertiseAreas = ref(['IT Infra', 'Graphic Design', 'Software Development', 'Data Science', 'UI/UX Design', 'Digital Marketing', 'Content Writing', 'Mobile Development', 'DevOps', 'Cyber Security', 'AI / Machine Learning', 'Product Management', 'Others'])

const templateRef = ref(null)
const previewTemplateRef = ref(null)
const analyzing = ref(false)
const analysisResult = ref(null)

// Font state
const selectedFont = ref('')
const selectedFontName = ref('')
const hoveredFont = ref('')
const googleFonts = ref([])
const fontLoading = ref(false)
const fontSearch = ref('')
const loadedFonts = ref([])
const fontListRef = ref(null)

// System fonts (tidak perlu di-load dari Google Fonts)
const SYSTEM_FONTS = [
  { family: 'Times New Roman', category: 'serif', system: true },
  { family: 'Georgia', category: 'serif', system: true },
  { family: 'Garamond', category: 'serif', system: true },
  { family: 'Arial', category: 'sans-serif', system: true },
  { family: 'Helvetica', category: 'sans-serif', system: true },
  { family: 'Calibri', category: 'sans-serif', system: true },
  { family: 'Verdana', category: 'sans-serif', system: true },
  { family: 'Tahoma', category: 'sans-serif', system: true },
  { family: 'Courier New', category: 'monospace', system: true },
]

// ===== COMPUTED =====
const activeTemplateComponent = computed(() => TEMPLATE_COMPONENT_MAP[selectedTemplate.value])
const activeSteps = computed(() => TEMPLATE_STEPS[selectedTemplate.value] || [])
const totalSteps = computed(() => 1 + activeSteps.value.length + 1) // 0: template select, 1..N: form, N+1: preview
const ExpertiseOptions = computed(() => expertiseAreas.value.map(a => ({ value: a, label: a })))

const templateFont = computed(() => {
  if (selectedFont.value) return `'${selectedFont.value}', sans-serif`
  return TEMPLATE_DEFAULT_FONT[selectedTemplate.value] || "'Calibri', sans-serif"
})

const hasPreviewData = computed(() => {
  return templateRef.value?.hasPreviewData || previewTemplateRef.value?.hasPreviewData || false
})

const filteredSystemFonts = computed(() => {
  if (!fontSearch.value.trim()) return SYSTEM_FONTS
  const q = fontSearch.value.trim().toLowerCase()
  return SYSTEM_FONTS.filter(f => f.family.toLowerCase().includes(q))
})

const filteredGoogleFonts = computed(() => {
  let list = googleFonts.value
  if (fontSearch.value.trim()) {
    const q = fontSearch.value.trim().toLowerCase()
    list = list.filter(f => f.family.toLowerCase().includes(q))
  }
  return list
})

// ===== FONT FUNCTIONS =====
async function fetchGoogleFonts() {
  fontLoading.value = true
  try {
    const res = await fetch('/api/google-fonts')
    if (!res.ok) throw new Error()
    googleFonts.value = await res.json()
  } catch { } finally { fontLoading.value = false }
}

async function loadFont(family) {
  if (loadedFonts.value.includes(family)) return
  const id = `gf-${family.replace(/\s+/g, '-')}`
  if (!document.getElementById(id)) {
    const link = document.createElement('link')
    link.id = id; link.rel = 'stylesheet'
    link.href = `https://fonts.googleapis.com/css2?family=${encodeURIComponent(family)}:wght@400;700&display=swap`
    document.head.appendChild(link)
  }
  try { await document.fonts.load(`16px '${family}'`) } catch { }
  if (!loadedFonts.value.includes(family)) loadedFonts.value = [...loadedFonts.value, family]
}

function onFontHover(family) {
  hoveredFont.value = family
  if (!loadedFonts.value.includes(family)) loadFont(family)
}

async function selectFont(f) {
  selectedFont.value = f.family; selectedFontName.value = f.family; hoveredFont.value = ''
  if (!f.system) await loadFont(f.family)
}


// ===== NAVIGATION =====
function isStepValid(stepIndex) {
  if (stepIndex === 0) return true // template select always valid
  if (stepIndex >= totalSteps.value - 1) return true // preview step
  const internalIdx = stepIndex - 1
  return templateRef.value?.validate(internalIdx) ?? true
}

function nextStep() {
  if (isStepValid(currentStep.value)) {
    if (currentStep.value < totalSteps.value - 1) {
      currentStep.value++
      if (currentStep.value > maxStepReached.value) maxStepReached.value = currentStep.value
    }
  } else {
    const stepId = activeSteps.value[currentStep.value - 1]?.id
    if (stepId === 'education') alert('Harap tambahkan minimal satu data pendidikan.')
    else if (stepId === 'experience') alert('Harap tambahkan minimal satu pengalaman kerja.')
    else if (stepId === 'competencies') alert('Harap isi minimal 3 kompetensi inti.')
    else if (stepId === 'achievements') alert('Harap isi minimal 1 pencapaian utama.')
    else alert('Harap lengkapi semua field yang wajib (*) sebelum melanjutkan.')
  }
}

function prevStep() { if (currentStep.value > 0) currentStep.value-- }

function goToStep(index) {
  if (index <= maxStepReached.value) { currentStep.value = index; return }
  if (index === currentStep.value + 1 && isStepValid(currentStep.value)) {
    currentStep.value = index
    if (index > maxStepReached.value) maxStepReached.value = index
  }
}

// ===== ATS ANALYSIS =====
const doughnutOptions = { responsive: true, maintainAspectRatio: false, cutout: '75%', plugins: { legend: { display: false }, tooltip: { enabled: false } } }

const overallChartData = computed(() => {
  const score = analysisResult.value?.analysis?.overallScore || 0
  return { labels: ['Score', 'Remaining'], datasets: [{ data: [score, 100 - score], backgroundColor: ['#ffffff', 'rgba(255,255,255,0.08)'], borderWidth: 0 }] }
})

const atsChartData = computed(() => {
  const score = analysisResult.value?.ats?.score || 0
  const color = score >= 25 ? '#00a87e' : '#e23b4a'
  return { labels: ['Score', 'Remaining'], datasets: [{ data: [score, 100 - score], backgroundColor: [color, 'rgba(255,255,255,0.08)'], borderWidth: 0 }] }
})

const lineOptions = { responsive: true, maintainAspectRatio: false, scales: { y: { min: 0, max: 100, ticks: { color: '#8d969e' }, grid: { color: 'rgba(255,255,255,0.06)' } }, x: { ticks: { color: '#8d969e' }, grid: { display: false } } }, plugins: { legend: { display: false } } }

const lineChartData = computed(() => {
  const cats = analysisResult.value?.analysis?.categories || {}
  return { labels: ['Skills', 'Experience', 'Education', 'Projects', 'Certificates', 'Soft Skills'], datasets: [{ label: 'Skor Kategori', data: [cats.Skills || 0, cats.Experience || 0, cats.Education || 0, cats.Projects || 0, cats.Certificates || 0, cats.SoftSkills || 0], borderColor: '#ffffff', backgroundColor: 'rgba(90, 90, 90, 0.3)', pointBackgroundColor: '#ffffff', fill: true, tension: 0.4 }] }
})

async function analyzeBuiltCV() {
  analyzing.value = true; analysisResult.value = null
  const cvText = templateRef.value?.getTextForAnalysis?.() || previewTemplateRef.value?.getTextForAnalysis?.() || ''
  try {
    const form = new FormData()
    form.append('expertise', targetExpertise.value)
    form.append('cv', new Blob([cvText], { type: 'text/plain' }), 'cv.txt')
    const { data } = await axios.post('/api/cv/analyze', form)
    if (data.analysis?.error) { analysisResult.value = data; return }
    if (data.analysis?.overallScore !== undefined) { analysisResult.value = data }
    else { analysisResult.value = { analysis: { error: true, message: 'Analisis gagal atau kosong.' }, ats: { isATS: false, score: 0, matchedSections: [], totalSections: 0 } } }
  } catch { analysisResult.value = { analysis: { error: true, message: 'Gagal memindai CV. Silakan coba lagi.' }, ats: { isATS: false, score: 0, matchedSections: [], totalSections: 0 } } }
  finally { analyzing.value = false }
}

function downloadPDF() { window.print() }

// ===== LIFECYCLE =====
onMounted(async () => {
  try {
    const [areaRes] = await Promise.all([axios.get('/api/expertise-areas')])
    expertiseAreas.value = areaRes.data
  } catch { }
  fetchGoogleFonts()

  const savedTemplate = localStorage.getItem('jobfinder_cv_template_v2')
  if (savedTemplate) selectedTemplate.value = savedTemplate
  const savedMaxStep = localStorage.getItem('jobfinder_cv_maxStep_v2')
  if (savedMaxStep) { try { maxStepReached.value = parseInt(savedMaxStep) || 0 } catch { } }
})

watch(selectedTemplate, val => {
  localStorage.setItem('jobfinder_cv_template_v2', val)
  currentStep.value = 0; maxStepReached.value = 0; analysisResult.value = null
})

watch(maxStepReached, val => localStorage.setItem('jobfinder_cv_maxStep_v2', val.toString()))
</script>

<style scoped>
.animate-fade-in { animation: fadeIn 0.5s ease-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
</style>

<style>
@media print {
  @page { margin: 0; size: A4 portrait; }
  body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  body * { visibility: hidden; }
  .print\:block { visibility: visible !important; }
  .print\:block * { visibility: visible; }
}
</style>