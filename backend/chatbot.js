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
  "developer", "engineer", "designer", "design", "ui", "ux",
  "analyst", "admin", "sales", "finance", "accounting", "hrd",
  "backend", "frontend", "fullstack", "mobile", "devops", "cloud", "qa",
]

function isJobQuery(message) {
  const q = message.toLowerCase()
  const adviceWords = ["tips", "bagaimana", "cara", "persiapan", "berikan", "prospek", "ceritakan"]
  if (adviceWords.some(w => q.includes(w))) return false
  return JOB_KEYWORDS.some(kw => q.includes(kw))
}

// ----- Relevance matching for job queries -----
const STOPWORDS = new Set([
  "yang","dan","di","ke","dengan","untuk","dalam","adalah","tidak","akan","dapat","anda","saya","ini","itu","pada","dari","atau","juga","sudah","bisa","harus","lebih","sangat","telah","saat","setelah","seperti","karena","jika","antara","tersebut","secara","mereka","kami","kita","sebuah","hal","bagi",
  "cari","kerja","kerjaan","lowongan","pekerjaan","posisi","bidang","mau","ingin","tolong","info","ada","mencari","tentang","bagaimana","saja","minta","lihat","semua","butuh","apa","kah","dkk","dll","please","bantu",
])

function extractTerms(message) {
  const cleaned = String(message).toLowerCase().replace(/[^a-z0-9\s]/g, " ")
  return [...new Set(cleaned.split(/\s+/).filter((t) => t.length >= 2 && !STOPWORDS.has(t)))]
}

function scoreJob(job, terms) {
  // Match against structured fields only (title, expertise, company, source,
  // jobType, workType). Description is excluded to avoid false positives from
  // short/common substrings (e.g. "ui" inside "juicer", "pilot" in prose).
  const fields = [job.title, job.expertise, job.company, job.source, job.jobType, job.workType]
  const words = new Set(
    fields.flatMap((f) => String(f || "").toLowerCase().split(/[^a-z0-9]+/).filter(Boolean))
  )

  let matched = 0
  for (const t of terms) {
    let hit = false
    for (const w of words) {
      if (t.length <= 2 ? w === t : w.startsWith(t)) { hit = true; break }
    }
    if (hit) matched++
  }
  return terms.length > 0 ? matched / terms.length : 0
}

// Answer a job query purely from the stored jobs (never hallucinate).
function answerJobQuery(message, scrapedJobs) {
  if (!scrapedJobs || scrapedJobs.length === 0) {
    return 'Data lowongan belum tersedia. Silakan tekan tombol "Perbarui Data" terlebih dahulu agar chatbot bisa mencarikan lowongan sesuai keinginanmu.'
  }

  const terms = extractTerms(message)
  if (terms.length === 0) {
    return "Saya bisa bantu mencari lowongan berdasarkan bidang. Contoh:\n- \"lowongan software developer\"\n- \"lowongan UI/UX design\"\n- \"magang data analyst\"\n- \"part time marketing\"\n\nAtau lihat semua lowongan di halaman Peluang."
  }

  const scored = scrapedJobs
    .map((job) => ({ job, score: scoreJob(job, terms) }))
    .filter((s) => s.score > 0)
    .sort((a, b) => b.score - a.score || String(b.job.postedDate || "").localeCompare(String(a.job.postedDate || "")))

  const exact = scored.filter((s) => s.score >= 1)
  if (exact.length > 0) {
    // Enrich sparse exact results with strong partial matches (>= 0.5) so the
    // answer reflects the whole field, e.g. "software developer" also surfaces
    // backend/fullstack/mobile dev roles.
    const list = [...exact]
    if (exact.length < 5) list.push(...scored.filter((s) => s.score >= 0.5 && s.score < 1))
    const seen = new Set()
    const uniq = []
    for (const s of list) {
      if (!seen.has(s.job.url)) { seen.add(s.job.url); uniq.push(s.job) }
      if (uniq.length === 5) break
    }
    return formatJobsAsText(uniq)
  }

  if (scored.length > 0) {
    return `Belum ada lowongan yang cocok persis dengan "${message}" untuk saat ini. Namun, ini lowongan yang mungkin relevan dengan keinginanmu:\n\n${formatJobsAsText(scored.map((s) => s.job))}`
  }

  return `Belum ada lowongan yang cocok dengan "${message}" untuk saat ini. Coba kata kunci lain (misal: "software developer", "UI/UX design", "data analyst", "marketing"), atau lihat semua lowongan di halaman Peluang.`
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

export async function chat(message, history = [], scrapedJobs = []) {
  // Job queries are answered directly from the stored jobs so the chatbot
  // always returns real, relevant listings (never invents jobs).
  if (isJobQuery(message)) {
    return answerJobQuery(message, scrapedJobs)
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
