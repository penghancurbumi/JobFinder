<template>
  <!-- ===== FORM MODE ===== -->
  <div v-if="!isPreview">
    <!-- PERSONAL INFO (with Designation field) -->
    <div v-if="currentId === 'personal_info'" class="flex flex-col gap-[20px]">
      <div class="p-[16px] rounded-[12px] bg-white/4 border border-hairline-dark mb-[8px]">
        <p class="text-[13px] text-on-dark-mute">Template <strong class="text-white">Executive ATS</strong> menggunakan layout dua kolom premium dengan sidebar. Ideal untuk posisi senior, manajerial, atau eksekutif.</p>
      </div>
      <div class="flex flex-col gap-sm mb-lg">
        <label class="flex items-center gap-sm cursor-pointer w-max">
          <input type="checkbox" v-model="useProfilePicture" class="w-[15px] h-[15px] rounded accent-white" />
          <span class="text-[14px] text-on-dark-mute font-semibold">Gunakan Foto Profil pada Sidebar</span>
        </label>
        <div v-if="useProfilePicture" class="flex flex-col gap-xs mt-sm">
          <div class="flex items-center gap-lg">
            <div class="w-[90px] h-[90px] rounded-full overflow-hidden border-2 border-hairline-dark bg-surface-deep flex shrink-0">
              <img v-if="profilePictureUrl" :src="profilePictureUrl" class="w-full h-full object-cover" />
              <Icon v-else icon="iconamoon:profile-fill" class="text-[60px] text-gray-500 mx-auto my-auto" />
            </div>
            <input type="file" accept="image/*" @change="onProfilePictureChange" class="w-full text-[14px] file:mr-4 file:py-2 file:px-4 file:rounded-full file:border file:border-hairline-dark file:text-sm file:font-medium file:bg-transparent file:text-on-dark hover:file:bg-surface-elevated file:cursor-pointer" />
          </div>
        </div>
      </div>
      <div v-for="f in personalFields" :key="f.key" class="flex flex-col">
        <label class="mb-[8px] font-semibold text-on-dark-mute">{{ f.label }} <span v-if="f.required" class="text-accent-danger font-bold">*</span></label>
        <input v-if="f.key === 'email'" type="email" v-model="formData[f.key]" :placeholder="f.placeholder" @input="validateEmail" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
        <input v-else-if="f.key === 'linkedin'" type="url" v-model="formData[f.key]" :placeholder="f.placeholder" @input="validateLinkedIn" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
        <input v-else v-model="formData[f.key]" :placeholder="f.placeholder" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
        <span class="text-[12px] text-stone mt-[6px]">{{ f.hint }}</span>
        <div v-if="errors[f.key]" class="text-accent-danger text-[12px] mt-[4px]">{{ errors[f.key] }}</div>
      </div>
    </div>

    <!-- EXECUTIVE SUMMARY (lebih panjang dan strategis dari summary biasa) -->
    <div v-else-if="currentId === 'exec_summary'" class="flex flex-col gap-[20px]">
      <div class="p-[16px] rounded-[12px] bg-white/4 border border-hairline-dark mb-[8px]">
        <p class="text-[13px] text-on-dark-mute"><strong class="text-white">Executive Summary</strong> adalah narasi kepemimpinan Anda — 3–5 kalimat yang menyoroti track record, dampak bisnis, dan visi profesional. Lebih kuat dari ringkasan biasa.</p>
      </div>
      <div class="flex flex-col">
        <label class="mb-[8px] font-semibold text-on-dark-mute">Executive Summary <span class="text-accent-danger font-bold">*</span>
          <button class="bg-transparent border-none text-white cursor-pointer text-[12px] ml-[12px] px-[8px] py-[2px] rounded-full hover:bg-white/10" @click.prevent="requestSuggestion('exec_summary', 'Executive Summary')">💡 AI Suggestion</button>
        </label>
        <textarea v-model="formData.exec_summary" placeholder="Contoh: Profesional IT berpengalaman 12+ tahun dalam memimpin transformasi digital enterprise. Terbukti meningkatkan efisiensi operasional sebesar 40% melalui implementasi solusi cloud-native. Berspesialisasi dalam membangun tim lintas fungsi dan menghadirkan produk yang berdampak pada skala jutaan pengguna." rows="6" class="w-full bg-transparent border border-hairline-dark rounded-[12px] p-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone resize-none"></textarea>
        <span class="text-[12px] text-stone mt-[6px]">Sertakan angka dan dampak konkret. Tulis dari perspektif kepemimpinan dan strategi. 3–5 kalimat.</span>
        <div v-if="suggestions.exec_summary" class="bg-surface-deep px-[16px] py-[12px] rounded-md text-[13px] text-on-dark-mute mt-[8px]"><span class="font-semibold text-white">Saran AI:</span> {{ suggestions.exec_summary }}</div>
      </div>
    </div>

    <!-- CORE COMPETENCIES (bullet list, unik di Executive) -->
    <div v-else-if="currentId === 'competencies'" class="flex flex-col gap-[20px]">
      <div class="p-[16px] rounded-[12px] bg-white/4 border border-hairline-dark mb-[8px]">
        <p class="text-[13px] text-on-dark-mute"><strong class="text-white">Core Competencies</strong> adalah daftar keahlian inti berbentuk tag pendek (2–4 kata per item). Ini ditampilkan di sidebar sebagai poin-poin kunci kompetensi Anda.</p>
      </div>
      <div>
        <label class="mb-[12px] font-semibold text-on-dark-mute block">Kompetensi Inti <span class="text-accent-danger font-bold">*</span></label>
        <div class="flex flex-col gap-[8px]">
          <div v-for="(comp, idx) in competencies" :key="'comp-'+idx" class="flex gap-[8px] items-center">
            <span class="text-on-dark-mute text-[14px] shrink-0 w-[20px]">{{ idx + 1 }}.</span>
            <input v-model="competencies[idx]" :placeholder="'Contoh: ' + compPlaceholders[idx % compPlaceholders.length]" class="flex-1 bg-transparent border border-hairline-dark rounded-[10px] h-[42px] px-[14px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone text-[14px]" />
            <button v-if="competencies.length > 1" @click="competencies.splice(idx, 1)" class="shrink-0 text-accent-danger w-[32px] h-[32px] rounded-full border border-accent-danger/30 flex items-center justify-center hover:bg-accent-danger/10 transition-colors text-[14px]">✕</button>
          </div>
        </div>
        <div v-if="compError" class="text-accent-danger text-[12px] mt-[8px]">{{ compError }}</div>
        <button @click="competencies.push('')" class="mt-[12px] text-[13px] px-[16px] py-[6px] rounded-full border border-hairline-dark text-on-dark hover:bg-surface-elevated transition-colors">+ Tambah Kompetensi</button>
        <p class="text-[12px] text-stone mt-[10px]">Rekomendasi: 6–10 kompetensi. Contoh: Strategic Planning, P&L Management, Agile Leadership, Digital Transformation.</p>
      </div>
    </div>

    <!-- EXPERIENCE (with optional Key Achievement per role) -->
    <div v-else-if="currentId === 'experience'">
      <div v-if="workExperiences.length > 0" class="mb-[24px]">
        <span class="text-[13px] font-semibold text-stone uppercase tracking-[1px] mb-[12px] block">Pengalaman Tersimpan ({{ workExperiences.length }})</span>
        <div v-for="(work, idx) in workExperiences" :key="'work-'+idx" class="border border-hairline-dark rounded-[12px] p-[16px] mb-[12px]">
          <div class="flex justify-between items-start gap-[12px]">
            <div class="flex-1 min-w-0">
              <div class="font-semibold text-on-dark text-[14px]">{{ work.position }}</div>
              <div class="text-[14px] text-on-dark-mute">{{ work.company }}<span v-if="work.location"> — {{ work.location }}</span></div>
              <div class="text-[13px] text-stone">{{ work.startMonth }} {{ work.startYear }} – {{ work.current ? 'Sekarang' : work.endMonth + ' ' + work.endYear }}</div>
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
          <div class="grid grid-cols-2 gap-[12px]">
            <div class="flex flex-col col-span-2 sm:col-span-1"><label class="mb-[8px] font-semibold text-on-dark-mute">Nama Perusahaan <span class="text-accent-danger font-bold">*</span></label>
              <input v-model="workForm.company" placeholder="Contoh: PT TechCorp Indonesia" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
              <div v-if="workErrors.company" class="text-accent-danger text-[12px] mt-[4px]">{{ workErrors.company }}</div>
            </div>
            <div class="flex flex-col col-span-2 sm:col-span-1"><label class="mb-[8px] font-semibold text-on-dark-mute">Lokasi</label>
              <input v-model="workForm.location" placeholder="Contoh: Jakarta, Indonesia" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
            </div>
          </div>
          <div class="flex flex-col"><label class="mb-[8px] font-semibold text-on-dark-mute">Posisi / Jabatan <span class="text-accent-danger font-bold">*</span></label>
            <input v-model="workForm.position" placeholder="Contoh: Chief Technology Officer" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
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
            <span class="text-[14px] text-on-dark-mute">Posisi saat ini (masih aktif)</span>
          </label>
          <div v-if="!workForm.current" class="grid grid-cols-2 gap-[12px]">
            <div class="flex flex-col"><label class="mb-[8px] font-semibold text-on-dark-mute">Bulan Selesai <span class="text-accent-danger font-bold">*</span></label>
              <select v-model="workForm.endMonth" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none appearance-none">
                <option value="" disabled class="bg-surface-elevated">-- Pilih Bulan --</option>
                <option v-for="m in MONTHS" :key="m" :value="m" class="bg-surface-elevated">{{ m }}</option>
              </select>
            </div>
            <div class="flex flex-col"><label class="mb-[8px] font-semibold text-on-dark-mute">Tahun Selesai <span class="text-accent-danger font-bold">*</span></label>
              <select v-model="workForm.endYear" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none appearance-none">
                <option value="" disabled class="bg-surface-elevated">-- Pilih Tahun --</option>
                <option v-for="y in YEARS" :key="y" :value="y" class="bg-surface-elevated">{{ y }}</option>
              </select>
            </div>
          </div>
          <div v-if="workErrors.period" class="text-accent-danger text-[12px]">{{ workErrors.period }}</div>
          <div class="border-t border-hairline-dark pt-[16px]">
            <h5 class="text-[14px] font-semibold text-on-dark mb-[4px]">Tanggung Jawab & Pencapaian <span class="text-accent-danger font-bold">*</span></h5>
            <p class="text-[12px] text-stone mb-[12px]">Tulis dengan format pencapaian: "Memimpin X, menghasilkan Y% peningkatan dalam Z."</p>
            <div class="flex flex-col gap-[8px]">
              <div v-for="(jd, jdIdx) in workForm.jobDescriptions" :key="'jd-'+jdIdx" class="flex gap-[8px] items-start">
                <span class="text-on-dark-mute text-[14px] mt-[12px] shrink-0">{{ jdIdx + 1 }}.</span>
                <textarea v-model="workForm.jobDescriptions[jdIdx]" :placeholder="'Pencapaian #' + (jdIdx + 1) + ' (gunakan angka konkret)'" rows="2" class="flex-1 h-40 bg-transparent border border-hairline-dark rounded-[12px] p-[12px] text-[14px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone resize-none"></textarea>
                <button v-if="workForm.jobDescriptions.length > 1" @click="workForm.jobDescriptions.splice(jdIdx, 1)" class="shrink-0 mt-[8px] text-accent-danger text-[16px] w-[32px] h-[32px] rounded-full border border-accent-danger/30 flex items-center justify-center hover:bg-accent-danger/10 transition-colors">✕</button>
              </div>
            </div>
            <div v-if="workErrors.jobDescriptions" class="text-accent-danger text-[12px] mt-[4px]">{{ workErrors.jobDescriptions }}</div>
            <button @click="workForm.jobDescriptions.push('')" class="mt-[12px] text-[13px] px-[16px] py-[6px] rounded-full border border-hairline-dark text-on-dark hover:bg-surface-elevated transition-colors">+ Tambah Poin</button>
          </div>
        </div>
        <div class="flex gap-[12px] mt-[24px] pt-[16px] border-t border-hairline-dark">
          <button @click="saveWork" class="inline-flex items-center justify-center font-semibold rounded-full transition-all duration-200 cursor-pointer text-[14px] px-[20px] h-[40px] bg-on-dark text-ink hover:bg-white/90">{{ workEditIndex >= 0 ? 'Simpan Perubahan' : 'Simpan Pengalaman' }}</button>
          <button v-if="workEditIndex >= 0" @click="resetWork" class="inline-flex items-center justify-center font-semibold rounded-full transition-all duration-200 cursor-pointer text-[14px] px-[20px] h-[40px] bg-transparent border border-hairline-dark text-on-dark hover:bg-surface-elevated">Batal</button>
        </div>
      </div>
    </div>

    <!-- EDUCATION -->
    <div v-else-if="currentId === 'education'">
      <div class="flex flex-col gap-[16px]">
        <div class="flex flex-col"><label class="mb-[8px] font-semibold text-on-dark-mute">Gelar <span class="text-accent-danger font-bold">*</span></label>
          <input v-model="eduForm.degree" placeholder="Contoh: Master of Business Administration (MBA)" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
          <div v-if="eduErrors.degree" class="text-accent-danger text-[12px] mt-[4px]">{{ eduErrors.degree }}</div>
        </div>
        <div class="flex flex-col"><label class="mb-[8px] font-semibold text-on-dark-mute">Jurusan <span class="text-accent-danger font-bold">*</span></label>
          <input v-model="eduForm.major" placeholder="Contoh: Manajemen Strategis" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
          <div v-if="eduErrors.major" class="text-accent-danger text-[12px] mt-[4px]">{{ eduErrors.major }}</div>
        </div>
        <div class="flex flex-col"><label class="mb-[8px] font-semibold text-on-dark-mute">Institusi <span class="text-accent-danger font-bold">*</span></label>
          <input v-model="eduForm.institution" placeholder="Contoh: Universitas Indonesia" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
          <div v-if="eduErrors.institution" class="text-accent-danger text-[12px] mt-[4px]">{{ eduErrors.institution }}</div>
        </div>
        <div class="grid grid-cols-2 gap-[12px]">
          <div class="flex flex-col"><label class="mb-[8px] font-semibold text-on-dark-mute">Tahun Mulai <span class="text-accent-danger font-bold">*</span></label>
            <select v-model="eduForm.startYear" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none appearance-none">
              <option value="" disabled class="bg-surface-elevated">-- Pilih Tahun --</option>
              <option v-for="y in YEARS" :key="y" :value="y" class="bg-surface-elevated">{{ y }}</option>
            </select>
            <div v-if="eduErrors.startYear" class="text-accent-danger text-[12px] mt-[4px]">{{ eduErrors.startYear }}</div>
          </div>
          <div class="flex flex-col"><label class="mb-[8px] font-semibold text-on-dark-mute">Tahun Selesai</label>
            <select v-model="eduForm.endYear" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none appearance-none">
              <option value="" class="bg-surface-elevated">-- Sekarang --</option>
              <option v-for="y in YEARS" :key="y" :value="y" class="bg-surface-elevated">{{ y }}</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- KEY ACHIEVEMENTS (unik di Executive — section tersendiri) -->
    <div v-else-if="currentId === 'achievements'" class="flex flex-col gap-[20px]">
      <div class="p-[16px] rounded-[12px] bg-white/4 border border-hairline-dark mb-[8px]">
        <p class="text-[13px] text-on-dark-mute"><strong class="text-white">Key Achievements</strong> adalah highlight pencapaian karir terbesar Anda — di luar tanggung jawab rutin. Ini yang membuat CV executive menonjol.</p>
      </div>
      <div>
        <label class="mb-[12px] font-semibold text-on-dark-mute block">Pencapaian Utama <span class="text-accent-danger font-bold">*</span>
          <button class="bg-transparent border-none text-white cursor-pointer text-[12px] ml-[12px] px-[8px] py-[2px] rounded-full hover:bg-white/10" @click.prevent="requestSuggestion('achievements', 'Key Achievements')">💡 AI Suggestion</button>
        </label>
        <div class="flex flex-col gap-[8px]">
          <div v-for="(ach, idx) in achievements" :key="'ach-'+idx" class="flex gap-[8px] items-start">
            <span class="text-on-dark-mute text-[14px] mt-[10px] shrink-0">▸</span>
            <textarea v-model="achievements[idx]" :placeholder="'Pencapaian #' + (idx+1) + ': contoh: Berhasil meningkatkan pendapatan 35% dalam 18 bulan dengan strategi digitalisasi end-to-end.'" rows="2" class="flex-1 bg-transparent border border-hairline-dark rounded-[12px] p-[12px] text-[14px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone resize-none"></textarea>
            <button v-if="achievements.length > 1" @click="achievements.splice(idx, 1)" class="shrink-0 mt-[8px] text-accent-danger text-[16px] w-[32px] h-[32px] rounded-full border border-accent-danger/30 flex items-center justify-center hover:bg-accent-danger/10 transition-colors">✕</button>
          </div>
        </div>
        <div v-if="suggestions.achievements" class="bg-surface-deep px-[16px] py-[12px] rounded-md text-[13px] text-on-dark-mute mt-[8px]"><span class="font-semibold text-white">Saran AI:</span> {{ suggestions.achievements }}</div>
        <div v-if="achError" class="text-accent-danger text-[12px] mt-[8px]">{{ achError }}</div>
        <button @click="achievements.push('')" class="mt-[12px] text-[13px] px-[16px] py-[6px] rounded-full border border-hairline-dark text-on-dark hover:bg-surface-elevated transition-colors">+ Tambah Pencapaian</button>
      </div>
    </div>
  </div>

  <!-- ===== PREVIEW MODE — Executive ATS: Two-column with dark sidebar ===== -->
  <div v-else class="bg-white text-black leading-[1.5] flex min-h-[1000px]" :style="{ fontFamily: templateFont }">
    <!-- LEFT SIDEBAR -->
    <div class="w-[200px] shrink-0 bg-[#1a1a2e] text-white p-[24px] flex flex-col gap-[20px]">
      <!-- Profile Picture -->
      <div v-if="useProfilePicture" class="mx-auto">
        <div class="w-[110px] h-[110px] rounded-full overflow-hidden border-2 border-white/30 mx-auto">
          <img v-if="profilePictureUrl" :src="profilePictureUrl" class="w-full h-full object-cover" />
          <Icon v-else icon="iconamoon:profile-fill" class="w-full h-full text-gray-500" />
        </div>
      </div>

      <!-- Name on Sidebar -->
      <div>
        <div class="text-[16px] font-bold uppercase tracking-[1px] leading-[1.2] text-white">{{ formData.full_name || '[Nama Anda]' }}</div>
        <div v-if="formData.designation" class="text-[11px] text-blue-300 mt-[4px] font-medium tracking-[0.5px]">{{ formData.designation }}</div>
      </div>

      <!-- Contact -->
      <div>
        <div class="text-[9px] uppercase font-bold tracking-[2px] text-white/50 mb-[8px]">Kontak</div>
        <div class="flex flex-col gap-[6px]">
          <div v-if="formData.email && !errors.email" class="text-[10px] text-white/80 break-all">{{ formData.email }}</div>
          <div v-if="formData.phone" class="text-[10px] text-white/80">{{ formData.phone }}</div>
          <div v-if="formData.address" class="text-[10px] text-white/80">{{ formData.address }}</div>
          <div v-if="formData.linkedin && !errors.linkedin" class="text-[10px] text-blue-300 break-all">{{ formData.linkedin }}</div>
        </div>
      </div>

      <!-- Core Competencies -->
      <div v-if="filteredCompetencies.length > 0">
        <div class="text-[9px] uppercase font-bold tracking-[2px] text-white/50 mb-[10px]">Kompetensi Inti</div>
        <div class="flex flex-col gap-[6px]">
          <div v-for="(comp, i) in filteredCompetencies" :key="i" class="flex items-center gap-[6px]">
            <div class="w-[4px] h-[4px] rounded-full bg-blue-400 shrink-0"></div>
            <span class="text-[10px] text-white/85 leading-[1.4]">{{ comp }}</span>
          </div>
        </div>
      </div>

      <!-- Education (on sidebar for executive) -->
      <div v-if="educations.length > 0">
        <div class="text-[9px] uppercase font-bold tracking-[2px] text-white/50 mb-[10px]">Pendidikan</div>
        <div v-for="(edu, i) in educations" :key="i" class="mb-[10px]">
          <div class="text-[11px] font-bold text-white">{{ edu.degree }}</div>
          <div class="text-[10px] text-white/70">{{ edu.major }}</div>
          <div class="text-[10px] text-white/50 mt-[2px]">{{ edu.institution }}</div>
          <div class="text-[10px] text-white/40">{{ edu.startYear }}{{ edu.endYear ? ' – ' + edu.endYear : '' }}</div>
        </div>
      </div>
    </div>

    <!-- RIGHT MAIN CONTENT -->
    <div class="flex-1 p-[32px]">
      <!-- Executive Summary -->
      <div v-if="formData.exec_summary" class="mb-[24px]">
        <div class="h-[3px] bg-[#1a1a2e] mb-[12px]"></div>
        <h2 class="text-[10px] uppercase font-bold tracking-[2px] text-[#1a1a2e] mb-[8px]">Executive Summary</h2>
        <p class="text-[12px] leading-[1.7] text-gray-700 text-justify">{{ formData.exec_summary }}</p>
      </div>

      <!-- Work Experience -->
      <div v-if="workExperiences.length > 0" class="mb-[24px]">
        <div class="h-[2px] bg-gray-200 mb-[12px]"></div>
        <h2 class="text-[10px] uppercase font-bold tracking-[2px] text-[#1a1a2e] mb-[12px]">Pengalaman Profesional</h2>
        <div v-for="(work, i) in workExperiences" :key="i" class="mb-[16px]">
          <div class="flex justify-between items-start mb-[2px]">
            <div>
              <div class="text-[13px] font-bold text-[#1a1a2e]">{{ work.position }}</div>
              <div class="text-[11px] text-gray-600 font-medium">{{ work.company }}<span v-if="work.location" class="font-normal"> — {{ work.location }}</span></div>
            </div>
            <div class="text-[10px] text-gray-400 shrink-0 text-right leading-[1.4]">
              {{ work.startMonth }} {{ work.startYear }}<br/>– {{ work.current ? 'Sekarang' : work.endMonth + ' ' + work.endYear }}
            </div>
          </div>
          <ul class="pl-[16px] mt-[4px]" style="list-style-type: '▸ '">
            <li v-for="(jd, ji) in work.jobDescriptions.filter(j => j.trim())" :key="ji" class="text-[11px] text-gray-700 mb-[3px] leading-[1.6]">{{ jd }}</li>
          </ul>
        </div>
      </div>

      <!-- Key Achievements -->
      <div v-if="filteredAchievements.length > 0" class="mb-[24px]">
        <div class="h-[2px] bg-gray-200 mb-[12px]"></div>
        <h2 class="text-[10px] uppercase font-bold tracking-[2px] text-[#1a1a2e] mb-[10px]">Pencapaian Utama</h2>
        <div class="grid grid-cols-1 gap-[6px]">
          <div v-for="(ach, i) in filteredAchievements" :key="i" class="flex gap-[8px] items-start">
            <span class="text-[#1a1a2e] font-bold text-[14px] shrink-0 mt-[-1px]">★</span>
            <p class="text-[11px] text-gray-700 leading-[1.6]">{{ ach }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted, watch } from 'vue'
