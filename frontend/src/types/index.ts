export interface Alert {
  id: number
  fingerprint: string
  alert_id?: string
  group_key?: string
  status: string
  alert_name: string
  severity?: string
  summary?: string
  description?: string
  labels?: Record<string, any>
  annotations?: Record<string, any>
  starts_at: string
  ends_at?: string
  update_count: number
  last_received_at: string
  created_at: string
}

export interface AlertListResponse {
  items: Alert[]
  total: number
  limit: number
  offset: number
}

export interface Analysis {
  id: number
  alert_id: number
  version: number
  is_latest: boolean
  root_cause?: string
  possible_solutions?: string[]
  reasoning?: string
  confidence_score?: number
  model_used?: string
  status: string
  error_message?: string
  started_at: string
  completed_at?: string
  created_at: string
}

export interface WebhookResponse {
  success: boolean
  message: string
  alert_ids?: number[]
}
