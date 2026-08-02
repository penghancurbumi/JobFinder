<template>
    
    <nav 
      :class="[
        'h-[72px] px-[32px] md:px-[72px] flex items-center sticky top-0 z-50 transition-all duration-300 border-b',
        (isScrolled || !isHome) ? 'bg-canvas-dark' : 'bg-transparent',
        isScrolled ? 'border-hairline-dark' : 'border-transparent'
      ]"
    >
      <div class="w-full mx-auto flex items-center justify-between">
        <router-link to="/" class="text-[20px] font-medium text-on-dark no-underline tracking-[-0.02em] flex items-center gap-[8px]">
          JobFinder
        </router-link>
        <div class="hidden lg:flex gap-lg">
          <router-link to="/" class="nav-link" active-class="nav-link-active">Home</router-link>
          <router-link to="/jobs" class="nav-link" active-class="nav-link-active">Peluang</router-link>
          <router-link to="/cv-analyzer" class="nav-link" active-class="nav-link-active">Analisis CV</router-link>
          <router-link to="/cv-builder" class="nav-link" active-class="nav-link-active">Pembuat CV</router-link>
          <router-link to="/chatbot" class="nav-link" active-class="nav-link-active">Asisten AI</router-link>
        </div>
      </div>
    </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const isScrolled = ref(false)
const isHome = computed(() => route.path === '/')

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

.nav-link {
  @apply relative text-on-dark-mute text-[16px] font-medium leading-[1.5] tracking-[0.24px] px-1 py-1 no-underline transition-colors duration-200 hover:text-white;
}

.nav-link::after {
  content: '';
  @apply absolute left-0 -bottom-[6px] w-full h-[2px] bg-white transition-transform duration-300 origin-left scale-x-0 rounded-full;
}

.nav-link-active::after {
  @apply scale-x-100;
}

.nav-link-active {
  @apply text-white;
}
</style>