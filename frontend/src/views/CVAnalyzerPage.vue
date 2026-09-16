<template>
  <div class="min-h-screen pt-[50px] md:pt-[88px] bg-canvas-dark text-on-dark font-sans">
    <div class="w-full mx-auto px-[32px] md:px-[72px]">
      <p class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-stone mb-xs">ATS Simulator</p>
      <h1 class="text-[32px] md:text-[40px] font-medium leading-[1.2] tracking-[-0.4px] mb-sm text-on-dark">CV Analyzer</h1>
      <p class="text-[12px] md:text-[16px] font-normal leading-[1.56] tracking-[-0.09px] text-on-dark-mute mb-xl">Unggah CV Anda untuk mendapatkan analisis mendalam berbasis AI dan simulasi sistem ATS.</p>

      <section class="bg-[#191919] border border-hairline-dark rounded-[15px] p-xl mb-xl">
        <div class="mb-md gap-sm">
          <label class="mb-lg block text-on-dark font-medium text-lg" for="cv-upload">Unggah Dokumen CV (PDF)</label>
          <div class="flex gap-md items-center flex-wrap">
            
            <div class="relative flex-1 min-w-[200px] h-[200px]">
              <label
                class="absolute inset-0 bg-[#191919] border-2 border-dashed border-hairline-dark rounded-sm flex items-center justify-center px-4 cursor-pointer hover:bg-surface-elevated"
              >
                <input
                  id="cv-upload"
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
          </div>

          <div v-if="file" class="flex-1 min-w-[200px] border border-hairline-dark rounded-sm mt-md">
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

           <button class="inline-flex items-center justify-center font-medium rounded-full transition-all duration-200 cursor-pointer bg-on-dark text-ink hover:bg-white/90 px-[24px] h-[48px] text-[14px] md:text-[16px] whitespace-nowrap disabled:opacity-50 disabled:cursor-not-allowed mt-md" @click="analyze" :disabled="analyzing || !file">
              {{ analyzing ? 'Menganalisis...' : 'Analisis Dokumen' }}
            </button>
        </div>
      </section>

      <div v-if="result" class="animate-fade-in">
        <h2 class="text-[24px] font-medium leading-[1.33] tracking-[0] mb-xl text-on-dark">Laporan Analisis</h2>

        <!-- Error Handling -->
        <div v-if="result.analysis?.error" class="bg-accent-danger text-white rounded-[20px] p-xxl mb-xl">
          Gagal menganalisis CV: {{ result.analysis.message }}
        </div>

        <template v-else>
          <!-- Score Summary -->
          <div class="grid grid-cols-1 lg:grid-cols-[2fr_3.5fr] gap-lg mb-lg">
            <!-- KIRI: AI Summary (atas) + Score Dashboard (bawah) -->
            <div class="col-span-1 flex flex-col gap-lg">

              <!-- Kolom 1: AI Analysis Summary -->
              <div class="min-w-0 bg-[#191919] rounded-[15px] p-[20px] flex flex-col border border-hairline-dark">
                <div class="inline-flex items-center gap-[12px] mb-xs">
                  <div class="flex items-center justify-center w-5 h-5 text-white">
                    <Icon icon="octicon:sparkle-fill-16" width="30" />
                  </div>
                  <h2 class="font-mono text-[15px] font-semibold text-white">AI Analysis Summary</h2>
                </div>
                <p class="text-[10px] md:text-sm font-normal leading-[1.56] tracking-[-0.09px] text-on-dark-mute">Review your resume performance, discover improvement areas, and get actionable recommendations from AI.</p>
              </div>

              <!-- Kolom 2: Score Dashboard (CV Analyzer) -->
              <div class="min-w-0 bg-[#191919] rounded-[15px] p-[20px] border border-hairline-dark">
                <!-- Header: CV Analyzer / ATS Evaluation -->
                <div class="flex items-center justify-between border-b border-[#313131] pb-2">
                  <h2 class="font-mono text-[12px] md:text-[15px] text-stone">CV Analyzer <span class="font-semibold text-white">/ ATS Evaluation</span></h2>
                  <span class="font-mono text-[12px] md:text-[15px] text-white"><CountUp :to="result.ats?.score ?? 0" suffix="%" /></span>
                </div>

                <!-- Score & Quality -->
                <div class="grid grid-cols-[2fr_1fr] gap-lg mt-lg">
                  <!-- Kolom kiri -->
                  <div class="flex flex-col gap-lg">
                    <h3 class="font-mono text-[8px] md:text-[10px] font-medium leading-[1.33] tracking-[0.5px] text-[#787676]">
                      OVERALL RESUME SCORE
                    </h3>

                    <p class="font-mono text-[60px] leading-none text-white">
                      <CountUp :to="result.ats?.score ?? 0" /><span class="text-[20px] text-on-dark-mute">%</span>
                    </p>
                  </div>

                  <!-- Kolom kanan -->
                  <div class="flex flex-col gap-xs">
                    <h3 class="font-mono text-[8px] md:text-[10px] font-medium leading-[1.33] tracking-[0.5px] text-[#787676]">
                      RESUME QUALITY
                    </h3>

                    <p
                      class="font-mono text-[15px] font-medium leading-none"
                      :class="qualityTone.color"
                    >
                      {{ qualityTone.label }}
                    </p>
                  </div>
                </div>

                <!-- Progress Bar -->
                <div class="mt-xl">
                  <div class="relative h-[13px] w-full overflow-hidden">
                    <!-- Background segmented -->
                    <div
                      class="absolute inset-0"
                      style="
                        background: repeating-linear-gradient(
                          to right,
                          #29292d 0px,
                          #29292d 4px,
                          transparent 4px,
                          transparent 7px
                        );
                      "
                    ></div>

                    <!-- Filled score (bergerak bareng angka count-up) -->
                    <div
                      class="absolute left-0 top-0 h-full bg-white"
                      :style="{ width: `${atsPercent}%` }"
                    ></div>
                  </div>

                  <!-- Scale -->
                  <div class="mt-sm flex justify-between font-mono text-[10px] text-on-dark-mute border-b border-[#313131] pb-5">
                    <span>0%</span>
                    <span>25%</span>
                    <span>50%</span>
                    <span>75%</span>
                    <span>100%</span>
                  </div>

                  <div class="mt-lg">
                    <h3 class="font-mono text-[8px] md:text-[10px] font-medium leading-[1.33] tracking-[0.5px] text-[#787676]">ANALYSIS BREAKDOWN</h3>
                    <div class="grid grid-cols-2 gap-x-xs gap-y-xxs mt-sm">
                     <div
                        v-for="item in analysisBreakdown"
                        :key="item.key"
                        class="flex items-center gap-xs"
                      >
                        <svg
                          width="15"
                          height="15"
                          viewBox="0 0 24 24"
                          fill="none"
                          xmlns="http://www.w3.org/2000/svg"
                          class="text-white"
                        >
                          <!-- Outer diamond -->
                          <path
                            d="M12 2L22 12L12 22L2 12L12 2Z"
                            stroke="currentColor"
                            stroke-width="2.8"
                            stroke-linejoin="round"
                          />

                          <!-- Inner diamond -->
                          <path
                            d="M12 7L17 12L12 17L7 12L12 7Z"
                            fill="currentColor"
                          />
                        </svg>

                        <span class="text-[10px]">{{ item.label }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- KANAN: 1 kolom (ANALISIS KATEGORI) -->
            <div class="col-span-1 min-w-0 bg-[#191919] rounded-[15px] p-xl border border-hairline-dark">
              <div class="flex items-center justify-between mb-xl">
                <h3 class="font-mono text-[16px] sm:text-[18px] lg:text-[20px] font-medium tracking-[1px] text-white">ANALISIS KATEGORI</h3>
                <div class="w-[30px] h-[30px] rounded-[5px] border border-hairline-dark flex items-center justify-center shrink-0">
                  <Icon icon="ant-design:more-outlined" class="text-on-dark-mute"/>
                </div>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-lg">
                <div
                  v-for="card in categoryCards"
                  :key="card.label"
                  class="min-w-0 bg-[#1F1F1F] px-4 py-3 rounded-sm border border-[#444444]"
                >
                  <div class="flex items-center justify-between gap-2">
                    <div class="flex items-center gap-2">
                      <div class="w-[32px] h-[32px] rounded-full flex items-center justify-center bg-[#19181B] shrink-0">
                        <Icon :icon="card.icon" width="22"/>
                      </div>
                      <span class="text-[13px] sm:text-[15px] truncate">{{ card.label }}</span>
                    </div>

                    <Icon icon="fluent-mdl2:more" class="shrink-0"/>
                  </div>
                  <div class="bg-[#181818] px-4 py-4 sm:py-5 border border-[#4C4C4C] rounded-sm mt-sm">
                    <div class="flex items-center justify-between gap-2 flex-wrap">
                      <span class="text-3xl sm:text-4xl lg:text-5xl leading-none"><CountUp :to="card.value" suffix="/100" /></span>
                      <p class="text-[12px] sm:text-[14px] text-[#BBBBBB]">{{ card.status }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-[2fr_1fr_1fr] gap-lg mb-xl">
            <div class="w-full rounded-[15px] border border-hairline-dark bg-[#191919] p-xl">
            <!-- Header -->
            <div class="grid grid-cols-2 gap-3 md:grid-cols-[0.7fr_1.65fr_120px] items-center">
              <h3 class="font-sans text-[12px] font-semibold tracking-[-0.3px] text-white">
                ANALISIS KATEGORI
              </h3>

              <h3 class="font-sans text-[12px] font-semibold tracking-[-0.3px] text-white text-right md:text-left">
                VALUE
              </h3>

              <h3 class="hidden md:block font-sans text-[12px] font-semibold tracking-[-0.3px] text-white pl-3">
                STATUS
              </h3>
            </div>

            <!-- Rows -->
            <div class="mt-5 flex flex-col gap-4">
              <div
                v-for="item in analysisCategories"
                :key="item.label"
              >
                <!-- MOBILE: label + status bertumpuk, lalu progress di bawah -->
                <div class="md:hidden flex flex-col gap-1">
                  <div class="flex min-w-0 items-center gap-2">
                    <Icon :icon="item.icon" class="h-[13px] w-[13px] shrink-0 text-[#85858b]" />
                    <span class="truncate font-sans text-[10px] font-normal tracking-[-0.3px] text-[#85858b]">
                      {{ item.label }}
                    </span>
                  </div>

                  <span class="font-sans text-[10px] font-normal tracking-[-0.3px] text-white">
                    {{ item.status }}
                  </span>

                  <div class="flex min-w-0 items-center gap-2">
                    <div class="flex-1 min-w-0">
                      <CountUpBar :to="item.value" />
                    </div>
                    <span class="w-[42px] shrink-0 font-sans text-[12px] font-medium tracking-[-0.3px] text-white">
                      <CountUp :to="item.value" suffix="%" />
                    </span>
                  </div>
                </div>

                <!-- DESKTOP: 3 kolom sejajar (tidak berubah) -->
                <div class="hidden md:grid grid-cols-[0.7fr_1.65fr_120px] items-center gap-3">
                  <!-- Category -->
                  <div class="flex min-w-0 items-center gap-2">
                    <Icon
                      :icon="item.icon"
                      class="h-[13px] w-[13px] shrink-0 text-[#85858b]"
                    />

                    <span class="truncate font-sans text-[10px] font-normal tracking-[-0.3px] text-[#85858b]">
                      {{ item.label }}
                    </span>
                  </div>

                  <!-- Progress + Value -->
                  <div class="flex min-w-0 items-center gap-2">
                    <div class="flex-1 min-w-0">
                      <CountUpBar :to="item.value" />
                    </div>

                    <span class="w-[42px] shrink-0 font-sans text-[12px] font-medium tracking-[-0.3px] text-white">
                      <CountUp :to="item.value" suffix="%" />
                    </span>
                  </div>

                  <!-- Status -->
                  <span class="shrink-0 font-sans text-[10px] font-normal tracking-[-0.3px] text-white pl-3">
                    {{ item.status }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-[#191919] rounded-[15px] p-xl border border-hairline-dark space-y-7">
            <h3 class="font-mono text-[18px] font-medium tracking-[1px] text-white mb-md">Keyword Analysis</h3>

            <div class="flex flex-col gap-xs">
              <div class="flex items-center gap-2">
                <span class="text-[12px] font-sans font-normal text-[#85858b]">Matched Keywords</span>
                <span class="text-[12px] font-sans font-normal text-white"><CountUp :to="keywordAnalysis.matchedCount" /></span>
              </div>

              <div class="flex items-center gap-2">
                <span class="text-[12px] font-sans font-normal text-[#85858b]">Missing Keywords</span>
                <span class="text-[12px] font-sans font-normal text-white"><CountUp :to="keywordAnalysis.missingCount" /></span>
              </div>
            </div>

            <div class="grid grid-cols-3 gap-2">
              <div
                v-for="(tag, idx) in keywordAnalysis.tags.slice(0, 5)"
                :key="tag + idx"
                class="px-5 py-1 border border-white rounded text-[12px] text-center truncate"
                :title="tag"
              >{{ tag }}</div>
            </div>

            <div class="flex items-baseline gap-4">
              <h3 class="text-[15px] leading-none font-medium text-white font-sans">Coverage</h3>
              <span class="text-[12px] leading-none font-normal text-white font-sans"><CountUp :to="keywordAnalysis.coverage" suffix="%" /></span>
            </div>
          </div>

          <div class="bg-[#191919] rounded-[15px] p-xl border border-hairline-dark space-y-3">
            <h3 class="font-mono text-[18px] font-medium tracking-[1px] text-white mb-md">AI Improvement Insights</h3>

            <div
              v-for="insight in improvementInsights"
              :key="insight.priority"
              class="flex flex-col gap-2"
            >
              <h3 class="text-[12px] font-semibold font-sans text-white">Priority {{ insight.priority }}</h3>
              <span class="text-[12px] font-light font-sans text-white">{{ insight.text }}</span>
            </div>
          </div>
        </div>

        <section>
          <!-- Section Header -->
          <div class="mb-xl flex items-center justify-between">
            <div>
              <h2 class="font-sans text-[20px] font-semibold tracking-[-0.7px] text-white">
                Jobs That Match Your Resume
              </h2>

              <p class="font-sans text-[12px] text-[#85858b]">
                Discover opportunities based on your resume profile.
              </p>
            </div>
          </div>

          <!-- Job Grid -->
          <div v-if="jobsLoading" class="py-xl text-center font-sans text-[13px] text-[#85858b]">
            Memuat lowongan yang cocok
          </div>

          <div v-else-if="!recommendedJobs.length" class="py-xl text-center font-sans text-[13px] text-[#85858b]">
            Belum ada lowongan yang cocok dengan CV Anda. Coba perbarui data lowongan di halaman Peluang.
          </div>

          <div v-else class="grid grid-cols-1 gap-lg md:grid-cols-2 xl:grid-cols-3">
            <article
              v-for="job in recommendedJobs"
              :key="job.id"
              class="rounded-[12px] border border-[#45454b] bg-[#1F1F1F] p-xl"
            >
              <!-- Job Header -->
              <div class="flex items-start justify-between gap-4">
                <div class="min-w-0">
                  <h3 class="font-sans text-[18px] sm:text-[20px] font-semibold leading-[1.2] tracking-[-0.6px] text-white">
                    {{ job.title }}
                  </h3>

                  <p class="mt-1 font-sans text-[15px] text-[#b5b5ba]">
                    {{ job.company }}
                  </p>
                </div>
              </div>

              <!-- Metadata -->
              <div class="mt-lg flex flex-wrap items-center gap-2">
                <span
                  v-for="meta in job.metadata"
                  :key="meta.label"
                  class="inline-flex items-center gap-2 rounded-full border border-[#85858b] px-4 py-2 font-sans md:text-[13px] text-[8px] text-[#b5b5ba]"
                >
                  <Icon
                    v-if="meta.icon"
                    :icon="meta.icon"
                    class="h-[14px] w-[14px]"
                  />

                  {{ meta.label }}
                </span>
              </div>

              <!-- Description (mobile: 2 baris, desktop: 3 baris) -->
              <p class="mt-lg line-clamp-2 lg:line-clamp-3 min-h-[38px] lg:min-h-[58px] font-sans md:text-[14px] text-[12px] leading-[1.6] text-[#b5b5ba]">
                {{ job.description || 'Deskripsi lowongan tidak tersedia. Klik "Apply Now" untuk melihat detail lengkap.' }}
              </p>

              <!-- Match Progress -->
              <div class="mt-sm">
                <CountUpBar :to="job.match" height-class="h-[6px]" />

                <div class="mt-2 flex items-center justify-between">
                  <span class="font-sans text-[13px] text-[#85858b]">
                    {{ job.matchLabel }}
                  </span>

                  <span class="font-sans text-[14px] font-semibold text-white">
                    <CountUp :to="job.match" suffix="%" />
                  </span>
                </div>
              </div>

              <!-- Action -->
              <div class="mt-lg flex justify-stretch sm:justify-end">
                <button
                  class="w-full sm:w-auto rounded-[6px] bg-white px-8 py-3 font-sans text-[14px] font-semibold text-[#111116] transition-opacity hover:opacity-85 disabled:opacity-40 disabled:cursor-not-allowed"
                  :disabled="!job.url"
                  @click="openJob(job.url)"
                >
                  Apply Now
                </button>
              </div>
            </article>
          </div>
        </section>
      </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import axios from "axios"
import { Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend, Title, CategoryScale, LinearScale, ArcElement } from 'chart.js'
import { Line, Doughnut } from 'vue-chartjs'
import { useHead } from "@vueuse/head"
import { Icon } from "@iconify/vue"
import CountUp from "../components/CountUp.vue"
import CountUpBar from "../components/CountUpBar.vue"
import { useCountUp } from "../composables/useCountUp"

useHead({
  title: 'Analisis CV & ATS Score ? JobFinder',
  meta: [
    { name: 'description', content: 'Unggah CV Anda dan dapatkan analisis mendalam berbasis AI. Simulasikan skor ATS, temukan kelemahan CV, dan dapatkan rekomendasi perbaikan yang komprehensif.' },
    { property: 'og:title', content: 'Analisis CV & ATS Score ? JobFinder' },
    { property: 'og:description', content: 'Simulasi ATS dan analisis CV berbasis AI untuk pencari kerja Indonesia.' },
  ]
})

// Helper: label status berdasarkan skor
function scoreStatus(score) {
  if (score >= 85) return 'EXCELLENT'
  if (score >= 70) return 'STRONG'
  if (score >= 55) return 'GOOD'
  if (score >= 40) return 'FAIR'
  return 'NEED WORKS'
}

// Tabel ANALISIS KATEGORI � dari categories AI
const CATEGORY_TABLE_MAP = [
  { key: 'TechnicalSkills', label: 'TECHNICAL SKILL', icon: 'solar:atom-linear' },
  { key: 'Experience',      label: 'EXPERIENCE',      icon: 'solar:case-linear' },
  { key: 'Education',       label: 'EDUCATION',       icon: 'solar:square-academic-cap-linear' },
  { key: 'Projects',        label: 'PROJECTS',        icon: 'solar:layers-minimalistic-linear' },
  { key: 'Certificates',    label: 'CERTIFICATES',    icon: 'solar:clipboard-list-linear' },
  { key: 'SoftSkills',      label: 'SOFT SKILL',      icon: 'solar:chart-2-linear' },
]

const analysisCategories = computed(() => {
  const categories = result.value?.analysis?.categories || {}
  return CATEGORY_TABLE_MAP.map((item) => {
    const value = Number(categories[item.key] ?? 0)
    return { ...item, value, status: scoreStatus(value) }
  })
})

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend, Title, CategoryScale, LinearScale, ArcElement)


const file = ref({ name: 'Contoh_CV_Development.pdf', size: 145200 })
const analyzing = ref(false)

// Mock data untuk keperluan development & preview styling (ganti ke null saat production)
const mockResult = {
  ats: {
    score: 85,
    isATS: true,
    matchedSections: ['Summary', 'Experience', 'Education', 'Skills', 'Contact'],
    totalSections: 5
  },
  eligible: true,
  analysis: {
    summary: "CV menunjukkan pengalaman yang sangat solid di bidang pengembangan web front-end dan back-end dengan penguasaan teknologi modern seperti Vue.js, Node.js, dan Python. Struktur dan penamaan bagian sudah memenuhi standar sistem ATS.",
    categories: {
      "TechnicalSkills": 80,
      "Experience": 75,
      "Education": 90,
      "Projects": 60,
      "Certificates": 50,
      "SoftSkills": 85
    },
    strengths: [
      "Format penulisan bersih dan mudah diparsing oleh parser ATS.",
      "Penggunaan kata kerja aksi yang kuat pada deskripsi pengalaman kerja.",
      "Pencantuman metrik dan hasil pencapaian yang terukur."
    ],
    weaknesses: [
      "Beberapa kata kunci industri spesifik belum dicantumkan pada bagian keahlian.",
      "Sertifikasi profesional belum dilampirkan secara lengkap."
    ],
    keywordMatch: ["Vue.js", "JavaScript", "TypeScript", "Node.js", "TailwindCSS", "REST API", "Git"],
    missingSkills: ["Docker", "CI/CD", "GraphQL", "AWS"],
    recommendations: [
      "Tambahkan sertifikasi atau pelatihan terkait Cloud Computing untuk meningkatkan daya saing.",
      "Sertakan link portofolio GitHub atau proyek live yang dapat diakses langsung oleh rekruter.",
      "Optimalkan bagian ringkasan profil agar lebih menonjolkan dampak bisnis dari proyek terdahulu."
    ]
  }
}

const result = ref(mockResult)

// Persentase ATS yang bergerak dari 0 � dipakai untuk mengisi progress bar,
// agar bar bergerak berbarengan dengan angka count-up (satu sumber animasi).
const atsTarget = computed(() => Number(result.value?.ats?.score ?? 0) || 0)
const { percent: atsPercent } = useCountUp(atsTarget, { duration: 1100, max: 100 })

// Klasifikasi kualitas resume berdasarkan skor ATS
const qualityTone = computed(() => {
  const score = result.value?.ats?.score ?? 0
  if (score >= 85) return { label: 'Excellent', color: 'text-accent-teal' }
  if (score >= 70) return { label: 'Good', color: 'text-emerald-400' }
  if (score >= 50) return { label: 'Fair', color: 'text-yellow-400' }
  return { label: 'Poor', color: 'text-accent-danger' }
})

// Item ANALYSIS BREAKDOWN ? status "relevan" (diamond solid) bila skor kategori >= 70
const ANALYSIS_BREAKDOWN_MAP = [
  { key: 'keywords',     label: 'Keywords Match',   category: 'TechnicalSkills' },
  { key: 'experience',   label: 'Experience',       category: 'Experience' },
  { key: 'skills',       label: 'Skills Relevance', category: 'SoftSkills' },
  { key: 'structure',    label: 'Resume Structure', category: 'Education' },
]

const analysisBreakdown = computed(() => {
  const categories = result.value?.analysis?.categories || {}
  return ANALYSIS_BREAKDOWN_MAP.map((item) => {
    const score = categories[item.category] ?? 0
    return { ...item, score, relevant: score >= 70 }
  })
})

// 4 kartu besar ANALISIS KATEGORI � dari categories AI
const CATEGORY_CARDS_MAP = [
  { key: 'TechnicalSkills', label: 'ATS Compatibility', icon: 'humbleicons:shield-check' },
  { key: 'SoftSkills',      label: 'Keyword Matching',  icon: 'iconmind:text-search-duotone-regular' },
  { key: 'Education',       label: 'Format Check',      icon: 'fluent:document-text-24-regular' },
  { key: 'Experience',      label: 'Readability',       icon: 'bx:briefcase-alt-2' },
]

const categoryCards = computed(() => {
  const categories = result.value?.analysis?.categories || {}
  return CATEGORY_CARDS_MAP.map((item) => {
    const value = Math.round(Number(categories[item.key] ?? 0))
    return { ...item, value, status: scoreStatus(value) }
  })
})

// Keyword Analysis � dari keywordMatch & missingSkills AI
const keywordAnalysis = computed(() => {
  const a = result.value?.analysis || {}
  const matched = a.keywordMatch || []
  const missing = a.missingSkills || []
  const total = matched.length + missing.length
  const coverage = total > 0 ? Math.round((matched.length / total) * 100) : 0
  return {
    matchedCount: matched.length,
    missingCount: missing.length,
    coverage,
    tags: [...matched, ...missing],
  }
})

// AI Improvement Insights � dari recommendations AI
const improvementInsights = computed(() => {
  const recs = result.value?.analysis?.recommendations || []
  return recs.slice(0, 3).map((text, i) => ({
    priority: String(i + 1).padStart(2, '0'),
    text,
  }))
})

// ---------- Job Recommendations (dari database) ----------
const allJobs = ref([])
const jobsLoading = ref(false)

async function loadJobs() {
  jobsLoading.value = true
  try {
    const { data } = await axios.get("/api/jobs", { params: { limit: 500 } })
    allJobs.value = data?.jobs || []
  } catch {
    allJobs.value = []
  } finally {
    jobsLoading.value = false
  }
}

// Token peran/posisi teknologi (untuk mencocokkan judul lowongan)
const ROLE_TOKENS = [
  "developer", "engineer", "programmer", "software", "frontend", "front-end",
  "backend", "back-end", "fullstack", "full-stack", "web", "data", "devops",
  "cloud", "qa", "tester", "it ", "analytics", "machine learning",
]

// Token teknologi (dicari di judul, expertise, dan deskripsi)
const TECH_TOKENS = [
  "react", "vue", "node", "python", "java", "php", "laravel", "django", "sql",
  "database", "api", "aws", "docker", "kubernetes", "typescript", "javascript",
  "html", "css", "tailwind", "git", "mongodb", "postgres", "redis", "golang",
  "kotlin", "swift", "flutter", "android", "ios", "machine learning",
  "artificial intelligence", "figma", "ux design", "ui design",
]

// Hitung skor kecocokan CV vs job (0-100)
function computeMatch(job, cvKeywords) {
  const title = String(job.title || "").toLowerCase()
  const expertise = String(job.expertise || "").toLowerCase()
  const desc = String(job.description || "").toLowerCase()
  const haystack = `${title} ${expertise} ${desc}`

  let pts = 0

  // 1) Peran teknologi cocok di judul (bobot terbesar)
  if (ROLE_TOKENS.some((t) => title.includes(t))) pts += 40

  // 2) Teknologi cocok di mana saja
  const techHits = TECH_TOKENS.filter((t) => haystack.includes(t)).length
  if (techHits > 0) pts += Math.min(35, techHits * 12)

  // 3) Keyword spesifik dari CV (hasil analisis)
  const cvHits = cvKeywords.filter((k) => {
    const term = String(k).toLowerCase().trim()
    return term && haystack.includes(term)
  }).length
  if (cvHits > 0) pts += Math.min(25, cvHits * 8)

  return Math.min(100, pts)
}

// Keyword dari hasil analisis CV (skill cocok + skill kurang)
function cvMatchTerms() {
  const a = result.value?.analysis || {}
  return [...(a.keywordMatch || []), ...(a.missingSkills || [])].map((k) => String(k))
}

function matchLabel(score) {
  if (score >= 70) return "Strong Match"
  if (score >= 50) return "Good Match"
  if (score >= 30) return "Fair Match"
  return "Low Match"
}

const recommendedJobs = computed(() => {
  if (!allJobs.value.length) return []
  const terms = cvMatchTerms()

  return allJobs.value
    .map((job) => ({ job, score: computeMatch(job, terms) }))
    .filter((x) => x.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 6)
    .map(({ job, score }) => {
      const metadata = []
      if (job.location) metadata.push({ label: job.location, icon: "solar:map-point-linear" })
      if (job.jobType) metadata.push({ label: job.jobType })
      if (job.expertise && job.expertise !== "Others") metadata.push({ label: job.expertise })

      const description = String(job.description || "").replace(/\s+/g, " ").trim()

      return {
        id: job.id,
        title: job.title || "Untitled",
        company: job.company || "",
        url: job.url || "",
        match: score,
        matchLabel: matchLabel(score),
        metadata,
        description: description.length > 180 ? description.slice(0, 180) + "�" : description,
      }
    })
})

function openJob(url) {
  if (url) window.open(url, "_blank", "noopener,noreferrer")
}

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

// Chart Configurations ? cobalt violet palette
const doughnutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '75%',
  plugins: { legend: { display: false }, tooltip: { enabled: false } }
}

const atsChartData = computed(() => {
  const score = result.value?.ats?.score || 0
  return {
    labels: ['Score', 'Remaining'],
    datasets: [{
      data: [score, 100 - score],
      backgroundColor: ['#ffffff', 'rgba(255,255,255,0.08)'],
      borderWidth: 0
    }]
  }
})

const lineOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: { mode: 'index', intersect: false },
  scales: { 
    y: { 
      min: 0, 
      max: 100, 
      ticks: { 
        color: '#8d969e',
        stepSize: 20,
        font: { size: 10 }
      }, 
      grid: { color: 'rgba(255, 255, 255, 0.06)' } 
    },
    x: { 
      ticks: { color: '#8d969e', font: { size: 10, weight: 500 } }, 
      grid: { display: false } 
    }
  },
  plugins: { 
    legend: { display: false },
    tooltip: {
      backgroundColor: '#171717',
      titleColor: '#ffffff',
      bodyColor: '#ffffff',
      borderColor: 'rgba(255, 255, 255, 0.2)',
      borderWidth: 1,
      padding: 10,
      displayColors: false,
      callbacks: {
        label: (context) => `Skor: ${context.raw}/100`
      }
    }
  }
}

const doughnutGradientPlugin = {
  id: 'doughnutGradient',
  beforeDatasetsDraw(chart) {
    const { ctx, chartArea } = chart
    if (!chartArea) return

    const centerX = (chartArea.left + chartArea.right) / 2
    const centerY = (chartArea.top + chartArea.bottom) / 2
    const score = result.value?.ats?.score || 0
    const fraction = Math.min(Math.max(score / 100, 0.01), 1)

    if (typeof ctx.createConicGradient === 'function') {
      const gradient = ctx.createConicGradient(-Math.PI / 2, centerX, centerY)
      gradient.addColorStop(0, 'rgba(255,255,255,0.08)')
      gradient.addColorStop(fraction, '#ffffff')

      chart.data.datasets[0].backgroundColor = [gradient, 'rgba(255, 255, 255, 0.08)']

      const meta = chart.getDatasetMeta(0)
      if (meta?.data?.[0]) {
        meta.data[0].options.backgroundColor = gradient
      }
    }
  }
}

const lineGradientPlugin = {
  id: 'lineGradient',
  beforeDatasetsDraw(chart) {
    const { ctx, chartArea } = chart
    if (!chartArea) return
    const gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom)
    gradient.addColorStop(0, 'rgba(255, 255, 255, 0.12)')
    gradient.addColorStop(1, 'rgba(255, 255, 255, 0)')
    chart.data.datasets[0].backgroundColor = gradient
  }
}

