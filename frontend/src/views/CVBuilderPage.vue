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

        <div class="mb-[24px] px-[16px]">
          <label class="text-[12px] mb-[4px] text-on-dark-mute block font-semibold">Target Keahlian / Bidang</label>
          <select v-model="targetExpertise" class="w-full text-[14px] bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none appearance-none">
            <option v-for="a in expertiseAreas" :key="a" :value="a" class="bg-surface-elevated text-on-dark">{{ a }}</option>
          </select>
        </div>
        
        <ul class="list-none m-0 p-0 flex md:block overflow-x-auto md:overflow-visible pb-[12px] md:pb-0">
          <li v-for="(section, index) in steps" :key="section.id" 
              class="flex shrink-0 items-center px-[16px] py-[12px] rounded-none transition-all duration-200 text-on-dark-mute hover:bg-surface-deep border-b-[3px] md:border-b-0 md:border-l-[3px] border-transparent"
              :class="{ 
                'bg-surface-deep !text-on-dark font-medium !border-white': currentStep === index, 
                'cursor-pointer': index <= maxStepReached || index === currentStep + 1,
                'opacity-50 cursor-not-allowed': index > maxStepReached && index !== currentStep + 1
              }"
              @click="goToStep(index)">
            <div class="w-[28px] h-[28px] rounded-full border border-hairline-dark flex items-center justify-center text-[12px] mr-[12px] shrink-0 transition-colors" :class="{ 'bg-white text-ink border-white': index < maxStepReached || (index < currentStep) }">{{ index + 1 }}</div>
            <div class="text-[14px]">{{ section.title }}</div>
          </li>
          <li class="flex shrink-0 items-center px-[16px] py-[12px] rounded-none transition-all duration-200 text-on-dark-mute hover:bg-surface-deep border-b-[3px] md:border-b-0 md:border-l-[3px] border-transparent"
              :class="{ 
                'bg-surface-deep !text-on-dark font-medium !border-white': currentStep === steps.length,
                'cursor-pointer': steps.length <= maxStepReached,
                'opacity-50 cursor-not-allowed': steps.length > maxStepReached
              }" 
              @click="goToStep(steps.length)">
            <div class="w-[28px] h-[28px] rounded-full border border-hairline-dark flex items-center justify-center text-[12px] mr-[12px] shrink-0 transition-colors" :class="{ 'bg-white text-ink border-white': maxStepReached >= steps.length }">✓</div>
            <div class="text-[14px]">Preview &amp; Export</div>
          </li>
        </ul>
      </aside>

      <!-- Main Content Panel -->
      <main class="flex-grow min-w-0 bg-surface-elevated rounded-[20px] p-xl md:p-xxl w-full border border-hairline-dark">
        <!-- Active Form Section -->
        <div v-if="currentStep < steps.length">
          <h3 class="text-[24px] font-medium leading-[1.33] mb-[24px] text-on-dark">
            {{ steps[currentStep].title }}
          </h3>

          <!-- =================== EDUCATION CUSTOM FORM =================== -->
          <div v-if="steps[currentStep]?.id === 'education'">

            <!-- Education Form (single entry) -->
            <div class="flex flex-col gap-[16px]">
              <!-- Gelar -->
              <div class="flex flex-col">
                <label class="mb-[8px] font-semibold text-on-dark-mute">Gelar <span class="text-accent-danger font-bold">*</span></label>
                <input v-model="eduForm.degree" placeholder="Contoh: S1" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
                <span class="text-[12px] text-stone mt-[6px]">Jenjang pendidikan (D3, S1, S2, dll.)</span>
                <div v-if="eduErrors.degree" class="text-accent-danger text-[12px] mt-[4px]">{{ eduErrors.degree }}</div>
              </div>

              <!-- Jurusan -->
              <div class="flex flex-col">
                <label class="mb-[8px] font-semibold text-on-dark-mute">Jurusan <span class="text-accent-danger font-bold">*</span></label>
                <input v-model="eduForm.major" placeholder="Contoh: Teknik Informatika" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
                <div v-if="eduErrors.major" class="text-accent-danger text-[12px] mt-[4px]">{{ eduErrors.major }}</div>
              </div>

              <!-- Institusi -->
              <div class="flex flex-col">
                <label class="mb-[8px] font-semibold text-on-dark-mute">Institusi / Universitas <span class="text-accent-danger font-bold">*</span></label>
                <input v-model="eduForm.institution" placeholder="Contoh: Universitas Indonesia" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
                <div v-if="eduErrors.institution" class="text-accent-danger text-[12px] mt-[4px]">{{ eduErrors.institution }}</div>
              </div>

              <!-- Show Date Toggle -->
              <label class="flex items-center gap-[8px] cursor-pointer">
                <input type="checkbox" v-model="eduForm.showDate" class="w-[18px] h-[18px] rounded accent-white" />
                <span class="text-[14px] text-on-dark-mute">Tampilkan tanggal pada CV</span>
              </label>

              <!-- Period Start (shown only if showDate) -->
              <div v-if="eduForm.showDate" class="grid grid-cols-2 gap-[12px]">
                <div class="flex flex-col">
                  <label class="mb-[8px] font-semibold text-on-dark-mute">Bulan Mulai <span class="text-accent-danger font-bold">*</span></label>
                  <select v-model="eduForm.startMonth" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none appearance-none">
                    <option value="" disabled class="bg-surface-elevated text-on-dark">-- Pilih Bulan --</option>
                    <option v-for="m in MONTHS" :key="'esm-'+m" :value="m" class="bg-surface-elevated text-on-dark">{{ m }}</option>
                  </select>
                  <div v-if="eduErrors.startMonth" class="text-accent-danger text-[12px] mt-[4px]">{{ eduErrors.startMonth }}</div>
                </div>
                <div class="flex flex-col">
                  <label class="mb-[8px] font-semibold text-on-dark-mute">Tahun Mulai <span class="text-accent-danger font-bold">*</span></label>
                  <select v-model="eduForm.startYear" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none appearance-none">
                    <option value="" disabled class="bg-surface-elevated text-on-dark">-- Pilih Tahun --</option>
                    <option v-for="y in YEARS" :key="'esy-'+y" :value="y" class="bg-surface-elevated text-on-dark">{{ y }}</option>
                  </select>
                  <div v-if="eduErrors.startYear" class="text-accent-danger text-[12px] mt-[4px]">{{ eduErrors.startYear }}</div>
                </div>
              </div>

              <!-- Is Currently Studying Checkbox (shown only if showDate) -->
              <label v-if="eduForm.showDate" class="flex items-center gap-[8px] cursor-pointer">
                <input type="checkbox" v-model="eduForm.isCurrent" class="w-[18px] h-[18px] rounded accent-white" />
                <span class="text-[14px] text-on-dark-mute">Saya masih dalam pendidikan ini</span>
              </label>

              <!-- Period End (shown only if showDate AND not current) -->
              <div v-if="eduForm.showDate && !eduForm.isCurrent" class="grid grid-cols-2 gap-[12px]">
                <div class="flex flex-col">
                  <label class="mb-[8px] font-semibold text-on-dark-mute">Bulan Selesai <span class="text-accent-danger font-bold">*</span></label>
                  <select v-model="eduForm.endMonth" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none appearance-none">
                    <option value="" disabled class="bg-surface-elevated text-on-dark">-- Pilih Bulan --</option>
                    <option v-for="m in MONTHS" :key="'eem-'+m" :value="m" class="bg-surface-elevated text-on-dark">{{ m }}</option>
                  </select>
                  <div v-if="eduErrors.endMonth" class="text-accent-danger text-[12px] mt-[4px]">{{ eduErrors.endMonth }}</div>
                </div>
                <div class="flex flex-col">
                  <label class="mb-[8px] font-semibold text-on-dark-mute">Tahun Selesai <span class="text-accent-danger font-bold">*</span></label>
                  <select v-model="eduForm.endYear" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none appearance-none">
                    <option value="" disabled class="bg-surface-elevated text-on-dark">-- Pilih Tahun --</option>
                    <option v-for="y in YEARS" :key="'eey-'+y" :value="y" class="bg-surface-elevated text-on-dark">{{ y }}</option>
                  </select>
                  <div v-if="eduErrors.endYear" class="text-accent-danger text-[12px] mt-[4px]">{{ eduErrors.endYear }}</div>
                </div>
              </div>
              <div v-if="eduErrors.period" class="text-accent-danger text-[12px]">{{ eduErrors.period }}</div>

              <!-- IPK -->
              <div class="flex flex-col">
                <label class="mb-[8px] font-semibold text-on-dark-mute">IPK <span class="text-accent-danger font-bold">*</span></label>
                <input v-model="eduForm.gpa" placeholder="Contoh: 3.50" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
                <span class="text-[12px] text-stone mt-[6px]">Format desimal, skala 0.00 - 4.00</span>
                <div v-if="eduErrors.gpa" class="text-accent-danger text-[12px] mt-[4px]">{{ eduErrors.gpa }}</div>
              </div>
            </div>
          </div>

          <!-- =================== EXPERIENCE CUSTOM FORM =================== -->
          <div v-else-if="steps[currentStep]?.id === 'experience'">

            <!-- Saved Work Experiences List -->
            <div v-if="workExperiences.length > 0" class="mb-[24px]">
              <span class="text-[13px] font-semibold text-stone uppercase tracking-[1px] mb-[12px] block">Pengalaman Kerja Tersimpan ({{ workExperiences.length }})</span>
              <div v-for="(work, idx) in workExperiences" :key="'work-'+idx" class="border border-hairline-dark rounded-[12px] p-[16px] mb-[12px]">
                <div class="flex justify-between items-start gap-[12px]">
                  <div class="flex-1 min-w-0">
                    <div class="font-semibold text-on-dark text-[14px]">{{ work.position }}</div>
                    <div class="text-[14px] text-on-dark-mute">{{ work.company }}</div>
                    <div class="text-[13px] text-stone">{{ work.startMonth }} {{ work.startYear }} - {{ work.current ? 'Sekarang' : work.endMonth + ' ' + work.endYear }}</div>
                    <div class="text-[12px] text-stone mt-[4px]">{{ work.jobDescriptions.filter(j => j.trim()).length }} jobdesk</div>
                  </div>
                  <div class="flex gap-[8px] shrink-0">
                    <button @click="editWorkExperience(idx)" class="text-[13px] px-[12px] py-[4px] rounded-full border border-hairline-dark text-on-dark-mute hover:bg-surface-elevated transition-colors">Edit</button>
                    <button @click="deleteWorkExperience(idx)" class="text-[13px] px-[12px] py-[4px] rounded-full border border-accent-danger/30 text-accent-danger hover:bg-accent-danger/10 transition-colors">Hapus</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Work Experience Form -->
            <div class="border border-hairline-dark rounded-[16px] p-[20px]">
              <h4 class="text-[16px] font-semibold text-on-dark mb-[20px]">{{ workEditIndex >= 0 ? 'Edit Pengalaman Kerja' : 'Tambah Pengalaman Kerja Baru' }}</h4>

              <div class="flex flex-col gap-[16px]">
                <!-- Perusahaan -->
                <div class="flex flex-col">
                  <label class="mb-[8px] font-semibold text-on-dark-mute">Nama Perusahaan <span class="text-accent-danger font-bold">*</span></label>
                  <input v-model="workForm.company" placeholder="Contoh: PT ABC" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
                  <div v-if="workErrors.company" class="text-accent-danger text-[12px] mt-[4px]">{{ workErrors.company }}</div>
                </div>

                <!-- Posisi -->
                <div class="flex flex-col">
                  <label class="mb-[8px] font-semibold text-on-dark-mute">Posisi/Jabatan <span class="text-accent-danger font-bold">*</span></label>
                  <input v-model="workForm.position" placeholder="Contoh: Frontend Developer" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
                  <div v-if="workErrors.position" class="text-accent-danger text-[12px] mt-[4px]">{{ workErrors.position }}</div>
                </div>

                <!-- Period Start -->
                <div class="grid grid-cols-2 gap-[12px]">
                  <div class="flex flex-col">
                    <label class="mb-[8px] font-semibold text-on-dark-mute">Bulan Mulai <span class="text-accent-danger font-bold">*</span></label>
                    <select v-model="workForm.startMonth" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none appearance-none">
                      <option value="" disabled class="bg-surface-elevated text-on-dark">-- Pilih Bulan --</option>
                      <option v-for="m in MONTHS" :key="'wsm-'+m" :value="m" class="bg-surface-elevated text-on-dark">{{ m }}</option>
                    </select>
                    <div v-if="workErrors.startMonth" class="text-accent-danger text-[12px] mt-[4px]">{{ workErrors.startMonth }}</div>
                  </div>
                  <div class="flex flex-col">
                    <label class="mb-[8px] font-semibold text-on-dark-mute">Tahun Mulai <span class="text-accent-danger font-bold">*</span></label>
                    <select v-model="workForm.startYear" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none appearance-none">
                      <option value="" disabled class="bg-surface-elevated text-on-dark">-- Pilih Tahun --</option>
                      <option v-for="y in YEARS" :key="'wsy-'+y" :value="y" class="bg-surface-elevated text-on-dark">{{ y }}</option>
                    </select>
                    <div v-if="workErrors.startYear" class="text-accent-danger text-[12px] mt-[4px]">{{ workErrors.startYear }}</div>
                  </div>
                </div>

                <!-- Current Job Checkbox -->
                <label class="flex items-center gap-[8px] cursor-pointer">
                  <input type="checkbox" v-model="workForm.current" class="w-[18px] h-[18px] rounded accent-white" />
                  <span class="text-[14px] text-on-dark-mute">Saya masih bekerja di perusahaan ini</span>
                </label>

                <!-- Period End (hidden if current job) -->
                <div v-if="!workForm.current" class="grid grid-cols-2 gap-[12px]">
                  <div class="flex flex-col">
                    <label class="mb-[8px] font-semibold text-on-dark-mute">Bulan Selesai <span class="text-accent-danger font-bold">*</span></label>
                    <select v-model="workForm.endMonth" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none appearance-none">
                      <option value="" disabled class="bg-surface-elevated text-on-dark">-- Pilih Bulan --</option>
                      <option v-for="m in MONTHS" :key="'wem-'+m" :value="m" class="bg-surface-elevated text-on-dark">{{ m }}</option>
                    </select>
                    <div v-if="workErrors.endMonth" class="text-accent-danger text-[12px] mt-[4px]">{{ workErrors.endMonth }}</div>
                  </div>
                  <div class="flex flex-col">
                    <label class="mb-[8px] font-semibold text-on-dark-mute">Tahun Selesai <span class="text-accent-danger font-bold">*</span></label>
                    <select v-model="workForm.endYear" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none appearance-none">
                      <option value="" disabled class="bg-surface-elevated text-on-dark">-- Pilih Tahun --</option>
                      <option v-for="y in YEARS" :key="'wey-'+y" :value="y" class="bg-surface-elevated text-on-dark">{{ y }}</option>
                    </select>
                    <div v-if="workErrors.endYear" class="text-accent-danger text-[12px] mt-[4px]">{{ workErrors.endYear }}</div>
                  </div>
                </div>
                <div v-if="workErrors.period" class="text-accent-danger text-[12px]">{{ workErrors.period }}</div>

                <!-- Jobdesk / Deskripsi Pekerjaan -->
                <div class="border-t border-hairline-dark pt-[16px] mt-[8px]">
                  <h5 class="text-[14px] font-semibold text-on-dark mb-[12px]">Jobdesk / Deskripsi Pekerjaan <span class="text-accent-danger font-bold">*</span></h5>
                  <div class="flex flex-col gap-[8px]">
                    <div v-for="(jd, jdIdx) in workForm.jobDescriptions" :key="'jd-'+jdIdx" class="flex gap-[8px] items-start">
                      <span class="text-on-dark-mute text-[14px] mt-[12px] shrink-0">{{ jdIdx + 1 }}.</span>
                      <textarea v-model="workForm.jobDescriptions[jdIdx]" :placeholder="'Deskripsi pekerjaan #' + (jdIdx + 1)" rows="2" class="flex-1 h-40 bg-transparent border border-hairline-dark rounded-[12px] p-[12px] text-[14px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone resize-none"></textarea>
                      <button v-if="workForm.jobDescriptions.length > 1" @click="removeJobDescription(jdIdx)" class="shrink-0 mt-[8px] text-accent-danger text-[16px] w-[32px] h-[32px] rounded-full border border-accent-danger/30 flex items-center justify-center hover:bg-accent-danger/10 transition-colors">✕</button>
                    </div>
                  </div>
                  <div v-if="workErrors.jobDescriptions" class="text-accent-danger text-[12px] mt-[4px]">{{ workErrors.jobDescriptions }}</div>
                  <button @click="addJobDescription" class="mt-[12px] text-[13px] px-[16px] py-[6px] rounded-full border border-hairline-dark text-on-dark hover:bg-surface-elevated transition-colors">+ Tambah Jobdesk</button>
                </div>
              </div>

              <!-- Save / Cancel for work experience -->
              <div class="flex gap-[12px] mt-[24px] pt-[16px] border-t border-hairline-dark">
                <button @click="saveWorkExperience" class="inline-flex items-center justify-center font-semibold rounded-full transition-all duration-200 cursor-pointer text-[14px] px-[20px] h-[40px] bg-on-dark text-ink hover:bg-white/90">
                  {{ workEditIndex >= 0 ? 'Simpan Perubahan' : 'Simpan Pengalaman Kerja' }}
                </button>
                <button v-if="workEditIndex >= 0" @click="cancelWorkEdit" class="inline-flex items-center justify-center font-semibold rounded-full transition-all duration-200 cursor-pointer text-[14px] px-[20px] h-[40px] bg-transparent border border-hairline-dark text-on-dark hover:bg-surface-elevated">Batal</button>
              </div>
            </div>
          </div>

          <!-- =================== GENERIC FORM (personal_info, summary, skills, certifications) =================== -->
          <div v-else class="flex flex-col gap-[20px]">
            <div v-for="field in steps[currentStep].fields" :key="field.key" class="flex flex-col">
              <label class="mb-[8px] font-semibold text-on-dark-mute">
                {{ field.label }} 
                <span v-if="field.required" class="text-accent-danger font-bold">*</span>
                <button v-if="field.key === 'description' || field.key === 'summary' || field.key === 'technical_skills' || field.key === 'soft_skills'" class="bg-transparent border-none text-white cursor-pointer text-[12px] ml-[12px] px-[8px] py-[2px] rounded-full transition-colors duration-200 hover:bg-white/10" @click.prevent="getSuggestion(field)" title="Minta saran AI">💡 AI Suggestion</button>
              </label>
              
              <input 
                v-if="field.key !== 'gpa' && field.key !== 'description' && field.key !== 'summary' && field.key !== 'email' && field.key !== 'linkedin'" 
                v-model="formData[field.key]" 
                :placeholder="field.placeholder" 
                class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone"
              />
              
              <input 
                v-else-if="field.key === 'email'"
                type="email"
                v-model="formData[field.key]" 
                :placeholder="field.placeholder" 
                @input="validateEmail"
                class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone"
              />

              <input 
                v-else-if="field.key === 'linkedin'"
                type="url"
                v-model="formData[field.key]" 
                :placeholder="field.placeholder" 
                @input="validateLinkedIn"
                class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone"
              />

              <input 
                v-else-if="field.key === 'gpa'"
                v-model="formData[field.key]" 
                :placeholder="field.placeholder" 
                @input="validateGPA"
                class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone"
              />

              <textarea 
                v-else 
                v-model="formData[field.key]" 
                :placeholder="field.placeholder"
                rows="4"
                class="w-full h-40 bg-transparent border border-hairline-dark rounded-[12px] p-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone resize-none"
              ></textarea>
              
              <span class="text-[12px] text-stone mt-[6px]">{{ field.hint }}</span>
              <div v-if="errors[field.key]" class="text-accent-danger text-[12px] mt-[6px]">{{ errors[field.key] }}</div>
              
              <div v-if="suggestions[field.key]" class="bg-surface-deep px-[16px] py-[12px] rounded-md text-[13px] text-on-dark-mute mt-[8px] border-white">
                <span class="font-semibold text-white">Saran AI:</span> {{ suggestions[field.key] }}
              </div>
            </div>
          </div>

          <!-- Wizard Actions -->
          <div class="flex justify-between mt-[32px] pt-[24px] border-t border-hairline-dark">
            <button class="inline-flex items-center justify-center font-medium rounded-full transition-all duration-200 cursor-pointer text-[14px] px-[20px] h-[40px] bg-transparent border border-hairline-dark text-on-dark hover:bg-surface-elevated disabled:opacity-50 disabled:cursor-not-allowed" :disabled="currentStep === 0" @click="prevStep">Sebelumnya</button>
            <button class="inline-flex items-center justify-center font-medium rounded-full transition-all duration-200 cursor-pointer text-[14px] px-[20px] h-[40px] bg-on-dark text-ink hover:bg-white/90" @click="nextStep">Selanjutnya</button>
          </div>
        </div>

        <!-- Preview Section -->
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
          
          <div v-if="analysisResult" class="mb-[24px] p-xl border border-hairline-dark rounded-[20px] bg-surface-deep">
            <h4 class="text-[20px] font-medium leading-[1.4] mb-[12px] text-on-dark">Hasil Analisis AI</h4>
            <div v-html="analysisResult" class="analysis-content"></div>
          </div>

          <!-- CV Visual Preview -->
          <div class="bg-white text-black p-[40px] rounded-[20px] leading-[1.5] max-w-[800px] mx-auto" v-if="hasPreviewData">
            <!-- Personal Info -->
            <div class="text-center mb-[20px]">
                <h2 class="text-[30px] mb-[4px] uppercase tracking-[1px] font-bold">{{ formData.full_name || '[Nama Anda]' }}</h2>
                <p class="text-[12px]">
                    {{ (!errors.email && formData.email) ? formData.email + ' | ' : '' }}
                    {{ formData.phone ? formData.phone + ' | ' : '' }}
                    {{ formData.address ? formData.address + ' | ' : '' }}
                    {{ (!errors.linkedin && formData.linkedin) ? formData.linkedin : '' }}
                </p>
            </div>
            
            <!-- Summary -->
            <div class="mb-[15px]" v-if="formData.summary">
                <h4 class="text-[14px] uppercase mb-[4px] font-bold">RINGKASAN PROFESIONAL</h4>
                <div class="border-b-2 border-black mb-[12px]"></div>
                <p class="text-[12px] text-justify">{{ formData.summary }}</p>
            </div>
            
            <!-- Education -->
            <div class="mb-[15px]" v-if="educations.length > 0">
                <h4 class="text-[14px] uppercase mb-[4px] font-bold">PENDIDIKAN</h4>
                <div class="border-b-2 border-black mb-[12px]"></div>
                <div v-for="(edu, idx) in educations" :key="'prev-edu-'+idx" class="mb-[16px]">
                  <div class="flex justify-between items-start flex-wrap gap-[4px]">
                    <div>
                      <div class="text-[12px] font-bold">{{ edu.degree }} {{ edu.major }} | IPK: {{ formatGPA(edu.gpa) }}/4.00</div>
                      <div class="text-[12px]">{{ edu.institution }}</div>
                    </div>
                    <div v-if="edu.showDate" class="text-[12px] text-black font-bold">{{ edu.startMonth }} {{ edu.startYear }} - {{ edu.isCurrent ? 'Sekarang' : edu.endMonth + ' ' + edu.endYear }}</div>
                  </div>
                </div>
            </div>
            
            <!-- Work Experience -->
            <div class="mb-[15px]" v-if="workExperiences.length > 0">
                <h4 class="text-[14px] uppercase mb-[4px] font-bold">PENGALAMAN & PROJEK</h4>
                <div class="border-b-2 border-black mb-[12px]"></div>
                <div v-for="(work, idx) in workExperiences" :key="'prev-work-'+idx" class="mb-[16px]">
                    <div class="flex justify-between items-start flex-wrap gap-[4px]">
                        <div>
                            <div class="text-[12px] font-bold">{{ work.company }}</div>
                            <div class="text-[11px] italic">{{ work.position }}</div> 
                        </div>
                        <div class="text-[12px] shrink-0 text-black font-bold">{{ work.startMonth }} {{ work.startYear }} - {{ work.current ? 'Sekarang' : work.endMonth + ' ' + work.endYear }}</div>
                    </div>
                    <ul class="mt-[2px] pl-[24px] list-disc">
                        <li v-for="(jd, jdIdx) in work.jobDescriptions.filter(j => j.trim())" :key="'prev-jd-'+jdIdx" class="text-[12px] mb-[2px]">{{ jd }}</li>
                    </ul>
                </div>
            </div>
            
            <!-- Skills -->
            <div class="mb-[15px]" v-if="formData.technical_skills || formData.soft_skills">
                <h4 class="text-[14px] uppercase mb-[4px] font-bold">KEAHLIAN</h4>
                <div class="border-b-2 border-black mb-[12px]"></div>
                <p v-if="formData.technical_skills" class="text-[12px]"><strong>Keahlian Teknis:</strong> {{ formData.technical_skills }}</p>
                <p v-if="formData.soft_skills" class="text-[12px]"><strong>Soft Skills:</strong> {{ formData.soft_skills }}</p>
            </div>
            
            <!-- Certifications -->
            <div class="mb-[15px]" v-if="formData.cert_name">
                <h4 class="text-[14px] uppercase mb-[4px] font-bold">SERTIFIKASI</h4>
                <div class="border-b-2 border-black mb-[12px]"></div>
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
            <button class="inline-flex items-center justify-center font-medium rounded-full transition-all duration-200 cursor-pointer text-[14px] px-[20px] h-[40px] bg-transparent border border-hairline-dark text-on-dark hover:bg-surface-elevated" @click="prevStep">Sebelumnya</button>
          </div>
        </div>
      </main>
    </div>

    <!-- Hidden Print Container -->
    <div class="hidden print:block absolute left-0 top-0 w-full m-0 p-[40px] border-none shadow-none rounded-none bg-white text-black leading-[1.5]">
        <!-- Personal -->
        <div class="text-center mb-[20px]">
            <h2 class="text-[30px] mb-[4px] uppercase tracking-[1px] font-bold">{{ formData.full_name || '[Nama Anda]' }}</h2>
            <p class="text-[12px]">
                {{ (!errors.email && formData.email) ? formData.email + ' | ' : '' }}
                {{ formData.phone ? formData.phone + ' | ' : '' }}
                {{ formData.address ? formData.address + ' | ' : '' }}
                {{ (!errors.linkedin && formData.linkedin) ? formData.linkedin : '' }}
            </p>
        </div>
        
        <!-- Summary -->
        <div class="mb-[15px]" v-if="formData.summary">
            <h4 class="text-[14px] uppercase mb-[4px] font-bold">RINGKASAN PROFESIONAL</h4>
            <div class="border-b-2 border-black mb-[12px]"></div>
            <p class="text-[12px] text-justify">{{ formData.summary }}</p>
        </div>
        
        <!-- Education (print) -->
        <div class="mb-[15px]" v-if="educations.length > 0">
            <h4 class="text-[14px] uppercase mb-[4px] font-bold">PENDIDIKAN</h4>
            <div class="border-b-2 border-black mb-[12px]"></div>
            <div v-for="(edu, idx) in educations" :key="'print-edu-'+idx" class="mb-[16px]">
                <div class="flex justify-between items-start flex-wrap gap-[4px]">
                    <div>
                        <div class="text-[12px] font-bold">{{ edu.degree }} {{ edu.major }} | IPK: {{ formatGPA(edu.gpa) }}/4.00</div>
                        <div class="text-[12px]">{{ edu.institution }}</div>
                    </div>
                    <div v-if="edu.showDate" class="text-[12px] text-black font-bold">{{ edu.startMonth }} {{ edu.startYear }} - {{ edu.isCurrent ? 'Sekarang' : edu.endMonth + ' ' + edu.endYear }}</div>
                </div>
            </div>
        </div>
        
        <!-- Work Experience (print) -->
        <div class="mb-[15px]" v-if="workExperiences.length > 0">
            <h4 class="text-[14px] uppercase mb-[4px] font-bold">PENGALAMAN & PROJEK</h4>
            <div class="border-b-2 border-black mb-[12px]"></div>
            <div v-for="(work, idx) in workExperiences" :key="'print-work-'+idx" class="mb-[16px]">
                <div class="flex justify-between items-start flex-wrap gap-[4px]">
                    <div>
                        <div class="text-[12px] font-bold">{{ work.company }}</div>
                        <div class="text-[11px] italic">{{ work.position }}</div>
                    </div>
                    <div class="text-[12px] shrink-0 text-black font-bold">{{ work.startMonth }} {{ work.startYear }} - {{ work.current ? 'Sekarang' : work.endMonth + ' ' + work.endYear }}</div>
                </div>
                <ul class="mt-[2px] pl-[24px] list-disc">
                    <li v-for="(jd, jdIdx) in work.jobDescriptions.filter(j => j.trim())" :key="'print-jd-'+jdIdx" class="text-[12px] mb-[2px]">{{ jd }}</li>
                </ul>
            </div>
        </div>
        
        <!-- Skills (print) -->
        <div class="mb-[15px]" v-if="formData.technical_skills || formData.soft_skills">
            <h4 class="text-[14px] uppercase mb-[4px] font-bold">KEAHLIAN</h4>
            <div class="border-b-2 border-black mb-[12px]"></div>
            <p v-if="formData.technical_skills" class="text-[12px]"><strong>Keahlian Teknis:</strong> {{ formData.technical_skills }}</p>
            <p v-if="formData.soft_skills" class="text-[12px]"><strong>Soft Skills:</strong> {{ formData.soft_skills }}</p>
        </div>
        
        <!-- Certifications (print) -->
        <div class="mb-[15px]" v-if="formData.cert_name">
            <h4 class="text-[14px] uppercase mb-[4px] font-bold">SERTIFIKASI</h4>
            <div class="border-b-2 border-black mb-[12px]"></div>
            <div class="mb-[12px]">
                <div class="flex justify-between text-[14px]">
                    <strong>{{ formData.cert_name }}</strong>
                    <span>{{ formData.issuer }}</span>
                </div>
            </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from "vue"
