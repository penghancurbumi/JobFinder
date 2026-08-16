<template>
  <!-- ===== FORM MODE ===== -->
  <div v-if="!isPreview">
    <!-- PERSONAL INFO -->
    <div v-if="currentId === 'personal_info'" class="flex flex-col gap-[20px]">
      <div class="flex flex-col gap-sm mb-lg">
        <label class="flex items-center gap-sm cursor-pointer w-max">
          <input type="checkbox" v-model="useProfilePicture" class="w-[15px] h-[15px] rounded accent-white" />
          <span class="text-[14px] text-on-dark-mute font-semibold">Gunakan Foto Profil</span>
        </label>
        <div v-if="useProfilePicture" class="flex flex-col gap-xs mt-sm">
          <label class="mb-[8px] font-semibold text-on-dark-mute">Foto Profil</label>
          <div class="flex items-center gap-lg">
            <div class="w-[100px] h-[100px] rounded-full overflow-hidden border-2 border-hairline-dark bg-white flex shrink-0">
              <img v-if="profilePictureUrl" :src="profilePictureUrl" class="w-full h-full object-cover" />
              <Icon v-else icon="iconamoon:profile-fill" class="text-[70px] text-gray-300 mx-auto my-auto" />
            </div>
            <input type="file" accept="image/*" @change="onProfilePictureChange" class="w-full text-[14px] file:mr-4 file:py-2 file:px-4 file:rounded-full file:border file:border-hairline-dark file:text-sm file:font-medium file:bg-transparent file:text-on-dark hover:file:bg-surface-elevated file:cursor-pointer" />
          </div>
        </div>
      </div>
      <div v-for="f in personalFields" :key="f.key" class="flex flex-col">
        <label class="mb-[8px] font-semibold text-on-dark-mute">{{ f.label }} <span v-if="f.required" class="text-accent-danger font-bold">*</span></label>
        <input v-if="f.key === 'email'" type="email" v-model="formData[f.key]" :placeholder="f.placeholder" @input="validateEmail" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
        <input v-else-if="f.key === 'linkedin'" type="url" v-model="formData[f.key]" :placeholder="f.placeholder" @input="validateLinkedIn" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
        <input v-else-if="f.key === 'github'" type="url" v-model="formData[f.key]" :placeholder="f.placeholder" @input="validateGitHub" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
        <input v-else v-model="formData[f.key]" :placeholder="f.placeholder" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
        <span class="text-[12px] text-stone mt-[6px]">{{ f.hint }}</span>
        <div v-if="errors[f.key]" class="text-accent-danger text-[12px] mt-[4px]">{{ errors[f.key] }}</div>
      </div>
    </div>

    <!-- SUMMARY -->
    <div v-else-if="currentId === 'summary'" class="flex flex-col gap-[20px]">
      <div class="flex flex-col">
        <label class="mb-[8px] font-semibold text-on-dark-mute">
          Ringkasan Profesional <span class="text-accent-danger font-bold">*</span>
          <button class="bg-transparent border-none text-white cursor-pointer text-[12px] ml-[12px] px-[8px] py-[2px] rounded-full transition-colors duration-200 hover:bg-white/10" @click.prevent="requestSuggestion('summary', 'Ringkasan Profesional')">💡 AI Suggestion</button>
        </label>
        <textarea v-model="formData.summary" placeholder="Ringkasan profesional 2–3 kalimat yang menonjolkan pencapaian dengan angka..." rows="4" class="w-full h-80 bg-transparent border border-hairline-dark rounded-[12px] p-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone resize-none"></textarea>
        <span class="text-[12px] text-stone mt-[6px]">Sorot pencapaian dengan angka. Maksimal 4 baris.</span>
        <div v-if="suggestions.summary" class="bg-surface-deep px-[16px] py-[12px] rounded-md text-[13px] text-on-dark-mute mt-[8px]">
          <span class="font-semibold text-white">Saran AI:</span> {{ suggestions.summary }}
        </div>
      </div>
    </div>

    <!-- EDUCATION -->
    <div v-else-if="currentId === 'education'">
      <div class="flex flex-col gap-[16px]">
        <div class="flex flex-col"><label class="mb-[8px] font-semibold text-on-dark-mute">Jurusan <span class="text-accent-danger font-bold">*</span></label>
          <input v-model="eduForm.major" placeholder="Contoh: Teknik Informatika" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
          <div v-if="eduErrors.major" class="text-accent-danger text-[12px] mt-[4px]">{{ eduErrors.major }}</div>
        </div>
        <div class="flex flex-col"><label class="mb-[8px] font-semibold text-on-dark-mute">Institusi / Universitas <span class="text-accent-danger font-bold">*</span></label>
          <input v-model="eduForm.institution" placeholder="Contoh: Universitas Indonesia" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
          <div v-if="eduErrors.institution" class="text-accent-danger text-[12px] mt-[4px]">{{ eduErrors.institution }}</div>
        </div>
        <div class="flex flex-col"><label class="mb-[8px] font-semibold text-on-dark-mute">Lokasi Institusi</label>
          <input v-model="eduForm.location" placeholder="Contoh: Jakarta, Indonesia" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
        </div>
        <label class="flex items-center gap-[8px] cursor-pointer">
          <input type="checkbox" v-model="eduForm.showDate" class="w-[15px] h-[15px] rounded accent-white" />
          <span class="text-[14px] text-on-dark-mute">Tampilkan tanggal pada CV</span>
        </label>
        <div v-if="eduForm.showDate" class="grid grid-cols-2 gap-[12px]">
          <div class="flex flex-col"><label class="mb-[8px] font-semibold text-on-dark-mute">Bulan Mulai <span class="text-accent-danger font-bold">*</span></label>
            <select v-model="eduForm.startMonth" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none appearance-none">
              <option value="" disabled class="bg-surface-elevated">-- Pilih Bulan --</option>
              <option v-for="m in MONTHS" :key="m" :value="m" class="bg-surface-elevated">{{ m }}</option>
            </select>
            <div v-if="eduErrors.startMonth" class="text-accent-danger text-[12px] mt-[4px]">{{ eduErrors.startMonth }}</div>
          </div>
          <div class="flex flex-col"><label class="mb-[8px] font-semibold text-on-dark-mute">Tahun Mulai <span class="text-accent-danger font-bold">*</span></label>
            <select v-model="eduForm.startYear" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none appearance-none">
              <option value="" disabled class="bg-surface-elevated">-- Pilih Tahun --</option>
              <option v-for="y in YEARS" :key="y" :value="y" class="bg-surface-elevated">{{ y }}</option>
            </select>
            <div v-if="eduErrors.startYear" class="text-accent-danger text-[12px] mt-[4px]">{{ eduErrors.startYear }}</div>
          </div>
        </div>
        <label v-if="eduForm.showDate" class="flex items-center gap-[8px] cursor-pointer">
          <input type="checkbox" v-model="eduForm.isCurrent" class="w-[15px] h-[15px] rounded accent-white" />
          <span class="text-[14px] text-on-dark-mute">Saya masih dalam pendidikan ini</span>
        </label>
        <div v-if="eduForm.showDate && !eduForm.isCurrent" class="grid grid-cols-2 gap-[12px]">
          <div class="flex flex-col"><label class="mb-[8px] font-semibold text-on-dark-mute">Bulan Selesai <span class="text-accent-danger font-bold">*</span></label>
            <select v-model="eduForm.endMonth" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none appearance-none">
              <option value="" disabled class="bg-surface-elevated">-- Pilih Bulan --</option>
              <option v-for="m in MONTHS" :key="m" :value="m" class="bg-surface-elevated">{{ m }}</option>
            </select>
            <div v-if="eduErrors.endMonth" class="text-accent-danger text-[12px] mt-[4px]">{{ eduErrors.endMonth }}</div>
          </div>
          <div class="flex flex-col"><label class="mb-[8px] font-semibold text-on-dark-mute">Tahun Selesai <span class="text-accent-danger font-bold">*</span></label>
            <select v-model="eduForm.endYear" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none appearance-none">
              <option value="" disabled class="bg-surface-elevated">-- Pilih Tahun --</option>
              <option v-for="y in YEARS" :key="y" :value="y" class="bg-surface-elevated">{{ y }}</option>
            </select>
            <div v-if="eduErrors.endYear" class="text-accent-danger text-[12px] mt-[4px]">{{ eduErrors.endYear }}</div>
          </div>
        </div>
        <div v-if="eduErrors.period" class="text-accent-danger text-[12px]">{{ eduErrors.period }}</div>
        <div class="flex flex-col"><label class="mb-[8px] font-semibold text-on-dark-mute">IPK <span class="text-accent-danger font-bold">*</span></label>
          <input v-model="eduForm.gpa" placeholder="Contoh: 3.50" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
          <span class="text-[12px] text-stone mt-[6px]">Format desimal, skala 0.00 – 4.00</span>
          <div v-if="eduErrors.gpa" class="text-accent-danger text-[12px] mt-[4px]">{{ eduErrors.gpa }}</div>
        </div>
        <!-- Pengalaman Perkuliahan -->
        <div class="border-t border-hairline-dark pt-[16px]">
          <h5 class="text-[14px] font-semibold text-on-dark mb-[12px]">Pengalaman Perkuliahan <span class="text-stone text-[12px] font-normal">(opsional)</span></h5>
          <div class="flex flex-col gap-[8px]">
            <div v-for="(act, actIdx) in eduForm.activities" :key="'act-'+actIdx" class="flex gap-[8px] items-start">
              <span class="text-on-dark-mute text-[14px] mt-[12px] shrink-0">{{ actIdx + 1 }}.</span>
              <textarea v-model="eduForm.activities[actIdx]" :placeholder="'Contoh: Ketua BEM, Asisten Dosen, Lomba Hackathon...'" rows="2" class="flex-1 h-[72px] bg-transparent border border-hairline-dark rounded-[12px] p-[12px] text-[14px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone resize-none"></textarea>
              <button v-if="eduForm.activities.length > 1" @click="eduForm.activities.splice(actIdx, 1)" class="shrink-0 mt-[8px] text-accent-danger text-[16px] w-[32px] h-[32px] rounded-full border border-accent-danger/30 flex items-center justify-center hover:bg-accent-danger/10 transition-colors">✕</button>
            </div>
          </div>
          <button @click="eduForm.activities.push('')" class="mt-[12px] text-[13px] px-[16px] py-[6px] rounded-full border border-hairline-dark text-on-dark hover:bg-surface-elevated transition-colors">+ Tambah Pengalaman</button>
        </div>
        <!-- Relevant Coursework -->
        <div class="border-t border-hairline-dark pt-[16px]">
          <h5 class="text-[14px] font-semibold text-on-dark mb-[4px]">Relevant Coursework <span class="text-stone text-[12px] font-normal">(opsional)</span></h5>
          <span class="text-[12px] text-stone mb-[8px] block">Pisahkan dengan koma. Contoh: Algoritma, Machine Learning, Basis Data</span>
          <textarea v-model="eduForm.coursework" placeholder="Algoritma & Pemrograman, Kecerdasan Buatan, Jaringan Komputer..." rows="2" class="w-full bg-transparent border border-hairline-dark rounded-[12px] p-[12px] text-[14px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone resize-none"></textarea>
        </div>
      </div>
    </div>

    <!-- EXPERIENCE -->
    <div v-else-if="currentId === 'experience'">
      <div v-if="workExperiences.length > 0" class="mb-[24px]">
        <span class="text-[13px] font-semibold text-stone uppercase tracking-[1px] mb-[12px] block">Pengalaman Tersimpan ({{ workExperiences.length }})</span>
        <div v-for="(work, idx) in workExperiences" :key="'work-'+idx" class="border border-hairline-dark rounded-[12px] p-[16px] mb-[12px]">
          <div class="flex justify-between items-start gap-[12px]">
            <div class="flex-1 min-w-0">
              <div class="font-semibold text-on-dark text-[14px]">{{ work.position }}</div>
              <div class="text-[14px] text-on-dark-mute">{{ work.company }}</div>
              <div class="text-[13px] text-stone">{{ work.startMonth }} {{ work.startYear }} – {{ work.current ? 'Sekarang' : work.endMonth + ' ' + work.endYear }}</div>
              <div class="text-[12px] text-stone mt-[4px]">{{ work.jobDescriptions.filter(j => j.trim()).length }} jobdesk</div>
            </div>
            <div class="flex gap-[8px] shrink-0">
              <button @click="editWork(idx)" class="text-[13px] px-[12px] py-[4px] rounded-full border border-hairline-dark text-on-dark-mute hover:bg-surface-elevated transition-colors">Edit</button>
              <button @click="deleteWork(idx)" class="text-[13px] px-[12px] py-[4px] rounded-full border border-accent-danger/30 text-accent-danger hover:bg-accent-danger/10 transition-colors">Hapus</button>
            </div>
          </div>
        </div>
      </div>

      <div class="border border-hairline-dark rounded-[16px] p-[20px]">
        <h4 class="text-[16px] font-semibold text-on-dark mb-[20px]">{{ workEditIndex >= 0 ? 'Edit Pengalaman' : 'Tambah Pengalaman Baru' }}</h4>
        <div class="flex flex-col gap-[16px]">
          <div class="flex flex-col"><label class="mb-[8px] font-semibold text-on-dark-mute">Nama Perusahaan / Organisasi <span class="text-accent-danger font-bold">*</span></label>
            <input v-model="workForm.company" placeholder="Contoh: PT ABC" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
            <div v-if="workErrors.company" class="text-accent-danger text-[12px] mt-[4px]">{{ workErrors.company }}</div>
          </div>
          <div class="flex flex-col"><label class="mb-[8px] font-semibold text-on-dark-mute">Lokasi</label>
            <input v-model="workForm.location" placeholder="Contoh: Jakarta, Indonesia" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
          </div>
          <div class="flex flex-col"><label class="mb-[8px] font-semibold text-on-dark-mute">Posisi/Jabatan <span class="text-accent-danger font-bold">*</span></label>
            <input v-model="workForm.position" placeholder="Contoh: Frontend Developer" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
            <div v-if="workErrors.position" class="text-accent-danger text-[12px] mt-[4px]">{{ workErrors.position }}</div>
          </div>
          <div class="grid grid-cols-2 gap-[12px]">
            <div class="flex flex-col"><label class="mb-[8px] font-semibold text-on-dark-mute">Bulan Mulai <span class="text-accent-danger font-bold">*</span></label>
              <select v-model="workForm.startMonth" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none appearance-none">
                <option value="" disabled class="bg-surface-elevated">-- Pilih Bulan --</option>
                <option v-for="m in MONTHS" :key="m" :value="m" class="bg-surface-elevated">{{ m }}</option>
              </select>
              <div v-if="workErrors.startMonth" class="text-accent-danger text-[12px] mt-[4px]">{{ workErrors.startMonth }}</div>
            </div>
            <div class="flex flex-col"><label class="mb-[8px] font-semibold text-on-dark-mute">Tahun Mulai <span class="text-accent-danger font-bold">*</span></label>
              <select v-model="workForm.startYear" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none appearance-none">
                <option value="" disabled class="bg-surface-elevated">-- Pilih Tahun --</option>
                <option v-for="y in YEARS" :key="y" :value="y" class="bg-surface-elevated">{{ y }}</option>
              </select>
              <div v-if="workErrors.startYear" class="text-accent-danger text-[12px] mt-[4px]">{{ workErrors.startYear }}</div>
            </div>
          </div>
          <label class="flex items-center gap-[8px] cursor-pointer">
            <input type="checkbox" v-model="workForm.current" class="w-[15px] h-[15px] rounded accent-white" />
            <span class="text-[14px] text-on-dark-mute">Saya masih bekerja di sini</span>
          </label>
          <div v-if="!workForm.current" class="grid grid-cols-2 gap-[12px]">
            <div class="flex flex-col"><label class="mb-[8px] font-semibold text-on-dark-mute">Bulan Selesai <span class="text-accent-danger font-bold">*</span></label>
              <select v-model="workForm.endMonth" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none appearance-none">
                <option value="" disabled class="bg-surface-elevated">-- Pilih Bulan --</option>
                <option v-for="m in MONTHS" :key="m" :value="m" class="bg-surface-elevated">{{ m }}</option>
              </select>
              <div v-if="workErrors.endMonth" class="text-accent-danger text-[12px] mt-[4px]">{{ workErrors.endMonth }}</div>
            </div>
            <div class="flex flex-col"><label class="mb-[8px] font-semibold text-on-dark-mute">Tahun Selesai <span class="text-accent-danger font-bold">*</span></label>
              <select v-model="workForm.endYear" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none appearance-none">
                <option value="" disabled class="bg-surface-elevated">-- Pilih Tahun --</option>
                <option v-for="y in YEARS" :key="y" :value="y" class="bg-surface-elevated">{{ y }}</option>
              </select>
              <div v-if="workErrors.endYear" class="text-accent-danger text-[12px] mt-[4px]">{{ workErrors.endYear }}</div>
            </div>
          </div>
          <div v-if="workErrors.period" class="text-accent-danger text-[12px]">{{ workErrors.period }}</div>
          <div class="border-t border-hairline-dark pt-[16px]">
            <h5 class="text-[14px] font-semibold text-on-dark mb-[12px]">Jobdesk / Deskripsi Pekerjaan <span class="text-accent-danger font-bold">*</span></h5>
            <div class="flex flex-col gap-[8px]">
              <div v-for="(jd, jdIdx) in workForm.jobDescriptions" :key="'jd-'+jdIdx" class="flex gap-[8px] items-start">
                <span class="text-on-dark-mute text-[14px] mt-[12px] shrink-0">{{ jdIdx + 1 }}.</span>
                <textarea v-model="workForm.jobDescriptions[jdIdx]" :placeholder="'Deskripsi pekerjaan #' + (jdIdx + 1)" rows="2" class="flex-1 h-40 bg-transparent border border-hairline-dark rounded-[12px] p-[12px] text-[14px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone resize-none"></textarea>
                <button v-if="workForm.jobDescriptions.length > 1" @click="workForm.jobDescriptions.splice(jdIdx, 1)" class="shrink-0 mt-[8px] text-accent-danger text-[16px] w-[32px] h-[32px] rounded-full border border-accent-danger/30 flex items-center justify-center hover:bg-accent-danger/10 transition-colors">✕</button>
              </div>
            </div>
            <div v-if="workErrors.jobDescriptions" class="text-accent-danger text-[12px] mt-[4px]">{{ workErrors.jobDescriptions }}</div>
            <button @click="workForm.jobDescriptions.push('')" class="mt-[12px] text-[13px] px-[16px] py-[6px] rounded-full border border-hairline-dark text-on-dark hover:bg-surface-elevated transition-colors">+ Tambah Jobdesk</button>
          </div>
        </div>
        <div class="flex gap-[12px] mt-[24px] pt-[16px] border-t border-hairline-dark">
          <button @click="saveWork" class="inline-flex items-center justify-center font-semibold rounded-full transition-all duration-200 cursor-pointer text-[14px] px-[20px] h-[40px] bg-on-dark text-ink hover:bg-white/90">{{ workEditIndex >= 0 ? 'Simpan Perubahan' : 'Simpan Pengalaman' }}</button>
          <button v-if="workEditIndex >= 0" @click="resetWork" class="inline-flex items-center justify-center font-semibold rounded-full transition-all duration-200 cursor-pointer text-[14px] px-[20px] h-[40px] bg-transparent border border-hairline-dark text-on-dark hover:bg-surface-elevated">Batal</button>
        </div>
      </div>
    </div>

    <!-- SKILLS -->
    <div v-else-if="currentId === 'skills'" class="flex flex-col gap-[20px]">
      <div class="flex flex-col">
        <label class="mb-[8px] font-semibold text-on-dark-mute">Keahlian Teknis <span class="text-accent-danger font-bold">*</span>
          <button class="bg-transparent border-none text-white cursor-pointer text-[12px] ml-[12px] px-[8px] py-[2px] rounded-full hover:bg-white/10" @click.prevent="requestSuggestion('technical_skills', 'Keahlian Teknis')">💡 AI Suggestion</button>
        </label>
        <textarea v-model="formData.technical_skills" placeholder="Contoh: Python, Vue.js, SQL, Docker" rows="3" class="w-full bg-transparent border border-hairline-dark rounded-[12px] p-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone resize-none"></textarea>
        <span class="text-[12px] text-stone mt-[6px]">Pisahkan dengan koma. Sebutkan yang relevan dengan posisi yang dilamar.</span>
        <div v-if="suggestions.technical_skills" class="bg-surface-deep px-[16px] py-[12px] rounded-md text-[13px] text-on-dark-mute mt-[8px]"><span class="font-semibold text-white">Saran AI:</span> {{ suggestions.technical_skills }}</div>
      </div>
      <div class="flex flex-col">
        <label class="mb-[8px] font-semibold text-on-dark-mute">Soft Skills <span class="text-accent-danger font-bold">*</span>
          <button class="bg-transparent border-none text-white cursor-pointer text-[12px] ml-[12px] px-[8px] py-[2px] rounded-full hover:bg-white/10" @click.prevent="requestSuggestion('soft_skills', 'Soft Skills')">💡 AI Suggestion</button>
        </label>
        <textarea v-model="formData.soft_skills" placeholder="Contoh: Kepemimpinan, Komunikasi, Pemecahan Masalah" rows="3" class="w-full bg-transparent border border-hairline-dark rounded-[12px] p-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone resize-none"></textarea>
        <span class="text-[12px] text-stone mt-[6px]">Buktikan dengan contoh di pengalaman kerja.</span>
        <div v-if="suggestions.soft_skills" class="bg-surface-deep px-[16px] py-[12px] rounded-md text-[13px] text-on-dark-mute mt-[8px]"><span class="font-semibold text-white">Saran AI:</span> {{ suggestions.soft_skills }}</div>
      </div>
    </div>

    <!-- CERTIFICATIONS -->
    <div v-else-if="currentId === 'certifications'" class="flex flex-col gap-[20px]">
      <div class="flex flex-col">
        <label class="mb-[8px] font-semibold text-on-dark-mute">Nama Sertifikasi</label>
        <input v-model="formData.cert_name" placeholder="Contoh: AWS Certified Developer" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
        <span class="text-[12px] text-stone mt-[6px]">Cantumkan nama lengkap sertifikasi</span>
      </div>
      <div class="flex flex-col">
        <label class="mb-[8px] font-semibold text-on-dark-mute">Penerbit</label>
        <input v-model="formData.issuer" placeholder="Contoh: Amazon Web Services" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
        <span class="text-[12px] text-stone mt-[6px]">Gunakan nama lembaga resmi</span>
      </div>
    </div>
  </div>

  <!-- ===== PREVIEW MODE — Modern ATS: clean single-column ===== -->
  <div v-else class="bg-white text-black p-[25px] leading-[1.3]" :style="{ fontFamily: templateFont }">
    <!-- Header -->
    <div :class="useProfilePicture ? 'flex items-start gap-[24px]' : 'text-center'">
      <div v-if="useProfilePicture" class="w-[90px] h-[100px] overflow-hidden shrink-0">
        <img v-if="profilePictureUrl" :src="profilePictureUrl" class="w-full h-full object-cover" />
        <Icon v-else icon="iconamoon:profile-fill" class="w-full h-full text-gray-400" />
      </div>

      <div :class="useProfilePicture ? 'flex-1' : ''">
        <h1 class="text-[30px] font-bold uppercase tracking-[2px] mb-0 leading-none">{{ formData.full_name || '[Nama Anda]' }}</h1>
        <div class="text-[12px] text-gray-500 flex flex-wrap gap-x-[2px]" :class="useProfilePicture ? '' : 'justify-center'">
          <span v-if="formData.phone">{{ formData.phone }} |</span>
          <span v-if="formData.email && !errors.email">{{ formData.email }} |</span>
          <span v-if="formData.linkedin && !errors.linkedin">{{ formData.linkedin }} |</span>
          <span v-if="formData.github && !errors.github">{{ formData.github }} |</span>
          <span v-if="formData.address"> {{ formData.address }}</span>
        </div>
        <p class="text-[12px] text-justify leading-[1.3] mt-[4px]">{{ formData.summary }}</p>
      </div>
    </div>

    <!-- Education -->
    <div v-if="educations.length > 0" class="mt-[8px]">
      <h2 class="text-[15px] font-bold tracking-[1px] mb-[8px] text-black border-b border-black">Pendidikan</h2>
      <div v-for="(edu, i) in educations" :key="i" class="mb-[4px]">
        <div class="flex justify-between items-start">
          <div>
            <div class="text-[12px] font-bold text-black">{{ edu.institution }}<span v-if="edu.location" class="text-gray-500 font-normal"> - {{ edu.location }}</span></div>
            <div class="text-[12px] italic text-black">{{ edu.major }} &nbsp;: {{ formatGPA(edu.gpa) }}/4.00</div>
          </div>
          <div v-if="edu.showDate" class="text-[12px] text-black shrink-0 text-right">
            {{ edu.startMonth }} {{ edu.startYear }} – {{ edu.isCurrent ? 'Sekarang' : edu.endMonth + ' ' + edu.endYear }}
          </div>
        </div>
        <ul v-if="edu.activities && edu.activities.filter(a => a.trim()).length" class="mt-[2px] pl-[16px] list-disc">
          <li v-for="(act, ai) in edu.activities.filter(a => a.trim())" :key="ai" class="text-[11px] mb-0 leading-[1.3] text-black">{{ act }}</li>
          <li v-if="edu.coursework" class="text-[12px] text-black">Mata Kuliah Relevan: {{ edu.coursework }}</li>
        </ul>
      </div>
    </div>

    <!-- Organizational Experience -->
    <div v-if="workExperiences.length > 0" class="mt-[8px] mb-[10px]">
      <h2 class="text-[15px] font-bold tracking-[2px] mb-[6px] text-black border-b border-black">Pengalaman Organisasi</h2>
      <div v-for="(work, i) in workExperiences" :key="i" class="mb-[6px]">
        <div class="flex justify-between items-start">
          <div>
            <div class="text-[12px] font-bold text-black">{{ work.company }}<span v-if="work.location" class="text-gray-500 font-normal"> - {{ work.location }}</span></div>
            <div class="text-[12px] italic text-black">{{ work.position }}</div>
          </div>
          <div class="text-[12px] text-black shrink-0 text-right">{{ work.startMonth }} {{ work.startYear }} – {{ work.current ? 'Sekarang' : work.endMonth + ' ' + work.endYear }}</div>
        </div>
        <ul class="mt-[2px] pl-[16px] list-disc">
          <li v-for="(jd, ji) in work.jobDescriptions.filter(j => j.trim())" :key="ji" class="text-[12px] mb-0 leading-[1.3]">{{ jd }}</li>
        </ul>
      </div>
    </div>

    <!-- Work Experience -->
    <div v-if="workExperiences.length > 0" class="mt-[8px] mb-[10px]">
      <h2 class="text-[15px] uppercase font-bold tracking-[2px] mb-[6px] text-black border-b border-black">Pengalaman Kerja</h2>
      <div v-for="(work, i) in workExperiences" :key="i" class="mb-[6px]">
        <div class="flex justify-between items-start">
          <div>
            <div class="text-[12px] text-black font-bold">{{ work.company }}<span v-if="work.location" class="text-gray-500 font-normal"> - {{ work.location }}</span></div>
            <div class="text-[12px] font-bold italic text-gray-600">{{ work.position }}</div>
          </div>
          <div class="text-[11px] text-gray-500 shrink-0 text-right">{{ work.startMonth }} {{ work.startYear }} – {{ work.current ? 'Sekarang' : work.endMonth + ' ' + work.endYear }}</div>
        </div>
        <ul class="mt-[2px] pl-[16px] list-disc">
          <li v-for="(jd, ji) in work.jobDescriptions.filter(j => j.trim())" :key="ji" class="text-[12px] mb-0 leading-[1.3]">{{ jd }}</li>
        </ul>
      </div>
    </div>

    <!-- Skills -->
    <div v-if="formData.technical_skills || formData.soft_skills" class="mt-[8px] mb-[10px]">
      <h2 class="text-[15px] uppercase font-bold tracking-[2px] mb-[6px] text-black border-b border-black">Keahlian</h2>
      <p v-if="formData.technical_skills" class="text-[12px] mb-[4px]"><strong>Teknis:</strong> {{ formData.technical_skills }}</p>
      <p v-if="formData.soft_skills" class="text-[12px]"><strong>Soft Skills:</strong> {{ formData.soft_skills }}</p>
    </div>

    <!-- Certifications -->
    <div v-if="formData.cert_name" class="mt-[8px] mb-[10px]">
      <h2 class="text-[15px] uppercase font-bold tracking-[2px] mb-[6px] text-black border-b border-black">Sertifikasi</h2>
      <div class="flex justify-between text-[12px]">
        <span class="font-semibold">{{ formData.cert_name }}</span>
        <span class="text-gray-500">{{ formData.issuer }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted, watch } from 'vue'
