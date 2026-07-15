<template>
  <div class="page">
    <h1 class="page-title stagger-1">Asisten AI</h1>
    <p class="hint stagger-2" style="margin-bottom: 32px; font-size: 14px;">Konsultasikan perjalanan karir Anda, struktur dokumen CV, hingga strategi wawancara.</p>

    <div class="chat-container card stagger-3" style="padding: 0; overflow: hidden;">
      <div class="chat-messages" ref="chatRef">
        <div v-for="(msg, i) in messages" :key="i" :class="['msg', msg.role]">
          <div class="msg-bubble" :class="{ 'editorial-serif': msg.role === 'assistant' }">
            {{ msg.content }}
          </div>
        </div>
        <div v-if="loading" class="msg assistant">
          <div class="msg-bubble typing mono" style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em;">Menganalisis...</div>
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

const messages = ref([
  { role: "assistant", content: "Halo! Saya adalah arsitek karir Anda. Apa yang bisa saya bantu terkait dokumentasi profesional atau pencarian kerja Anda hari ini?" }
])
const input = ref("")
const loading = ref(false)
const chatRef = ref(null)

async function send() {
  if (!input.value.trim() || loading.value) return
  const userMsg = input.value
  messages.value.push({ role: "user", content: userMsg })
  input.value = ""
  loading.value = true
  scrollDown()

  try {
    const { data } = await axios.post("/api/chat", {
      message: userMsg,
      history: messages.value.map(m => ({ role: m.role, content: m.content })),
    })
    messages.value.push({ role: "assistant", content: data.reply })
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
.msg { display: flex; }
.msg.user { justify-content: flex-end; }
.msg.assistant { justify-content: flex-start; }
.msg-bubble { max-width: 80%; padding: 16px 24px; border-radius: 4px; font-size: 14px; line-height: 1.6; white-space: pre-wrap; }
.user .msg-bubble { background: var(--text-primary); color: #fff; }
.assistant .msg-bubble { background: var(--bg-canvas); color: var(--text-primary); border: 1px solid var(--border-color); font-size: 1.05rem; }
.typing { animation: pulse 1.5s infinite; }
@keyframes pulse { 0%, 100% { opacity: 0.4; } 50% { opacity: 1; } }
.chat-input { display: flex; gap: 12px; padding: 16px; border-top: 1px solid var(--border-color); background: var(--bg-surface); }
.chat-input input { flex: 1; background: transparent; padding: 8px; }
</style>