import axios from "axios"
import { useHead } from "@vueuse/head"

useHead({
  title: 'Pembuat CV ATS-Friendly — JobFinder',
  meta: [
    { name: 'description', content: 'Buat CV profesional berstandar ATS langkah demi langkah dengan panduan asisten AI. Template minimalis yang dioptimalkan untuk sistem perekrutan otomatis di Indonesia.' },
    { property: 'og:title', content: 'Pembuat CV ATS-Friendly — JobFinder' },
    { property: 'og:description', content: 'Buat CV ATS-friendly dengan panduan AI. Template profesional dan siap lamar.' },
  ]
})


// ===================== STATE =====================
const steps = ref([])
const expertiseAreas = ref([])
const targetExpertise = ref("Software Development")
const formData = reactive({})
const suggestions = reactive({})
const errors = reactive({ gpa: "", email: "", linkedin: "" })
const analysisResult = ref("")
const analyzing = ref(false)
const currentStep = ref(0)
const maxStepReached = ref(0)

// Simple form fields (personal info, summary, skills, certifications)
const FIELDS = [
  "full_name", "email", "phone", "address", "linkedin",
  "summary",
  "technical_skills", "soft_skills",
  "cert_name", "issuer",
]
FIELDS.forEach(k => formData[k] = "")

