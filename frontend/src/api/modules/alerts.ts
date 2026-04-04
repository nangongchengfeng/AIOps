import api from '@/api/index'
import type { Alert, AlertListResponse, Analysis, WebhookResponse } from '@/api/types'

export interface AlertTrendItem {
  date: string
  count: number
}

export interface AlertTrendResponse {
  items: AlertTrendItem[]
  total: number
}

/**
 * 告警相关 API
 */
export const alertsApi = {
  /**
   * 获取告警列表
   */
  async getAlerts(params?: {
    status?: string
    limit?: number
    offset?: number
  }): Promise<AlertListResponse> {
    const response = await api.get('/api/v1/alerts', { params })
    return response.data
  },

  /**
   * 获取单个告警详情
   */
  async getAlert(alertId: number): Promise<Alert> {
    const response = await api.get(`/api/v1/alerts/${alertId}`)
    return response.data
  },

  /**
   * 通过 fingerprint 获取告警
   */
  async getAlertByFingerprint(fingerprint: string): Promise<Alert> {
    const response = await api.get(`/api/v1/alerts/fingerprint/${fingerprint}`)
    return response.data
  },

  /**
   * 分析告警
   */
  async analyzeAlert(alertId: number): Promise<Analysis> {
    const response = await api.post(`/api/v1/alerts/${alertId}/analyze`)
    return response.data
  },

  /**
   * 获取告警的分析历史
   */
  async getAlertAnalyses(alertId: number): Promise<Analysis[]> {
    const response = await api.get(`/api/v1/alerts/${alertId}/analyses`)
    return response.data
  },

  /**
   * 获取最新的分析记录
   */
  async getLatestAnalyses(limit: number = 10): Promise<Analysis[]> {
    const response = await api.get('/api/v1/alerts/analyses/latest', {
      params: { limit },
    })
    return response.data
  },

  /**
   * 接收 webhook (用于测试)
   */
  async receiveWebhook(webhook: any): Promise<WebhookResponse> {
    const response = await api.post('/api/v1/alerts/webhook', webhook)
    return response.data
  },

  /**
   * 获取告警趋势统计
   */
  async getTrend(days: number = 7): Promise<AlertTrendResponse> {
    const response = await api.get('/api/v1/alerts/trend', { params: { days } })
    return response.data as AlertTrendResponse
  },
}
