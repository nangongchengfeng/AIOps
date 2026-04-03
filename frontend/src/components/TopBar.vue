<template>
  <header class="top-bar">
    <div class="top-bar-left">
      <h1 class="page-title">{{ currentPageTitle }}</h1>
    </div>
    <div class="top-bar-right">
      <div class="search-box">
        <Search :size="16" />
        <input
          type="text"
          placeholder="搜索告警..."
          class="search-input"
        />
      </div>
      <button class="icon-btn">
        <Bell :size="18" />
      </button>
      <div class="user-avatar">
        <User :size="18" />
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { Search, Bell, User } from 'lucide-vue-next'

const route = useRoute()

const currentPageTitle = computed(() => {
  return route.meta.title || 'AIOps'
})
</script>

<style scoped>
.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 28px;
  background: var(--bg-surface);
  border-bottom: 1px solid rgba(155, 127, 232, 0.1);
  position: relative;
  z-index: 10;
}

.top-bar-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.page-title {
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.top-bar-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(155, 127, 232, 0.05);
  border: 1.5px solid rgba(155, 127, 232, 0.18);
  border-radius: 16px 10px 14px 8px;
  padding: 10px 16px;
  transition: all var(--duration-hover) var(--easing-smooth);
}

.search-box:focus-within {
  border-color: var(--color-primary);
  background: rgba(155, 127, 232, 0.08);
  box-shadow: 0 0 0 3px rgba(155, 127, 232, 0.12);
}

.search-input {
  border: none;
  background: transparent;
  outline: none;
  font-size: var(--text-sm);
  color: var(--text-primary);
  width: 200px;
  font-family: var(--font-body);
}

.search-input::placeholder {
  color: var(--text-muted);
}

.icon-btn {
  width: 40px;
  height: 40px;
  border: none;
  background: rgba(155, 127, 232, 0.08);
  border-radius: 12px 8px 10px 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--duration-hover) var(--easing-organic);
}

.icon-btn:hover {
  background: rgba(155, 127, 232, 0.15);
  color: var(--color-primary);
  transform: translateY(-2px);
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: var(--gradient-primary);
  border-radius: 14px 10px 12px 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  cursor: pointer;
  transition: transform var(--duration-hover) var(--easing-organic);
}

.user-avatar:hover {
  transform: scale(1.05);
}
</style>
