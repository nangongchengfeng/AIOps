<template>
  <div class="analyses-page">
    <div class="page-header">
      <div>
        <h1 class="page-title">AI 分析</h1>
        <p class="page-subtitle">查看所有告警的 AI 分析记录</p>
      </div>
    </div>

    <OrgCard class="list-card">
      <div v-if="loading" class="loading-state">
        <div class="spinner" />
        <span>加载中...</span>
      </div>

      <div v-else-if="analyses.length === 0" class="empty-state">
        <div class="empty-icon">
          <Sparkles :size="64" />
        </div>
        <p>暂无分析记录</p>
      </div>

      <div v-else class="analyses-container">
        <div
          v-for="analysis in analyses"
          :key="analysis.id"
          class="analysis-card"
        >
          <div class="analysis-header">
            <div class="analysis-id">
              <span class="alert-link" @click="goToAlert(analysis.alert_id)">
                告警 #{{ analysis.alert_id }}
              </span>
              <span class="analysis-version">v{{ analysis.version }}</span>
            </div>
            <div class="header-right">
              <Badge :type="getAnalysisBadgeType(analysis.status)">
                {{ getAnalysisStatusText(analysis.status) }}
              </Badge>
              <span v-if="analysis.is_latest" class="latest-tag">最新</span>
            </div>
          </div>

          <div v-if="analysis.status === 'completed'" class="analysis-content">
            <div v-if="analysis.root_cause" class="content-section">
              <div class="section-icon" style="background: linear-gradient(135deg, #5b9bd5, #8ecae6);">
                <Search :size="18" />
              </div>
              <div class="section-content">
                <h4 class="section-title">根本原因</h4>
                <p class="section-text">{{ analysis.root_cause }}</p>
              </div>
            </div>

            <div v-if="analysis.possible_solutions && analysis.possible_solutions.length > 0" class="content-section">
              <div class="section-icon" style="background: linear-gradient(135deg, #7ecec4, #a8cfe0);">
                <Lightbulb :size="18" />
              </div>
              <div class="section-content">
                <h4 class="section-title">解决方案</h4>
                <ul class="solutions-list">
                  <li v-for="(solution, index) in analysis.possible_solutions" :key="index">
                    {{ solution }}
                  </li>
                </ul>
              </div>
            </div>

            <div v-if="analysis.confidence_score" class="confidence-bar">
              <span class="confidence-label">置信度</span>
              <div class="bar-container">
                <div class="bar-fill" :style="{ width: `${analysis.confidence_score * 100}%` }"></div>
              </div>
              <span class="confidence-value">{{ (analysis.confidence_score * 100).toFixed(0) }}%</span>
            </div>
          </div>

          <div v-else-if="analysis.status === 'failed'" class="analysis-error">
            <div class="error-icon">
              <AlertCircle :size="32" />
            </div>
            <p class="error-text">{{ analysis.error_message || '分析失败' }}</p>
          </div>

          <div v-else class="analysis-pending">
            <div class="pending-icon">
              <div class="spinner" />
            </div>
            <p>分析进行中...</p>
          </div>

          <div class="analysis-footer">
            <span class="analysis-time">
              <Clock :size="14" />
              {{ formatTime(analysis.created_at) }}
            </span>
            <span v-if="analysis.model_used" class="model-used">
              模型: {{ analysis.model_used }}
            </span>
            <OrgButton variant="secondary" size="sm" @click="goToAlert(analysis.alert_id)">
              查看告警
            </OrgButton>
          </div>
        </div>
      </div>
    </OrgCard>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Sparkles, Search, Lightbulb, AlertCircle, Clock } from 'lucide-vue-next'
import OrgCard from '@/components/OrgCard.vue'
import OrgButton from '@/components/OrgButton.vue'
import Badge from '@/components/Badge.vue'
import { alertsApi } from '@/api'
import type { Analysis } from '@/types'

const router = useRouter()
const analyses = ref<Analysis[]>([])
const loading = ref(true)
const isUnmounted = ref(false)

