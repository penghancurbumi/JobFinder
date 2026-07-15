<template>
  <div class="page">
    <h1 class="page-title stagger-1">Asisten AI</h1>
    <p class="hint stagger-2" style="margin-bottom: 32px; font-size: 14px;">Konsultasikan perjalanan karir Anda, struktur dokumen CV, hingga strategi wawancara.</p>

    <div class="chat-container card stagger-3" style="padding: 0; overflow: hidden;">
      <div class="chat-messages" ref="chatRef">
        <div v-if="loadingHistory" class="loading-msg mono">Memuat riwayat...</div>

        <div v-for="(msg, i) in messages" :key="i" :class="['msg', msg.role]">
          <div class="msg-bubble" :class="{ 'editorial-serif': msg.role === 'assistant' }">
            {{ msg.content }}
          </div>
        </div>

        <div v-if="loading" class="msg assistant">
          <div class="msg-bubble typing mono" style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em;">Menganalisis...</div>
        </div>
      </div>

      <div class="quick-replies-container">
        <div class="quick-replies">
          <button
            v-for="q in quickQuestions"
            :key="q.text"
            class="quick-btn"
            @click="sendQuick(q.text)"
          >
            {{ q.label }}
          </button>
        </div>
      </div>

      <div class="chat-input">
        <input v-model="input" placeholder="Tanyakan seputar persiapan karir..." @keyup.enter="send" :disabled="loading" style="border: none; box-shadow: none;" />
        <button class="btn btn-primary btn-sm" @click="send" :disabled="loading || !input.trim()" style="border-radius: 4px;">Kirim</button>
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
  { label: "Cari lowongan Software Dev", text: "Saya ingin cari lowongan software development" },
  { label: "Cari magang UI/UX Design", text: "Saya ingin cari magang di bidang UI/UX design" },
  { label: "Lowongan Graphic Design", text: "Ada lowongan graphic design tidak?" },
  { label: "Tips membuat CV ATS", text: "Bagaimana cara membuat CV yang ramah ATS?" },
  { label: "Persiapan wawancara", text: "Berikan tips persiapan wawancara kerja" },
  { label: "Info seputar karir IT", text: "Ceritakan tentang prospek karir di bidang IT" },
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
.chat-container { display: flex; flex-direction: column; height: 600px; }
.chat-messages { flex: 1; overflow-y: auto; padding: 24px; display: flex; flex-direction: column; gap: 24px; }
.loading-msg { text-align: center; padding: 20px; color: var(--text-muted); font-size: 12px; }
.msg { display: flex; }
.msg.user { justify-content: flex-end; }
.msg.assistant { justify-content: flex-start; }
.msg-bubble { max-width: 80%; padding: 16px 24px; border-radius: 4px; font-size: 14px; line-height: 1.6; white-space: pre-wrap; }
.user .msg-bubble { background: var(--text-primary); color: #fff; }
.assistant .msg-bubble { background: var(--bg-canvas); color: var(--text-primary); border: 1px solid var(--border-color); font-size: 1.05rem; }

.quick-replies-container {
  width: 100%;
  overflow-x: auto;
  border-top: 1px solid var(--border-color);
  background: var(--bg-surface);
  scrollbar-width: none;
  -ms-overflow-style: none;
}
.quick-replies-container::-webkit-scrollbar { display: none; }
.quick-replies { display: flex; flex-wrap: nowrap; gap: 8px; padding: 12px 16px; width: max-content; }
.quick-btn {
  padding: 8px 16px; background: var(--bg-canvas); border: 1px solid var(--border-color); border-radius: 9999px; font-size: 12px; cursor: pointer; transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1); color: var(--text-primary);
  white-space: nowrap;
}
.quick-btn:hover { background: var(--border-color); transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
.quick-btn:active { transform: translateY(0); }

.typing { animation: pulse 1.5s infinite; }
@keyframes pulse { 0%, 100% { opacity: 0.4; } 50% { opacity: 1; } }
.chat-input { display: flex; gap: 12px; padding: 16px; border-top: 1px solid var(--border-color); background: var(--bg-surface); }
.chat-input input { flex: 1; background: transparent; padding: 8px; }
</style>
