<template>
  <!-- ===== FORM MODE ===== -->
  <div v-if="!isPreview">
    <!-- PERSONAL INFO (no photo, classic style) -->
    <div v-if="currentId === 'personal_info'" class="flex flex-col gap-[20px]">
      <div class="p-[16px] rounded-[12px] bg-white/4 border border-hairline-dark mb-[8px]">
        <p class="text-[13px] text-on-dark-mute">Template <strong class="text-white">Classic ATS</strong> menampilkan format akademis formal tanpa foto. Nama dan kontak akan ditampilkan di tengah.</p>
      </div>
      <div v-for="f in personalFields" :key="f.key" class="flex flex-col">
        <label class="mb-[8px]  text-on-dark-mute">{{ f.label }} <span v-if="f.required" class="text-accent-danger ">*</span></label>
        <input v-if="f.key === 'email'" type="email" v-model="formData[f.key]" :placeholder="f.placeholder" @input="validateEmail" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
        <input v-else-if="f.key === 'linkedin'" type="url" v-model="formData[f.key]" :placeholder="f.placeholder" @input="validateLinkedIn" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
        <input v-else v-model="formData[f.key]" :placeholder="f.placeholder" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
        <span class="text-[12px] text-stone mt-[6px]">{{ f.hint }}</span>
        <div v-if="errors[f.key]" class="text-accent-danger text-[12px] mt-[4px]">{{ errors[f.key] }}</div>
      </div>
    </div>

    <!-- OBJECTIVE (beda dari Modern — singkat dan fokus tujuan karir) -->
    <div v-else-if="currentId === 'objective'" class="flex flex-col gap-[20px]">
      <div class="p-[16px] rounded-[12px] bg-white/4 border border-hairline-dark mb-[8px]">
        <p class="text-[13px] text-on-dark-mute"><strong class="text-white">Objective</strong> berbeda dari ringkasan profesional — tulis tujuan karir Anda secara spesifik dan langsung (1–2 kalimat).</p>
      </div>
      <div class="flex flex-col">
        <label class="mb-[8px]  text-on-dark-mute">Tujuan Karir (Objective) <span class="text-accent-danger ">*</span>
          <button class="bg-transparent border-none text-white cursor-pointer text-[12px] ml-[12px] px-[8px] py-[2px] rounded-full hover:bg-white/10" @click.prevent="requestSuggestion('objective', 'Tujuan Karir')">💡 AI Suggestion</button>
        </label>
        <textarea v-model="formData.objective" placeholder="Contoh: Mencari posisi Software Engineer di perusahaan teknologi terkemuka untuk berkontribusi dalam pengembangan solusi berbasis cloud yang berdampak bagi jutaan pengguna." rows="4" class="w-full bg-transparent border border-hairline-dark rounded-[12px] p-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone resize-none"></textarea>
        <span class="text-[12px] text-stone mt-[6px]">Singkat dan spesifik. Sebutkan posisi yang dituju dan kontribusi yang ingin diberikan. Maksimal 3 kalimat.</span>
        <div v-if="suggestions.objective" class="bg-surface-deep px-[16px] py-[12px] rounded-md text-[13px] text-on-dark-mute mt-[8px]"><span class=" text-white">Saran AI:</span> {{ suggestions.objective }}</div>
      </div>
    </div>

    <!-- EDUCATION -->
    <div v-else-if="currentId === 'education'">
      <div class="flex flex-col gap-[16px]">
        <div class="flex flex-col"><label class="mb-[8px]  text-on-dark-mute">Gelar <span class="text-accent-danger ">*</span></label>
          <input v-model="eduForm.degree" placeholder="Contoh: Sarjana (S1)" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
          <div v-if="eduErrors.degree" class="text-accent-danger text-[12px] mt-[4px]">{{ eduErrors.degree }}</div>
        </div>
        <div class="flex flex-col"><label class="mb-[8px]  text-on-dark-mute">Jurusan <span class="text-accent-danger ">*</span></label>
          <input v-model="eduForm.major" placeholder="Contoh: Ilmu Komputer" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
          <div v-if="eduErrors.major" class="text-accent-danger text-[12px] mt-[4px]">{{ eduErrors.major }}</div>
        </div>
        <div class="flex flex-col"><label class="mb-[8px]  text-on-dark-mute">Institusi / Universitas <span class="text-accent-danger ">*</span></label>
          <input v-model="eduForm.institution" placeholder="Contoh: Universitas Gadjah Mada" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
          <div v-if="eduErrors.institution" class="text-accent-danger text-[12px] mt-[4px]">{{ eduErrors.institution }}</div>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-[12px]">
          <div class="flex flex-col"><label class="mb-[8px]  text-on-dark-mute">Tahun Mulai <span class="text-accent-danger ">*</span></label>
            <select v-model="eduForm.startYear" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none appearance-none">
              <option value="" disabled class="bg-surface-elevated">-- Pilih Tahun --</option>
              <option v-for="y in YEARS" :key="y" :value="y" class="bg-surface-elevated">{{ y }}</option>
            </select>
            <div v-if="eduErrors.startYear" class="text-accent-danger text-[12px] mt-[4px]">{{ eduErrors.startYear }}</div>
          </div>
          <div class="flex flex-col"><label class="mb-[8px]  text-on-dark-mute">Tahun Selesai</label>
            <select v-model="eduForm.endYear" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none appearance-none">
              <option value="" class="bg-surface-elevated">-- Sekarang --</option>
              <option v-for="y in YEARS" :key="y" :value="y" class="bg-surface-elevated">{{ y }}</option>
            </select>
          </div>
        </div>
        <div class="flex flex-col"><label class="mb-[8px]  text-on-dark-mute">IPK <span class="text-accent-danger ">*</span></label>
          <input v-model="eduForm.gpa" placeholder="Contoh: 3.75" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
          <span class="text-[12px] text-stone mt-[6px]">Skala 0.00 – 4.00</span>
          <div v-if="eduErrors.gpa" class="text-accent-danger text-[12px] mt-[4px]">{{ eduErrors.gpa }}</div>
        </div>
        <div class="flex flex-col"><label class="mb-[8px]  text-on-dark-mute">Penghargaan / Prestasi Akademik</label>
          <input v-model="eduForm.honors" placeholder="Contoh: Cum Laude, Beasiswa Bidikmisi" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
          <span class="text-[12px] text-stone mt-[6px]">Opsional. Tambahkan jika ada penghargaan akademik.</span>
        </div>
      </div>
    </div>

    <!-- EXPERIENCE -->
    <div v-else-if="currentId === 'experience'">
      <div v-if="workExperiences.length > 0" class="mb-[24px]">
        <span class="text-[13px]  text-stone uppercase tracking-[1px] mb-[12px] block">Pengalaman Tersimpan ({{ workExperiences.length }})</span>
        <div v-for="(work, idx) in workExperiences" :key="'work-'+idx" class="border border-hairline-dark rounded-[12px] p-[16px] mb-[12px]">
          <div class="flex justify-between items-start gap-[12px]">
            <div class="flex-1 min-w-0">
              <div class=" text-on-dark text-[14px]">{{ work.position }}</div>
              <div class="text-[14px] text-on-dark-mute">{{ work.company }}</div>
              <div class="text-[13px] text-stone">{{ work.startYear }} – {{ work.endYear || 'Sekarang' }}</div>
            </div>
            <div class="flex gap-[8px] shrink-0">
              <button @click="editWork(idx)" class="text-[13px] px-[12px] py-[4px] rounded-full border border-hairline-dark text-on-dark-mute hover:bg-surface-elevated transition-colors">Edit</button>
              <button @click="deleteWork(idx)" class="text-[13px] px-[12px] py-[4px] rounded-full border border-accent-danger/30 text-accent-danger hover:bg-accent-danger/10 transition-colors">Hapus</button>
            </div>
          </div>
        </div>
      </div>
      <div class="border border-hairline-dark rounded-[16px] p-[20px]">
        <h4 class="text-[16px]  text-on-dark mb-[20px]">{{ workEditIndex >= 0 ? 'Edit Pengalaman' : 'Tambah Pengalaman Baru' }}</h4>
        <div class="flex flex-col gap-[16px]">
          <div class="flex flex-col"><label class="mb-[8px]  text-on-dark-mute">Nama Perusahaan / Organisasi <span class="text-accent-danger ">*</span></label>
            <input v-model="workForm.company" placeholder="Contoh: PT Maju Bersama" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
            <div v-if="workErrors.company" class="text-accent-danger text-[12px] mt-[4px]">{{ workErrors.company }}</div>
          </div>
          <div class="flex flex-col"><label class="mb-[8px]  text-on-dark-mute">Posisi / Jabatan <span class="text-accent-danger ">*</span></label>
            <input v-model="workForm.position" placeholder="Contoh: Staff Programmer" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
            <div v-if="workErrors.position" class="text-accent-danger text-[12px] mt-[4px]">{{ workErrors.position }}</div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-[12px]">
            <div class="flex flex-col"><label class="mb-[8px]  text-on-dark-mute">Tahun Mulai <span class="text-accent-danger ">*</span></label>
              <select v-model="workForm.startYear" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none appearance-none">
                <option value="" disabled class="bg-surface-elevated">-- Pilih Tahun --</option>
                <option v-for="y in YEARS" :key="y" :value="y" class="bg-surface-elevated">{{ y }}</option>
              </select>
              <div v-if="workErrors.startYear" class="text-accent-danger text-[12px] mt-[4px]">{{ workErrors.startYear }}</div>
            </div>
            <div class="flex flex-col"><label class="mb-[8px]  text-on-dark-mute">Tahun Selesai</label>
              <select v-model="workForm.endYear" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none appearance-none">
                <option value="" class="bg-surface-elevated">-- Sekarang --</option>
                <option v-for="y in YEARS" :key="y" :value="y" class="bg-surface-elevated">{{ y }}</option>
              </select>
            </div>
          </div>
          <div class="border-t border-hairline-dark pt-[16px]">
            <h5 class="text-[14px]  text-on-dark mb-[12px]">Deskripsi Tugas <span class="text-accent-danger ">*</span></h5>
            <div class="flex flex-col gap-[8px]">
              <div v-for="(jd, jdIdx) in workForm.jobDescriptions" :key="'jd-'+jdIdx" class="flex gap-[8px] items-start">
                <span class="text-on-dark-mute text-[14px] mt-[12px] shrink-0">{{ jdIdx + 1 }}.</span>
                <textarea v-model="workForm.jobDescriptions[jdIdx]" :placeholder="'Deskripsi tugas #' + (jdIdx + 1)" rows="2" class="flex-1 h-40 bg-transparent border border-hairline-dark rounded-[12px] p-[12px] text-[14px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone resize-none"></textarea>
                <button v-if="workForm.jobDescriptions.length > 1" @click="workForm.jobDescriptions.splice(jdIdx, 1)" class="shrink-0 mt-[8px] text-accent-danger text-[16px] w-[32px] h-[32px] rounded-full border border-accent-danger/30 flex items-center justify-center hover:bg-accent-danger/10 transition-colors">✕</button>
              </div>
            </div>
            <div v-if="workErrors.jobDescriptions" class="text-accent-danger text-[12px] mt-[4px]">{{ workErrors.jobDescriptions }}</div>
            <button @click="workForm.jobDescriptions.push('')" class="mt-[12px] text-[13px] px-[16px] py-[6px] rounded-full border border-hairline-dark text-on-dark hover:bg-surface-elevated transition-colors">+ Tambah Deskripsi</button>
          </div>
        </div>
        <div class="flex gap-[12px] mt-[24px] pt-[16px] border-t border-hairline-dark">
          <button @click="saveWork" class="inline-flex items-center justify-center  rounded-full transition-all duration-200 cursor-pointer text-[14px] px-[20px] h-[40px] bg-on-dark text-ink hover:bg-white/90">{{ workEditIndex >= 0 ? 'Simpan Perubahan' : 'Simpan Pengalaman' }}</button>
          <button v-if="workEditIndex >= 0" @click="resetWork" class="inline-flex items-center justify-center  rounded-full transition-all duration-200 cursor-pointer text-[14px] px-[20px] h-[40px] bg-transparent border border-hairline-dark text-on-dark hover:bg-surface-elevated">Batal</button>
        </div>
      </div>
    </div>

    <!-- SKILLS (single combined field — classic style) -->
    <div v-else-if="currentId === 'skills'" class="flex flex-col gap-[20px]">
      <div class="p-[16px] rounded-[12px] bg-white/4 border border-hairline-dark mb-[8px]">
        <p class="text-[13px] text-on-dark-mute">Pada template Classic, keahlian digabung dalam satu bagian. Cantumkan semua skill yang relevan, pisahkan dengan koma atau titik koma.</p>
      </div>
      <div class="flex flex-col">
        <label class="mb-[8px]  text-on-dark-mute">Keahlian <span class="text-accent-danger ">*</span>
          <button class="bg-transparent border-none text-white cursor-pointer text-[12px] ml-[12px] px-[8px] py-[2px] rounded-full hover:bg-white/10" @click.prevent="requestSuggestion('skills', 'Keahlian')">💡 AI Suggestion</button>
        </label>
        <textarea v-model="formData.skills" placeholder="Contoh: Microsoft Office, C++, Java, Manajemen Proyek, Komunikasi, Kepemimpinan, Analisis Data" rows="5" class="w-full bg-transparent border border-hairline-dark rounded-[12px] p-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone resize-none"></textarea>
        <span class="text-[12px] text-stone mt-[6px]">Gabungkan keahlian teknis dan soft skills. Sebutkan yang paling relevan dengan posisi yang dituju.</span>
        <div v-if="suggestions.skills" class="bg-surface-deep px-[16px] py-[12px] rounded-md text-[13px] text-on-dark-mute mt-[8px]"><span class=" text-white">Saran AI:</span> {{ suggestions.skills }}</div>
      </div>
    </div>

    <!-- REFERENCES (unik di Classic — tidak ada di template lain) -->
    <div v-else-if="currentId === 'references'" class="flex flex-col gap-[20px]">
      <div class="p-[16px] rounded-[12px] bg-white/4 border border-hairline-dark mb-[8px]">
        <p class="text-[13px] text-on-dark-mute"><strong class="text-white">Referensi</strong> adalah bagian khas CV formal/klasik. Cantumkan 1–2 orang yang dapat memberikan rekomendasi profesional Anda.</p>
      </div>
      <div class="border border-hairline-dark rounded-[16px] p-[20px]">
        <h4 class="text-[15px]  text-on-dark mb-[16px]">Referensi 1</h4>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-[12px]">
          <div class="flex flex-col"><label class="mb-[8px]  text-on-dark-mute">Nama Lengkap</label>
            <input v-model="formData.ref1_name" placeholder="Contoh: Dr. Andi Wijaya" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
          </div>
          <div class="flex flex-col"><label class="mb-[8px]  text-on-dark-mute">Jabatan</label>
            <input v-model="formData.ref1_title" placeholder="Contoh: Dosen Pembimbing" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
          </div>
          <div class="flex flex-col"><label class="mb-[8px]  text-on-dark-mute">Institusi</label>
            <input v-model="formData.ref1_company" placeholder="Contoh: Universitas Indonesia" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
          </div>
          <div class="flex flex-col"><label class="mb-[8px]  text-on-dark-mute">Kontak (Email/Telepon)</label>
            <input v-model="formData.ref1_contact" placeholder="Contoh: andi@ui.ac.id" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
          </div>
        </div>
      </div>
      <div class="border border-hairline-dark rounded-[16px] p-[20px]">
        <h4 class="text-[15px]  text-on-dark mb-[16px]">Referensi 2 (Opsional)</h4>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-[12px]">
          <div class="flex flex-col"><label class="mb-[8px]  text-on-dark-mute">Nama Lengkap</label>
            <input v-model="formData.ref2_name" placeholder="Contoh: Budi Santosa, S.E." class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
          </div>
          <div class="flex flex-col"><label class="mb-[8px]  text-on-dark-mute">Jabatan</label>
            <input v-model="formData.ref2_title" placeholder="Contoh: Manager HRD" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
          </div>
          <div class="flex flex-col"><label class="mb-[8px]  text-on-dark-mute">Institusi</label>
            <input v-model="formData.ref2_company" placeholder="Contoh: PT Maju Jaya" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
          </div>
          <div class="flex flex-col"><label class="mb-[8px]  text-on-dark-mute">Kontak (Email/Telepon)</label>
            <input v-model="formData.ref2_contact" placeholder="Contoh: +6281234567890" class="w-full bg-transparent border border-hairline-dark rounded-[12px] h-[48px] px-[16px] text-on-dark focus:border-white focus:outline-none placeholder:text-stone" />
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ===== PREVIEW MODE — Classic ATS: formal centered header, thick borders ===== -->
  <div v-else class="bg-white text-black leading-[1.6]" :style="{ fontFamily: templateFont }">
    <div class="p-[48px]">
      <!-- Centered Header -->
      <div class="text-center mb-[6px]">
        <h1 class="text-[24px] uppercase tracking-[3px] mb-[6px]">{{ formData.full_name || '[Nama Anda]' }}</h1>
        <div class="text-[15px] text-gray-600">
          <span v-if="formData.email && !errors.email">{{ formData.email }}</span>
          <span v-if="formData.phone"> &nbsp;|&nbsp; {{ formData.phone }}</span>
          <span v-if="formData.address"> &nbsp;|&nbsp; {{ formData.address }}</span>
          <span v-if="formData.linkedin && !errors.linkedin"> &nbsp;|&nbsp; {{ formData.linkedin }}</span>
        </div>
      </div>

      <!-- Objective -->
      <div v-if="formData.objective" class="mb-[20px]">
        <h2 class="text-[12px] uppercase tracking-[2px] text-center mb-[6px]">Tujuan Karir</h2>
        <div class="h-px bg-black mb-[10px]"></div>
        <p class="text-[12px] italic text-justify">{{ formData.objective }}</p>
      </div>

      <!-- Education -->
      <div v-if="educations.length > 0" class="mb-[20px]">
        <h2 class="text-[12px] uppercase tracking-[2px] text-center mb-[6px]">Pendidikan</h2>
        <div class="h-px bg-black mb-[10px]"></div>
        <div v-for="(edu, i) in educations" :key="i" class="mb-[12px]">
          <div class="flex justify-between items-start">
            <div>
              <div class="text-[12px] uppercase">{{ edu.institution }}</div>
              <div class="text-[12px]">{{ edu.degree }}, {{ edu.major }} &nbsp;|&nbsp; IPK: {{ formatGPA(edu.gpa) }}/4.00</div>
              <div v-if="edu.honors" class="text-[11px] italic text-gray-600">{{ edu.honors }}</div>
            </div>
            <div class="text-[11px] text-gray-500 shrink-0 text-right">
              {{ edu.startYear }} – {{ edu.endYear || 'Sekarang' }}
            </div>
          </div>
        </div>
      </div>

      <!-- Work Experience -->
      <div v-if="workExperiences.length > 0" class="mb-[20px]">
        <h2 class="text-[12px] uppercase tracking-[2px] text-center mb-[6px]">Pengalaman Kerja</h2>
        <div class="h-px bg-black mb-[10px]"></div>
        <div v-for="(work, i) in workExperiences" :key="i" class="mb-[14px]">
          <div class="flex justify-between items-start">
            <div>
              <div class="text-[12px] uppercase">{{ work.company }}</div>
              <div class="text-[12px] italic">{{ work.position }}</div>
            </div>
            <div class="text-[11px] text-gray-500 shrink-0">{{ work.startYear }} – {{ work.endYear || 'Sekarang' }}</div>
          </div>
          <ul class="mt-[4px] pl-[20px] list-disc">
            <li v-for="(jd, ji) in work.jobDescriptions.filter(j => j.trim())" :key="ji" class="text-[12px] mb-[2px]">{{ jd }}</li>
          </ul>
        </div>
      </div>

      <!-- Skills -->
      <div v-if="formData.skills" class="mb-[20px]">
        <h2 class="text-[12px] uppercase tracking-[2px] text-center mb-[6px]">Keahlian</h2>
        <div class="h-px bg-black mb-[10px]"></div>
        <p class="text-[12px] text-center">{{ formData.skills }}</p>
      </div>

      <!-- References -->
      <div v-if="formData.ref1_name" class="mb-[20px]">
        <h2 class="text-[12px]  uppercase tracking-[2px] text-center mb-[6px]">Referensi</h2>
        <div class="h-px bg-black mb-[10px]"></div>
        <div class="grid grid-cols-2 gap-[20px]">
          <div v-if="formData.ref1_name">
            <div class="text-[12px] ">{{ formData.ref1_name }}</div>
            <div class="text-[11px] italic">{{ formData.ref1_title }}</div>
            <div class="text-[11px]">{{ formData.ref1_company }}</div>
            <div class="text-[11px] text-gray-500">{{ formData.ref1_contact }}</div>
          </div>
          <div v-if="formData.ref2_name">
            <div class="text-[12px] ">{{ formData.ref2_name }}</div>
            <div class="text-[11px] italic">{{ formData.ref2_title }}</div>
            <div class="text-[11px]">{{ formData.ref2_company }}</div>
            <div class="text-[11px] text-gray-500">{{ formData.ref2_contact }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted, watch } from 'vue'
