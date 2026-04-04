import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

/**
 * 应用全局状态 store
 */
export const useAppStore = defineStore('app', () => {
  // 侧边栏折叠状态
  const sidebarCollapsed = ref(false)
  // 加载状态
  const loading = ref(false)

  /**
   * 切换侧边栏
   */
  const toggleSidebar = () => {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  /**
   * 设置加载状态
   */
  const setLoading = (status: boolean) => {
    loading.value = status
  }

  return {
    sidebarCollapsed,
    loading,
    toggleSidebar,
    setLoading,
  }
})
