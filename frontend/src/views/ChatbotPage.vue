<template>
  <div class="min-h-screen pt-[50px] bg-canvas-dark text-on-dark font-sans">
    <div class="w-full max-w-[1200px] mx-auto px-xl">
      <h1 class="text-[32px] md:text-[40px] font-medium leading-[1.2] tracking-[-0.4px] text-on-dark mb-xs">Asisten AI</h1>
    <p class="text-[18px] font-normal leading-[1.56] tracking-[-0.09px] text-on-dark-mute mb-xl">Konsultasikan perjalanan karir Anda, struktur dokumen CV, hingga strategi wawancara.</p>

    <div class="bg-surface-elevated rounded-[20px] overflow-hidden flex flex-col h-[500px]">
      <div class="flex-1 overflow-y-auto p-xl flex flex-col gap-lg bg-surface-deep" ref="chatRef">
        <div v-if="loadingHistory" class="font-mono text-[11px] uppercase tracking-[0.5px] font-semibold text-center text-stone p-xl">Memuat riwayat...</div>

        <div v-for="(msg, i) in messages" :key="i" class="flex" :class="msg.role === 'user' ? 'justify-end' : 'justify-start'">
          <div class="max-w-[80%] px-[16px] py-[12px] rounded-[20px] text-[15px] leading-[1.6] whitespace-pre-wrap tracking-[0.24px]" 
               :class="msg.role === 'user' ? 'bg-white text-ink rounded-br-[4px]' : 'bg-surface-elevated text-on-dark rounded-bl-[4px]'">
            {{ msg.content }}
          </div>
        </div>

        <div v-if="loading" class="flex justify-start">
          <div class="max-w-[80%] px-[16px] py-[12px] rounded-[20px] text-[15px] leading-[1.6] whitespace-pre-wrap tracking-[0.24px] bg-surface-elevated text-on-dark rounded-bl-[4px] typing">Menganalisis...</div>
        </div>
      </div>

      <div class="w-full overflow-x-auto border-t border-hairline-dark bg-surface-deep scrollbar-hide">
        <div class="flex flex-nowrap gap-sm px-xl py-sm w-max">
          <button
            v-for="q in quickQuestions"
            :key="q.text"
            class="bg-surface-elevated text-on-dark-mute border border-hairline-dark rounded-full px-[14px] py-[6px] text-[13px] font-sans cursor-pointer transition-all duration-200 whitespace-nowrap hover:bg-canvas-dark hover:text-on-dark hover:border-primary"
            @click="sendQuick(q.text)"
          >
            {{ q.label }}
          </button>
        </div>
      </div>

      <div class="flex gap-sm px-lg py-sm bg-surface-elevated border-t border-hairline-dark items-center">
        <input class="border-none bg-transparent text-on-dark h-[44px] flex-1 focus:outline-none focus:ring-0 placeholder:text-stone" v-model="input" placeholder="Tanyakan seputar persiapan karir..." @keyup.enter="send" :disabled="loading" />
        <button class="inline-flex items-center justify-center font-semibold rounded-full transition-all duration-200 cursor-pointer bg-on-dark text-ink hover:bg-white/90 px-[20px] h-[40px] text-[14px] shrink-0 disabled:opacity-50 disabled:cursor-not-allowed" @click="send" :disabled="loading || !input.trim()">Kirim</button>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from "vue"
import axios from "axios"

const messages = ref([])
const input = ref("")
const loading = ref(false)
const loadingHistory = ref(true)
const chatRef = ref(null)
const sessionId = ref("")

const quickQuestions = [
  { label: "Lowongan Software Dev", text: "Saya ingin cari lowongan software development" },
  { label: "Magang UI/UX Design", text: "Saya ingin cari magang di bidang UI/UX design" },
  { label: "Tips membuat CV ATS", text: "Bagaimana cara membuat CV yang ramah ATS?" },
  { label: "Persiapan wawancara", text: "Berikan tips persiapan wawancara kerja" }
]

onMounted(async () => {
  sessionId.value = localStorage.getItem("chat_session_id")
  if (!sessionId.value) {
    sessionId.value = crypto.randomUUID()
    localStorage.setItem("chat_session_id", sessionId.value)
  } else {
    await loadHistory()
  }
  if (messages.value.length === 0) {
    messages.value.push({ role: "assistant", content: "Halo! Saya adalah arsitek karir Anda. Apa yang bisa saya bantu terkait dokumentasi profesional atau pencarian kerja Anda hari ini?" })
  }
  loadingHistory.value = false
  scrollDown()
})

async function loadHistory() {
  try {
    const { data } = await axios.get(`/api/chat/history/${sessionId.value}`)
    if (data.messages && data.messages.length > 0) {
      messages.value = data.messages
    }
  } catch {
    // history not found, start fresh
  }
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
</style>