import { MONTHS, YEARS, formatGPA, getSuggestion } from '@/composables/useCVShared.js'

const props = defineProps({
  stepIndex: { type: Number, default: 0 },
  isPreview: { type: Boolean, default: false },
  templateFont: { type: String, default: "'Times New Roman', serif" },
  targetExpertise: { type: String, default: 'Software Development' },
})

const STORE = 'classic'

// ===== STEPS — Classic has different sections =====
const steps = [
  { id: 'personal_info', title: 'Informasi Pribadi' },
  { id: 'objective', title: 'Tujuan Karir' },
  { id: 'education', title: 'Pendidikan' },
  { id: 'experience', title: 'Pengalaman Kerja' },
  { id: 'skills', title: 'Keahlian' },
  { id: 'references', title: 'Referensi' },
]

const currentId = computed(() => steps[props.stepIndex]?.id)

// ===== FORM DATA =====
const formData = reactive({ full_name: '', email: '', phone: '', address: '', linkedin: '', objective: '', skills: '', ref1_name: '', ref1_title: '', ref1_company: '', ref1_contact: '', ref2_name: '', ref2_title: '', ref2_company: '', ref2_contact: '' })
const errors = reactive({ email: '', linkedin: '' })
const suggestions = reactive({})

const personalFields = [
  { key: 'full_name', label: 'Nama Lengkap', placeholder: 'Contoh: Siti Rahayu, S.Kom.', hint: 'Gunakan nama resmi beserta gelar jika ada', required: true },
  { key: 'email', label: 'Email', placeholder: 'Contoh: siti@email.com', hint: 'Gunakan email profesional', required: true },
  { key: 'phone', label: 'Nomor Telepon', placeholder: 'Contoh: +628123456789', hint: 'Sertakan kode negara', required: true },
  { key: 'address', label: 'Alamat', placeholder: 'Contoh: Surabaya, Jawa Timur', hint: 'Kota dan provinsi sudah cukup', required: false },
  { key: 'linkedin', label: 'URL LinkedIn', placeholder: 'Contoh: linkedin.com/in/sitirahayu', hint: 'Pastikan profil publik', required: false },
]

