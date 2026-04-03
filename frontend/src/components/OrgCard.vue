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
  border-radius: var(--radius-organic-md);
  box-shadow: var(--shadow-md);
  padding: 24px 28px;
  border: 1px solid rgba(155, 127, 232, 0.1);
  transition: transform var(--duration-hover) var(--easing-organic),
    box-shadow var(--duration-hover) var(--easing-organic);
  position: relative;
  overflow: hidden;
}

.org-card:nth-child(2n) {
  border-radius: 28px 38px 22px 32px;
}

.org-card:nth-child(3n) {
  border-radius: 36px 22px 38px 18px;
}

.org-card:not(.no-decoration)::before {
  content: '';
  position: absolute;
  width: 180px;
  height: 180px;
  top: -60px;
  right: -50px;
  background: var(--gradient-primary);
  opacity: 0.06;
  border-radius: var(--radius-blob);
  animation: morphBlob var(--duration-morph) ease-in-out infinite alternate;
  pointer-events: none;
}

.org-card:hover {
  transform: translateY(-3px) scale(1.008);
  box-shadow: var(--shadow-lg);
}

.org-card:active {
  transform: translateY(0) scale(1);
  transition-duration: var(--duration-active);
}
</style>
