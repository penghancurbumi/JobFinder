<template>
  <div id="app-root" class="theme-dark">
    <nav class="nav-bar-dark">
      <div class="container nav-inner">
        <router-link to="/" class="logo">
          <span class="brand-dot"></span>
          JobFinder
        </router-link>
        <div class="nav-links">
          <router-link to="/" class="nav-link">Home</router-link>
          <router-link to="/jobs" class="nav-link">Peluang</router-link>
          <router-link to="/cv-analyzer" class="nav-link">Analisis CV</router-link>
          <router-link to="/cv-builder" class="nav-link">Pembuat CV</router-link>
          <router-link to="/chatbot" class="nav-link">Asisten AI</router-link>
        </div>
        <div class="nav-actions">
          <a href="#" class="btn btn-secondary-dark">Masuk</a>
          <router-link to="/cv-builder" class="btn btn-primary">Mulai Gratis</router-link>
        </div>
      </div>
    </nav>
    <!-- Render main pages using the standard container; we remove 'container' from main here because some pages like LandingPage will have full-width bands. The pages themselves should use the .container class internally. -->
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
</script>

<style scoped>
/* App Root is scoped with dark theme */
#app-root {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.nav-bar-dark { 
  background: var(--color-canvas); 
  height: 64px;
  padding: 0 var(--spacing-lg);
  display: flex;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 1px solid var(--color-hairline-soft);
}

.nav-inner { 
  display: flex; 
  align-items: center; 
  justify-content: space-between; 
  width: 100%;
}

.logo { 
  font-size: 24px; 
  font-weight: 500; 
  color: var(--color-on-primary); 
  text-decoration: none; 
  letter-spacing: -0.02em; 
  display: flex;
  align-items: center;
}

.brand-dot {
  margin-right: 8px;
}

.nav-links { 
  display: flex; 
  gap: var(--spacing-sm); 
}

.nav-link { 
  background: var(--color-canvas);
  color: var(--color-on-primary);
  font-size: 16px; 
  font-weight: 500; 
  line-height: 1.5;
  padding: var(--spacing-xs); 
  text-decoration: none; 
  transition: opacity 0.2s; 
}
.nav-link:hover { opacity: 0.8; }
.nav-link.router-link-active { 
  border-bottom: 2px solid var(--color-brand); 
  padding-bottom: 6px; 
}

.nav-actions {
  display: flex;
  gap: var(--spacing-md);
  align-items: center;
}

@media (max-width: 960px) {
  .nav-links { display: none; }
  .nav-actions { display: none; }
}

@media print {
  nav { display: none !important; }
}
</style>