function validateEmail() {
  const v = formData.email
  errors.email = v && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) ? 'Format email tidak valid.' : ''
}
function validateLinkedIn() {
  const v = formData.linkedin
  errors.linkedin = v && !/linkedin\.com\/(in|pub|profile)/i.test(v) ? 'Harus berformat linkedin.com/in/...' : ''
}

async function requestSuggestion(key, label) {
  suggestions[key] = await getSuggestion(label, props.targetExpertise)
}

// ===== EDUCATION (simplified for Classic — year only) =====
const educations = ref([])
const eduForm = reactive({ degree: '', major: '', institution: '', startYear: '', endYear: '', gpa: '', honors: '' })
const eduErrors = reactive({})

function clearEduErrors() { Object.keys(eduErrors).forEach(k => delete eduErrors[k]) }

function validateEduForm() {
  clearEduErrors(); let ok = true
  if (!eduForm.degree.trim()) { eduErrors.degree = 'Gelar wajib diisi.'; ok = false }
  if (!eduForm.major.trim()) { eduErrors.major = 'Jurusan wajib diisi.'; ok = false }
  if (!eduForm.institution.trim()) { eduErrors.institution = 'Institusi wajib diisi.'; ok = false }
  if (!eduForm.startYear) { eduErrors.startYear = 'Tahun mulai wajib diisi.'; ok = false }
  if (!eduForm.gpa.toString().trim()) { eduErrors.gpa = 'IPK wajib diisi.'; ok = false }
  else { const n = parseFloat(eduForm.gpa); if (isNaN(n) || n < 0 || n > 4) { eduErrors.gpa = 'IPK harus 0.00–4.00.'; ok = false } }
  return ok
}

