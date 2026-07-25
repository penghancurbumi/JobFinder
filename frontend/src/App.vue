<template>
  <div id="app-root" class="min-h-screen flex flex-col bg-canvas-dark text-on-dark font-sans">
    <nav 
      :class="[
        'h-[72px] px-xl flex items-center sticky top-0 z-50 transition-all duration-300 border-b',
        isScrolled ? 'bg-canvas-dark border-hairline-dark' : 'bg-transparent border-transparent'
      ]"
    >
      <div class="w-full max-w-[1200px] mx-auto px-xl flex items-center justify-between">
        <router-link to="/" class="text-[20px] font-medium text-on-dark no-underline tracking-[-0.02em] flex items-center gap-[8px]">
          <span class="w-3 h-3 rounded-full bg-primary inline-block"></span>
          JobFinder
        </router-link>
        <div class="hidden lg:flex gap-sm">
          <router-link to="/" class="bg-transparent text-on-dark-mute text-[16px] font-medium leading-[1.5] tracking-[0.24px] px-[12px] py-[8px] no-underline transition-colors duration-200 rounded-full hover:text-on-dark hover:bg-surface-deep" active-class="text-on-dark bg-surface-elevated">Home</router-link>
          <router-link to="/jobs" class="bg-transparent text-on-dark-mute text-[16px] font-medium leading-[1.5] tracking-[0.24px] px-[12px] py-[8px] no-underline transition-colors duration-200 rounded-full hover:text-on-dark hover:bg-surface-deep" active-class="text-on-dark bg-surface-elevated">Peluang</router-link>
          <router-link to="/cv-analyzer" class="bg-transparent text-on-dark-mute text-[16px] font-medium leading-[1.5] tracking-[0.24px] px-[12px] py-[8px] no-underline transition-colors duration-200 rounded-full hover:text-on-dark hover:bg-surface-deep" active-class="text-on-dark bg-surface-elevated">Analisis CV</router-link>
          <router-link to="/cv-builder" class="bg-transparent text-on-dark-mute text-[16px] font-medium leading-[1.5] tracking-[0.24px] px-[12px] py-[8px] no-underline transition-colors duration-200 rounded-full hover:text-on-dark hover:bg-surface-deep" active-class="text-on-dark bg-surface-elevated">Pembuat CV</router-link>
          <router-link to="/chatbot" class="bg-transparent text-on-dark-mute text-[16px] font-medium leading-[1.5] tracking-[0.24px] px-[12px] py-[8px] no-underline transition-colors duration-200 rounded-full hover:text-on-dark hover:bg-surface-deep" active-class="text-on-dark bg-surface-elevated">Asisten AI</router-link>
        </div>
        <div class="hidden lg:flex gap-md items-center">
          <a href="#" class="px-5 py-2 text-[14px] font-semibold text-on-dark bg-surface-elevated hover:bg-surface-deep rounded-full transition-colors border border-hairline-dark">Masuk</a>
          <router-link to="/cv-builder" class="h-[40px] px-[20px] py-[8px] text-[14px] font-semibold bg-on-dark text-ink rounded-full hover:bg-white/90 transition-colors flex items-center justify-center">Mulai Gratis</router-link>
        </div>
      </div>
    </nav>
    <main class="flex-grow flex flex-col">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const isScrolled = ref(false)

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
@media print {
  nav { display: none !important; }
}
</style>
