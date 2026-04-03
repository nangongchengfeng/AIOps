<template>
  <div class="global-blobs" aria-hidden="true">
    <div class="blob blob-1" />
    <div class="blob blob-2" />
    <div class="blob blob-3" />
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.global-blobs {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.blob {
  position: absolute;
  border-radius: var(--radius-blob);
  animation: morphBlob var(--duration-morph) ease-in-out infinite alternate;
  filter: blur(60px);
  opacity: 0.5;
}

.blob-1 {
  width: 520px;
  height: 520px;
  top: -200px;
  right: -100px;
  background: radial-gradient(circle, rgba(155, 127, 232, 0.18), transparent 70%);
  animation-duration: 9s;
}

.blob-2 {
  width: 380px;
  height: 380px;
  bottom: 10%;
  left: -80px;
  background: radial-gradient(circle, rgba(126, 206, 196, 0.15), transparent 70%);
  animation-duration: 7s;
  animation-delay: -3s;
}

.blob-3 {
  width: 280px;
  height: 280px;
  top: 50%;
  left: 40%;
  background: radial-gradient(circle, rgba(232, 164, 184, 0.12), transparent 70%);
  animation-duration: 11s;
  animation-delay: -5s;
}
</style>
