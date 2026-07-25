<template>
  <div id="app-root" class="min-h-screen flex flex-col text-on-dark font-sans relative">
    
    <!-- Animated Sliding Background -->
    <div class="fixed inset-0 pointer-events-none z-[-1] overflow-hidden bg-canvas-dark">
      <div v-for="i in 25" :key="i" class="rainbow"></div>
    </div>

    <nav 
      :class="[
        'h-[72px] px-xl flex items-center sticky top-0 z-50 transition-all duration-300 border-b',
        (isScrolled || !isHome) ? 'bg-canvas-dark border-hairline-dark' : 'bg-transparent border-transparent'
      ]"
    >
      <div class="w-full max-w-[1200px] mx-auto px-xl flex items-center justify-between">
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
    <main class="flex-grow flex flex-col relative z-10">
      <router-view />
    </main>
  </div>
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

<style lang="scss" scoped>
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

$black: #000000;
$gray: #080808;
$white: #121212;

$animationtime: 45s;
$length: 25;

.rainbow {
  height: 100vh;
  width: 0;
  top: 0;
  position: absolute;
  transform: rotate(10deg);
  transform-origin: top right;
  
  @for $i from 1 through $length {
    &:nth-child(#{$i}) {
      $colors: 0;
      $r: random(6);
      @if $r == 1 { $colors: $black, $gray, $white; }
      @else if $r == 2 { $colors: $black, $white, $gray; }
      @else if $r == 3 { $colors: $white, $black, $gray; }
      @else if $r == 4 { $colors: $white, $gray, $black; }
      @else if $r == 5 { $colors: $gray, $white, $black; }
      @else if $r == 6 { $colors: $gray, $black, $white; }
      
      box-shadow: -130px 0 80px 40px #000000, -50px 0 50px 25px nth($colors, 1),
        0 0 50px 25px nth($colors, 2), 50px 0 50px 25px nth($colors, 3),
        130px 0 80px 40px #000000;

      animation: #{$animationtime - $animationtime / $length / 2 * $i} linear infinite slide;
      animation-delay: -#{$i / $length * $animationtime};
    }
  }
}

@keyframes slide {
  from { right: -25vw; }
  to { right: 125vw; }
}
</style>
