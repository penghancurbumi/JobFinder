import "dotenv/config"
import { GoogleGenerativeAI } from "@google/generative-ai"

const MODEL = "gemini-3.5-flash"

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
    id: "education", title: "Pendidikan", customForm: true, fields: [],
  },
  {
    id: "experience", title: "Pengalaman Kerja", customForm: true, fields: [],
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
