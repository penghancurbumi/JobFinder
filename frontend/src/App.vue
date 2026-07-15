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

    <!-- Telegram Floating Button -->
    <a href="https://t.me/placeholder_bot" target="_blank" class="telegram-fab" title="Chat via Telegram">
      <svg viewBox="0 0 24 24" fill="currentColor" width="24" height="24">
        <path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a5.8 5.8 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.892-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/>
      </svg>
    </a>
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

.telegram-fab {
  position: fixed;
  bottom: 32px;
  right: 32px;
  width: 56px;
  height: 56px;
  background-color: #2481cc;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(36, 129, 204, 0.3);
  transition: transform 0.2s, box-shadow 0.2s;
  z-index: 1000;
}
.telegram-fab:hover {
  transform: scale(1.05) translateY(-4px);
  box-shadow: 0 6px 16px rgba(36, 129, 204, 0.4);
}
@media print {
  .telegram-fab { display: none !important; }
}
</style>
