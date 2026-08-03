import "dotenv/config"
import { GoogleGenerativeAI } from "@google/generative-ai"

const MODEL = "gemini-3.5-flash"

function getClient(systemInstruction) {
  const apiKey = process.env.GEMINI_API_KEY
  if (!apiKey || apiKey === "your_api_key_here") return null
  const genAI = new GoogleGenerativeAI(apiKey)
  return genAI.getGenerativeModel({
    model: MODEL,
    systemInstruction
  })
}

const JOB_KEYWORDS = [
  "cari kerja", "lowongan", "pekerjaan", "job", "kerja",
  "internship", "magang", "karir", "career", "posisi",
  "graphic design", "software", "data", "marketing", "it",
  "apply", "lamar", "hire", "recruit", "vacancy",
  "lulusan", "fresh graduate", "entry level",
]

function isJobQuery(message) {
  const q = message.toLowerCase()
  const adviceWords = ["tips", "bagaimana", "cara", "persiapan", "berikan", "prospek", "ceritakan"]
  if (adviceWords.some(w => q.includes(w))) return false
  return JOB_KEYWORDS.some(kw => q.includes(kw))
}

function formatJobsAsText(jobs, limit = 5) {
  if (!jobs || jobs.length === 0) return ""
  const shown = jobs.slice(0, limit)
  let text = `Saya menemukan ${jobs.length} peluang yang cocok untuk Anda:\n\n`
  shown.forEach((job, i) => {
    text += `${i + 1}. ${job.title}\n`
    text += `   Perusahaan: ${job.company}\n`
    text += `   Lokasi: ${job.location}\n`
    text += `   Tipe: ${job.jobType || "Pekerjaan"}\n`
    text += `   Bidang: ${job.expertise}\n`
    text += `   Sumber: ${job.source}\n`
    text += `   Lamar di: ${job.url}\n\n`
  })
  if (jobs.length > limit) {
    text += `...dan ${jobs.length - limit} peluang lainnya. Gunakan fitur pencarian di halaman Peluang untuk detail lebih lanjut.\n`
  }
  return text
}