import { Icon } from '@iconify/vue'
import { MONTHS, YEARS, isPeriodValid, formatGPA, getSuggestion } from '@/composables/useCVShared.js'

const props = defineProps({
  stepIndex: { type: Number, default: 0 },
  isPreview: { type: Boolean, default: false },
  templateFont: { type: String, default: "'Calibri', sans-serif" },
  targetExpertise: { type: String, default: 'Software Development' },
})

const STORE = 'modern'

// ===== STEPS =====
const steps = [
  { id: 'personal_info', title: 'Informasi Pribadi' },
  { id: 'summary', title: 'Ringkasan Profesional' },
  { id: 'education', title: 'Pendidikan' },
  { id: 'experience', title: 'Pengalaman Kerja' },
  { id: 'skills', title: 'Keahlian' },
  { id: 'certifications', title: 'Sertifikasi' },
]

const currentId = computed(() => steps[props.stepIndex]?.id)

// ===== FORM DATA =====
const formData = reactive({ full_name: '', email: '', phone: '', address: '', linkedin: '', github: '', summary: '', technical_skills: '', soft_skills: '', cert_name: '', issuer: '' })
const errors = reactive({ email: '', linkedin: '', github: '' })
const suggestions = reactive({})
const useProfilePicture = ref(false)
const profilePictureUrl = ref('')

