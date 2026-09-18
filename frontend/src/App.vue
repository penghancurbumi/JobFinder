<template>
  <div id="app-root" class="min-h-screen flex flex-col text-on-dark font-sans relative">
    
    <!-- Static Dark Background -->
    <div class="fixed inset-0 pointer-events-none z-[-1] bg-canvas-dark"></div>
    <Navbar />
    <main class="flex-grow flex flex-col relative z-10">
      <router-view />
    </main>
    <Footer v-if="showFooter" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from './components/navbar.vue'
import Footer from './components/footer.vue'

const route = useRoute()
const isChatbot = computed(() => route.name === 'Chatbot')
// Sembunyikan footer di halaman asisten AI (chatbot)
const showFooter = computed(() => !isChatbot.value)
</script>


