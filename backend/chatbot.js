import "dotenv/config"
import { GoogleGenerativeAI } from "@google/generative-ai"

const MODEL = "gemma-4-26b-a4b-it"

function getClient() {
  const apiKey = process.env.GEMINI_API_KEY
  if (!apiKey || apiKey === "your_api_key_here") return null
  const genAI = new GoogleGenerativeAI(apiKey)
  return genAI.getGenerativeModel({ model: MODEL })
}

const SYSTEM_PROMPT = `System Prompt: Kamu adalah AI agent handal yang ahli dalam merekrut, menganalisis CV (Resume), dan mencari pekerjaan/internship.

Tugasmu adalah membantu pengguna menemukan peluang, memberikan tips menulis CV, memberikan saran karir, dan persiapan wawancara.
ATURAN SANGAT PENTING FORMAT OUTPUT: 
- Jawab LANGSUNG ke inti pertanyaan pengguna menggunakan Bahasa Indonesia yang profesional dan ramah.
- DILARANG KERAS menyertakan proses berpikir, instruksi internal, label role, self-correction, tone, atau struktur prompt awal (jangan gunakan awalan '* Role:', '* Tone:', '* Crucial Professional Insight:', dll).
- Dilarang membocorkan identitas bahwa kamu sedang membaca prompt.`

export async function chat(message, history = []) {
  const model = getClient()
  if (!model) return "Chatbot is unavailable. Please configure GEMINI_API_KEY in .env."

  let context = SYSTEM_PROMPT + "\n\n"
  for (const h of (history || []).slice(-6)) {
    context += `${h.role}: ${h.content}\n`
  }
  context += `user: ${message}\nassistant:`

  try {
    const result = await model.generateContent(context)
    return result.response.text().trim()
  } catch (e) {
    return `Error: ${e.message}`
  }
}