function saveEdu() {
  if (!validateEduForm()) return
  educations.value = [{ degree: eduForm.degree.trim(), major: eduForm.major.trim(), institution: eduForm.institution.trim(), startYear: eduForm.startYear, endYear: eduForm.endYear, gpa: eduForm.gpa.toString().trim(), honors: eduForm.honors.trim() }]
}

// ===== WORK EXPERIENCE (year-only for Classic) =====
const workExperiences = ref([])
const workEditIndex = ref(-1)
const workForm = reactive({ company: '', position: '', startYear: '', endYear: '', jobDescriptions: [''] })
const workErrors = reactive({})

function clearWorkErrors() { Object.keys(workErrors).forEach(k => delete workErrors[k]) }

function validateWorkForm() {
  clearWorkErrors(); let ok = true
  if (!workForm.company.trim()) { workErrors.company = 'Nama perusahaan wajib diisi.'; ok = false }
  if (!workForm.position.trim()) { workErrors.position = 'Posisi wajib diisi.'; ok = false }
  if (!workForm.startYear) { workErrors.startYear = 'Tahun mulai wajib dipilih.'; ok = false }
  if (workForm.jobDescriptions.length === 0 || workForm.jobDescriptions.every(j => !j.trim())) { workErrors.jobDescriptions = 'Minimal satu deskripsi wajib diisi.'; ok = false }
  return ok
}

