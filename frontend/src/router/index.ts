import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: { title: '仪表盘' }
  },
  {
    path: '/alerts',
    name: 'Alerts',
    component: () => import('@/views/Alerts.vue'),
    meta: { title: '告警管理' }
  },
  {
    path: '/alerts/:id',
    name: 'AlertDetail',
    component: () => import('@/views/AlertDetail.vue'),
    meta: { title: '告警详情' }
  },
  {
    path: '/analyses',
    name: 'Analyses',
    component: () => import('@/views/Analyses.vue'),
    meta: { title: 'AI 分析' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title || 'AIOps'} - 智能运维平台`
  next()
})

export default router
