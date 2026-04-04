import { defineStore } from 'pinia'
import { ref } from 'vue'

/**
 * 用户状态 store
 */
export const useUserStore = defineStore('user', () => {
  // 用户信息
  const userInfo = ref<{ id: number; name: string; avatar?: string } | null>(null)
  // 登录 token
  const token = ref<string>('')

  /**
   * 设置用户信息
   */
  const setUserInfo = (info: { id: number; name: string; avatar?: string }) => {
    userInfo.value = info
  }

  /**
   * 设置 token
   */
  const setToken = (t: string) => {
    token.value = t
  }

  /**
   * 清除用户状态
   */
  const clearUser = () => {
    userInfo.value = null
    token.value = ''
  }

  return {
    userInfo,
    token,
    setUserInfo,
    setToken,
    clearUser,
  }
})