// Personal info fields
const personalFields = [
  { key: 'full_name', label: 'Nama Lengkap', placeholder: 'Contoh: Budi Santoso', hint: 'Gunakan nama resmi', required: true },
  { key: 'email', label: 'Email', placeholder: 'Contoh: budi@email.com', hint: 'Gunakan email profesional', required: true },
  { key: 'phone', label: 'Nomor Telepon', placeholder: 'Contoh: +628123456789', hint: 'Sertakan kode negara', required: true },
  { key: 'address', label: 'Alamat', placeholder: 'Contoh: Jakarta, Indonesia', hint: 'Kota dan negara saja', required: false },
  { key: 'linkedin', label: 'URL LinkedIn', placeholder: 'Contoh: linkedin.com/in/budisantoso', hint: 'Pastikan profil publik', required: true },
  { key: 'github', label: 'URL GitHub', placeholder: 'Contoh: github.com/budisantoso', hint: 'Opsional', required: false },
]

function validateEmail() {
  const v = formData.email
  errors.email = v && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) ? 'Format email tidak valid.' : ''
}
function validateLinkedIn() {
  const v = formData.linkedin
  errors.linkedin = v && !/linkedin\.com\/(in|pub|profile)/i.test(v) ? 'Harus berformat linkedin.com/in/...' : ''
}

