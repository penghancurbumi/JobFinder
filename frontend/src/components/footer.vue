<template>
  <footer class="bg-canvas-dark mt-block pt-xxl pb-lg">
      <div class="w-full mx-auto px-[32px] md:px-[72px]">
        <div class="grid grid-cols-1 md:grid-cols-[1.5fr_1fr_1fr_1fr] gap-xxl md:gap-xl mb-block">
          <div class="flex flex-col gap-sm">
          <div class="flex items-center gap-xs mb-sm">
              <span class="text-[20px] font-medium leading-[1.4] text-on-dark">JobFinder</span>
          </div>
          <p class="text-[14px] font-normal leading-[1.5] text-on-dark-mute max-w-[280px]">Platform agregasi lowongan kerja dan alat karier untuk pencari kerja di Indonesia.</p>
          </div>

          <div class="flex flex-col gap-sm">
            <span class="font-mono text-[12px] uppercase tracking-[1px] font-bold text-stone mb-xs">Fitur</span>
            <router-link to="/" class="text-on-dark-mute hover:text-on-dark text-[14px] transition-colors no-underline">Home</router-link>
            <router-link to="/jobs" class="text-on-dark-mute hover:text-on-dark text-[14px] transition-colors no-underline">Cari Lowongan</router-link>
            <router-link to="/cv-analyzer" class="text-on-dark-mute hover:text-on-dark text-[14px] transition-colors no-underline">Analisis CV</router-link>
            <router-link to="/cv-builder" class="text-on-dark-mute hover:text-on-dark text-[14px] transition-colors no-underline">Buat CV</router-link>
            <router-link to="/chatbot" class="text-on-dark-mute hover:text-on-dark text-[14px] transition-colors no-underline">AI Chatbot</router-link>
          </div>

          <div class="flex flex-col gap-sm">
            <span class="font-mono text-[12px] uppercase tracking-[1px] font-bold text-stone mb-xs cursor-pointer">Sumber</span>
            <span class="text-on-dark-mute hover:text-on-dark text-[14px] transition-colors cursor-pointer">LinkedIn</span>
            <span class="text-on-dark-mute hover:text-on-dark text-[14px] transition-colors cursor-pointer">Glints</span>
            <span class="text-on-dark-mute hover:text-on-dark text-[14px] transition-colors cursor-pointer">Jobstreet</span>
            <span class="text-on-dark-mute hover:text-on-dark text-[14px] transition-colors cursor-pointer">Fastwork</span>
            <span class="text-on-dark-mute hover:text-on-dark text-[14px] transition-colors cursor-pointer">Pintarnya</span>
            <span class="text-on-dark-mute hover:text-on-dark text-[14px] transition-colors cursor-pointer">LinkedIn</span>
            <span class="text-on-dark-mute hover:text-on-dark text-[14px] transition-colors cursor-pointer">KitaLulus</span>
          </div>
          <div class="flex flex-col gap-sm">
          <span class="font-mono text-[12px] uppercase tracking-[1px] font-bold text-stone mb-xs">Hubungi</span>

          <div class="flex flex-row gap-sm">
              <a href="https://github.com/penghancurbumi" aria-label="GitHub penghancurbumi" class="text-on-dark-mute hover:text-on-dark text-[14px] transition-colors no-underline">
              <Icon icon="mdi:github" width="24" height="24" aria-hidden="true" />
              </a>

              <a href="https://www.linkedin.com/in/muhammad-al-fakhreza-dwi-putra-b16962301/" aria-label="LinkedIn Muhammad Al Fakhreza" class="text-on-dark-mute hover:text-on-dark text-[14px] transition-colors no-underline">
              <Icon icon="mdi:linkedin" width="24" height="24" aria-hidden="true" />
              </a>
          </div>
          </div>
      </div>

      <div class="flex justify-between items-center pt-lg border-t border-hairline-dark">
          <span class="text-[13px] font-normal leading-[1.5] text-on-dark-mute">&copy; {{ new Date().getFullYear() }} JobFinder. All rights reserved.</span>
          <span class="text-[13px] font-normal leading-[1.5] text-stone">Built with editorial precision</span>
      </div>
      </div>
  </footer>
</template>

<script setup>
import { Icon } from '@iconify/vue'
</script>