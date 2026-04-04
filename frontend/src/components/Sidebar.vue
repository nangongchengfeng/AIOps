<template>
  <aside class="sidebar">
    <div class="sidebar-content">
      <div class="logo">
        <div class="logo-icon">
          <Brain :size="28" />
        </div>
        <span class="logo-text">AIOps</span>
      </div>

      <nav class="nav">
        <RouterLink
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ active: isActive(item.path) }"
        >
          <component :is="item.icon" :size="20" />
          <span>{{ item.label }}</span>
        </RouterLink>
      </nav>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router'
import { LayoutDashboard, AlertTriangle, Sparkles, Brain } from 'lucide-vue-next'

const route = useRoute()

const navItems = [
  { path: '/dashboard', label: '仪表盘', icon: LayoutDashboard },
  { path: '/alerts', label: '告警管理', icon: AlertTriangle },
  { path: '/analyses', label: 'AI 分析', icon: Sparkles }
]

const isActive = (path: string) => {
  return route.path.startsWith(path)
}
</script>

<style scoped>
.sidebar {
  width: 240px;
  background: rgba(91, 155, 213, 0.12);
  padding: 24px 0;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-right: 1px solid rgba(91, 155, 213, 0.15);
  border-radius: 0 24px 20px 0;
}

.sidebar-content {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 24px 32px;
}

.logo-icon {
  width: 44px;
  height: 44px;
  background: var(--gradient-primary);
  border-radius: 14px 8px 12px 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.logo-text {
  font-family: var(--font-display);
  font-size: 22px;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 0 12px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  border-radius: var(--radius-md);
  transition: all var(--duration-hover) var(--easing-smooth);
  position: relative;
}

.nav-item:hover {
  color: var(--text-primary);
  background: rgba(91, 155, 213, 0.08);
}

.nav-item.active {
  color: var(--color-primary);
  background: linear-gradient(90deg, rgba(91, 155, 213, 0.15), rgba(91, 155, 213, 0.05));
  border-left: 3px solid var(--color-primary);
}
</style>
