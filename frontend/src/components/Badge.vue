<template>
  <span class="badge" :class="badgeClass">
    <slot />
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  type?: 'success' | 'warning' | 'error' | 'info' | 'default'
}

const props = withDefaults(defineProps<Props>(), {
  type: 'default'
})

const badgeClass = computed(() => {
  if (props.type === 'default') return ''
  return `badge-${props.type}`
})
</script>

<style scoped>
.badge {
  display: inline-flex;
  align-items: center;
  padding: 3px 12px;
  font-size: var(--text-xs);
  font-weight: 600;
  border-radius: 50px 28px 44px 24px;
  background: color-mix(in srgb, var(--color-primary) 15%, transparent);
  color: var(--color-primary-dark);
}

.badge-success {
  background: color-mix(in srgb, var(--color-success) 15%, transparent);
  color: var(--color-success);
  filter: brightness(0.8);
}

.badge-warning {
  background: color-mix(in srgb, var(--color-warning) 20%, transparent);
  color: var(--color-warning);
  filter: brightness(0.75);
}

.badge-error {
  background: color-mix(in srgb, var(--color-error) 15%, transparent);
  color: var(--color-error);
  filter: brightness(0.85);
}

.badge-info {
  background: color-mix(in srgb, var(--color-info) 15%, transparent);
  color: var(--color-info);
  filter: brightness(0.75);
}
</style>