// ===================== EDUCATION DATA =====================
const educations = ref([])
const eduEditIndex = ref(-1)
const eduForm = reactive({
  degree: '', major: '', institution: '',
  startMonth: '', startYear: '', endMonth: '', endYear: '',
  gpa: '', experiences: [],
  showDate: true, isCurrent: false
})
const eduErrors = reactive({})

// Education sub-experience
const eduExpEditIndex = ref(-1)
const eduExpForm = reactive({
  title: '', role: '', month: '', year: '', description: ''
})
const eduExpErrors = reactive({})

// ===================== WORK EXPERIENCE DATA =====================
const workExperiences = ref([])
const workEditIndex = ref(-1)
const workForm = reactive({
  company: '', position: '',
  startMonth: '', startYear: '', endMonth: '', endYear: '',
  current: false, jobDescriptions: ['']
})
const workErrors = reactive({})

// ===================== CONSTANTS =====================
const MONTHS = [
  'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
  'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
]
const currentYearNum = new Date().getFullYear()
const YEARS = []
for (let y = currentYearNum + 5; y >= 1990; y--) { YEARS.push(y) }

// ===================== COMPUTED =====================
const hasPreviewData = computed(() => {
  return formData.full_name || formData.summary || educations.value.length > 0 || workExperiences.value.length > 0 || formData.technical_skills || formData.cert_name
})

