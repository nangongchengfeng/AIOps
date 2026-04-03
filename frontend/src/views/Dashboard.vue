<template>
  <div class="dashboard">
    <div class="page-header">
      <div>
        <h1 class="page-title">仪表盘</h1>
        <p class="page-subtitle">实时监控系统运行状态</p>
      </div>
    </div>

    <div class="kpi-grid card-grid">
      <OrgCard class="kpi-card" :no-decoration="true">
        <div class="kpi-content">
          <div class="kpi-icon" style="background: linear-gradient(135deg, #9b7fe8, #c4aeef);">
            <AlertTriangle :size="28" />
          </div>
          <div class="kpi-main">
            <div class="kpi-value">{{ stats.totalAlerts }}</div>
            <div class="kpi-label">总告警数</div>
          </div>
        </div>
        <div class="kpi-decoration" aria-hidden="true" />
      </OrgCard>

      <OrgCard class="kpi-card" :no-decoration="true">
        <div class="kpi-content">
          <div class="kpi-icon" style="background: linear-gradient(135deg, #e8968c, #e8a4b8);">
            <AlertCircle :size="28" />
          </div>
          <div class="kpi-main">
            <div class="kpi-value">{{ stats.activeAlerts }}</div>
            <div class="kpi-label">活跃告警</div>
          </div>
        </div>
        <div class="kpi-decoration" aria-hidden="true" />
      </OrgCard>

      <OrgCard class="kpi-card" :no-decoration="true">
        <div class="kpi-content">
          <div class="kpi-icon" style="background: linear-gradient(135deg, #7ecec4, #a8cfe0);">
            <Sparkles :size="28" />
          </div>
          <div class="kpi-main">
            <div class="kpi-value">{{ stats.analysesCount }}</div>
            <div class="kpi-label">AI 分析</div>
          </div>
        </div>
        <div class="kpi-decoration" aria-hidden="true" />
      </OrgCard>

      <OrgCard class="kpi-card" :no-decoration="true">
        <div class="kpi-content">
          <div class="kpi-icon" style="background: linear-gradient(135deg, #8ecba8, #b8e0c8);">
            <CheckCircle :size="28" />
          </div>
          <div class="kpi-main">
            <div class="kpi-value">{{ stats.resolvedToday }}</div>
            <div class="kpi-label">今日解决</div>
          </div>
        </div>
        <div class="kpi-decoration" aria-hidden="true" />
      </OrgCard>
    </div>

    <div class="content-grid" style="margin-top: 24px;">
      <OrgCard class="chart-card">
        <div class="card-header">
          <h3 class="card-title">告警趋势</h3>
        </div>
        <div ref="trendChartRef" class="chart-container" />
      </OrgCard>

      <OrgCard class="list-card">
        <div class="card-header">
          <h3 class="card-title">最新分析</h3>
          <RouterLink to="/analyses" class="view-more">查看全部</RouterLink>
        </div>
        <div class="analyses-list">
          <div v-if="loading" class="loading-state">
            <div class="spinner" />
            <span>加载中...</span>
          </div>
          <div v-else-if="latestAnalyses.length === 0" class="empty-state">
            <div class="empty-icon">
              <Inbox :size="48" />
            </div>
            <p>暂无分析记录</p>
          </div>
          <RouterLink
            v-for="analysis in latestAnalyses"
            :key="analysis.id"
            :to="`/alerts/${analysis.alert_id}`"
            class="analysis-item"
          >
            <div class="analysis-status" :class="`status-${analysis.status}`" />
            <div class="analysis-info">
              <div class="analysis-alert-id">告警 #{{ analysis.alert_id }}</div>
              <div class="analysis-time">{{ formatTime(analysis.created_at) }}</div>
            </div>
            <Badge :type="getAnalysisBadgeType(analysis.status)">
              {{ getAnalysisStatusText(analysis.status) }}
            </Badge>
          </RouterLink>
        </div>
      </OrgCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { RouterLink } from 'vue-router'
import * as echarts from 'echarts'
import { AlertTriangle, AlertCircle, Sparkles, CheckCircle, Inbox } from 'lucide-vue-next'
import OrgCard from '@/components/OrgCard.vue'
import Badge from '@/components/Badge.vue'
import { alertsApi } from '@/api'
import type { Analysis } from '@/types'

const stats = ref({
  totalAlerts: 0,
  activeAlerts: 0,
  analysesCount: 0,
  resolvedToday: 0
})

const latestAnalyses = ref<Analysis[]>([])
const loading = ref(true)
const trendChartRef = ref<HTMLElement>()
let trendChart: echarts.ECharts | null = null
const isUnmounted = ref(false)

const loadData = async () => {
  loading.value = true
  try {
    const [alertsRes, analysesRes] = await Promise.all([
      alertsApi.getAlerts({ limit: 100 }),
      alertsApi.getLatestAnalyses(5)
    ])

    if (!isUnmounted.value) {
      stats.value.totalAlerts = alertsRes.total
      stats.value.activeAlerts = alertsRes.items.filter(a => a.status === 'firing').length
      stats.value.analysesCount = analysesRes.length
      stats.value.resolvedToday = alertsRes.items.filter(a => a.status === 'resolved').length

      latestAnalyses.value = analysesRes
    }
  } catch (error) {
    if (!isUnmounted.value) {
      console.error('Failed to load dashboard data:', error)
      latestAnalyses.value = []
    }
  } finally {
    if (!isUnmounted.value) {
      loading.value = false
    }
  }
}

