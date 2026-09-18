<template>
  <div class="w-full flex-1 min-h-0 bg-[#000000] text-white font-sans flex flex-col items-center">
    <div class="w-full max-w-[800px] mx-auto flex flex-col relative flex-1 min-h-0">
  
      <template v-if="!chatStarted">
        <div
          class="w-full flex-1 min-h-0 flex flex-col items-center justify-end md:justify-center px-[20px] md:px-0 pt-[48px] pb-[24px] md:py-[64px]"
        >

          <!-- Heading -->
          <h1
            class="w-full flex-1 md:flex-none flex items-center justify-center
                   text-[36px] sm:text-[40px] md:text-[44px]
                   font-medium
                   leading-[1.2]
                   tracking-[-0.5px]
                   text-center
                   mb-0 md:mb-[32px]"
          >
            How Can I Help With Your Career?
          </h1>

          <!-- AI Input -->
          <div
            class="w-full p-[14px] md:p-[16px] flex flex-col gap-[10px] md:gap-[12px] bg-[#171717] border border-[#303030] rounded-[16px]"
          >

            <!-- Placeholder / Input -->
            <input
              v-model="input"
              class="w-full h-[24px] bg-transparent border-0 outline-none focus:outline-none focus:ring-0 text-[14px] md:text-[15px] text-white placeholder:text-[#777]"
              placeholder="Ask BidikKerja AI Anything..."
              @keyup.enter="send"
              :disabled="loading"
            />

            <!-- Bottom Controls -->
            <div class="flex items-center justify-between">

              <!-- Attachment -->
              <button
                type="button"
                class="w-[36px] h-[36px] md:w-[40px] md:h-[40px] bg-[#101010] rounded-full flex items-center justify-center text-[#999] hover:text-white hover:bg-white/10 transition-colors"
                aria-label="Tambah lampiran"
              >
                <Icon
                  icon="ant-design:plus-outlined"
                  width="18"
                  height="18"
                />
              </button>

              <!-- Send -->
              <button
                type="button"
                class="w-[36px] h-[36px] md:w-[40px] md:h-[40px] rounded-full bg-[#e5e5e5] text-black flex items-center justify-center transition-all hover:bg-white disabled:opacity-50 disabled:cursor-not-allowed"
                @click="send"
                :disabled="loading || !input.trim()"
                aria-label="Kirim pesan"
              >
                <Icon
                  icon="akar-icons:arrow-up"
                  width="18"
                  height="18"
                />
              </button>

            </div>
          </div>

          <!-- Quick Questions -->
          <div
            class="hidden md:flex w-full flex-wrap justify-center gap-[8px] mt-[16px] md:mt-[20px]"
          >
            <button
              v-for="q in quickQuestions"
              :key="q.text"
              class="bg-[#171717] text-[#999] border border-[#303030] rounded-full px-[12px] md:px-[16px] py-[7px] md:py-[8px] text-[12px] md:text-[13px] font-normal whitespace-nowrap transition-colors hover:bg-[#222] hover:text-white"
              @click="sendQuick(q.text)"
            >
              {{ q.label }}
            </button>
          </div>

        </div>
      </template>

      <template v-else>

        <!-- Chat Messages -->
        <div
          ref="chatRef"
          class="w-full px-[16px] md:px-[24px] pt-[16px] md:pt-[24px] pb-[170px] md:pb-[190px] flex flex-col gap-xxl"
        >

          <div
            v-if="loadingHistory"
            class="font-mono text-[11px] uppercase tracking-[0.5px] font-semibold text-center text-[#777] p-[24px]"
          >
            Memuat riwayat...
          </div>

          <div
            v-for="(msg, i) in messages"
            :key="i"
            class="flex"
            :class="
              msg.role === 'user'
                ? 'justify-end'
                : 'justify-start'
            "
          >
            <!-- Output AI: tanpa bubble / background -->
            <div
              v-if="msg.role === 'assistant'"
              class="w-full text-[14px] md:text-[15px] leading-[1.7] whitespace-pre-wrap tracking-[0.24px] text-white"
            >
              <span v-html="renderContent(msg.content)"></span>
              <span v-if="msg.streaming" class="stream-cursor"></span>
            </div>

            <!-- Pesan user: tetap dengan bubble -->
            <div
              v-else
              class="max-w-[88%] md:max-w-[80%] px-[14px] md:px-[16px] py-[10px] md:py-[12px] rounded-[15px] text-[14px] md:text-[15px] leading-[1.6] whitespace-pre-wrap tracking-[0.24px] bg-white text-black rounded-br-[4px]"
            >
              <span v-html="escapeHtml(msg.content)"></span>
            </div>
          </div>

          <!-- Thinking -->
          <div
            v-if="loading"
            class="flex justify-start"
          >
            <div
              class="text-[15px] leading-[1.7] text-white"
            >
              <span class="thinking-dots">
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="dot"></span>
              </span>

              <span class="text-[#777] text-sm">
                AI sedang berpikir
              </span>
            </div>
          </div>

        </div>


        <!-- Fixed Chat Input -->
        <div class="fixed left-1/2 -translate-x-1/2 bottom-[16px] md:bottom-[24px] w-full max-w-[800px] px-[16px] md:px-[24px] z-20">
          <div
            class="w-full
                   p-[14px] md:p-[16px]
                   flex flex-col gap-[10px] md:gap-[12px]
                   bg-[#171717]
                   border border-[#303030]
                   rounded-[16px]"
          >

            <input
              v-model="input"
              class="w-full h-[24px]
                     bg-transparent
                     border-0 outline-none
                     focus:outline-none focus:ring-0
                     text-[14px] md:text-[15px]
                     text-white
                     placeholder:text-[#777]"
              placeholder="Ask BidikKerja AI Anything..."
              @keyup.enter="send"
              :disabled="loading"
            />

            <div class="flex items-center justify-between">

              <button
                type="button"
                class="w-[36px] h-[36px] md:w-[40px] md:h-[40px]
                       rounded-full
                       flex items-center justify-center
                       text-[#999]
                       hover:text-white
                       hover:bg-white/10
                       transition-colors"
                aria-label="Tambah lampiran"
              >
                <Icon
                  icon="ant-design:plus-outlined"
                  width="18"
                  height="18"
                />
              </button>

              <button
                type="button"
                class="w-[36px] h-[36px] md:w-[40px] md:h-[40px]
                       rounded-full
                       bg-[#e5e5e5]
                       text-black
                       flex items-center justify-center
                       transition-all
                       hover:bg-white
                       disabled:opacity-50
                       disabled:cursor-not-allowed"
                @click="send"
                :disabled="loading || !input.trim()"
                aria-label="Kirim pesan"
              >
                <Icon
                  icon="akar-icons:arrow-up"
                  width="18"
                  height="18"
                />
              </button>

            </div>
          </div>
        </div>

      </template>

    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, onUnmounted } from "vue"
import axios from "axios"
import { useHead } from "@vueuse/head"
import { Icon } from "@iconify/vue"

useHead({
  title: 'Asisten AI Karier — BidikKerja',
  meta: [
    { name: 'description', content: 'Konsultasikan perjalanan karier Anda dengan asisten AI. Tanya soal lowongan kerja, strategi membuat CV ATS, tips wawancara, hingga saran pengembangan karier secara personal.' },
    { property: 'og:title', content: 'Asisten AI Karier — BidikKerja' },
    { property: 'og:description', content: 'Dapatkan saran karier personal dari asisten AI untuk persiapan kerja dan pembuatan CV.' },
  ]
})


const messages = ref([])
const input = ref("")
const chatStarted = ref(false)
const loading = ref(false)
const loadingHistory = ref(true)
const chatRef = ref(null)
const sessionId = ref("")
let typeTimers = []

const quickQuestions = [
  { label: "Find Jobs", text: "Bantu saya mencari lowongan kerja yang cocok" },
  { label: "Resume Analysis", text: "Tolong analisis resume/CV saya" },
  { label: "CV Templates", text: "Tampilkan template CV yang tersedia" },
  { label: "Career Advice", text: "Berikan saran pengembangan karier saya" },
  { label: "Application Status", text: "Bagaimana cara memantau status lamaran kerja saya?" }
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
  chatStarted.value = true
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
    window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" })
  })
}
</script>

<style scoped>
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
