<template>
  <div id="app-root" class="min-h-screen flex flex-col text-on-dark font-sans relative">
    
    <!-- Static Dark Background -->
    <div class="fixed inset-0 pointer-events-none z-[-1] bg-canvas-dark"></div>
    <Navbar />
    <main class="flex-grow flex flex-col relative z-10">
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<script setup>
import Navbar from './components/navbar.vue'
import Footer from './components/footer.vue'
</script>


