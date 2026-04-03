<template>
  <div class="app">
    <GlobalBlobs />
    <AppLayout />
  </div>
</template>

<script setup lang="ts">
import AppLayout from '@/components/AppLayout.vue'
import GlobalBlobs from '@/components/GlobalBlobs.vue'
</script>

<style scoped>
.app {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}
</style>
