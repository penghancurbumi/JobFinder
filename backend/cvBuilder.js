import "dotenv/config"
import { GoogleGenerativeAI } from "@google/generative-ai"

const MODEL = "gemma-4-26b-a4b-it"

function getClient() {
  const apiKey = process.env.GEMINI_API_KEY
  if (!apiKey || apiKey === "your_api_key_here") return null
  const genAI = new GoogleGenerativeAI(apiKey)
  return genAI.getGenerativeModel({ model: MODEL })
}

export const CV_SECTIONS = [
  {
    id: "personal_info", title: "Informasi Pribadi", fields: [
      { key: "full_name", label: "Nama Lengkap", placeholder: "Contoh: Budi Santoso", hint: "Gunakan nama resmi", required: true },
      { key: "email", label: "Email", placeholder: "Contoh: budi@email.com", hint: "Gunakan email profesional", required: true },
      { key: "phone", label: "Nomor Telepon", placeholder: "Contoh: +628123456789", hint: "Sertakan kode negara", required: true },
      { key: "address", label: "Alamat", placeholder: "Contoh: Jakarta, Indonesia", hint: "Kota dan negara saja sudah cukup", required: false },
      { key: "linkedin", label: "URL LinkedIn", placeholder: "Contoh: linkedin.com/in/budisantoso", hint: "Pastikan profil LinkedIn publik (gunakan format linkedin.com/...)", required: true },
    ],
  },
  {
    id: "summary", title: "Ringkasan Profesional", fields: [
      { key: "summary", label: "Ringkasan", placeholder: "Ringkasan profesional 2-3 kalimat...", hint: "Sorot pencapaian dengan angka. Maksimal 4 baris.", required: true },
    ],
  },
  {
    id: "education", title: "Pendidikan", fields: [
      { key: "degree", label: "Gelar / Jurusan", placeholder: "Contoh: S1 Teknik Informatika", hint: "Sebutkan jurusan dengan jelas", required: true },
      { key: "institution", label: "Institusi", placeholder: "Contoh: Universitas Indonesia", hint: "Gunakan nama resmi universitas", required: true },
      { key: "gpa", label: "IPK (opsional)", placeholder: "Contoh: 3.8/4.0", hint: "Format desimal, misal 3.8", required: false },
    ],
  },
  {
    id: "experience", title: "Pengalaman Kerja", fields: [
      { key: "company", label: "Perusahaan", placeholder: "Contoh: Tech Corp", hint: "Gunakan nama resmi perusahaan", required: true },
      { key: "position", label: "Posisi", placeholder: "Contoh: Software Engineer Intern", hint: "Gunakan nama jabatan resmi", required: true },
      { key: "description", label: "Deskripsi", placeholder: "Jelaskan tanggung jawab...", hint: "Gunakan kata kerja aktif (Memimpin, Mengembangkan). Sertakan metrik.", required: true },
    ],
  },
  {
    id: "skills", title: "Keahlian", fields: [
      { key: "technical_skills", label: "Keahlian Teknis", placeholder: "Contoh: Python, Vue.js, SQL", hint: "Sebutkan keahlian yang relevan", required: true },
      { key: "soft_skills", label: "Soft Skills", placeholder: "Contoh: Kepemimpinan, Komunikasi", hint: "Buktikan dengan contoh di pengalaman", required: true },
    ],
  },
  {
    id: "certifications", title: "Sertifikasi", fields: [
      { key: "cert_name", label: "Nama Sertifikasi", placeholder: "Contoh: AWS Certified Developer", hint: "Cantumkan nama lengkap sertifikasi", required: false },
      { key: "issuer", label: "Penerbit", placeholder: "Contoh: Amazon Web Services", hint: "Gunakan nama lembaga resmi", required: false },
    ],
  },
]

export async function getSuggestion(fieldLabel, expertise) {
  const model = getClient()
  if (!model) {
    return `Tip for ${fieldLabel}: Be specific, use keywords relevant to ${expertise}, and include measurable achievements.`
  }

  const prompt = `You are an ATS CV expert. Give ONE short, actionable suggestion (max 2 sentences) for filling the "${fieldLabel}" field in a CV for a ${expertise} position.

Keep it concise and practical. Example: "Use action verbs like 'developed' and 'implemented'. Include numbers, e.g., 'Reduced load time by 30%'."`

  try {
    const result = await model.generateContent(prompt)
    return result.response.text().trim()
  } catch {
    return `Tip: Be specific and relevant to ${expertise}.`
  }
}

export function getBuilderSections() {
  return CV_SECTIONS
}
