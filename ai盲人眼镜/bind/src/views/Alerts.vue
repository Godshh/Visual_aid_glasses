<template>
  <div class="alerts-page">
    <!-- 页头 -->
    <div class="alerts-header">
      <div class="header-left">
        <h1 class="page-title">告警中心</h1>
        <div class="summary-chips">
          <div class="chip critical">
            <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.6"/><path d="M12 7v6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="12" cy="16.5" r="0.9" fill="currentColor"/></svg>
            <span class="chip-num">{{ criticalCount }}</span>
            <span class="chip-label">严重</span>
          </div>
          <div class="chip warning">
            <svg viewBox="0 0 24 24" fill="none"><path d="M12 2L3 20h18L12 2z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M12 9v5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="12" cy="17" r="0.8" fill="currentColor"/></svg>
            <span class="chip-num">{{ warningCount }}</span>
            <span class="chip-label">警告</span>
          </div>
          <div class="chip info">
            <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.6"/><path d="M12 11v6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="12" cy="8" r="0.9" fill="currentColor"/></svg>
            <span class="chip-num">{{ infoCount }}</span>
            <span class="chip-label">提示</span>
          </div>
        </div>
      </div>
      <div class="header-right">
        <select class="filter-sel" v-model="filterSeverity">
          <option value="all">全部级别</option>
          <option value="critical">严重</option>
          <option value="warning">警告</option>
          <option value="info">提示</option>
        </select>
        <select class="filter-sel" v-model="filterStatus">
          <option value="all">全部状态</option>
          <option value="unread">未读</option>
          <option value="read">已读</option>
        </select>
        <button class="hdr-btn" @click="markAllRead">
          <svg viewBox="0 0 24 24" fill="none"><path d="M20 6L9 17l-5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          全部标记已读
        </button>
      </div>
    </div>

    <!-- 主体 -->
    <div class="alerts-body">
      <!-- 左：告警列表 -->
      <div class="alerts-list">
        <div
          v-for="item in filteredAlerts"
          :key="item.id"
          class="alert-card"
          :class="[item.severity, { unread: !item.read }]"
          @click="openDetail(item)"
        >
          <div class="card-left">
            <div class="alert-icon-wrap" :class="item.severity">
              <svg v-if="item.type === 'fall'" viewBox="0 0 24 24" fill="none"><path d="M12 2a4 4 0 100 8 4 4 0 000-8zM3 20c0-4 4-7 9-7s9 3 9 7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><path d="M16 14l3 3-3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
              <svg v-else-if="item.type === 'low_battery'" viewBox="0 0 24 24" fill="none"><rect x="2" y="7" width="16" height="10" rx="2" stroke="currentColor" stroke-width="1.5"/><path d="M20 10v4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M8 12h4M10 10v4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
              <svg v-else-if="item.type === 'geofence'" viewBox="0 0 24 24" fill="none"><rect x="3" y="11" width="18" height="11" rx="2" stroke="currentColor" stroke-width="1.6"/><path d="M7 11V7a5 5 0 0110 0v4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
              <svg v-else-if="item.type === 'no_response'" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.6"/><path d="M12 7v5l3 3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
              <svg v-else-if="item.type === 'obstacle'" viewBox="0 0 24 24" fill="none"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M12 9v5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="12" cy="17" r="0.8" fill="currentColor"/></svg>
              <svg v-else viewBox="0 0 24 24" fill="none"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" stroke="currentColor" stroke-width="1.6"/><path d="M12 9v5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="12" cy="17" r="0.8" fill="currentColor"/></svg>
            </div>
            <div class="alert-info">
              <div class="alert-title">{{ item.title }}</div>
              <div class="alert-desc">{{ item.description }}</div>
              <div class="alert-meta">
                <span class="meta-time">{{ getRelativeTime(item.time) }}</span>
                <span class="meta-dot">·</span>
                <span class="meta-device">{{ item.device }}</span>
              </div>
            </div>
          </div>
          <div class="card-right">
            <span class="severity-badge" :class="item.severity">{{ getSeverityLabel(item.severity) }}</span>
            <span class="read-badge" :class="{ read: item.read }">{{ item.read ? '已读' : '未读' }}</span>
            <div class="card-actions">
              <button class="card-action-btn confirm" @click.stop="doConfirm(item)" title="确认">
                <svg viewBox="0 0 24 24" fill="none"><path d="M20 6L9 17l-5-5" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              </button>
              <button class="card-action-btn ignore" @click.stop="doIgnore(item)" title="忽略">
                <svg viewBox="0 0 24 24" fill="none"><path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
              </button>
              <button class="card-action-btn detail" @click.stop="openDetail(item)" title="详情">
                <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.6"/><path d="M12 11v6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="12" cy="8" r="0.9" fill="currentColor"/></svg>
              </button>
            </div>
          </div>
        </div>

        <div v-if="filteredAlerts.length === 0" class="empty-state">
          <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="#cbd5e1" stroke-width="1.5"/><path d="M20 6L9 17l-5-5" stroke="#cbd5e1" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <span>暂无符合条件的告警</span>
        </div>
      </div>

      <!-- 右：面板 -->
      <div class="right-panel">
        <!-- 统计卡片 -->
        <div class="panel-card">
          <div class="card-head">
            <svg viewBox="0 0 24 24" fill="none"><rect x="3" y="3" width="7" height="9" rx="1.5" stroke="currentColor" stroke-width="1.6"/><rect x="14" y="3" width="7" height="5" rx="1.5" stroke="currentColor" stroke-width="1.6"/><rect x="14" y="12" width="7" height="9" rx="1.5" stroke="currentColor" stroke-width="1.6"/><rect x="3" y="16" width="7" height="5" rx="1.5" stroke="currentColor" stroke-width="1.6"/></svg>
            告警统计
          </div>
          <div class="stat-row">
            <div class="stat-block critical">
              <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.6"/><path d="M12 7v6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="12" cy="16.5" r="0.9" fill="currentColor"/></svg>
              <span class="stat-n">{{ criticalCount }}</span>
              <span class="stat-l">严重</span>
            </div>
            <div class="stat-block warning">
              <svg viewBox="0 0 24 24" fill="none"><path d="M12 2L3 20h18L12 2z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M12 9v5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="12" cy="17" r="0.8" fill="currentColor"/></svg>
              <span class="stat-n">{{ warningCount }}</span>
              <span class="stat-l">警告</span>
            </div>
            <div class="stat-block info">
              <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.6"/><path d="M12 11v6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="12" cy="8" r="0.9" fill="currentColor"/></svg>
              <span class="stat-n">{{ infoCount }}</span>
              <span class="stat-l">提示</span>
            </div>
          </div>
        </div>

        <!-- 快速操作 -->
        <div class="panel-card">
          <div class="card-head">
            <svg viewBox="0 0 24 24" fill="none"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>
            快速操作
          </div>
          <div class="quick-ops">
            <button class="quick-op-btn" @click="handleAllCritical">
              <div class="qop-icon critical-bg">
                <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.6"/><path d="M12 7v6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="12" cy="16.5" r="0.9" fill="currentColor"/></svg>
              </div>
              <span>处理所有严重告警</span>
              <svg class="arrow" viewBox="0 0 24 24" fill="none"><path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </button>
            <button class="quick-op-btn" @click="exportAlerts">
              <div class="qop-icon export-bg">
                <svg viewBox="0 0 24 24" fill="none"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
              </div>
              <span>导出告警记录</span>
              <svg class="arrow" viewBox="0 0 24 24" fill="none"><path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </button>
            <button class="quick-op-btn" @click="refreshAlerts">
              <div class="qop-icon refresh-bg">
                <svg viewBox="0 0 24 24" fill="none"><path d="M23 4v6h-6M1 20v-6h6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
              </div>
              <span>刷新告警列表</span>
              <svg class="arrow" viewBox="0 0 24 24" fill="none"><path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </button>
          </div>
        </div>

        <!-- 常用联系人 -->
        <div class="panel-card">
          <div class="card-head">
            <svg viewBox="0 0 24 24" fill="none"><circle cx="9" cy="8" r="3" stroke="currentColor" stroke-width="1.5"/><circle cx="17" cy="9" r="2.5" stroke="currentColor" stroke-width="1.5"/><path d="M3 20c0-3.314 2.686-6 6-6s6 2.686 6 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><path d="M17 14c1.657 0 3 1.343 3 3v1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
            常用联系人
          </div>
          <div class="contacts">
            <div
              v-for="contact in contacts"
              :key="contact.id"
              class="contact-row"
            >
              <div class="contact-avatar">
                <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="8" r="4" stroke="currentColor" stroke-width="1.6"/><path d="M4 20c0-4 3.582-7 8-7s8 3 8 7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
              </div>
              <div class="contact-info">
                <span class="contact-name">{{ contact.name }}</span>
                <span class="contact-phone">{{ contact.phone }}</span>
              </div>
              <button class="call-btn" @click="callContact(contact)">
                <svg viewBox="0 0 24 24" fill="none"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.63 10.8a19.79 19.79 0 01-3.07-8.67A2 2 0 012.52 0h3a2 2 0 012 1.72c.13 1 .36 1.97.71 2.9a2 2 0 01-.45 2.11L6.91 7.91a16 16 0 006.18 6.18l1.18-.87a2 2 0 012.11-.45c.93.35 1.9.58 2.9.71A2 2 0 0122 16.92z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 详情弹窗 -->
    <div class="modal-wrap" v-if="showDetailModal" @click.self="showDetailModal = false">
      <div class="modal-box">
        <div class="modal-head" :class="selectedItem?.severity">
          <div class="modal-head-left">
            <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.6"/><path d="M12 11v6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="12" cy="8" r="0.9" fill="currentColor"/></svg>
            告警详情
          </div>
          <button class="close-btn" @click="showDetailModal = false">
            <svg viewBox="0 0 24 24" fill="none"><path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
          </button>
        </div>
        <div class="modal-body" v-if="selectedItem">
          <div class="detail-grid">
            <div class="detail-item">
              <span class="detail-label">告警类型</span>
              <span class="detail-val">{{ selectedItem.title }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">严重程度</span>
              <span class="detail-val severity-txt" :class="selectedItem.severity">{{ getSeverityLabel(selectedItem.severity) }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">发生时间</span>
              <span class="detail-val">{{ formatTime(selectedItem.time) }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">设备名称</span>
              <span class="detail-val">{{ selectedItem.device }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">经度</span>
              <span class="detail-val">{{ selectedItem.location.lng }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">纬度</span>
              <span class="detail-val">{{ selectedItem.location.lat }}</span>
            </div>
            <div class="detail-item full">
              <span class="detail-label">详细地址</span>
              <span class="detail-val">{{ selectedItem.address }}</span>
            </div>
            <div class="detail-item full">
              <span class="detail-label">告警描述</span>
              <span class="detail-val">{{ selectedItem.description }}</span>
            </div>
          </div>

          <div class="push-section" v-if="selectedItem.pushRecords?.length">
            <div class="push-title">推送记录</div>
            <div class="push-list">
              <div v-for="(rec, i) in selectedItem.pushRecords" :key="i" class="push-row">
                <span class="push-time">{{ formatTime(rec.time) }}</span>
                <span class="push-target">{{ rec.target }}</span>
                <span class="push-status" :class="rec.status">{{ rec.status === 'success' ? '成功' : '失败' }}</span>
              </div>
            </div>
          </div>

          <div class="modal-actions">
            <button class="modal-btn primary" @click="markHandled(selectedItem)">
              <svg viewBox="0 0 24 24" fill="none"><path d="M20 6L9 17l-5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              标记为已处理
            </button>
            <button class="modal-btn secondary" @click="gotoLocation(selectedItem)">
              <svg viewBox="0 0 24 24" fill="none"><path d="M12 22s-8-6.686-8-12a8 8 0 0116 0c0 5.314-8 12-8 12z" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="10" r="2.5" stroke="currentColor" stroke-width="1.5"/></svg>
              查看位置
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const filterSeverity = ref('all')
const filterStatus = ref('all')
const showDetailModal = ref(false)
const selectedItem = ref(null)

const alertItems = ref([
  {
    id: 1,
    type: 'fall',
    title: '跌倒预警',
    description: '检测到用户可能跌倒，请立即确认安全状况',
    severity: 'critical',
    read: false,
    time: Date.now() - 5 * 60 * 1000,
    device: '智能盲人眼镜 #001',
    location: { lng: 116.4074, lat: 39.9042 },
    address: '北京市朝阳区建国路88号',
    pushRecords: [
      { time: Date.now() - 5 * 60 * 1000, target: '家属手机', status: 'success' },
      { time: Date.now() - 5 * 60 * 1000 + 5000, target: '紧急联系人', status: 'success' }
    ]
  },
  {
    id: 2,
    type: 'low_battery',
    title: '电量过低',
    description: '设备电量低于 20%，请及时充电',
    severity: 'warning',
    read: false,
    time: Date.now() - 30 * 60 * 1000,
    device: '智能盲人眼镜 #001',
    location: { lng: 116.4074, lat: 39.9042 },
    address: '北京市朝阳区建国路88号',
    pushRecords: [
      { time: Date.now() - 30 * 60 * 1000, target: '家属手机', status: 'success' }
    ]
  },
  {
    id: 3,
    type: 'geofence',
    title: '偏离电子围栏',
    description: '用户已离开设定的安全区域',
    severity: 'warning',
    read: true,
    time: Date.now() - 2 * 60 * 60 * 1000,
    device: '智能盲人眼镜 #001',
    location: { lng: 116.4074, lat: 39.9042 },
    address: '北京市朝阳区建国路88号',
    pushRecords: [
      { time: Date.now() - 2 * 60 * 60 * 1000, target: '家属手机', status: 'success' }
    ]
  },
  {
    id: 4,
    type: 'no_response',
    title: '长时间无响应',
    description: '用户超过 30 分钟无任何操作或语音交互',
    severity: 'critical',
    read: false,
    time: Date.now() - 60 * 60 * 1000,
    device: '智能盲人眼镜 #001',
    location: { lng: 116.4074, lat: 39.9042 },
    address: '北京市朝阳区建国路88号',
    pushRecords: [
      { time: Date.now() - 60 * 60 * 1000, target: '家属手机', status: 'success' },
      { time: Date.now() - 60 * 60 * 1000 + 5000, target: '紧急联系人', status: 'success' }
    ]
  },
  {
    id: 5,
    type: 'deviation',
    title: '偏离盲道',
    description: '用户偏离盲道约 2 米，已发出语音提醒',
    severity: 'info',
    read: true,
    time: Date.now() - 3 * 60 * 60 * 1000,
    device: '智能盲人眼镜 #001',
    location: { lng: 116.4074, lat: 39.9042 },
    address: '北京市朝阳区建国路88号',
    pushRecords: []
  },
  {
    id: 6,
    type: 'obstacle',
    title: '障碍物检测',
    description: '前方 5 米检测到障碍物，已发出语音提醒',
    severity: 'info',
    read: true,
    time: Date.now() - 10 * 60 * 1000,
    device: '智能盲人眼镜 #001',
    location: { lng: 116.4074, lat: 39.9042 },
    address: '北京市朝阳区建国路88号',
    pushRecords: []
  }
])

const contacts = ref([
  { id: 1, name: '张三（家属）', phone: '138****1234' },
  { id: 2, name: '李四（监护人）', phone: '139****5678' },
  { id: 3, name: '王五（紧急联系人）', phone: '137****9012' }
])

// ── 计算属性 ──────────────────────────────────────
const criticalCount = computed(() => alertItems.value.filter(a => a.severity === 'critical' && !a.read).length)
const warningCount  = computed(() => alertItems.value.filter(a => a.severity === 'warning'  && !a.read).length)
const infoCount     = computed(() => alertItems.value.filter(a => a.severity === 'info'     && !a.read).length)

const filteredAlerts = computed(() => {
  return alertItems.value.filter(item => {
    const sv = filterSeverity.value === 'all' || item.severity === filterSeverity.value
    const st = filterStatus.value === 'all' ||
      (filterStatus.value === 'unread' && !item.read) ||
      (filterStatus.value === 'read'   &&  item.read)
    return sv && st
  })
})

// ── 工具函数 ──────────────────────────────────────
const getSeverityLabel = (s) => ({ critical: '严重', warning: '警告', info: '提示' }[s] || '未知')

const formatTime = (ts) => {
  return new Date(ts).toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

const getRelativeTime = (ts) => {
  const diff = Date.now() - ts
  const m = Math.floor(diff / 60000)
  const h = Math.floor(m / 60)
  const d = Math.floor(h / 24)
  if (d > 0) return `${d}天前`
  if (h > 0) return `${h}小时前`
  if (m > 0) return `${m}分钟前`
  return '刚刚'
}

// ── 操作 ──────────────────────────────────────────
const openDetail = (item) => {
  selectedItem.value = item
  item.read = true
  showDetailModal.value = true
}

const doConfirm = (item) => {
  item.read = true
}

const doIgnore = (item) => {
  item.read = true
}

const markAllRead = () => {
  alertItems.value.forEach(item => { item.read = true })
}

const handleAllCritical = () => {
  const list = alertItems.value.filter(a => a.severity === 'critical' && !a.read)
  list.forEach(a => { a.read = true })
  window.alert(`已处理 ${list.length} 个严重告警`)
}

const exportAlerts = () => {
  window.alert('导出告警记录')
}

const refreshAlerts = () => {
  window.alert('刷新告警列表')
}

const markHandled = (item) => {
  item.read = true
  showDetailModal.value = false
}

const gotoLocation = (item) => {
  window.alert(`跳转到地图位置：${item.address}`)
}

const callContact = (contact) => {
  window.alert(`拨打联系人：${contact.name} (${contact.phone})`)
}
</script>

<style scoped>
/* ── 整体 ── */
.alerts-page {
  padding: 20px 20px 16px 24px;
  background: #f1f5f9;
  min-height: calc(100vh - 52px);
  display: flex;
  flex-direction: column;
  gap: 14px;
}

/* ── 页头 ── */
.alerts-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.page-title {
  font-size: 22px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.summary-chips {
  display: flex;
  gap: 8px;
}

.chip {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  border: 1px solid;
}

.chip svg { width: 13px; height: 13px; }

.chip.critical { background: #fef2f2; border-color: #fca5a5; color: #dc2626; }
.chip.warning  { background: #fffbeb; border-color: #fcd34d; color: #d97706; }
.chip.info     { background: #eff6ff; border-color: #93c5fd; color: #2563eb; }

.chip-num { font-size: 14px; font-weight: 700; }
.chip-label { color: #64748b; font-weight: 500; }

.header-right {
  display: flex;
  gap: 8px;
  align-items: center;
}

.filter-sel {
  padding: 7px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 13px;
  color: #334155;
  background: #fff;
  cursor: pointer;
  outline: none;
}

.hdr-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  background: #3b82f6;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.hdr-btn svg { width: 15px; height: 15px; }
.hdr-btn:hover { background: #2563eb; box-shadow: 0 3px 10px rgba(59,130,246,0.35); }

/* ── 主体两列 ── */
.alerts-body {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 14px;
  flex: 1;
  min-height: 0;
}

/* ── 告警列表 ── */
.alerts-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow-y: auto;
}

.alerts-list::-webkit-scrollbar { width: 4px; }
.alerts-list::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 2px; }

.alert-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 18px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  border-left: 4px solid transparent;
  cursor: pointer;
  transition: box-shadow 0.2s ease, transform 0.15s ease;
}

.alert-card:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  transform: translateY(-1px);
}

.alert-card.unread { background: #fefce8; }
.alert-card.critical { border-left-color: #ef4444; }
.alert-card.warning  { border-left-color: #f59e0b; }
.alert-card.info     { border-left-color: #3b82f6; }

.card-left {
  display: flex;
  align-items: center;
  gap: 14px;
  flex: 1;
  min-width: 0;
}

.alert-icon-wrap {
  width: 42px;
  height: 42px;
  border-radius: 11px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.alert-icon-wrap svg { width: 20px; height: 20px; }
.alert-icon-wrap.critical { background: #fee2e2; color: #dc2626; }
.alert-icon-wrap.warning  { background: #fef3c7; color: #d97706; }
.alert-icon-wrap.info     { background: #dbeafe; color: #2563eb; }

.alert-info { flex: 1; min-width: 0; }

.alert-title {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 3px;
}

.alert-desc {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.alert-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
}

.meta-time { color: #3b82f6; font-weight: 600; }
.meta-dot  { color: #cbd5e1; }
.meta-device { color: #94a3b8; }

.card-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 6px;
  flex-shrink: 0;
}

.severity-badge {
  padding: 3px 10px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 700;
}

.severity-badge.critical { background: #fee2e2; color: #991b1b; }
.severity-badge.warning  { background: #fef3c7; color: #92400e; }
.severity-badge.info     { background: #dbeafe; color: #1e40af; }

.read-badge {
  font-size: 11px;
  color: #f59e0b;
  font-weight: 600;
}
.read-badge.read { color: #94a3b8; }

.card-actions {
  display: flex;
  gap: 6px;
}

.card-action-btn {
  width: 30px;
  height: 30px;
  border-radius: 7px;
  border: 1px solid;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.card-action-btn svg { width: 14px; height: 14px; }

.card-action-btn.confirm {
  background: #dcfce7;
  border-color: #86efac;
  color: #16a34a;
}
.card-action-btn.confirm:hover { background: #16a34a; color: #fff; border-color: #16a34a; }

.card-action-btn.ignore {
  background: #fff;
  border-color: #fca5a5;
  color: #ef4444;
}
.card-action-btn.ignore:hover { background: #fee2e2; }

.card-action-btn.detail {
  background: #dbeafe;
  border-color: #93c5fd;
  color: #2563eb;
}
.card-action-btn.detail:hover { background: #2563eb; color: #fff; border-color: #2563eb; }

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 48px 24px;
  color: #94a3b8;
  font-size: 14px;
}
.empty-state svg { width: 48px; height: 48px; }

/* ── 右侧面板 ── */
.right-panel {
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow-y: auto;
}

.right-panel::-webkit-scrollbar { width: 3px; }
.right-panel::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 2px; }

.panel-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  overflow: hidden;
}

.card-head {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  font-size: 13.5px;
  font-weight: 600;
  color: #1e293b;
  border-bottom: 1px solid #f1f5f9;
}

.card-head svg { width: 15px; height: 15px; color: #64748b; }

/* ── 统计行 ── */
.stat-row {
  display: flex;
  padding: 14px 12px;
  gap: 8px;
}

.stat-block {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 12px 8px;
  border-radius: 10px;
}

.stat-block svg { width: 20px; height: 20px; }

.stat-block.critical { background: #fef2f2; color: #dc2626; }
.stat-block.warning  { background: #fffbeb; color: #d97706; }
.stat-block.info     { background: #eff6ff; color: #2563eb; }

.stat-n { font-size: 22px; font-weight: 700; }
.stat-l { font-size: 11px; color: #94a3b8; }

/* ── 快速操作 ── */
.quick-ops {
  padding: 10px 12px 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.quick-op-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 9px;
  cursor: pointer;
  font-size: 13px;
  color: #334155;
  font-weight: 500;
  text-align: left;
  transition: all 0.2s ease;
}

.quick-op-btn:hover {
  background: #f0f9ff;
  border-color: #bae6fd;
  transform: translateX(3px);
}

.qop-icon {
  width: 30px;
  height: 30px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.qop-icon svg { width: 16px; height: 16px; }
.critical-bg { background: #fee2e2; color: #dc2626; }
.export-bg   { background: #dbeafe; color: #2563eb; }
.refresh-bg  { background: #dcfce7; color: #16a34a; }

.quick-op-btn span { flex: 1; }

.arrow { width: 14px; height: 14px; color: #94a3b8; flex-shrink: 0; }

/* ── 联系人 ── */
.contacts { padding: 10px 12px 12px; display: flex; flex-direction: column; gap: 8px; }

.contact-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  background: #f8fafc;
  border-radius: 9px;
  transition: background 0.2s ease;
}
.contact-row:hover { background: #eff6ff; }

.contact-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #dbeafe;
  color: #2563eb;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.contact-avatar svg { width: 17px; height: 17px; }

.contact-info { flex: 1; display: flex; flex-direction: column; gap: 1px; min-width: 0; }
.contact-name { font-size: 13px; font-weight: 600; color: #1e293b; }
.contact-phone { font-size: 11px; color: #94a3b8; }

.call-btn {
  width: 30px;
  height: 30px;
  border: 1px solid #bae6fd;
  border-radius: 8px;
  background: #f0f9ff;
  color: #0369a1;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.2s ease;
}
.call-btn svg { width: 14px; height: 14px; }
.call-btn:hover { background: #0ea5e9; color: #fff; border-color: #0ea5e9; }

/* ── 弹窗 ── */
.modal-wrap {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.45);
  backdrop-filter: blur(3px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-box {
  width: 580px;
  max-height: 80vh;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.18);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  animation: modal-in 0.25s ease;
}

@keyframes modal-in {
  from { opacity: 0; transform: scale(0.93) translateY(16px); }
  to   { opacity: 1; transform: scale(1)    translateY(0); }
}

.modal-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  border-bottom: 1px solid #f1f5f9;
}

.modal-head-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.modal-head-left svg { width: 18px; height: 18px; color: #3b82f6; }

.modal-head.critical { background: #fff5f5; }
.modal-head.warning  { background: #fffbeb; }
.modal-head.info     { background: #f0f9ff; }

.close-btn {
  width: 30px;
  height: 30px;
  border: none;
  border-radius: 7px;
  background: #f1f5f9;
  cursor: pointer;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}
.close-btn svg { width: 14px; height: 14px; }
.close-btn:hover { background: #e2e8f0; }

.modal-body {
  overflow-y: auto;
  padding: 20px;
  flex: 1;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 20px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 3px;
  padding: 10px 12px;
  background: #f8fafc;
  border-radius: 8px;
}

.detail-item.full { grid-column: 1 / -1; }

.detail-label { font-size: 11px; color: #94a3b8; }
.detail-val { font-size: 13px; font-weight: 500; color: #1e293b; }

.severity-txt.critical { color: #dc2626; }
.severity-txt.warning  { color: #d97706; }
.severity-txt.info     { color: #2563eb; }

.push-section { margin-bottom: 20px; }

.push-title {
  font-size: 13px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 8px;
}

.push-list { display: flex; flex-direction: column; gap: 6px; }

.push-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  background: #f8fafc;
  border-radius: 7px;
  font-size: 12px;
}

.push-time { color: #94a3b8; font-family: monospace; min-width: 130px; }
.push-target { flex: 1; color: #334155; font-weight: 500; }

.push-status {
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 600;
}
.push-status.success { background: #dcfce7; color: #166534; }
.push-status.failed  { background: #fee2e2; color: #991b1b; }

.modal-actions {
  display: flex;
  gap: 10px;
  padding-top: 16px;
  border-top: 1px solid #f1f5f9;
}

.modal-btn {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 9px 18px;
  border: none;
  border-radius: 9px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.modal-btn svg { width: 15px; height: 15px; }

.modal-btn.primary { background: #22c55e; color: #fff; }
.modal-btn.primary:hover { background: #16a34a; box-shadow: 0 3px 10px rgba(34,197,94,0.35); }

.modal-btn.secondary { background: #f0f9ff; color: #0369a1; border: 1px solid #bae6fd; }
.modal-btn.secondary:hover { background: #e0f2fe; }
</style>