import { Icon } from '@iconify/vue'
import { MONTHS, YEARS, isPeriodValid, getSuggestion } from '@/composables/useCVShared.js'

const props = defineProps({
  stepIndex: { type: Number, default: 0 },
  isPreview: { type: Boolean, default: false },
  templateFont: { type: String, default: "'Cambria', serif" },
  targetExpertise: { type: String, default: 'Software Development' },
})

const STORE = 'executive'

// ===== STEPS — Executive has unique sections =====
const steps = [
  { id: 'personal_info', title: 'Informasi Pribadi' },
  { id: 'exec_summary', title: 'Executive Summary' },
  { id: 'competencies', title: 'Core Competencies' },
  { id: 'experience', title: 'Pengalaman Profesional' },
  { id: 'education', title: 'Pendidikan' },
  { id: 'achievements', title: 'Key Achievements' },
]

const currentId = computed(() => steps[props.stepIndex]?.id)

const compPlaceholders = ['Strategic Planning', 'Digital Transformation', 'P&L Management', 'Agile Leadership', 'Team Building', 'Stakeholder Management', 'Business Development', 'Change Management']

// ===== FORM DATA =====
const formData = reactive({ full_name: '', designation: '', email: '', phone: '', address: '', linkedin: '', exec_summary: '' })
const errors = reactive({ email: '', linkedin: '' })
const suggestions = reactive({})
const useProfilePicture = ref(false)
const profilePictureUrl = ref('')

