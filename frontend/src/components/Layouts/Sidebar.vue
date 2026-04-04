<template>
  <aside class="w-60 bg-gradient-to-b from-slate-900 to-slate-800 py-6 flex flex-col rounded-r-3xl">
    <div class="flex flex-col h-full">
      <div class="flex items-center gap-3 px-6 pb-8">
        <div class="w-11 h-11 bg-gradient-to-r from-[#0052FF] to-[#4D7CFF] rounded-xl flex items-center justify-center text-white">
          <el-icon :size="28"><Platform /></el-icon>
        </div>
        <span class="text-2xl font-extrabold text-white">AIOps</span>
      </div>

      <nav class="flex flex-col gap-1 px-3">
        <RouterLink
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="flex items-center gap-3 px-4 py-3 text-white/70 no-underline text-sm font-medium rounded-r-xl transition-all duration-200"
          :class="{ 'text-white bg-white/10 border-l-3 border-blue-400': isActive(item.path) }"
          @click.prevent="navigateTo(item.path)"
        >
          <el-icon :size="20">
            <component :is="item.icon" />
          </el-icon>
          <span>{{ item.label }}</span>
        </RouterLink>
      </nav>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { Platform, DataLine, WarningFilled, Star } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const navItems = [
  { path: '/dashboard', label: '仪表盘', icon: DataLine },
  { path: '/alerts', label: '告警管理', icon: WarningFilled },
  { path: '/analyses', label: 'AI 分析', icon: Star },
]

const isActive = (path: string) => {
  return route.path.startsWith(path)
}

const navigateTo = (path: string) => {
  router.push(path)
}
</script>

<style scoped>
.router-link-active {
  color: white !important;
  background: rgba(255, 255, 255, 0.1) !important;
  border-left: 3px solid #4d7cff !important;
}
</style>
