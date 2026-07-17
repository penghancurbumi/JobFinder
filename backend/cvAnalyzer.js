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

Tolong balas HANYA dengan sebuah JSON object yang valid (tanpa blok markdown seperti \`\`\`json). Format JSON-nya adalah:
{
  "overallScore": 85,
  "summary": "Ringkasan profesional CV dalam 1-2 kalimat.",
  "strengths": ["Kekuatan 1", "Kekuatan 2"],
  "weaknesses": ["Kekurangan 1", "Kekurangan 2"],
  "missingSkills": ["Skill yang kurang 1", "Skill yang kurang 2"],
  "keywordMatch": ["Keyword cocok 1", "Keyword cocok 2"],
  "recommendations": ["Saran 1", "Saran 2"],
  "categories": {
    "Skills": 80,
    "Experience": 75,
    "Education": 90,
    "Projects": 60,
    "Certificates": 50,
    "SoftSkills": 85
  }
}

Skor harus berupa angka 0-100.

CV Text:
${normalizedText.slice(0, 3000)}`

  try {
    const result = await model.generateContent(prompt)
    let analysisStr = result.response.text()
    // Bersihkan dari markdown jika ada
    analysisStr = analysisStr.replace(/```json\n?/g, "").replace(/```\n?/g, "").trim()
    const analysisObj = JSON.parse(analysisStr)
    return { ats: atsResult, eligible: true, analysis: analysisObj }
  } catch (e) {
    return { ats: atsResult, eligible: true, analysis: { error: "Failed to parse AI response as JSON", message: e.message } }
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
