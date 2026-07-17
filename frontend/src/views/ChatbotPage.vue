<template>
  <div class="page" style="padding-top: var(--spacing-section);">
    <div class="container" style="max-width: 800px;">
      <h1 class="display-md stagger-1" style="margin-bottom: var(--spacing-xs);">Asisten AI</h1>
      <p class="subtitle stagger-2" style="color: var(--color-mute); margin-bottom: var(--spacing-xl);">Konsultasikan perjalanan karir Anda, struktur dokumen CV, hingga strategi wawancara.</p>

      <div class="card stagger-3" style="padding: 0; overflow: hidden; display: flex; flex-direction: column; height: 600px; border-radius: var(--rounded-marketing);">
        <div class="chat-messages" ref="chatRef">
          <div v-if="loadingHistory" class="mono-micro" style="text-align: center; color: var(--color-mute); padding: var(--spacing-lg);">Memuat riwayat...</div>

          <div v-for="(msg, i) in messages" :key="i" :class="['msg', msg.role]">
            <div class="msg-bubble" :class="{ 'editorial-bubble': msg.role === 'assistant', 'user-bubble': msg.role === 'user' }">
              {{ msg.content }}
            </div>
          </div>

          <div v-if="loading" class="msg assistant">
            <div class="msg-bubble editorial-bubble typing mono-caps" style="color: var(--color-mute);">Menganalisis...</div>
          </div>
        </div>

        <div class="quick-replies-container">
          <div class="quick-replies">
            <button
              v-for="q in quickQuestions"
              :key="q.text"
              class="badge-neutral"
              style="cursor: pointer; border: 1px solid var(--color-hairline); background: var(--color-canvas-light);"
              @click="sendQuick(q.text)"
            >
              {{ q.label }}
            </button>
          </div>
        </div>

        <div class="chat-input" style="background: var(--color-canvas-paper); padding: var(--spacing-sm); border-top: 1px solid var(--color-hairline);">
          <input v-model="input" placeholder="Tanyakan seputar persiapan karir..." @keyup.enter="send" :disabled="loading" style="border: none; box-shadow: none; background: transparent;" />
          <button class="btn btn-primary-on-light" @click="send" :disabled="loading || !input.trim()" style="border-radius: var(--rounded-app-md); height: 40px; padding: 0 var(--spacing-md);">Kirim</button>
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
.chat-messages { flex: 1; overflow-y: auto; padding: var(--spacing-xl); display: flex; flex-direction: column; gap: var(--spacing-lg); background: var(--color-canvas-light); }
.msg { display: flex; }
.msg.user { justify-content: flex-end; }
.msg.assistant { justify-content: flex-start; }
.msg-bubble { max-width: 80%; padding: var(--spacing-sm) var(--spacing-md); border-radius: var(--rounded-app-md); font-size: 15px; line-height: 1.6; white-space: pre-wrap; }
.user-bubble { background: var(--color-ink); color: var(--color-on-primary); border-bottom-right-radius: 4px; }
.editorial-bubble { background: var(--color-canvas-paper); color: var(--color-ink); font-family: inherit; font-size: 16px; border-bottom-left-radius: 4px; }

.quick-replies-container {
  width: 100%;
  overflow-x: auto;
  border-top: 1px solid var(--color-hairline);
  background: var(--color-canvas-light);
  scrollbar-width: none;
  -ms-overflow-style: none;
}
.quick-replies-container::-webkit-scrollbar { display: none; }
.quick-replies { display: flex; flex-wrap: nowrap; gap: var(--spacing-xs); padding: var(--spacing-sm) var(--spacing-lg); width: max-content; }

.typing { animation: pulse 1.5s infinite; }
@keyframes pulse { 0%, 100% { opacity: 0.4; } 50% { opacity: 1; } }
.chat-input { display: flex; gap: var(--spacing-sm); }
.chat-input input:focus { outline: none; }
</style>
