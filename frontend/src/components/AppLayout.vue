<template>
  <div class="app-layout">
    <Sidebar />
    <div class="main-area">
      <main class="page-content">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import Sidebar from './Sidebar.vue'
</script>

<style scoped>
.app-layout {
  display: flex;
  width: 100%;
  height: 100%;
  position: relative;
  z-index: 1;
}

.main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.page-content {
  flex: 1;
  padding: 28px;
  overflow-y: auto;
  position: relative;
}
</style>
