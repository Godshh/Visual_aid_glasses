<template>
  <header class="top-nav">
    <div class="nav-left">
      <router-link to="/" class="home-link">
        <svg viewBox="0 0 24 24" fill="none" class="home-icon"><path d="M3 9.5L12 3l9 6.5V20a1 1 0 01-1 1H4a1 1 0 01-1-1V9.5z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M9 21V12h6v9" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>
        <span class="home-text">返回主页</span>
      </router-link>
      <div class="page-title">{{ currentPageTitle }}</div>
    </div>
    <div class="nav-right">
      <div class="user-info">
        <div class="user-avatar-wrap">
          <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="8" r="4" stroke="currentColor" stroke-width="1.6"/><path d="M4 20c0-4 3.582-7 8-7s8 3 8 7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
        </div>
        <span class="user-name">管理员</span>
      </div>
      <button class="notification-btn" @click="showNotifications">
        <svg viewBox="0 0 24 24" fill="none"><path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M13.73 21a2 2 0 01-3.46 0" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
        <span class="notification-badge" v-if="unreadCount > 0">{{ unreadCount }}</span>
      </button>
    </div>
  </header>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const pageTitleMap = {
  '/dashboard': '实时监控仪表盘',
  '/history': '历史轨迹回放',
  '/alerts': '告警中心',
  '/devices': '设备管理',
  '/logs': '语音交互日志'
}

const currentPageTitle = computed(() => {
  return pageTitleMap[route.path] || '管理后台'
})

const unreadCount = ref(3)

const showNotifications = () => {
  alert('查看通知')
}
</script>

<style scoped>
.top-nav {
  height: 52px;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.07);
  box-shadow: 0 1px 16px rgba(0, 0, 0, 0.06);
  position: fixed;
  top: 0;
  left: 64px;
  right: 0;
  z-index: 100;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 24px;
}

.home-link {
  display: flex;
  align-items: center;
  gap: 7px;
  text-decoration: none;
  color: #334155;
  padding: 6px 13px;
  border-radius: 8px;
  transition: all 0.2s ease;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
}

.home-link:hover {
  background: #f0f9ff;
  border-color: #bae6fd;
  color: #0369a1;
}

.home-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.home-text {
  font-size: 13px;
  font-weight: 500;
}

.page-title {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 12px;
  background: #f8fafc;
  border-radius: 20px;
  border: 1px solid #e2e8f0;
}

.user-avatar-wrap {
  width: 24px;
  height: 24px;
  background: #dbeafe;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #2563eb;
}

.user-avatar-wrap svg {
  width: 14px;
  height: 14px;
}

.user-name {
  font-size: 13px;
  font-weight: 500;
  color: #1e293b;
}

.notification-btn {
  position: relative;
  width: 36px;
  height: 36px;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  background: #f8fafc;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
}

.notification-btn svg {
  width: 17px;
  height: 17px;
}

.notification-btn:hover {
  background: #f0f9ff;
  border-color: #bae6fd;
  color: #0369a1;
}

.notification-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  min-width: 17px;
  height: 17px;
  background: #ef4444;
  color: #ffffff;
  font-size: 10px;
  font-weight: 700;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 4px;
  border: 2px solid #fff;
}
</style>