const loadAnalyses = async () => {
  loading.value = true
  try {
    const data = await alertsApi.getLatestAnalyses(20)
    if (!isUnmounted.value) {
      analyses.value = data
    }
  } catch (error) {
    if (!isUnmounted.value) {
      console.error('Failed to load analyses:', error)
      analyses.value = []
    }
  } finally {
    if (!isUnmounted.value) {
      loading.value = false
    }
  }
}

const goToAlert = (alertId: number) => {
  router.push(`/alerts/${alertId}`)
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
  return date.toLocaleString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

onMounted(() => {
  loadAnalyses()
})

onUnmounted(() => {
  isUnmounted.value = true
})
</script>

<style scoped>
.analyses-page {
  position: relative;
  z-index: 1;
}

.page-header {
  margin-bottom: 24px;
  animation: fadeSlideUp 0.6s var(--easing-organic) both;
}

.page-title {
  font-family: var(--font-display);
  font-size: 28px;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0 0 4px;
}

.page-subtitle {
  color: var(--text-secondary);
  font-size: 14px;
  margin: 0;
}

.list-card {
  padding: 0;
  animation: fadeSlideUp 0.6s var(--easing-organic) 0.1s both;
}

.loading-state,
.empty-state {
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
  border: 3px solid rgba(91, 155, 213, 0.2);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.empty-icon {
  opacity: 0.3;
}

.analyses-container {
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.analysis-card {
  background: rgba(91, 155, 213, 0.04);
  border-radius: 28px 18px 24px 20px;
  padding: 20px;
  border: 1px solid rgba(91, 155, 213, 0.08);
  transition: all var(--duration-hover) var(--easing-organic);
}

.analysis-card:hover {
  background: rgba(91, 155, 213, 0.08);
  border-color: rgba(91, 155, 213, 0.15);
  transform: translateY(-2px);
}

.analysis-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.analysis-id {
  display: flex;
  align-items: center;
  gap: 10px;
}

.alert-link {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
  color: var(--color-primary);
  cursor: pointer;
  transition: color var(--duration-hover) var(--easing-smooth);
}

.alert-link:hover {
  color: var(--color-primary-dark);
  text-decoration: underline;
}

.analysis-version {
  font-size: 12px;
  color: var(--text-muted);
  background: rgba(91, 155, 213, 0.1);
  padding: 2px 8px;
  border-radius: 8px 4px 6px 4px;
  font-weight: 600;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.latest-tag {
  font-size: 11px;
  font-weight: 700;
  color: var(--color-primary);
  background: rgba(91, 155, 213, 0.15);
  padding: 3px 10px;
  border-radius: 50px 28px 44px 24px;
}

.analysis-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.content-section {
  display: flex;
  gap: 12px;
}

.section-icon {
  width: 40px;
  height: 40px;
  border-radius: 14px 8px 12px 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.section-content {
  flex: 1;
}

.section-title {
  font-family: var(--font-display);
  font-size: 13px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 6px;
}

.section-text {
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
  margin-bottom: 4px;
}

.confidence-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  background: rgba(91, 155, 213, 0.06);
  border-radius: 14px 8px 12px 10px;
}

.confidence-label {
  font-size: 12px;
  color: var(--text-muted);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.bar-container {
  flex: 1;
  height: 8px;
  background: rgba(91, 155, 213, 0.15);
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: var(--gradient-primary);
  border-radius: 4px;
  transition: width 0.6s var(--easing-organic);
}

.confidence-value {
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 700;
  color: var(--color-primary);
}

.analysis-error,
.analysis-pending {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 32px;
  gap: 12px;
}

.error-icon,
.pending-icon {
  opacity: 0.5;
}

.error-text {
  color: var(--text-secondary);
  margin: 0;
}

.analysis-footer {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid rgba(91, 155, 213, 0.1);
}

.analysis-time {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--text-muted);
}

.model-used {
  font-size: 12px;
  color: var(--text-muted);
  background: rgba(91, 155, 213, 0.08);
  padding: 4px 10px;
  border-radius: 10px 6px 8px 4px;
}

.analysis-footer :deep(.org-button) {
  margin-left: auto;
}
</style>
