<template>
  <div class="min-h-screen pt-[50px] bg-canvas-dark text-on-dark font-sans">
    <div class="w-full mx-auto px-[32px] md:px-[72px]">
      <h1 class="text-[32px] md:text-[40px] font-medium leading-[1.2] tracking-[-0.4px] text-on-dark mb-xs">Asisten AI</h1>
      <p class="text-[16px] font-normal leading-[1.56] tracking-[-0.09px] text-on-dark-mute mb-xl">Konsultasikan perjalanan karir Anda, struktur dokumen CV, hingga strategi wawancara.</p>

    <div class="bg-surface-elevated border border-hairline-dark rounded-[20px] overflow-hidden flex flex-col h-[500px]">
      <div class="flex-1 overflow-y-auto p-xl flex flex-col gap-lg bg-surface-deep" ref="chatRef">
        <div v-if="loadingHistory" class="font-mono text-[11px] uppercase tracking-[0.5px] font-semibold text-center text-stone p-xl">Memuat riwayat...</div>

        <div v-for="(msg, i) in messages" :key="i" class="flex" :class="msg.role === 'user' ? 'justify-end' : 'justify-start'">
          <div class="max-w-[80%] px-[16px] py-[12px] rounded-[20px] text-[15px] leading-[1.6] whitespace-pre-wrap tracking-[0.24px]" 
               :class="msg.role === 'user' ? 'bg-white text-ink rounded-br-[4px]' : 'bg-surface-elevated text-on-dark rounded-bl-[4px]'">
            <span v-html="msg.role === 'assistant' ? renderContent(msg.content) : escapeHtml(msg.content)"></span><span v-if="msg.streaming" class="stream-cursor"></span>
          </div>
        </div>

        <div v-if="loading" class="flex justify-start">
          <div class="max-w-[80%] px-[16px] py-[12px] rounded-[20px] text-[15px] leading-[1.6] whitespace-pre-wrap tracking-[0.24px] bg-surface-elevated text-on-dark rounded-bl-[4px]">
            <span class="thinking-dots"><span class="dot"></span><span class="dot"></span><span class="dot"></span></span>
            <span class="text-stone text-sm">AI sedang berpikir</span>
          </div>
        </div>
      </div>

      <div class="w-full overflow-x-auto border-t border-hairline-dark bg-surface-deep scrollbar-hide">
        <div class="flex flex-nowrap gap-sm px-xl py-sm w-max">
          <button
            v-for="q in quickQuestions"
            :key="q.text"
            class="bg-surface-elevated text-on-dark-mute border border-hairline-dark rounded-full px-[14px] py-[6px] text-[13px] font-sans cursor-pointer transition-all duration-200 whitespace-nowrap hover:bg-canvas-dark hover:text-on-dark"
            @click="sendQuick(q.text)"
          >
            {{ q.label }}
          </button>
        </div>
      </div>

      <div class="flex gap-sm px-lg py-sm bg-surface-elevated border-t border-hairline-dark items-center">
        <input class="border-none bg-transparent text-on-dark h-[44px] flex-1 focus:outline-none focus:ring-0 placeholder:text-stone" v-model="input" placeholder="Tanyakan seputar persiapan karir..." @keyup.enter="send" :disabled="loading" />
        <button class="inline-flex items-center justify-center font-medium rounded-full transition-all duration-200 cursor-pointer bg-on-dark text-ink hover:bg-white/90 px-[20px] h-[40px] text-[14px] shrink-0 disabled:opacity-50 disabled:cursor-not-allowed" @click="send" :disabled="loading || !input.trim()">Kirim</button>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, onUnmounted } from "vue"
import axios from "axios"
import { useHead } from "@vueuse/head"

useHead({
  title: 'Asisten AI Karier — JobFinder',
  meta: [
    { name: 'description', content: 'Konsultasikan perjalanan karier Anda dengan asisten AI. Tanya soal lowongan kerja, strategi membuat CV ATS, tips wawancara, hingga saran pengembangan karier secara personal.' },
    { property: 'og:title', content: 'Asisten AI Karier — JobFinder' },
    { property: 'og:description', content: 'Dapatkan saran karier personal dari asisten AI untuk persiapan kerja dan pembuatan CV.' },
  ]
})


const messages = ref([])
const input = ref("")
const loading = ref(false)
const loadingHistory = ref(true)
const chatRef = ref(null)
const sessionId = ref("")
let typeTimers = []