function validateGitHub() {
  const v = formData.github
  errors.github = v && !/^(https?:\/\/)?(www\.)?github\.com\/[a-zA-Z0-9_-]+/.test(v) ? 'Harus berformat github.com/username' : ''
}

function onProfilePictureChange(e) {
  const file = e.target.files[0]
  if (!file) {
    profilePictureUrl.value = ''
    localStorage.removeItem(`cv_${STORE}_photo`)
    return
  }
  const reader = new FileReader()
  reader.onload = (ev) => {
    profilePictureUrl.value = ev.target.result
    localStorage.setItem(`cv_${STORE}_photo`, ev.target.result)
  }
  reader.readAsDataURL(file)
}

async function requestSuggestion(key, label) {
  suggestions[key] = await getSuggestion(label, props.targetExpertise)
}

// ===== EDUCATION =====
const educations = ref([])
const eduForm = reactive({ major: '', institution: '', location: '', startMonth: '', startYear: '', endMonth: '', endYear: '', gpa: '', showDate: true, isCurrent: false, activities: [''], coursework: '' })
const eduErrors = reactive({})

function clearEduErrors() { Object.keys(eduErrors).forEach(k => delete eduErrors[k]) }

function validateEduForm() {
  clearEduErrors()
  let ok = true
  if (!eduForm.major.trim()) { eduErrors.major = 'Jurusan wajib diisi.'; ok = false }
  if (!eduForm.institution.trim()) { eduErrors.institution = 'Institusi wajib diisi.'; ok = false }
  if (eduForm.showDate) {
    if (!eduForm.startMonth) { eduErrors.startMonth = 'Bulan mulai wajib dipilih.'; ok = false }
    if (!eduForm.startYear) { eduErrors.startYear = 'Tahun mulai wajib dipilih.'; ok = false }
    if (!eduForm.isCurrent) {
      if (!eduForm.endMonth) { eduErrors.endMonth = 'Bulan selesai wajib dipilih.'; ok = false }
      if (!eduForm.endYear) { eduErrors.endYear = 'Tahun selesai wajib dipilih.'; ok = false }
    }
  }
  if (!eduForm.gpa.toString().trim()) { eduErrors.gpa = 'IPK wajib diisi.'; ok = false }
  else { const n = parseFloat(eduForm.gpa); if (isNaN(n) || n < 0 || n > 4) { eduErrors.gpa = 'IPK harus 0.00 – 4.00.'; ok = false } }
  if (eduForm.showDate && !eduForm.isCurrent && eduForm.startMonth && eduForm.startYear && eduForm.endMonth && eduForm.endYear) {
    if (!isPeriodValid(eduForm.startMonth, eduForm.startYear, eduForm.endMonth, eduForm.endYear)) { eduErrors.period = 'Periode selesai tidak boleh lebih awal.'; ok = false }
  }
  return ok
}