const personalFields = [
  { key: 'full_name', label: 'Nama Lengkap', placeholder: 'Contoh: Ahmad Fauzi', hint: 'Gunakan nama resmi', required: true },
  { key: 'designation', label: 'Jabatan / Gelar Profesional', placeholder: 'Contoh: Chief Technology Officer | MBA', hint: 'Gelar atau jabatan yang mencerminkan posisi eksekutif Anda', required: false },
  { key: 'email', label: 'Email', placeholder: 'Contoh: ahmad@perusahaan.com', hint: 'Gunakan email profesional', required: true },
  { key: 'phone', label: 'Nomor Telepon', placeholder: 'Contoh: +628123456789', hint: 'Sertakan kode negara', required: true },
  { key: 'address', label: 'Lokasi', placeholder: 'Contoh: Jakarta, Indonesia', hint: 'Kota dan negara', required: false },
  { key: 'linkedin', label: 'URL LinkedIn', placeholder: 'Contoh: linkedin.com/in/ahmadfauzi', hint: 'Pastikan profil publik', required: false },
]

function validateEmail() {
  const v = formData.email
  errors.email = v && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) ? 'Format email tidak valid.' : ''
}
function validateLinkedIn() {
  const v = formData.linkedin
  errors.linkedin = v && !/linkedin\.com\/(in|pub|profile)/i.test(v) ? 'Harus berformat linkedin.com/in/...' : ''
}
function onProfilePictureChange(e) {
  const file = e.target.files[0]
  profilePictureUrl.value = file ? URL.createObjectURL(file) : ''
}
async function requestSuggestion(key, label) {
  suggestions[key] = await getSuggestion(label, props.targetExpertise)
}

