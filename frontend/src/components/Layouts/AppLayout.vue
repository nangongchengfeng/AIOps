<template>
  <div class="app-layout flex w-full h-full relative z-1 bg-[#FAFAFA]">
    <Sidebar />
    <div class="main-area flex-1 flex flex-col overflow-hidden">
      <main class="page-content flex-1 p-7 overflow-y-auto relative">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import Sidebar from './Sidebar.vue'
</script>