const quickQuestions = [
  { label: "Lowongan Software Dev", text: "Saya ingin cari lowongan software development" },
  { label: "Magang UI/UX Design", text: "Saya ingin cari magang di bidang UI/UX design" },
  { label: "Tips membuat CV ATS", text: "Bagaimana cara membuat CV yang ramah ATS?" },
  { label: "Persiapan wawancara", text: "Berikan tips persiapan wawancara kerja" }
]

onMounted(async () => {
  sessionId.value = crypto.randomUUID()
  if (messages.value.length === 0) {
    messages.value.push({ role: "assistant", content: "Halo! Saya adalah arsitek karir Anda. Apa yang bisa saya bantu terkait dokumentasi profesional atau pencarian kerja Anda hari ini?" })
  }
  loadingHistory.value = false
  scrollDown()
})

onUnmounted(() => {
  typeTimers.forEach(clearInterval)
  typeTimers = []
})

// Escape HTML then turn URLs into clickable links (safe for assistant replies).
function escapeHtml(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
}

function renderContent(text) {
  const escaped = escapeHtml(text)
  return escaped.replace(/(https?:\/\/[^\s<]+)/g, (match) => {
    let url = match
    const trailing = url.match(/[),.;:!?'"]+$/)
    if (trailing) url = url.slice(0, -trailing[0].length)
    return `<a href="${url}" target="_blank" rel="noopener noreferrer" class="chat-link">${url}</a>${match.slice(url.length)}`
  })
}

// Type out the latest assistant message progressively (typewriter effect).
function typeAssistantReply(msg, fullText) {
  msg.content = ""
  msg.streaming = true
  const tickMs = 30
  const ticks = Math.max(18, Math.min(110, Math.round(fullText.length / 9)))
  const chunk = Math.max(1, Math.ceil(fullText.length / ticks))
  let i = 0
  const timer = setInterval(() => {
    i += chunk
    msg.content = fullText.slice(0, i)
    scrollDown()
    if (i >= fullText.length) {
      msg.content = fullText
      msg.streaming = false
      clearInterval(timer)
    }
  }, tickMs)
  typeTimers.push(timer)
}

async function send() {
  if (!input.value.trim() || loading.value) return
  await sendMessage(input.value)
  input.value = ""
}

async function sendQuick(text) {
  if (loading.value) return
  await sendMessage(text)
}

async function sendMessage(text) {
  const userMsg = text
  messages.value.push({ role: "user", content: userMsg })
  loading.value = true
  scrollDown()

  try {
    const { data } = await axios.post("/api/chat", {
      message: userMsg,
      sessionId: sessionId.value,
    })
    if (data.history) {
      messages.value = data.history
    } else {
      messages.value.push({ role: "assistant", content: data.reply })
    }
    const last = messages.value[messages.value.length - 1]
    if (last && last.role === "assistant") {
      typeAssistantReply(last, last.content || "")
    }
  } catch {
    messages.value.push({ role: "assistant", content: "Terjadi kesalahan saat menghubungi asisten. Silakan coba lagi." })
  } finally {
    loading.value = false
    scrollDown()
  }
}

function scrollDown() {
  nextTick(() => {
    if (chatRef.value) chatRef.value.scrollTop = chatRef.value.scrollHeight
  })
}
</script>

<style scoped>
.scrollbar-hide {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.typing::after {
  content: " ";
  display: inline-block;
  width: 6px;
  height: 6px;
  background-color: currentColor;
  border-radius: 50%;
  margin-left: 4px;
  animation: pulse-opacity 1s infinite;
}
.thinking-dots {
  display: inline-flex;
  gap: 3px;
  margin-right: 8px;
  vertical-align: middle;
}
.thinking-dots .dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background-color: currentColor;
  animation: dot-bounce 1.2s infinite;
}
.thinking-dots .dot:nth-child(2) { animation-delay: 0.2s; }
.thinking-dots .dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes dot-bounce {
  0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
  30% { transform: translateY(-3px); opacity: 1; }
}
.stream-cursor {
  display: inline-block;
  width: 7px;
  height: 1em;
  margin-left: 2px;
  vertical-align: -0.15em;
  background-color: currentColor;
  animation: cursor-blink 0.8s step-end infinite;
}
.chat-link {
  color: #93c5fd;
  text-decoration: underline;
  word-break: break-all;
}
.chat-link:hover {
  color: #60a5fa;
}
@keyframes cursor-blink {
  50% { opacity: 0; }
}
</style>
