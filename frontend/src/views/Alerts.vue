<template>
  <div class="alerts-page">
    <div class="page-header">
      <div>
        <h1 class="page-title">告警管理</h1>
        <p class="page-subtitle">查看和管理所有系统告警</p>
      </div>
      <OrgButton @click="loadAlerts">
        <RefreshCw :size="16" />
        刷新
      </OrgButton>
    </div>

    <OrgCard class="filter-card">
      <div class="filter-row">
        <div class="filter-item">
          <span class="filter-label">状态：</span>
          <select v-model="statusFilter" class="org-select" @change="loadAlerts">
            <option value="">全部</option>
            <option value="firing">触发中</option>
            <option value="resolved">已解决</option>
          </select>
        </div>
      </div>
    </OrgCard>

    <OrgCard class="table-card">
      <div v-if="loading" class="loading-state">
        <div class="spinner" />
        <span>加载中...</span>
      </div>

      <div v-else-if="alerts.length === 0" class="empty-state">
        <div class="empty-icon">
          <Inbox :size="64" />
        </div>
        <p>暂无告警数据</p>
      </div>

      <div v-else class="table-container">
        <table class="org-table">
          <thead>
            <tr>
              <th>状态</th>
              <th>告警名称</th>
              <th>严重程度</th>
              <th>摘要</th>
              <th>开始时间</th>
              <th>推送次数</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="alert in alerts" :key="alert.id" class="table-row">
              <td>
                <Badge :type="getStatusBadgeType(alert.status)">
                  {{ getStatusText(alert.status) }}
                </Badge>
              </td>
              <td class="alert-name">
                <span class="name-text">{{ alert.alert_name }}</span>
                <span class="fingerprint">{{ alert.fingerprint.slice(0, 8) }}...</span>
              </td>
              <td>
                <span class="severity-dot" :class="`severity-${alert.severity || 'unknown'}`"></span>
                {{ alert.severity || 'unknown' }}
              </td>
              <td class="summary-cell">
                {{ alert.summary || alert.description || '-' }}
              </td>
              <td>{{ formatTime(alert.starts_at) }}</td>
              <td>{{ alert.update_count }}</td>
              <td>
                <div class="action-buttons">
                  <RouterLink :to="`/alerts/${alert.id}`" class="action-btn">
                    <Eye :size="14" />
                    查看
                  </RouterLink>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="!loading && total > 0" class="pagination">
        <button
          class="page-btn"
          :disabled="offset === 0"
          @click="changePage(-1)"
        >
          <ChevronLeft :size="16" />
        </button>
        <span class="page-info">{{ offset + 1 }} - {{ Math.min(offset + limit, total) }} / {{ total }}</span>
        <button
          class="page-btn"
          :disabled="offset + limit >= total"
          @click="changePage(1)"
        >
          <ChevronRight :size="16" />
        </button>
      </div>
    </OrgCard>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'
import { RefreshCw, Inbox, Eye, ChevronLeft, ChevronRight } from 'lucide-vue-next'
import OrgCard from '@/components/OrgCard.vue'
import OrgButton from '@/components/OrgButton.vue'
import Badge from '@/components/Badge.vue'
import { alertsApi } from '@/api'
import type { Alert } from '@/types'

const alerts = ref<Alert[]>([])
const loading = ref(true)
const statusFilter = ref('')
const total = ref(0)
const offset = ref(0)
const limit = ref(20)
const isUnmounted = ref(false)

const loadAlerts = async () => {
  loading.value = true
  try {
    const params: any = {
      limit: limit.value,
      offset: offset.value
    }
    if (statusFilter.value) {
      params.status = statusFilter.value
    }
    const res = await alertsApi.getAlerts(params)
    if (!isUnmounted.value) {
      alerts.value = res.items
      total.value = res.total
    }
  } catch (error) {
    if (!isUnmounted.value) {
      console.error('Failed to load alerts:', error)
      alerts.value = []
    }
  } finally {
    if (!isUnmounted.value) {
      loading.value = false
    }
  }
}

const changePage = (direction: number) => {
  offset.value = Math.max(0, offset.value + direction * limit.value)
  loadAlerts()
}

const getStatusText = (status: string) => {
  const map: Record<string, string> = {
    firing: '触发中',
    resolved: '已解决'
  }
  return map[status] || status
}

const getStatusBadgeType = (status: string): 'success' | 'warning' | 'error' | 'info' => {
  const map: Record<string, any> = {
    firing: 'error',
    resolved: 'success'
  }
  return map[status] || 'info'
}

const formatTime = (time: string) => {
  const date = new Date(time)
  return date.toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  loadAlerts()
})

onUnmounted(() => {
  isUnmounted.value = true
})
</script>

<style scoped>
.alerts-page {
  position: relative;
  z-index: 1;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
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

.filter-card {
  margin-bottom: 20px;
  padding: 16px 24px;
  animation: fadeSlideUp 0.6s var(--easing-organic) 0.1s both;
}

.filter-row {
  display: flex;
  align-items: center;
  gap: 24px;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-label {
  font-size: 14px;
  color: var(--text-secondary);
}

.org-select {
  background: rgba(155, 127, 232, 0.05);
  border: 1.5px solid rgba(155, 127, 232, 0.18);
  border-radius: 16px 10px 14px 8px;
  padding: 10px 16px;
  font-size: var(--text-sm);
  color: var(--text-primary);
  font-family: var(--font-body);
  cursor: pointer;
  transition: all var(--duration-hover) var(--easing-smooth);
  outline: none;
}

.org-select:focus {
  border-color: var(--color-primary);
  background: rgba(155, 127, 232, 0.08);
  box-shadow: 0 0 0 3px rgba(155, 127, 232, 0.12);
}

.table-card {
  padding: 0;
  animation: fadeSlideUp 0.6s var(--easing-organic) 0.2s both;
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
  border: 3px solid rgba(155, 127, 232, 0.2);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.empty-icon {
  opacity: 0.3;
}

.table-container {
  overflow-x: auto;
}

.org-table {
  width: 100%;
  border-collapse: collapse;
}

.org-table thead tr {
  background: linear-gradient(90deg, rgba(155, 127, 232, 0.08), rgba(126, 206, 196, 0.08));
}

.org-table thead th {
  padding: 14px 16px;
  text-align: left;
  font-size: var(--text-xs);
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-secondary);
  border-bottom: 1px solid rgba(155, 127, 232, 0.1);
  font-family: var(--font-display);
}

.table-row {
  transition: background var(--duration-hover) var(--easing-smooth);
  border-bottom: 1px solid rgba(155, 127, 232, 0.06);
}

.table-row:hover {
  background: rgba(155, 127, 232, 0.04);
}

.org-table tbody td {
  padding: 13px 16px;
  font-size: var(--text-sm);
  color: var(--text-primary);
}

.alert-name {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.name-text {
  font-weight: 500;
}

.fingerprint {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-muted);
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

.summary-cell {
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  font-size: 12px;
  color: var(--color-primary);
  text-decoration: none;
  background: rgba(155, 127, 232, 0.1);
  border-radius: 12px 6px 10px 8px;
  transition: all var(--duration-hover) var(--easing-organic);
}

.action-btn:hover {
  background: rgba(155, 127, 232, 0.2);
  transform: translateY(-1px);
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 16px 24px;
  border-top: 1px solid rgba(155, 127, 232, 0.1);
}

.page-btn {
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

.page-btn:hover:not(:disabled) {
  background: rgba(155, 127, 232, 0.2);
  color: var(--color-primary);
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-info {
  font-size: 13px;
  color: var(--text-secondary);
}
</style>