function saveEdu() {
  if (!validateEduForm()) return
  educations.value = [{ major: eduForm.major.trim(), institution: eduForm.institution.trim(), location: eduForm.location.trim(), startMonth: eduForm.showDate ? eduForm.startMonth : '', startYear: eduForm.showDate ? eduForm.startYear : '', endMonth: (eduForm.showDate && !eduForm.isCurrent) ? eduForm.endMonth : '', endYear: (eduForm.showDate && !eduForm.isCurrent) ? eduForm.endYear : '', gpa: eduForm.gpa.toString().trim(), showDate: eduForm.showDate, isCurrent: eduForm.isCurrent, activities: eduForm.activities.map(a => a.trim()).filter(a => a), coursework: eduForm.coursework.trim() }]
}

// ===== WORK EXPERIENCE =====
const workExperiences = ref([])
const workEditIndex = ref(-1)
const workForm = reactive({ company: '', location: '', position: '', startMonth: '', startYear: '', endMonth: '', endYear: '', current: false, jobDescriptions: [''] })
const workErrors = reactive({})

function clearWorkErrors() { Object.keys(workErrors).forEach(k => delete workErrors[k]) }

function validateWorkForm() {
  clearWorkErrors(); let ok = true
  if (!workForm.company.trim()) { workErrors.company = 'Nama perusahaan wajib diisi.'; ok = false }
  if (!workForm.position.trim()) { workErrors.position = 'Posisi/jabatan wajib diisi.'; ok = false }
  if (!workForm.startMonth) { workErrors.startMonth = 'Bulan mulai wajib dipilih.'; ok = false }
  if (!workForm.startYear) { workErrors.startYear = 'Tahun mulai wajib dipilih.'; ok = false }
  if (!workForm.current) {
    if (!workForm.endMonth) { workErrors.endMonth = 'Bulan selesai wajib dipilih.'; ok = false }
    if (!workForm.endYear) { workErrors.endYear = 'Tahun selesai wajib dipilih.'; ok = false }
    if (workForm.startMonth && workForm.startYear && workForm.endMonth && workForm.endYear) {
      if (!isPeriodValid(workForm.startMonth, workForm.startYear, workForm.endMonth, workForm.endYear)) { workErrors.period = 'Periode selesai tidak boleh lebih awal.'; ok = false }
    }
  }
  if (workForm.jobDescriptions.length === 0 || workForm.jobDescriptions.every(j => !j.trim())) { workErrors.jobDescriptions = 'Minimal satu jobdesk wajib diisi.'; ok = false }
  else if (workForm.jobDescriptions.some(j => !j.trim())) { workErrors.jobDescriptions = 'Setiap jobdesk tidak boleh kosong.'; ok = false }
  return ok
}

