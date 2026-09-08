<template>
  <div class="relative" ref="selectContainer">
    <!-- Select Trigger -->
    <button 
      type="button"
      @click="toggleDropdown"
      class="w-full bg-transparent border border-hairline-dark rounded-sm h-[40px] px-[12px] text-on-dark focus:border-white focus:outline-none flex items-center justify-between text-xs md:text-sm cursor-pointer transition-colors"
      :class="{ 'border-white': isOpen }"
    >
      <span class="truncate">{{ selectedLabel }}</span>
      <svg 
        xmlns="http://www.w3.org/2000/svg" 
        class="h-4 w-4 text-stone transition-transform duration-200"
        :class="{ 'rotate-180': isOpen }"
        fill="none" 
        viewBox="0 0 24 24" 
        stroke="currentColor"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>

    <!-- Dropdown Menu -->
    <transition
      enter-active-class="transition ease-out duration-100"
      enter-from-class="transform opacity-0 scale-95"
      enter-to-class="transform opacity-100 scale-100"
      leave-active-class="transition ease-in duration-75"
      leave-from-class="transform opacity-100 scale-100"
      leave-to-class="transform opacity-0 scale-95"
    >
      <div 
        v-if="isOpen" 
        class="absolute z-[100] w-full rounded-[12px] bg-surface-elevated border border-hairline-dark shadow-xl overflow-hidden"
        :class="openUpward ? 'bottom-[calc(100%+8px)]' : 'top-[calc(100%+8px)]'"
      >
        <ul class="max-h-60 overflow-auto py-1 custom-scrollbar">
          <li 
            v-for="option in options" 
            :key="option.value"
            @click="selectOption(option)"
            class="px-[12px] py-[8px] text-xs md:text-sm cursor-pointer transition-colors flex items-center justify-between hover:bg-white/5"
            :class="{
              'text-white bg-white/10': modelValue === option.value,
              'text-on-dark': modelValue !== option.value
            }"
          >
            {{ option.label }}
            <svg v-if="modelValue === option.value" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </li>
        </ul>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    required: true
  },
  options: {
    type: Array,
    required: true,
    // Array of objects: { label: '...', value: '...' }
  },
  placeholder: {
    type: String,
    default: 'Select an option'
  }
})

const emit = defineEmits(['update:modelValue'])

const isOpen = ref(false)
const openUpward = ref(false)
const selectContainer = ref(null)

const selectedLabel = computed(() => {
  const selected = props.options.find(opt => opt.value === props.modelValue)
  return selected ? selected.label : props.placeholder
})

const DROPDOWN_HEIGHT = 256 // max-h-60 = 15rem ≈ 240px + padding buffer

const toggleDropdown = () => {
  if (!isOpen.value && selectContainer.value) {
    const rect = selectContainer.value.getBoundingClientRect()
    const spaceBelow = window.innerHeight - rect.bottom
    openUpward.value = spaceBelow < DROPDOWN_HEIGHT && rect.top > DROPDOWN_HEIGHT
  }
  isOpen.value = !isOpen.value
}

const selectOption = (option) => {
  emit('update:modelValue', option.value)
  isOpen.value = false
}

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
  if (selectContainer.value && !selectContainer.value.contains(event.target)) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.2);
}
</style>
