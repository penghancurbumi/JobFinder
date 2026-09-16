<script setup>
import { computed } from 'vue'
import { useCountUp } from '../composables/useCountUp'

const props = defineProps({
  // Nilai target (0-100).
  to: { type: [Number, String], default: 0 },
  // Durasi animasi (ms).
  duration: { type: Number, default: 1000 },
  // Jeda sebelum animasi mulai (ms).
  delay: { type: Number, default: 0 },
  // Warna isian bar.
  barClass: { type: String, default: 'bg-[#dcdcdf]' },
  // Warna track (latar belakang).
  trackClass: { type: String, default: 'bg-[#3b3b40]' },
  // Tinggi bar.
  heightClass: { type: String, default: 'h-[5px]' },
})

const target = computed(() => {
  const n = Number(props.to)
  return Number.isFinite(n) ? n : 0
})

// Sumber animasi yang sama dengan yang dipakai angka → bar & angka bergerak bareng.
const { percent } = useCountUp(target, {
  duration: props.duration,
  delay: props.delay,
  max: 100,
})
</script>

<template>
  <div class="w-full overflow-hidden rounded-full" :class="[heightClass, trackClass]">
    <div
      class="h-full rounded-full"
      :class="barClass"
      :style="{ width: `${percent}%` }"
    ></div>
  </div>
</template>
