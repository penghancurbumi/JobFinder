<script setup>
import { computed } from 'vue'
import { useCountUp } from '../composables/useCountUp'

const props = defineProps({
  // Nilai target. Number atau string numerik.
  to: { type: [Number, String], default: 0 },
  // Durasi animasi (ms).
  duration: { type: Number, default: 1000 },
  // Jumlah angka di belakang koma.
  decimals: { type: Number, default: 0 },
  // Jeda sebelum animasi mulai (ms).
  delay: { type: Number, default: 0 },
  // Teks yang ditempel di belakang angka (mis. "%", "/100").
  suffix: { type: String, default: '' },
})

const target = computed(() => {
  const n = Number(props.to)
  return Number.isFinite(n) ? n : 0
})

const { display } = useCountUp(target, {
  duration: props.duration,
  decimals: props.decimals,
  delay: props.delay,
})
</script>

<template><span>{{ display }}{{ suffix }}</span></template>