function saveWork() {
  if (!validateWorkForm()) return
  const entry = { company: workForm.company.trim(), location: workForm.location.trim(), position: workForm.position.trim(), startMonth: workForm.startMonth, startYear: workForm.startYear, endMonth: workForm.current ? '' : workForm.endMonth, endYear: workForm.current ? '' : workForm.endYear, current: workForm.current, jobDescriptions: workForm.jobDescriptions.map(j => j.trim()).filter(j => j) }
  if (workEditIndex.value >= 0) workExperiences.value[workEditIndex.value] = entry
  else workExperiences.value.push(entry)
  resetWork()
}

function editWork(idx) {
  const w = workExperiences.value[idx]
  Object.assign(workForm, { company: w.company, location: w.location || '', position: w.position, startMonth: w.startMonth, startYear: w.startYear, endMonth: w.endMonth, endYear: w.endYear, current: w.current, jobDescriptions: [...w.jobDescriptions] })
  if (!workForm.jobDescriptions.length) workForm.jobDescriptions = ['']
  workEditIndex.value = idx; clearWorkErrors()
}

function deleteWork(idx) {
  if (confirm('Hapus pengalaman ini?')) {
    workExperiences.value.splice(idx, 1)
    if (workEditIndex.value === idx) resetWork()
    else if (workEditIndex.value > idx) workEditIndex.value--
  }
}

