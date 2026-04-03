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
  background: rgba(155, 127, 232, 0.15);
  color: var(--color-primary-dark);
}

.badge-success {
  background: rgba(142, 203, 168, 0.15);
  color: #4a9464;
}

.badge-warning {
  background: rgba(232, 204, 138, 0.2);
  color: #9a7020;
}

.badge-error {
  background: rgba(232, 150, 140, 0.15);
  color: #9c3a30;
}

.badge-info {
  background: rgba(138, 180, 232, 0.15);
  color: #2a5e9a;
}
</style>
