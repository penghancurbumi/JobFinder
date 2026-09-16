import { ref, watch, computed, onUnmounted, unref, isRef } from 'vue'

/**
 * Animasi count-up 0 → target dengan easing easeOutCubic.
 * Mengembalikan nilai mentah (`value`) dan persentase 0-100 (`percent`)
 * sehingga ANGKA dan PROGRESS BAR bisa bergerak dari sumber animasi yang sama.
 *
 * @param {number|import('vue').Ref<number>|Function} source - Nilai target.
 * @param {Object} [options]
 * @param {number} [options.duration=1000] - Durasi animasi (ms).
 * @param {number} [options.decimals=0]    - Angka di belakang koma.
 * @param {number} [options.delay=0]       - Jeda sebelum mulai (ms).
 * @param {number} [options.max=100]       - Nilai maksimum untuk hitung `percent`.
 * @returns {{ value, percent, display }}
 */
export function useCountUp(source, options = {}) {
  const { duration = 1000, decimals = 0, delay = 0, max = 100 } = options

  const value = ref(0)
  let rafId = null
  let startTimer = null

  function readTarget() {
    const raw = typeof source === 'function' ? source() : unref(source)
    const n = Number(raw)
    return Number.isFinite(n) ? n : 0
  }

  function stop() {
    if (rafId) cancelAnimationFrame(rafId)
    if (startTimer) clearTimeout(startTimer)
    rafId = null
    startTimer = null
  }

  function run() {
    stop()
    const to = readTarget()

    if (duration <= 0) {
      value.value = to
      return
    }

    const startAt = performance.now()
    const step = (now) => {
      const progress = Math.min((now - startAt) / duration, 1)
      const eased = 1 - Math.pow(1 - progress, 3) // easeOutCubic
      value.value = to * eased

      if (progress < 1) {
        rafId = requestAnimationFrame(step)
      } else {
        value.value = to
        rafId = null
      }
    }

    startTimer = setTimeout(() => {
      rafId = requestAnimationFrame(step)
    }, delay)
  }

  // Sumber reaktif → animasi ulang saat target berubah.
  if (isRef(source) || typeof source === 'function') {
    watch(source, run)
  }

  startTimer = setTimeout(run, 0)
  onUnmounted(stop)

  const display = computed(() => value.value.toFixed(decimals))
  // Persentase 0-100 dari nilai sekarang (untuk lebar progress bar)
  const percent = computed(() => {
    const m = max > 0 ? max : 100
    return Math.max(0, Math.min(100, (value.value / m) * 100))
  })

  return { value, percent, display }
}
