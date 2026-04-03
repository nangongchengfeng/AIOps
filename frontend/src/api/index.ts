import axios from 'axios'
import type { Alert, AlertListResponse, Analysis, WebhookResponse } from '@/types'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 告警相关 API
export const alertsApi = {
  // 获取告警列表
  getAlerts: async (params?: {
    status?: string
    limit?: number
    offset?: number
  }): Promise<AlertListResponse> => {
    const response = await api.get('/api/v1/alerts', { params })
    return response.data
  },

  // 获取单个告警详情
  getAlert: async (alertId: number): Promise<Alert> => {
    const response = await api.get(`/api/v1/alerts/${alertId}`)
    return response.data
  },

  // 通过 fingerprint 获取告警
  getAlertByFingerprint: async (fingerprint: string): Promise<Alert> => {
    const response = await api.get(`/api/v1/alerts/fingerprint/${fingerprint}`)
    return response.data
  },

  // 分析告警
  analyzeAlert: async (alertId: number): Promise<Analysis> => {
    const response = await api.post(`/api/v1/alerts/${alertId}/analyze`)
    return response.data
  },

  // 获取告警的分析历史
  getAlertAnalyses: async (alertId: number): Promise<Analysis[]> => {
    const response = await api.get(`/api/v1/alerts/${alertId}/analyses`)
    return response.data
  },

  // 获取最新的分析记录
  getLatestAnalyses: async (limit: number = 10): Promise<Analysis[]> => {
    const response = await api.get('/api/v1/alerts/analyses/latest', {
      params: { limit }
    })
    return response.data
  },

  // 接收 webhook (用于测试)
  receiveWebhook: async (webhook: any): Promise<WebhookResponse> => {
    const response = await api.post('/api/v1/alerts/webhook', webhook)
    return response.data
  }
}

export default api