function resetWork() {
  Object.assign(workForm, { company: '', location: '', position: '', startMonth: '', startYear: '', endMonth: '', endYear: '', current: false, jobDescriptions: [''] })
  workEditIndex.value = -1; clearWorkErrors()
}

// ===== VALIDATION for wizard =====
function validate(stepIdx) {
  const id = steps[stepIdx]?.id
  if (id === 'personal_info') {
    if (!formData.full_name.trim() || !formData.email.trim() || !formData.phone.trim() || !formData.linkedin.trim()) return false
    if (errors.email || errors.linkedin) return false
    return true
  }
  if (id === 'summary') return !!formData.summary.trim()
  if (id === 'education') {
    if (eduForm.major.trim() && eduForm.institution.trim()) saveEdu()
    return educations.value.length > 0
  }
  if (id === 'experience') return workExperiences.value.length > 0
  if (id === 'skills') return !!formData.technical_skills.trim() && !!formData.soft_skills.trim()
  if (id === 'certifications') return true
  return true
}

// ===== TEXT FOR ANALYSIS =====
function getTextForAnalysis() {
  const eduText = educations.value.map(e => `${e.major} di ${e.institution}${e.location ? ', ' + e.location : ''} (IPK: ${e.gpa})`).join('\n')
  const workText = workExperiences.value.map(w => `${w.position} di ${w.company}\nJobdesk: ${w.jobDescriptions.join('; ')}`).join('\n')
  return `Name: ${formData.full_name}\nEmail: ${formData.email} | Phone: ${formData.phone} | Address: ${formData.address}\nLinkedIn: ${formData.linkedin}\nSummary: ${formData.summary}\nEducation: ${eduText}\nWork Experience: ${workText}\nTechnical Skills: ${formData.technical_skills}\nSoft Skills: ${formData.soft_skills}\nCertifications: ${formData.cert_name} from ${formData.issuer}`
}