const initChart = () => {
  if (!trendChartRef.value) return

  try {
    trendChart = echarts.init(trendChartRef.value)

    const option = {
      tooltip: {
        trigger: 'axis',
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        borderColor: 'rgba(155, 127, 232, 0.2)',
        borderWidth: 1,
        textStyle: {
          color: '#2d2640',
          fontFamily: 'DM Sans'
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        top: '10%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
        axisLine: { lineStyle: { color: 'rgba(155, 127, 232, 0.2)' } },
        axisLabel: { color: '#6b5f80', fontFamily: 'DM Sans' }
      },
      yAxis: {
        type: 'value',
        axisLine: { show: false },
        splitLine: { lineStyle: { color: 'rgba(155, 127, 232, 0.1)' } },
        axisLabel: { color: '#6b5f80', fontFamily: 'DM Sans' }
      },
      series: [
        {
          name: '告警数',
          type: 'line',
          smooth: true,
          symbol: 'circle',
          symbolSize: 8,
          lineStyle: {
            width: 3,
            color: {
              type: 'linear',
              x: 0, y: 0, x2: 1, y2: 0,
              colorStops: [
                { offset: 0, color: '#9b7fe8' },
                { offset: 1, color: '#e8a4b8' }
              ]
            }
          },
          itemStyle: {
            color: '#9b7fe8',
            borderColor: '#fff',
            borderWidth: 2
          },
          areaStyle: {
            color: {
              type: 'linear',
              x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: 'rgba(155, 127, 232, 0.3)' },
                { offset: 1, color: 'rgba(155, 127, 232, 0.05)' }
              ]
            }
          },
          data: [12, 19, 15, 25, 22, 18, 14]
        }
      ]
    }

    trendChart.setOption(option)
  } catch (e) {
    console.error('Failed to init chart:', e)
  }
}

const formatTime = (time: string) => {
  const date = new Date(time)
  return date.toLocaleString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getAnalysisStatusText = (status: string) => {
  const map: Record<string, string> = {
    pending: '分析中',
    completed: '已完成',
    failed: '失败'
  }
  return map[status] || status
}

const getAnalysisBadgeType = (status: string): 'success' | 'warning' | 'error' | 'info' => {
  const map: Record<string, any> = {
    pending: 'warning',
    completed: 'success',
    failed: 'error'
  }
  return map[status] || 'info'
}

const handleResize = () => {
  trendChart?.resize()
}

onMounted(() => {
  loadData()
  nextTick(() => {
    setTimeout(initChart, 200)
  })
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  isUnmounted.value = true
  window.removeEventListener('resize', handleResize)
  if (trendChart) {
    try {
      trendChart.dispose()
    } catch (e) {
      console.error('Failed to dispose chart:', e)
    }
    trendChart = null
  }
})
</script>

<style scoped>
.dashboard {
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

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.kpi-card {
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.kpi-content {
  display: flex;
  align-items: center;
  gap: 16px;
  position: relative;
  z-index: 2;
}

.kpi-icon {
  width: 56px;
  height: 56px;
  border-radius: 16px 10px 14px 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.kpi-main {
  flex: 1;
}

.kpi-value {
  font-family: var(--font-display);
  font-size: 32px;
  font-weight: 800;
  color: var(--text-primary);
  line-height: 1.2;
}

.kpi-label {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 2px;
}

.kpi-decoration {
  position: absolute;
  width: 140px;
  height: 140px;
  bottom: -50px;
  right: -40px;
  background: var(--gradient-primary);
  opacity: 0.08;
  border-radius: var(--radius-blob);
  animation: morphBlob 10s ease-in-out infinite alternate;
}

.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
}

.chart-card,
.list-card {
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.card-title {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.view-more {
  font-size: 13px;
  color: var(--color-primary);
  text-decoration: none;
  transition: color var(--duration-hover) var(--easing-smooth);
}

.view-more:hover {
  color: var(--color-primary-dark);
}

.chart-container {
  height: 280px;
}

.analyses-list {
  padding: 4px 0;
}

.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 24px;
  gap: 12px;
  color: var(--text-muted);
}

.spinner {
  width: 24px;
  height: 24px;
  border: 3px solid rgba(155, 127, 232, 0.2);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.empty-icon {
  opacity: 0.4;
}

.analysis-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 0;
  text-decoration: none;
  transition: background var(--duration-hover) var(--easing-smooth);
  border-bottom: 1px solid rgba(155, 127, 232, 0.06);
}

.analysis-item:last-child {
  border-bottom: none;
}

.analysis-item:hover {
  background: rgba(155, 127, 232, 0.04);
  margin: 0 -12px;
  padding: 14px 12px;
  border-radius: 12px;
}

.analysis-status {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-info);
}

.analysis-status.status-pending {
  background: var(--color-warning);
  animation: pulseSoft 2s ease-in-out infinite;
}

.analysis-status.status-completed {
  background: var(--color-success);
}

.analysis-status.status-failed {
  background: var(--color-error);
}

.analysis-info {
  flex: 1;
}

.analysis-alert-id {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.analysis-time {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 2px;
}
</style>
