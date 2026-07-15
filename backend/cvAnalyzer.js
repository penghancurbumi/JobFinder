import "dotenv/config"
import { GoogleGenerativeAI } from "@google/generative-ai"

const MODEL = "gemma-4-26b-a4b-it"

function getClient() {
  const apiKey = process.env.GEMINI_API_KEY
  if (!apiKey || apiKey === "your_api_key_here") return null
  const genAI = new GoogleGenerativeAI(apiKey)
  return genAI.getGenerativeModel({ model: MODEL })
}

export async function analyzeCV(cvText, expertise) {
  const atsResult = checkATSFormat(cvText)
  if (!atsResult.isATS) {
    return { ats: atsResult, eligible: false, message: "CV not in ATS format — blacklisted. Please reformat your CV.", analysis: null }
  }

  const model = getClient()
  if (!model) {
    return { ats: atsResult, eligible: true, analysis: "AI analysis unavailable (API key not configured)." }
  }

  const prompt = `System Prompt: Kamu adalah AI agent handal yang ahli dalam merekrut, menganalisis CV (Resume), dan mencari pekerjaan/internship di bidang ${expertise}.

Tugasmu adalah menganalisis CV berikut untuk posisi ${expertise}.
Buatlah output dengan rapi, jangan gunakan asterisks (**) untuk bold, gunakan tag HTML <b> </b> jika perlu, atau text biasa. 
Sajikan hasilnya dalam bentuk yang terstruktur:
1. Match Percentage (0-100%).
2. Tabel Komparasi: Buat tabel (gunakan format HTML <table>) yang membandingkan "Keahlian di CV" vs "Keahlian yang Dibutuhkan untuk ${expertise}".
3. Kekuatan (Strengths).
4. Saran Perbaikan.

CV Text:
${cvText.slice(0, 3000)}`

  try {
    const result = await model.generateContent(prompt)
    return { ats: atsResult, eligible: true, analysis: result.response.text() }
  } catch (e) {
    return { ats: atsResult, eligible: true, analysis: `Analysis error: ${e.message}` }
  }
}

const ATS_PATTERNS = [
  /pendidikan|education|university/i,
  /pengalaman|experience/i,
  /keahlian|skills?/i,
  /pekerjaan|employment/i,
  /nama|name/i,
  /kontak|contact|email|phone|telepon/i,
  /ringkasan|summary|profil|profile/i,
  /organisasi|organization/i,
  /sertifikat|certification/i,
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
  return { isATS: percentage >= 50, score: percentage, matchedSections: matched, totalSections: ATS_PATTERNS.length }
}

export { checkATSFormat }
