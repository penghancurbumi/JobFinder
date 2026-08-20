<template>
    
    <nav 
      :class="[
        'py-[18px] md:py-[20px] px-[32px] md:px-[72px] flex items-center sticky top-0 z-50 transition-all duration-300 border-b',
        (isScrolled || !isHome || isOpen) ? 'bg-canvas-dark' : 'bg-transparent',
        isScrolled ? 'border-hairline-dark' : 'border-transparent'
      ]"
    >
      <div class="w-full mx-auto flex items-center justify-between">
        <router-link to="/" class="text-[25px] md:text-[30px] font-medium text-on-dark no-underline tracking-[-0.02em] leading-none flex items-center gap-[8px]">
          JobFinder
        </router-link>

        <!-- Desktop Nav -->
        <div class="hidden lg:flex gap-lg">
          <router-link to="/" class="nav-link" active-class="nav-link-active">Home</router-link>
          <router-link to="/jobs" class="nav-link" active-class="nav-link-active">Peluang</router-link>
          <router-link to="/cv-analyzer" class="nav-link" active-class="nav-link-active">Analisis CV</router-link>
          <router-link to="/cv-builder" class="nav-link" active-class="nav-link-active">Pembuat CV</router-link>
          <router-link to="/chatbot" class="nav-link" active-class="nav-link-active">Asisten AI</router-link>
        </div>

        <!-- Hamburger Button (mobile only) -->
        <button
          class="lg:hidden flex justify-center items-center w-[40px] h-[40px] cursor-pointer bg-transparent border-none p-0 text-white transition-all duration-300"
          @click="toggleMenu"
          aria-label="Toggle navigation menu"
        >
          <Transition name="icon-swap" mode="out-in">
            <Icon v-if="!isOpen" key="menu" icon="griddy-icons:menu-alt-03" width="30" style="display:block" />
            <Icon v-else key="close" icon="griddy-icons:minus" width="30" style="display:block" />
          </Transition>
        </button>
      </div>
    </nav>

    <!-- Mobile Menu Full Screen -->
    <Transition name="mobile-menu">
      <div
        v-if="isOpen"
        class="lg:hidden fixed top-[72px] left-0 right-0 bottom-0 z-40 bg-canvas-dark flex flex-col"
      >
        <div class="flex flex-col px-[32px] py-[80px] gap-xs">
          <router-link to="/" class="text-[40px] sm:text-[50px] font-light" @click="closeMenu">Home</router-link>
          <router-link to="/jobs" class="text-[40px] sm:text-[50px] font-light" @click="closeMenu">Peluang</router-link>
          <router-link to="/cv-analyzer" class="text-[40px] sm:text-[50px] font-light" @click="closeMenu">Analisis CV</router-link>
          <router-link to="/cv-builder" class="text-[40px] sm:text-[50px] font-light" @click="closeMenu">Pembuat CV</router-link>
          <router-link to="/chatbot" class="text-[40px] sm:text-[50px] font-light" @click="closeMenu">Asisten AI</router-link>
        </div>

        <!-- Footer -->
        <div class="absolute flex justify-between items-center bottom-0 left-0 right-0 px-[32px] py-[30px]">
          <p class="text-[14px] font-normal leading-[1.6] text-on-dark-mute">JobFinder &copy; 2026</p>
          
          <div class="flex flex-row gap-sm">
            <Icon icon="mdi:github" width="30"/>
            <Icon icon="mdi:linkedin" width="30"/>
          </div>
        </div>
      </div>
    </Transition>

</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import { Icon } from '@iconify/vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const isScrolled = ref(false)
const isHome = computed(() => route.path === '/')
const isOpen = ref(false)

const toggleMenu = () => { isOpen.value = !isOpen.value }
const closeMenu = () => { isOpen.value = false }

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20
}

// Lock/unlock body scroll saat menu buka/tutup
watch(isOpen, (val) => {
  document.body.style.overflow = val ? 'hidden' : ''
})

// Close menu on route change
watch(() => route.path, () => closeMenu())

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  document.body.style.overflow = '' // cleanup
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

/* Icon swap transition */
.icon-swap-enter-active,
.icon-swap-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}
.icon-swap-enter-from {
  opacity: 0;
  transform: rotate(-90deg) scale(0.7);
}
.icon-swap-leave-to {
  opacity: 0;
  transform: rotate(90deg) scale(0.7);
}

/* Mobile menu transition */
.mobile-menu-enter-active {
  transition: opacity 0.35s ease, transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}
.mobile-menu-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}
.mobile-menu-enter-from,
.mobile-menu-leave-to {
  opacity: 0;
  transform: translateY(-12px);
}

/* Stagger animasi tiap link saat masuk */
.mobile-menu-enter-active a:nth-child(1) { transition-delay: 0.05s; }
.mobile-menu-enter-active a:nth-child(2) { transition-delay: 0.10s; }
.mobile-menu-enter-active a:nth-child(3) { transition-delay: 0.15s; }
.mobile-menu-enter-active a:nth-child(4) { transition-delay: 0.20s; }
.mobile-menu-enter-active a:nth-child(5) { transition-delay: 0.25s; }

</style>