// Garis vertikal (crosshair) yang mengikuti titik data saat hover
const crosshairPlugin = {
  id: 'crosshair',
  afterDatasetsDraw(chart) {
    const active = chart.tooltip?._active
    if (!active?.length) return
    const { ctx, chartArea } = chart
    if (!chartArea) return
    const x = active[0].element.x
    ctx.save()
    ctx.beginPath()
    ctx.setLineDash([4, 4])
    ctx.moveTo(x, chartArea.top)
    ctx.lineTo(x, chartArea.bottom)
    ctx.lineWidth = 1
    ctx.strokeStyle = 'rgba(255,255,255,0.45)'
    ctx.stroke()
    ctx.restore()
  }
}

const lineChartData = computed(() => {
  const cats = result.value?.analysis?.categories || {}
  return {
    labels: ['Technical Skills', 'Experience', 'Education', 'Projects', 'Certificates', 'Soft Skills'],
    datasets: [{
      label: 'Skor Kategori',
      data: [
        cats.TechnicalSkills ?? cats.Skills ?? 0,
        cats.Experience || 0,
        cats.Education || 0,
        cats.Projects || 0,
        cats.Certificates || 0,
        cats.SoftSkills || 0,
      ],
      borderColor: '#ffffff',
      borderWidth: 2,
      fill: true,
      tension: 0.4,
      pointBackgroundColor: '#ffffff',
      pointBorderColor: '#ffffff',
      pointRadius: 3,
      pointHoverRadius: 4.5,
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

// Muat daftar lowongan dari database saat halaman dibuka
onMounted(() => {
  loadJobs()
})

</script>

<style scoped>
/* Scoped styles removed because we used Tailwind */
</style>