function saveWork() {
  if (!validateWorkForm()) return
  const entry = { company: workForm.company.trim(), position: workForm.position.trim(), startYear: workForm.startYear, endYear: workForm.endYear, jobDescriptions: workForm.jobDescriptions.map(j => j.trim()).filter(j => j) }
  if (workEditIndex.value >= 0) workExperiences.value[workEditIndex.value] = entry
  else workExperiences.value.push(entry)
  resetWork()
}

function editWork(idx) {
  const w = workExperiences.value[idx]
  Object.assign(workForm, { company: w.company, position: w.position, startYear: w.startYear, endYear: w.endYear, jobDescriptions: [...w.jobDescriptions] })
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
  Object.assign(workForm, { company: '', position: '', startYear: '', endYear: '', jobDescriptions: [''] })
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
  if (id === 'objective') return !!formData.objective.trim()
  if (id === 'education') {
    if (eduForm.degree.trim() && eduForm.major.trim() && eduForm.institution.trim()) saveEdu()
    return educations.value.length > 0
  }
  if (id === 'experience') return workExperiences.value.length > 0
  if (id === 'skills') return !!formData.skills.trim()
  if (id === 'references') return true
  return true
}

function getTextForAnalysis() {
  const eduText = educations.value.map(e => `${e.degree} ${e.major} di ${e.institution} (IPK: ${e.gpa})`).join('\n')
  const workText = workExperiences.value.map(w => `${w.position} di ${w.company} (${w.startYear}–${w.endYear || 'Sekarang'})\n${w.jobDescriptions.join('; ')}`).join('\n')
  return `Name: ${formData.full_name}\nContact: ${formData.email} | ${formData.phone} | ${formData.address}\nObjective: ${formData.objective}\nEducation: ${eduText}\nExperience: ${workText}\nSkills: ${formData.skills}`
}

