<template>
  <button
    class="org-button"
    :class="buttonClass"
    :disabled="disabled"
    @click="$emit('click', $event)"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  disabled: false
})

defineEmits(['click'])

const buttonClass = computed(() => {
  return [
    `btn-${props.variant}`,
    `btn-${props.size}`
  ]
})
</script>

<style scoped>
.org-button {
  border: none;
  padding: 10px 28px;
  font-weight: 600;
  font-size: var(--text-sm);
  font-family: var(--font-body);
  cursor: pointer;
  transition: all var(--duration-hover) var(--easing-organic);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.org-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

/* Primary button */
.btn-primary {
  background: var(--gradient-primary);
  border-radius: var(--radius-pill);
  color: white;
  box-shadow: 0 4px 16px rgba(155, 127, 232, 0.35);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px) scale(1.03);
  box-shadow: var(--shadow-md);
}

.btn-primary:active:not(:disabled) {
  transform: translateY(0) scale(0.98);
}

/* Secondary button */
.btn-secondary {
  background: transparent;
  border: 1.5px solid var(--color-primary-light);
  border-radius: 28px 18px 24px 14px;
  color: var(--color-primary);
}

.btn-secondary:hover:not(:disabled) {
  background: rgba(155, 127, 232, 0.1);
  transform: translateY(-2px);
}

.btn-secondary:active:not(:disabled) {
  transform: translateY(0);
}

/* Danger button */
.btn-danger {
  background: linear-gradient(135deg, #e8968c, #e8a4b8);
  border-radius: var(--radius-pill);
  color: white;
  box-shadow: 0 4px 16px rgba(232, 150, 140, 0.35);
}

.btn-danger:hover:not(:disabled) {
  transform: translateY(-2px) scale(1.03);
  box-shadow: 0 6px 20px rgba(232, 150, 140, 0.4);
}

.btn-danger:active:not(:disabled) {
  transform: translateY(0) scale(0.98);
}

/* Size variants */
.btn-sm {
  padding: 6px 16px;
  font-size: 12px;
}

.btn-md {
  padding: 10px 28px;
  font-size: var(--text-sm);
}

.btn-lg {
  padding: 14px 36px;
  font-size: var(--text-base);
}
</style>