// ===================== LIFECYCLE =====================
onMounted(async () => {
  // Load saved simple form data
  const savedData = localStorage.getItem('jobfinder_cv_data')
  if (savedData) {
    try {
      const parsed = JSON.parse(savedData)
      Object.keys(parsed).forEach(k => {
        if (FIELDS.includes(k)) formData[k] = parsed[k]
      })
    } catch(e) {}
  }

  // Load saved educations
  const savedEdu = localStorage.getItem('jobfinder_cv_educations')
  if (savedEdu) {
    try { educations.value = JSON.parse(savedEdu) } catch(e) {}
  }

  // Load saved work experiences
  const savedWork = localStorage.getItem('jobfinder_cv_work')
  if (savedWork) {
    try { workExperiences.value = JSON.parse(savedWork) } catch(e) {}
  }

  // Load edu form from saved education data
  loadEduFormFromSaved()

  // Load saved navigation progress
  const savedMaxStep = localStorage.getItem('jobfinder_cv_maxStep')
  if (savedMaxStep) {
    try { maxStepReached.value = parseInt(savedMaxStep) || 0 } catch(e) {}
  }

  // Load steps and expertise areas from API
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

// ===================== WATCHERS =====================
watch(formData, (newVal) => {
  localStorage.setItem('jobfinder_cv_data', JSON.stringify(newVal))
}, { deep: true })

watch(educations, (val) => {
  localStorage.setItem('jobfinder_cv_educations', JSON.stringify(val))
}, { deep: true })

watch(workExperiences, (val) => {
  localStorage.setItem('jobfinder_cv_work', JSON.stringify(val))
}, { deep: true })

watch(maxStepReached, (val) => {
  localStorage.setItem('jobfinder_cv_maxStep', val.toString())
})

// Auto-load education form when navigating to the education step
watch(currentStep, (newStep) => {
  if (steps.value.length > 0 && steps.value[newStep]?.id === 'education') {
    loadEduFormFromSaved()
  }
})

// ===================== NAVIGATION =====================
function isStepValid(stepIndex) {
  if (stepIndex >= steps.value.length) return true
  const section = steps.value[stepIndex]

  if (section.id === 'education') {
    // Auto-save education from form if form has data
    if (eduForm.degree.trim() && eduForm.major.trim() && eduForm.institution.trim()) {
      saveEducation()
    }
    return educations.value.length > 0
  }
  if (section.id === 'experience') return workExperiences.value.length > 0

  let valid = true
  for (const field of section.fields) {
    if (field.required && !formData[field.key]) valid = false
    if (errors[field.key]) valid = false
  }
  return valid
}

function nextStep() {
  if (isStepValid(currentStep.value)) {
    if (currentStep.value < steps.value.length) {
      currentStep.value++
      if (currentStep.value > maxStepReached.value) {
        maxStepReached.value = currentStep.value
      }
    }
  } else {
    const section = steps.value[currentStep.value]
    if (section?.id === 'education') alert("Harap tambahkan minimal satu data pendidikan.")
    else if (section?.id === 'experience') alert("Harap tambahkan minimal satu pengalaman kerja.")
    else alert("Harap lengkapi semua field yang wajib (*).")
  }
}

function prevStep() {
  if (currentStep.value > 0) currentStep.value--
}

function goToStep(index) {
  // Allow free navigation to any previously visited step
  if (index <= maxStepReached.value) {
    currentStep.value = index
    return
  }
  // Allow going one step forward if current step is valid
  if (index === currentStep.value + 1 && isStepValid(currentStep.value)) {
    currentStep.value = index
    if (index > maxStepReached.value) {
      maxStepReached.value = index
    }
    return
  }
}

// ===================== VALIDATION HELPERS =====================
function validateEmail() {
  const val = formData.email
  if (!val) { errors.email = ""; return }
  errors.email = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val) ? "" : "Format email tidak valid."
}

function validateLinkedIn() {
  const val = formData.linkedin
  if (!val) { errors.linkedin = ""; return }
  errors.linkedin = /linkedin\.com\/(in|pub|profile)/i.test(val) ? "" : "Format harus tautan profil LinkedIn (misal: linkedin.com/in/nama)."
}

function validateGPA() {
  const val = formData.gpa
  if (!val) { errors.gpa = ""; return }
  const isValid = /^([0-4](\.\d+)?)(?:\/4(?:\.0+)?)?$/.test(val)
  if (!isValid) { errors.gpa = "Format harus desimal (misal 3.8 atau 3.8/4.0). Maksimal 4.0."; return }
  const num = parseFloat(val.split('/')[0])
  errors.gpa = num < 3.0 ? "Saran: Sebaiknya hanya cantumkan IPK jika di atas 3.0." : ""
}

function formatGPA(val) {
  const num = parseFloat(val)
  return isNaN(num) ? val : num.toFixed(2)
}

function isPeriodValid(startMonth, startYear, endMonth, endYear) {
  if (!startMonth || !startYear || !endMonth || !endYear) return true
  const sy = Number(startYear), ey = Number(endYear)
  if (ey < sy) return false
  if (ey === sy) return MONTHS.indexOf(endMonth) >= MONTHS.indexOf(startMonth)
  return true
}

// ===================== EDUCATION CRUD =====================
function clearEduErrors() { Object.keys(eduErrors).forEach(k => delete eduErrors[k]) }

function validateEduForm() {
  clearEduErrors()
  let valid = true
  if (!eduForm.degree.trim()) { eduErrors.degree = 'Gelar wajib diisi.'; valid = false }
  if (!eduForm.major.trim()) { eduErrors.major = 'Jurusan wajib diisi.'; valid = false }
  if (!eduForm.institution.trim()) { eduErrors.institution = 'Institusi wajib diisi.'; valid = false }
  if (eduForm.showDate) {
    if (!eduForm.startMonth) { eduErrors.startMonth = 'Bulan mulai wajib dipilih.'; valid = false }
    if (!eduForm.startYear) { eduErrors.startYear = 'Tahun mulai wajib dipilih.'; valid = false }
    if (!eduForm.isCurrent) {
      if (!eduForm.endMonth) { eduErrors.endMonth = 'Bulan selesai wajib dipilih.'; valid = false }
      if (!eduForm.endYear) { eduErrors.endYear = 'Tahun selesai wajib dipilih.'; valid = false }
    }
  }

  if (!eduForm.gpa.toString().trim()) {
    eduErrors.gpa = 'IPK wajib diisi.'; valid = false
  } else {
    const num = parseFloat(eduForm.gpa)
    if (isNaN(num) || num < 0 || num > 4) { eduErrors.gpa = 'IPK harus berada pada rentang 0.00 - 4.00.'; valid = false }
  }

  if (eduForm.showDate && !eduForm.isCurrent && eduForm.startMonth && eduForm.startYear && eduForm.endMonth && eduForm.endYear) {
    if (!isPeriodValid(eduForm.startMonth, eduForm.startYear, eduForm.endMonth, eduForm.endYear)) {
      eduErrors.period = 'Periode selesai tidak boleh lebih awal dari periode mulai.'; valid = false
    }
  }
  return valid
}

function resetEduForm() {
  eduForm.degree = ''; eduForm.major = ''; eduForm.institution = ''
  eduForm.startMonth = ''; eduForm.startYear = ''; eduForm.endMonth = ''; eduForm.endYear = ''
  eduForm.gpa = ''; eduForm.experiences = []
  eduForm.showDate = true; eduForm.isCurrent = false
  eduEditIndex.value = -1
  clearEduErrors(); resetEduExpForm()
}

function saveEducation() {
  if (!validateEduForm()) return
  const entry = {
    degree: eduForm.degree.trim(), major: eduForm.major.trim(), institution: eduForm.institution.trim(),
    startMonth: eduForm.showDate ? eduForm.startMonth : '', startYear: eduForm.showDate ? eduForm.startYear : '',
    endMonth: (eduForm.showDate && !eduForm.isCurrent) ? eduForm.endMonth : '',
    endYear: (eduForm.showDate && !eduForm.isCurrent) ? eduForm.endYear : '',
    gpa: eduForm.gpa.toString().trim(),
    experiences: [],
    showDate: eduForm.showDate, isCurrent: eduForm.isCurrent
  }
  // Always save as single entry (index 0)
  educations.value = [entry]
}

function loadEduFormFromSaved() {
  if (educations.value.length > 0) {
    const edu = educations.value[0]
    eduForm.degree = edu.degree; eduForm.major = edu.major; eduForm.institution = edu.institution
    eduForm.startMonth = edu.startMonth; eduForm.startYear = edu.startYear
    eduForm.endMonth = edu.endMonth; eduForm.endYear = edu.endYear
    eduForm.gpa = edu.gpa; eduForm.experiences = []
    eduForm.showDate = edu.showDate !== undefined ? edu.showDate : true
    eduForm.isCurrent = edu.isCurrent || false
    clearEduErrors()
  }
}

// ===================== EDUCATION SUB-EXPERIENCE CRUD =====================
function clearEduExpErrors() { Object.keys(eduExpErrors).forEach(k => delete eduExpErrors[k]) }

function validateEduExpForm() {
  clearEduExpErrors()
  const missing = []
  if (!eduExpForm.title.trim()) missing.push('Nama kegiatan')
  if (!eduExpForm.role.trim()) missing.push('Posisi/peran')
  if (!eduExpForm.month) missing.push('Bulan')
  if (!eduExpForm.year) missing.push('Tahun')
  if (!eduExpForm.description.trim()) missing.push('Deskripsi')
  if (missing.length) { eduExpErrors.general = missing.join(', ') + ' wajib diisi.'; return false }
  return true
}

function resetEduExpForm() {
  eduExpForm.title = ''; eduExpForm.role = ''; eduExpForm.month = ''; eduExpForm.year = ''; eduExpForm.description = ''
  eduExpEditIndex.value = -1; clearEduExpErrors()
}

function addEduExperience() {
  if (!validateEduExpForm()) return
  const entry = {
    title: eduExpForm.title.trim(), role: eduExpForm.role.trim(),
    month: eduExpForm.month, year: eduExpForm.year, description: eduExpForm.description.trim()
  }
  if (eduExpEditIndex.value >= 0) { eduForm.experiences[eduExpEditIndex.value] = entry }
  else { eduForm.experiences.push(entry) }
  resetEduExpForm()
}

function editEduExperience(idx) {
  const exp = eduForm.experiences[idx]
  eduExpForm.title = exp.title; eduExpForm.role = exp.role
  eduExpForm.month = exp.month; eduExpForm.year = exp.year; eduExpForm.description = exp.description
  eduExpEditIndex.value = idx; clearEduExpErrors()
}

function deleteEduExperience(idx) {
  if (confirm('Hapus pengalaman ini?')) {
    eduForm.experiences.splice(idx, 1)
    if (eduExpEditIndex.value === idx) resetEduExpForm()
    else if (eduExpEditIndex.value > idx) eduExpEditIndex.value--
  }
}

function cancelEduExpEdit() { resetEduExpForm() }

// ===================== WORK EXPERIENCE CRUD =====================
function clearWorkErrors() { Object.keys(workErrors).forEach(k => delete workErrors[k]) }

function validateWorkForm() {
  clearWorkErrors()
  let valid = true
  if (!workForm.company.trim()) { workErrors.company = 'Nama perusahaan wajib diisi.'; valid = false }
  if (!workForm.position.trim()) { workErrors.position = 'Posisi/jabatan wajib diisi.'; valid = false }
  if (!workForm.startMonth) { workErrors.startMonth = 'Bulan mulai wajib dipilih.'; valid = false }
  if (!workForm.startYear) { workErrors.startYear = 'Tahun mulai wajib dipilih.'; valid = false }

  if (!workForm.current) {
    if (!workForm.endMonth) { workErrors.endMonth = 'Bulan selesai wajib dipilih.'; valid = false }
    if (!workForm.endYear) { workErrors.endYear = 'Tahun selesai wajib dipilih.'; valid = false }
    if (workForm.startMonth && workForm.startYear && workForm.endMonth && workForm.endYear) {
      if (!isPeriodValid(workForm.startMonth, workForm.startYear, workForm.endMonth, workForm.endYear)) {
        workErrors.period = 'Periode selesai tidak boleh lebih awal dari periode mulai.'; valid = false
      }
    }
  }

  const hasEmpty = workForm.jobDescriptions.some(jd => !jd.trim())
  if (workForm.jobDescriptions.length === 0 || workForm.jobDescriptions.every(jd => !jd.trim())) {
    workErrors.jobDescriptions = 'Minimal satu jobdesk wajib diisi.'; valid = false
  } else if (hasEmpty) {
    workErrors.jobDescriptions = 'Setiap jobdesk tidak boleh kosong. Hapus yang tidak diperlukan.'; valid = false
  }
  return valid
}

function resetWorkForm() {
  workForm.company = ''; workForm.position = ''
  workForm.startMonth = ''; workForm.startYear = ''; workForm.endMonth = ''; workForm.endYear = ''
  workForm.current = false; workForm.jobDescriptions = ['']
  workEditIndex.value = -1; clearWorkErrors()
}

function saveWorkExperience() {
  if (!validateWorkForm()) return
  const entry = {
    company: workForm.company.trim(), position: workForm.position.trim(),
    startMonth: workForm.startMonth, startYear: workForm.startYear,
    endMonth: workForm.current ? '' : workForm.endMonth,
    endYear: workForm.current ? '' : workForm.endYear,
    current: workForm.current,
    jobDescriptions: workForm.jobDescriptions.map(jd => jd.trim()).filter(jd => jd)
  }
  if (workEditIndex.value >= 0) { workExperiences.value[workEditIndex.value] = entry }
  else { workExperiences.value.push(entry) }
  resetWorkForm()
}

function editWorkExperience(idx) {
  const work = workExperiences.value[idx]
  workForm.company = work.company; workForm.position = work.position
  workForm.startMonth = work.startMonth; workForm.startYear = work.startYear
  workForm.endMonth = work.endMonth; workForm.endYear = work.endYear
  workForm.current = work.current
  workForm.jobDescriptions = [...work.jobDescriptions]
  if (workForm.jobDescriptions.length === 0) workForm.jobDescriptions = ['']
  workEditIndex.value = idx; clearWorkErrors()
}

function deleteWorkExperience(idx) {
  if (confirm('Apakah Anda yakin ingin menghapus pengalaman kerja ini?')) {
    workExperiences.value.splice(idx, 1)
    if (workEditIndex.value === idx) resetWorkForm()
    else if (workEditIndex.value > idx) workEditIndex.value--
  }
}

function cancelWorkEdit() { resetWorkForm() }

function addJobDescription() { workForm.jobDescriptions.push('') }
function removeJobDescription(idx) { workForm.jobDescriptions.splice(idx, 1) }

// ===================== AI SUGGESTION =====================
async function getSuggestion(field) {
  try {
    const { data } = await axios.post("/api/cv/suggestion", {
      fieldLabel: field.label, expertise: targetExpertise.value,
    })
    suggestions[field.key] = data.suggestion
  } catch {
    suggestions[field.key] = `Saran: Buat agar relevan dengan posisi ${targetExpertise.value}.`
  }
}

// ===================== ANALYZE CV =====================
async function analyzeBuiltCV() {
  analyzing.value = true
  analysisResult.value = ""
  
  const eduText = educations.value.map(e => {
    let dateStr = ''
    if (e.showDate) {
      dateStr = `, ${e.startMonth} ${e.startYear} - ${e.isCurrent ? 'Sekarang' : e.endMonth + ' ' + e.endYear}`
    }
    let t = `${e.degree} ${e.major} di ${e.institution} (IPK: ${e.gpa}/4.00)${dateStr}`
    if (e.experiences.length) {
      t += '\nPengalaman: ' + e.experiences.map(x => `${x.role} ${x.title}: ${x.description}`).join('; ')
    }
    return t
  }).join('\n')

  const workText = workExperiences.value.map(w => {
    let t = `${w.position} di ${w.company}, ${w.startMonth} ${w.startYear} - ${w.current ? 'Sekarang' : w.endMonth + ' ' + w.endYear}`
    t += '\nJobdesk: ' + w.jobDescriptions.join('; ')
    return t
  }).join('\n')

  const cvText = `
    Name: ${formData.full_name}
    Contact: ${formData.email} | ${formData.phone} | ${formData.address}
    LinkedIn: ${formData.linkedin}
    Summary: ${formData.summary}
    Education: ${eduText}
    Work Experience: ${workText}
    Skills: Technical (${formData.technical_skills}), Soft (${formData.soft_skills})
    Certifications: ${formData.cert_name} from ${formData.issuer}
  `
  
  try {
    const form = new FormData()
    form.append("expertise", targetExpertise.value)
    const blob = new Blob([cvText], { type: 'text/plain' })
    form.append("cv", blob, "cv.txt")
    
    const { data } = await axios.post("/api/cv/analyze", form)
    
    if (data.analysis && typeof data.analysis === "object" && data.analysis.error) {
        analysisResult.value = `<p>Salah: ${data.analysis.message}</p>`
        return
    }

    if (data.analysis && data.analysis.overallScore !== undefined) {
        analysisResult.value = formatAnalysisHtml(data, data.analysis)
    } else if (data.analysis && typeof data.analysis === "string") {
        analysisResult.value = data.analysis
            .replace(/```html\n?/g, "")
            .replace(/```\n?/g, "")
            .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
    } else {
        analysisResult.value = "Analisis gagal atau kosong."
    }
  } catch (e) {
    console.error(e)
    analysisResult.value = "Gagal memindai CV. Silakan coba lagi."
  } finally {
    analyzing.value = false
  }
}

function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]))
}