const hasPreviewData = computed(() => !!(formData.full_name || formData.objective || educations.value.length || workExperiences.value.length || formData.skills))

function loadFromStorage() {
  try {
    const d = localStorage.getItem(`cv_${STORE}_data`)
    if (d) Object.assign(formData, JSON.parse(d))
    const e = localStorage.getItem(`cv_${STORE}_edu`)
    if (e) {
      educations.value = JSON.parse(e)
      if (educations.value.length) {
        const edu = educations.value[0]
        Object.assign(eduForm, { degree: edu.degree, major: edu.major, institution: edu.institution, startYear: edu.startYear, endYear: edu.endYear, gpa: edu.gpa, honors: edu.honors || '' })
      }
    }
    const w = localStorage.getItem(`cv_${STORE}_work`)
    if (w) workExperiences.value = JSON.parse(w)
  } catch {}
}

onMounted(() => {
  loadFromStorage()
})

// Saat prop isPreview berubah jadi true (navigasi ke step preview), reload data
watch(() => props.isPreview, (val) => {
  if (val) loadFromStorage()
})

watch(formData, v => localStorage.setItem(`cv_${STORE}_data`, JSON.stringify(v)), { deep: true })
watch(educations, v => localStorage.setItem(`cv_${STORE}_edu`, JSON.stringify(v)), { deep: true })
watch(workExperiences, v => localStorage.setItem(`cv_${STORE}_work`, JSON.stringify(v)), { deep: true })

defineExpose({ steps, validate, getTextForAnalysis, hasPreviewData })
</script>