// ===== COMPETENCIES =====
const competencies = ref(['', '', ''])
const compError = ref('')
const filteredCompetencies = computed(() => competencies.value.filter(c => c.trim()))

// ===== ACHIEVEMENTS =====
const achievements = ref(['', ''])
const achError = ref('')
const filteredAchievements = computed(() => achievements.value.filter(a => a.trim()))

// ===== EDUCATION =====
const educations = ref([])
const eduForm = reactive({ degree: '', major: '', institution: '', startYear: '', endYear: '' })
const eduErrors = reactive({})

function clearEduErrors() { Object.keys(eduErrors).forEach(k => delete eduErrors[k]) }

function validateEduForm() {
  clearEduErrors(); let ok = true
  if (!eduForm.degree.trim()) { eduErrors.degree = 'Gelar wajib diisi.'; ok = false }
  if (!eduForm.major.trim()) { eduErrors.major = 'Jurusan wajib diisi.'; ok = false }
  if (!eduForm.institution.trim()) { eduErrors.institution = 'Institusi wajib diisi.'; ok = false }
  if (!eduForm.startYear) { eduErrors.startYear = 'Tahun mulai wajib diisi.'; ok = false }
  return ok
}

function saveEdu() {
  if (!validateEduForm()) return
  educations.value = [{ degree: eduForm.degree.trim(), major: eduForm.major.trim(), institution: eduForm.institution.trim(), startYear: eduForm.startYear, endYear: eduForm.endYear }]
}

