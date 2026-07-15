import "dotenv/config"
import { GoogleGenerativeAI } from "@google/generative-ai"

const MODEL = "gemma-4-26b-a4b-it"

function getClient(systemInstruction) {
  const apiKey = process.env.GEMINI_API_KEY
  if (!apiKey || apiKey === "your_api_key_here") return null
  const genAI = new GoogleGenerativeAI(apiKey)
  return genAI.getGenerativeModel({ model: MODEL, systemInstruction })
}

// Normalisasi teks PDF: collapse spasi ganda, hapus karakter aneh
function normalizePdfText(text) {
  return text
    .replace(/\r\n/g, "\n")
    .replace(/[ \t]{2,}/g, " ")
    .replace(/([a-zA-Z]) ([a-zA-Z])/g, "$1$2")
    .replace(/[^\x20-\x7E\n\r\u00C0-\u024F\u1E00-\u1EFF]/g, " ")
    .replace(/ {2,}/g, " ")
    .trim()
}

export async function analyzeCV(cvText, expertise) {
  const normalizedText = normalizePdfText(cvText)
  const atsResult = checkATSFormat(normalizedText)

  // Selalu analisis dengan AI, tidak pernah blacklist
  const model = getClient(`Kamu adalah AI agent handal yang ahli dalam merekrut, menganalisis CV, dan mencari pekerjaan/internship di bidang ${expertise}. Jawab dalam bahasa Indonesia. Jangan gunakan asterisks (**) untuk bold. Jangan tampilkan proses berpikirmu.`)
  if (!model) {
    return { ats: atsResult, eligible: true, analysis: "AI analysis unavailable (API key not configured)." }
  }

  const prompt = `Analisis CV berikut untuk posisi ${expertise}.

Sajikan hasilnya dalam format yang rapi dan terstruktur:
1. Skor Kesesuaian (Match Percentage 0-100%).
2. Tabel Komparasi: gunakan format HTML <table> yang membandingkan "Keahlian di CV" vs "Keahlian yang Dibutuhkan untuk ${expertise}".
3. Kekuatan (Strengths) dari CV ini.
4. Saran Perbaikan yang spesifik.
5. Apakah CV ini sudah ATS-friendly? Jelaskan alasannya.

CV Text:
${normalizedText.slice(0, 3000)}`

  try {
    const result = await model.generateContent(prompt)
    let analysis = result.response.text()
    analysis = analysis.replace(/\*\*(.*?)\*\*/g, "$1")
    return { ats: atsResult, eligible: true, analysis }
  } catch (e) {
    return { ats: atsResult, eligible: true, analysis: `Analysis error: ${e.message}` }
  }
}

const ATS_PATTERNS = [
  /pendidikan|education|university|universitas|sekolah|school/i,
  /pengalaman|experience|work\s*history/i,
  /keahlian|skills?|kemampuan|competenc/i,
  /pekerjaan|employment|jabatan|position/i,
  /nama|name|fullname/i,
  /kontak|contact|email|phone|telepon|whatsapp|linkedin|github/i,
  /ringkasan|summary|profil|profile|tentang\s*saya|about\s*me|objective/i,
  /organisasi|organization|volunteering|komunitas/i,
  /sertifikat|certification|lisensi|license/i,
  /proyek|project|portofolio|portfolio/i,
  /bahasa|language/i,
  /alamat|address|domisili|lokasi/i,
]

function checkATSFormat(cvText) {
  let score = 0
  const matched = []
  for (const p of ATS_PATTERNS) {
    if (p.test(cvText)) {
      score++
      matched.push(p.source)
    }
  }
  const percentage = Math.round((score / ATS_PATTERNS.length) * 100)
  return { isATS: percentage >= 25, score: percentage, matchedSections: matched, totalSections: ATS_PATTERNS.length }
}

export { checkATSFormat }
