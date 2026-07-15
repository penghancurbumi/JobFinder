<template>
  <div id="app-root">
    <nav class="navbar">
      <div class="container nav-inner">
        <router-link to="/" class="logo editorial-serif">JobFinder</router-link>
        <div class="nav-links">
          <router-link to="/jobs" class="nav-link">Peluang</router-link>
          <router-link to="/cv-analyzer" class="nav-link">Analisis CV</router-link>
          <router-link to="/cv-builder" class="nav-link">Pembuat CV</router-link>
          <router-link to="/chatbot" class="nav-link">Asisten AI</router-link>
        </div>
      </div>
    </nav>
    <main class="container">
      <router-view />
    </main>
  </div>
</template>

<script setup>
</script>

<style scoped>
.navbar { background: var(--bg-surface); border-bottom: 1px solid var(--border-color); padding: 20px 0; }
.nav-inner { display: flex; align-items: center; justify-content: space-between; }
.logo { font-size: 1.5rem; font-weight: 500; color: var(--text-primary); text-decoration: none; letter-spacing: -0.02em; }
.nav-links { display: flex; gap: 16px; }
.nav-link { padding: 6px 12px; text-decoration: none; color: var(--text-muted); font-size: 14px; font-weight: 500; transition: color 0.2s; text-transform: uppercase; letter-spacing: 0.05em; font-size: 11px; }
.nav-link:hover { color: var(--text-primary); }
.nav-link.router-link-active { color: var(--text-primary); border-bottom: 1px solid var(--text-primary); padding-bottom: 4px; }
@media (max-width: 640px) {
  .nav-inner { flex-direction: column; gap: 16px; }
  .nav-links { flex-wrap: wrap; justify-content: center; }
}

@media print {
  nav { display: none !important; }
}
</style>