// ===== WORK EXPERIENCE =====
const workExperiences = ref([])
const workEditIndex = ref(-1)
const workForm = reactive({ company: '', position: '', location: '', startMonth: '', startYear: '', endMonth: '', endYear: '', current: false, jobDescriptions: [''] })
const workErrors = reactive({})

function clearWorkErrors() { Object.keys(workErrors).forEach(k => delete workErrors[k]) }

function validateWorkForm() {
  clearWorkErrors(); let ok = true
  if (!workForm.company.trim()) { workErrors.company = 'Nama perusahaan wajib diisi.'; ok = false }
  if (!workForm.position.trim()) { workErrors.position = 'Posisi wajib diisi.'; ok = false }
  if (!workForm.startMonth) { workErrors.startMonth = 'Bulan mulai wajib dipilih.'; ok = false }
  if (!workForm.startYear) { workErrors.startYear = 'Tahun mulai wajib dipilih.'; ok = false }
  if (!workForm.current) {
    if (!workForm.endMonth || !workForm.endYear) { workErrors.period = 'Periode selesai wajib diisi.'; ok = false }
    if (workForm.startMonth && workForm.startYear && workForm.endMonth && workForm.endYear) {
      if (!isPeriodValid(workForm.startMonth, workForm.startYear, workForm.endMonth, workForm.endYear)) { workErrors.period = 'Periode selesai tidak boleh lebih awal.'; ok = false }
    }
  }
  if (workForm.jobDescriptions.length === 0 || workForm.jobDescriptions.every(j => !j.trim())) { workErrors.jobDescriptions = 'Minimal satu poin wajib diisi.'; ok = false }
  return ok
}

