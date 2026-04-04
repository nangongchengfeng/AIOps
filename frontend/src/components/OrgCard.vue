<template>
  <div class="org-card" :class="{ 'no-decoration': noDecoration }">
    <slot />
  </div>
</template>

<script setup lang="ts">
interface Props {
  noDecoration?: boolean
}

withDefaults(defineProps<Props>(), {
  noDecoration: false
})
</script>

<style scoped>
.org-card {
  background: var(--gradient-surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  padding: 24px 28px;
  border: 1px solid rgba(91, 155, 213, 0.1);
  transition: transform var(--duration-hover) var(--easing-smooth),
    box-shadow var(--duration-hover) var(--easing-smooth);
  position: relative;
  overflow: hidden;
}

.org-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.org-card:active {
  transform: translateY(0) scale(1);
  transition-duration: var(--duration-active);
}
</style>