// ===== COMPUTED =====
const hasPreviewData = computed(() => !!(formData.full_name || formData.summary || educations.value.length || workExperiences.value.length || formData.technical_skills))

// ===== LOCALSTORAGE =====
onMounted(() => {
  try {
    const d = localStorage.getItem(`cv_${STORE}_data`)
    if (d) Object.assign(formData, JSON.parse(d))
    const e = localStorage.getItem(`cv_${STORE}_edu`)
    if (e) { educations.value = JSON.parse(e); if (educations.value.length) { const edu = educations.value[0]; Object.assign(eduForm, { major: edu.major, institution: edu.institution, location: edu.location || '', startMonth: edu.startMonth, startYear: edu.startYear, endMonth: edu.endMonth, endYear: edu.endYear, gpa: edu.gpa, showDate: edu.showDate !== undefined ? edu.showDate : true, isCurrent: edu.isCurrent || false, activities: edu.activities && edu.activities.length ? edu.activities : [''], coursework: edu.coursework || '' }) } }
    const w = localStorage.getItem(`cv_${STORE}_work`)
    if (w) workExperiences.value = JSON.parse(w)
    const photo = localStorage.getItem(`cv_${STORE}_photo`)
    if (photo) { profilePictureUrl.value = photo; useProfilePicture.value = true }
    const usePic = localStorage.getItem(`cv_${STORE}_usePhoto`)
    if (usePic !== null) useProfilePicture.value = usePic === 'true'
  } catch {}
})

watch(formData, v => localStorage.setItem(`cv_${STORE}_data`, JSON.stringify(v)), { deep: true })
watch(educations, v => localStorage.setItem(`cv_${STORE}_edu`, JSON.stringify(v)), { deep: true })
watch(workExperiences, v => localStorage.setItem(`cv_${STORE}_work`, JSON.stringify(v)), { deep: true })
watch(useProfilePicture, v => localStorage.setItem(`cv_${STORE}_usePhoto`, String(v)))

defineExpose({ steps, validate, getTextForAnalysis, hasPreviewData })
</script>