function saveWork() {
  if (!validateWorkForm()) return
  const entry = { company: workForm.company.trim(), position: workForm.position.trim(), location: workForm.location.trim(), startMonth: workForm.startMonth, startYear: workForm.startYear, endMonth: workForm.current ? '' : workForm.endMonth, endYear: workForm.current ? '' : workForm.endYear, current: workForm.current, jobDescriptions: workForm.jobDescriptions.map(j => j.trim()).filter(j => j) }
  if (workEditIndex.value >= 0) workExperiences.value[workEditIndex.value] = entry
  else workExperiences.value.push(entry)
  resetWork()
}

function editWork(idx) {
  const w = workExperiences.value[idx]
  Object.assign(workForm, { company: w.company, position: w.position, location: w.location || '', startMonth: w.startMonth, startYear: w.startYear, endMonth: w.endMonth, endYear: w.endYear, current: w.current, jobDescriptions: [...w.jobDescriptions] })
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
  Object.assign(workForm, { company: '', position: '', location: '', startMonth: '', startYear: '', endMonth: '', endYear: '', current: false, jobDescriptions: [''] })
  workEditIndex.value = -1; clearWorkErrors()
}

// ===== VALIDATION =====
function validate(stepIdx) {
  const id = steps[stepIdx]?.id
  if (id === 'personal_info') {
    if (!formData.full_name.trim() || !formData.email.trim() || !formData.phone.trim()) return false
    if (errors.email || errors.linkedin) return false
    return true
  }
  if (id === 'exec_summary') return !!formData.exec_summary.trim()
  if (id === 'competencies') {
    compError.value = ''
    if (filteredCompetencies.value.length < 3) { compError.value = 'Minimal 3 kompetensi wajib diisi.'; return false }
    return true
  }
  if (id === 'experience') return workExperiences.value.length > 0
  if (id === 'education') {
    if (eduForm.degree.trim() && eduForm.major.trim() && eduForm.institution.trim()) saveEdu()
    return educations.value.length > 0
  }
  if (id === 'achievements') {
    achError.value = ''
    if (filteredAchievements.value.length < 1) { achError.value = 'Minimal 1 pencapaian wajib diisi.'; return false }
    return true
  }
  return true
}