function listItems(arr) {
  if (!Array.isArray(arr)) return ""
  return arr.length ? `<ul>${arr.map(x => `<li>${esc(x)}</li>`).join("")}</ul>` : ""
}

function formatAnalysisHtml(data, a) {
  let html = ""
  const ats = data.ats || {}

  html += `<p class="mb-[16px]"><strong>Skor Keseluruhan: ${esc(a.overallScore)}/100</strong></p>`

  if (ats.score !== undefined) {
    html += `<p class="mb-[16px]"><strong>Skor ATS: ${esc(ats.score)}%</strong>${ats.isATS ? " (Format ATS terdeteksi)" : " (Gaya CV non-ATS)"}</p>`
  }

  if (a.summary) html += `<p class="mb-[16px]">${esc(a.summary)}</p>`

  if (Array.isArray(a.strengths) && a.strengths.length) {
    html += `<p class="mb-[8px]"><strong>Keunggulan:</strong></p>${listItems(a.strengths)}`
  }
  if (Array.isArray(a.weaknesses) && a.weaknesses.length) {
    html += `<p class="mb-[8px]"><strong>Kelemahan:</strong></p>${listItems(a.weaknesses)}`
  }
  if (Array.isArray(a.missingSkills) && a.missingSkills.length) {
    html += `<p class="mb-[8px]"><strong>Skill yang Perlu Dilengkapi:</strong></p>${listItems(a.missingSkills)}`
  }
  if (Array.isArray(a.keywordMatch) && a.keywordMatch.length) {
    html += `<p class="mb-[8px]"><strong>Keyword Cocok:</strong></p>${listItems(a.keywordMatch)}`
  }
  if (Array.isArray(a.recommendations) && a.recommendations.length) {
    html += `<p class="mb-[8px]"><strong>Rekomendasi:</strong></p>${listItems(a.recommendations)}`
  }
  if (a.categories && typeof a.categories === "object") {
    html += `<p class="mb-[8px]"><strong>Skor per Kategori:</strong></p><ul>`
    for (const [k, v] of Object.entries(a.categories)) {
      html += `<li>${esc(k)}: ${esc(v)}</li>`
    }
    html += `</ul>`
  }
  return html
}

function downloadPDF() { window.print() }
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