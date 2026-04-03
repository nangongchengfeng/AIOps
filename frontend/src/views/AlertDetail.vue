<template>
  <div class="alert-detail">
    <div class="page-header">
      <button class="back-btn" @click="goBack">
        <ArrowLeft :size="20" />
        返回
      </button>
      <div class="header-title">
        <h1 class="page-title">告警详情</h1>
        <p class="page-subtitle">#{{ alertId }}</p>
      </div>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner" />
      <span>加载中...</span>
    </div>

    <div v-else-if="!alert" class="error-state">
      <div class="error-icon">
        <AlertCircle :size="64" />
      </div>
      <p>未找到该告警</p>
    </div>

    <template v-else>
      <div class="content-grid">
        <div class="main-content">
          <OrgCard class="info-card">
            <div class="card-header-row">
              <h2 class="card-title">基本信息</h2>
              <Badge :type="getStatusBadgeType(alert.status)">
                {{ getStatusText(alert.status) }}
              </Badge>
            </div>

            <div class="info-grid">
              <div class="info-item">
                <span class="info-label">告警名称</span>
                <span class="info-value">{{ alert.alert_name }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">严重程度</span>
                <span class="info-value">
                  <span class="severity-dot" :class="`severity-${alert.severity || 'unknown'}`"></span>
                  {{ alert.severity || 'unknown' }}
                </span>
              </div>
              <div class="info-item">
                <span class="info-label">Fingerprint</span>
                <span class="info-value mono">{{ alert.fingerprint }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">状态</span>
                <span class="info-value">{{ getStatusText(alert.status) }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">开始时间</span>
                <span class="info-value">{{ formatFullTime(alert.starts_at) }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">结束时间</span>
                <span class="info-value">{{ alert.ends_at ? formatFullTime(alert.ends_at) : '-' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">推送次数</span>
                <span class="info-value">{{ alert.update_count }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">最后接收</span>
                <span class="info-value">{{ formatFullTime(alert.last_received_at) }}</span>
              </div>
            </div>

            <div v-if="alert.summary || alert.description" class="section">
              <h3 class="section-title">描述</h3>
              <p v-if="alert.summary" class="description-text">{{ alert.summary }}</p>
              <p v-if="alert.description" class="description-text secondary">{{ alert.description }}</p>
            </div>

            <div v-if="alert.labels && Object.keys(alert.labels).length > 0" class="section">
              <h3 class="section-title">标签</h3>
              <div class="tags-list">
                <span v-for="(value, key) in alert.labels" :key="key" class="tag">
                  <span class="tag-key">{{ key }}</span>
                  <span class="tag-value">{{ value }}</span>
                </span>
              </div>
            </div>

            <div v-if="alert.annotations && Object.keys(alert.annotations).length > 0" class="section">
              <h3 class="section-title">注解</h3>
              <div class="annotations-grid">
                <div v-for="(value, key) in alert.annotations" :key="key" class="annotation-item">
                  <span class="annotation-key">{{ key }}</span>
                  <span class="annotation-value">{{ value }}</span>
                </div>
              </div>
            </div>
          </OrgCard>
        </div>

        <div class="side-content">
          <OrgCard class="action-card">
            <h2 class="card-title">操作</h2>
            <OrgButton class="full-width" @click="startAnalysis" :disabled="analyzing">
              <Sparkles :size="16" />
              {{ analyzing ? '分析中...' : '开始 AI 分析' }}
            </OrgButton>
          </OrgCard>

          <OrgCard class="analyses-card">
            <h2 class="card-title">分析历史</h2>
            <div v-if="loadingAnalyses" class="small-loading">
              <div class="spinner small" />
            </div>
            <div v-else-if="analyses.length === 0" class="empty-small">
              <p>暂无分析记录</p>
            </div>
            <div v-else class="analyses-list">
              <div
                v-for="analysis in analyses"
                :key="analysis.id"
                class="analysis-item"
                :class="{ latest: analysis.is_latest }"
                @click="showAnalysisDetail(analysis)"
              >
                <div class="analysis-header">
                  <span class="analysis-version">v{{ analysis.version }}</span>
                  <Badge :type="getAnalysisBadgeType(analysis.status)">
                    {{ getAnalysisStatusText(analysis.status) }}
                  </Badge>
                </div>
                <div class="analysis-time">{{ formatTime(analysis.created_at) }}</div>
                <div v-if="analysis.is_latest" class="latest-badge">最新</div>
              </div>
            </div>
          </OrgCard>
        </div>
      </div>
    </template>

    <div v-if="selectedAnalysis" class="analysis-modal" @click.self="closeAnalysisDetail">
      <div class="modal-content">
        <div class="modal-header">
          <h3>分析结果 v{{ selectedAnalysis.version }}</h3>
          <button class="close-btn" @click="closeAnalysisDetail">
            <X :size="20" />
          </button>
        </div>
        <div class="modal-body">
          <div class="analysis-status-row">
            <Badge :type="getAnalysisBadgeType(selectedAnalysis.status)">
              {{ getAnalysisStatusText(selectedAnalysis.status) }}
            </Badge>
            <span v-if="selectedAnalysis.confidence_score" class="confidence">
              置信度: {{ (selectedAnalysis.confidence_score * 100).toFixed(0) }}%
            </span>
          </div>

          <div v-if="selectedAnalysis.status === 'completed'" class="analysis-result">
            <div v-if="selectedAnalysis.root_cause" class="result-section">
              <h4 class="result-title">
                <Search :size="18" />
                根本原因
              </h4>
              <p class="result-text">{{ selectedAnalysis.root_cause }}</p>
            </div>

            <div v-if="selectedAnalysis.possible_solutions && selectedAnalysis.possible_solutions.length > 0" class="result-section">
              <h4 class="result-title">
                <Lightbulb :size="18" />
                解决方案
              </h4>
              <ul class="solutions-list">
                <li v-for="(solution, index) in selectedAnalysis.possible_solutions" :key="index">
                  {{ solution }}
                </li>
              </ul>
            </div>

            <div v-if="selectedAnalysis.reasoning" class="result-section">
              <h4 class="result-title">
                <Brain :size="18" />
                推理过程
              </h4>
              <p class="result-text">{{ selectedAnalysis.reasoning }}</p>
            </div>
          </div>

          <div v-else-if="selectedAnalysis.status === 'failed'" class="analysis-error">
            <div class="error-icon">
              <AlertCircle :size="48" />
            </div>
            <p class="error-message">{{ selectedAnalysis.error_message || '分析失败' }}</p>
          </div>

          <div v-else class="analysis-pending">
            <div class="pending-icon">
              <div class="spinner" />
            </div>
            <p>分析进行中...</p>
          </div>

          <div class="analysis-meta">
            <span>模型: {{ selectedAnalysis.model_used || '-' }}</span>
            <span>开始: {{ formatFullTime(selectedAnalysis.started_at) }}</span>
            <span v-if="selectedAnalysis.completed_at">完成: {{ formatFullTime(selectedAnalysis.completed_at) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, AlertCircle, Sparkles, X, Search, Lightbulb, Brain } from 'lucide-vue-next'
import OrgCard from '@/components/OrgCard.vue'
import OrgButton from '@/components/OrgButton.vue'
import Badge from '@/components/Badge.vue'
import { alertsApi } from '@/api'
import type { Alert, Analysis } from '@/types'

const route = useRoute()
const router = useRouter()
const alertId = computed(() => Number(route.params.id))

const alert = ref<Alert | null>(null)
const analyses = ref<Analysis[]>([])
const loading = ref(true)
const loadingAnalyses = ref(false)
const analyzing = ref(false)
const selectedAnalysis = ref<Analysis | null>(null)
const isUnmounted = ref(false)
let pollTimer: number | null = null

const loadAlert = async () => {
  loading.value = true
  try {
    const data = await alertsApi.getAlert(alertId.value)
    if (!isUnmounted.value) {
      alert.value = data
    }
  } catch (error) {
    if (!isUnmounted.value) {
      console.error('Failed to load alert:', error)
      alert.value = null
    }
  } finally {
    if (!isUnmounted.value) {
      loading.value = false
    }
  }
}

const loadAnalyses = async () => {
  loadingAnalyses.value = true
  try {
    const data = await alertsApi.getAlertAnalyses(alertId.value)
    if (!isUnmounted.value) {
      analyses.value = data
      // 如果有 pending 的分析且没有在轮询，自动开始轮询
      const hasPending = data.some((a: Analysis) => a.status === 'pending')
      if (hasPending && !pollTimer) {
        analyzing.value = true
        startPolling()
      }
    }
  } catch (error) {
    if (!isUnmounted.value) {
      console.error('Failed to load analyses:', error)
      analyses.value = []
    }
  } finally {
    if (!isUnmounted.value) {
      loadingAnalyses.value = false
    }
  }
}

const startPolling = () => {
  stopPolling()
  pollTimer = window.setInterval(async () => {
    if (!isUnmounted.value) {
      await loadAnalyses()
      // 检查是否有 pending 的分析
      const hasPending = analyses.value.some(a => a.status === 'pending')
      if (!hasPending) {
        stopPolling()
        analyzing.value = false
      }
    }
  }, 2000)
}

const stopPolling = () => {
  if (pollTimer !== null) {
    clearInterval(pollTimer)
    pollTimer = null
  }
}

const startAnalysis = async () => {
  analyzing.value = true
  try {
    await alertsApi.analyzeAlert(alertId.value)
    if (!isUnmounted.value) {
      await loadAnalyses()
      // 开始轮询检查状态
      startPolling()
    }
  } catch (error) {
    if (!isUnmounted.value) {
      console.error('Failed to start analysis:', error)
      analyzing.value = false
    }
  }
}

const showAnalysisDetail = (analysis: Analysis) => {
  selectedAnalysis.value = analysis
}

const closeAnalysisDetail = () => {
  selectedAnalysis.value = null
}

const goBack = () => {
  router.back()
}

const getStatusText = (status: string) => {
  const map: Record<string, string> = { firing: '触发中', resolved: '已解决' }
  return map[status] || status
}

const getStatusBadgeType = (status: string): any => {
  const map: Record<string, any> = { firing: 'error', resolved: 'success' }
  return map[status] || 'info'
}

const getAnalysisStatusText = (status: string) => {
  const map: Record<string, string> = { pending: '分析中', completed: '已完成', failed: '失败' }
  return map[status] || status
}

const getAnalysisBadgeType = (status: string): any => {
  const map: Record<string, any> = { pending: 'warning', completed: 'success', failed: 'error' }
  return map[status] || 'info'
}

const formatTime = (time: string) => {
  const date = new Date(time)
  return date.toLocaleString('zh-CN', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

const formatFullTime = (time: string) => {
  const date = new Date(time)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  loadAlert()
  loadAnalyses()
})

onUnmounted(() => {
  isUnmounted.value = true
  stopPolling()
})
</script>

<style scoped>
.alert-detail {
  position: relative;
  z-index: 1;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  animation: fadeSlideUp 0.6s var(--easing-organic) both;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  font-size: 14px;
  font-family: var(--font-body);
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 12px 8px 10px 6px;
  transition: all var(--duration-hover) var(--easing-organic);
}

.back-btn:hover {
  background: rgba(155, 127, 232, 0.1);
  color: var(--color-primary);
}

.header-title {
  flex: 1;
}

.page-title {
  font-family: var(--font-display);
  font-size: 28px;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0 0 2px;
}

.page-subtitle {
  color: var(--text-muted);
  font-size: 14px;
  margin: 0;
}

.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 24px;
  gap: 16px;
  color: var(--text-muted);
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid rgba(155, 127, 232, 0.2);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.spinner.small {
  width: 20px;
  height: 20px;
}

.error-icon {
  opacity: 0.4;
}

.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
}

.info-card,
.action-card,
.analyses-card {
  animation: fadeSlideUp 0.6s var(--easing-organic) 0.1s both;
}

.card-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.card-title {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 12px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: 600;
}

.info-value {
  font-size: 14px;
  color: var(--text-primary);
  font-weight: 500;
}

.info-value.mono {
  font-family: var(--font-mono);
  font-size: 12px;
}

.severity-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 6px;
  vertical-align: middle;
}

.severity-critical { background: var(--color-error); }
.severity-warning { background: var(--color-warning); }
.severity-info { background: var(--color-info); }
.severity-unknown { background: var(--text-muted); }

.section {
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid rgba(155, 127, 232, 0.1);
}

.section-title {
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 700;
  color: var(--text-secondary);
  margin: 0 0 12px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.description-text {
  font-size: 14px;
  color: var(--text-primary);
  line-height: var(--leading-loose);
  margin: 0;
}

.description-text.secondary {
  color: var(--text-secondary);
  margin-top: 8px;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  background: rgba(155, 127, 232, 0.1);
  border-radius: 12px 6px 10px 8px;
  font-size: 12px;
}

.tag-key {
  color: var(--text-secondary);
  font-weight: 500;
}

.tag-value {
  color: var(--text-primary);
  font-weight: 600;
}

.annotations-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.annotation-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 10px 14px;
  background: rgba(155, 127, 232, 0.05);
  border-radius: 12px 8px 10px 6px;
}

.annotation-key {
  font-size: 11px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: 600;
}

.annotation-value {
  font-size: 13px;
  color: var(--text-primary);
}

.action-card {
  margin-bottom: 16px;
}

.full-width {
  width: 100%;
}

.small-loading {
  display: flex;
  justify-content: center;
  padding: 24px;
}

.empty-small {
  text-align: center;
  padding: 24px;
  color: var(--text-muted);
  font-size: 13px;
}

.analyses-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 12px;
}

.analysis-item {
  padding: 12px 14px;
  background: rgba(155, 127, 232, 0.05);
  border-radius: 14px 8px 12px 10px;
  cursor: pointer;
  transition: all var(--duration-hover) var(--easing-organic);
  position: relative;
}

.analysis-item:hover {
  background: rgba(155, 127, 232, 0.12);
  transform: translateY(-2px);
}

.analysis-item.latest {
  border: 1.5px solid var(--color-primary-light);
  background: rgba(155, 127, 232, 0.1);
}

.analysis-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 4px;
}

.analysis-version {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 13px;
  color: var(--text-primary);
}

.analysis-time {
  font-size: 12px;
  color: var(--text-muted);
}

.latest-badge {
  position: absolute;
  top: 8px;
  right: 10px;
  font-size: 10px;
  font-weight: 700;
  color: var(--color-primary);
  background: rgba(155, 127, 232, 0.2);
  padding: 2px 8px;
  border-radius: 8px 4px 6px 4px;
}

.analysis-modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 24px;
  animation: fadeIn 0.2s ease-out both;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-content {
  background: var(--bg-surface);
  border-radius: var(--radius-organic-lg);
  box-shadow: var(--shadow-lg);
  max-width: 700px;
  width: 100%;
  max-height: 80vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  animation: fadeSlideUp 0.3s var(--easing-organic) both;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(155, 127, 232, 0.1);
}

.modal-header h3 {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.close-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: rgba(155, 127, 232, 0.1);
  border-radius: 12px 8px 10px 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--duration-hover) var(--easing-organic);
}

.close-btn:hover {
  background: rgba(155, 127, 232, 0.2);
  color: var(--text-primary);
}

.modal-body {
  padding: 24px;
  overflow-y: auto;
}

.analysis-status-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.confidence {
  font-size: 13px;
  color: var(--text-secondary);
}

.analysis-result {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.result-section {
  padding: 16px 18px;
  background: rgba(155, 127, 232, 0.06);
  border-radius: 18px 12px 16px 10px;
}

.result-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 10px;
}

.result-text {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: var(--leading-loose);
  margin: 0;
}

.solutions-list {
  margin: 0;
  padding-left: 18px;
}

.solutions-list li {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: var(--leading-loose);
  margin-bottom: 6px;
}

.solutions-list li:last-child {
  margin-bottom: 0;
}

.analysis-error,
.analysis-pending {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 24px;
  gap: 16px;
}

.error-icon,
.pending-icon {
  opacity: 0.5;
}

.error-message {
  color: var(--text-secondary);
  margin: 0;
}

.analysis-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid rgba(155, 127, 232, 0.1);
}

.analysis-meta span {
  font-size: 12px;
  color: var(--text-muted);
}
</style>