function getTextForAnalysis() {
  const eduText = educations.value.map(e => `${e.degree} ${e.major} di ${e.institution}`).join('\n')
  const workText = workExperiences.value.map(w => `${w.position} di ${w.company}\n${w.jobDescriptions.join('; ')}`).join('\n')
  return `Name: ${formData.full_name}\nTitle: ${formData.designation}\nContact: ${formData.email} | ${formData.phone}\nLinkedIn: ${formData.linkedin}\nExecutive Summary: ${formData.exec_summary}\nCore Competencies: ${filteredCompetencies.value.join(', ')}\nExperience: ${workText}\nEducation: ${eduText}\nKey Achievements: ${filteredAchievements.value.join('; ')}`
}

const hasPreviewData = computed(() => !!(formData.full_name || formData.exec_summary || workExperiences.value.length || filteredCompetencies.value.length))

// ===== LOCALSTORAGE =====
onMounted(() => {
  try {
    const d = localStorage.getItem(`cv_${STORE}_data`)
    if (d) Object.assign(formData, JSON.parse(d))
    const c = localStorage.getItem(`cv_${STORE}_comp`)
    if (c) competencies.value = JSON.parse(c)
    const a = localStorage.getItem(`cv_${STORE}_ach`)
    if (a) achievements.value = JSON.parse(a)
    const e = localStorage.getItem(`cv_${STORE}_edu`)
    if (e) { educations.value = JSON.parse(e); if (educations.value.length) { const edu = educations.value[0]; Object.assign(eduForm, { degree: edu.degree, major: edu.major, institution: edu.institution, startYear: edu.startYear, endYear: edu.endYear }) } }
    const w = localStorage.getItem(`cv_${STORE}_work`)
    if (w) workExperiences.value = JSON.parse(w)
  } catch {}
})

watch(formData, v => localStorage.setItem(`cv_${STORE}_data`, JSON.stringify(v)), { deep: true })
watch(competencies, v => localStorage.setItem(`cv_${STORE}_comp`, JSON.stringify(v)), { deep: true })
watch(achievements, v => localStorage.setItem(`cv_${STORE}_ach`, JSON.stringify(v)), { deep: true })
watch(educations, v => localStorage.setItem(`cv_${STORE}_edu`, JSON.stringify(v)), { deep: true })
watch(workExperiences, v => localStorage.setItem(`cv_${STORE}_work`, JSON.stringify(v)), { deep: true })

defineExpose({ steps, validate, getTextForAnalysis, hasPreviewData })
</script>