function cleanOutput(text) {
  let result = text

  // 1. Strip <FINAL_ANSWER> wrapper if present
  result = result.replace(/<\/?FINAL_ANSWER>/gi, "")

  // 2. Split into paragraphs
  let paragraphs = result.split(/\n\s*\n/).map(p => p.trim()).filter(Boolean)

  // Known English meta prefixes to strip before scoring
  const metaPrefix = /^(Final\s+\w+|Text|Answer|Response|Let'?s\s+\w+)[\s:.]*/i

  // Strip prefixes first, then filter
  const stripped = paragraphs.map(p => ({
    original: p,
    text: p.replace(metaPrefix, "").trim()
  })).filter(s => s.text.length > 0)

  // Indonesian stop words for scoring
  const idStopWords = ["yang", "dan", "di", "ke", "dengan", "untuk", "dalam", "adalah", "tidak", "akan", "dapat", "anda", "saya", "ini", "itu", "pada", "dari", "atau", "juga", "sudah", "bisa", "harus", "lebih", "sangat", "telah", "saat", "setelah", "seperti", "karena", "jika", "antara", "tersebut", "secara", "mereka", "kami", "kita", "sebuah", "hal", "bagi"]
  const metaMarkers = [
    /^(Career Assistant|Tips for|Friendly|No asterisks|No backticks|Drafting|Final Check|Paragraph \d+:)/i,
    /^\*\s+(Paragraph|Research|Practicing|Closing|Mock)/i,
    /^[•\-*]\s*(Role|Tone|Language|Format|User Question|Paragraph|Constraint|Draft|Self-Correction|Friendly|Neat|Indonesian|Practical)/i,
    /^(Expert AI agent|Professional and friendly|Direct answer|Ensure no prohibited|Removing any potential|Self-Correction)/i,
    /^\*Final Selection/i,
    /^(Wait|Hold on|Let me|Okay,|Alright,|Let'?s go)/i,
  ]

  // Score each paragraph
  const scored = stripped.map(s => {
    const firstLine = s.text.split("\n")[0].trim()
    const isMeta = metaMarkers.some(r => r.test(firstLine))
    const idWordCount = idStopWords.filter(w => s.text.toLowerCase().includes(w)).length
    const totalWords = s.text.split(/\s+/).length
    const idRatio = totalWords > 0 ? idWordCount / totalWords : 0
    const isEnglishPlan = /^[A-Z][a-z]+ (Assistant|for|and|is|are|to|should|can|will|may)/.test(firstLine)
    const englishAlpha = (s.text.match(/[a-zA-Z]/g) || []).length
    const totalAlpha = s.text.replace(/\s/g, "").length
    const englishRatio = totalAlpha > 0 ? englishAlpha / totalAlpha : 0
    const hasIdWord = idWordCount > 0
    return { text: s.text, idRatio, isMeta, isEnglishPlan, englishRatio, hasIdWord }
  })

  // Keep only paragraphs that look like Indonesian answers
  let valid = scored.filter(p =>
    !p.isMeta &&
    !p.isEnglishPlan &&
    (p.hasIdWord || p.text.length > 120) &&
    !(p.englishRatio > 0.8 && !p.hasIdWord)
  )

  // Deduplicate from bottom (model often repeats the answer)
  const seen = new Set()
  const deduped = []
  for (let i = valid.length - 1; i >= 0; i--) {
    const key = valid[i].text.toLowerCase().replace(/\s+/g, " ").slice(0, 80)
    if (!seen.has(key)) {
      seen.add(key)
      deduped.unshift(valid[i])
    }
  }

  // Take only the last 3 paragraphs (the actual answer is at the end)
  result = deduped.slice(-3).map(p => p.text).join("\n\n")

  // 3. Strip remaining markdown artifacts
  result = result.replace(/\*\*(.*?)\*\*/g, "$1")
  result = result.replace(/\*(.*?)\*/g, "$1")
  result = result.replace(/`[^`]*`/g, "")
  result = result.replace(/^[ \t]+/gm, "")
  result = result.replace(/\n{3,}/g, "\n\n")

  return result.trim()
}

function formatJobSearchResult(jobs, query) {
  if (!jobs || jobs.length === 0) {
    return `Maaf, saya tidak menemukan lowongan yang cocok dengan "${query}" saat ini. Coba gunakan kata kunci lain atau periksa kembali halaman Peluang untuk data terbaru.`
  }
  return formatJobsAsText(jobs)
}

export async function chat(message, history = [], scrapedJobs = []) {
  if (isJobQuery(message) && scrapedJobs.length > 0) {
    const q = message.toLowerCase()
    const filtered = scrapedJobs.filter(j => {
      const searchText = `${j.title} ${j.expertise} ${j.company} ${j.description || ""} ${j.source}`.toLowerCase()
      return searchText.includes(q)
    })

    if (filtered.length > 0) {
      return cleanOutput(formatJobSearchResult(filtered, q))
    }

    const broadFilter = scrapedJobs.filter(j => {
      const searchText = `${j.title} ${j.expertise} ${j.company} ${j.description || ""}`.toLowerCase()
      const keywords = q.split(/\s+/).filter(k => k.length > 2)
      return keywords.some(k => searchText.includes(k))
    })

    if (broadFilter.length > 0) {
      return cleanOutput(formatJobSearchResult(broadFilter, q))
    }
  }

  const SYSTEM_PROMPT = `Kamu adalah asisten karir yang membantu pengguna mencari pekerjaan dan mengembangkan karir.

Tugasmu adalah menjawab pertanyaan dengan bahasa Indonesia yang ramah, padat, dan profesional.
Aturan:
- Jawab langsung dalam 2-3 paragraf pendek saja.
- Gunakan bahasa Indonesia saja.
- Berikan saran yang praktis dan spesifik.
- JANGAN gunakan tanda bintang (*), backtick (\`), atau format markdown apapun.
- JANGAN merencanakan, mendraft, atau memeriksa jawabanmu. Langsung tulis jawaban akhir.
- INGAT: jawab LANGSUNG tanpa ada proses berpikir yang dituliskan.`

  const model = getClient(SYSTEM_PROMPT)
  if (!model) return "Asisten sedang tidak tersedia. Silakan konfigurasi GEMINI_API_KEY di .env."

  // Sanitize history: remove markdown artifacts before feeding as context
  const sanitizedHistory = (history || []).slice(-6).map(h => ({
    ...h,
    content: h.content.replace(/\*\*/g, "")
  }))

  let context = "Riwayat percakapan:\n"
  for (const h of sanitizedHistory) {
    context += `${h.role === "user" ? "Pengguna" : "Asisten"}: ${h.content}\n`
  }
  context += `\nPengguna: ${message}\nAsisten:`

  try {
    const result = await model.generateContent(context)
    let rawText = result.response.text()
    return cleanOutput(rawText.trim())
  } catch (e) {
    return `Maaf, terjadi kesalahan: ${e.message}`
  }
}
