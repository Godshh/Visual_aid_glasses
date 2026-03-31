<template>
  <div
    class="sidebar"
    :class="{ expanded: isExpanded }"
    @mouseenter="isExpanded = true"
    @mouseleave="isExpanded = false"
  >
    <div class="sidebar-header">
      <div class="logo">
        <div class="logo-icon-wrap">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5z" stroke="#60a5fa" stroke-width="1.5" stroke-linejoin="round"/>
            <circle cx="12" cy="12" r="3.5" fill="#3b82f6" stroke="#60a5fa" stroke-width="1"/>
            <circle cx="12" cy="12" r="1.5" fill="#fff"/>
          </svg>
        </div>
        <span class="logo-text">视界 AI</span>
      </div>
      <div class="subtitle">智能盲人眼镜管理平台</div>
    </div>

    <nav class="sidebar-nav">
      <div class="nav-section">
        <div class="nav-section-title">概览</div>
        <router-link to="/" class="nav-item" active-class="active">
          <span class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none"><path d="M3 9.5L12 3l9 6.5V20a1 1 0 01-1 1H4a1 1 0 01-1-1V9.5z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M9 21V12h6v9" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>
          </span>
          <span class="nav-text">主页</span>
        </router-link>
      </div>

      <div class="nav-section">
        <div class="nav-section-title">核心功能</div>
        <router-link to="/dashboard" class="nav-item" active-class="active">
          <span class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none"><rect x="3" y="3" width="7" height="9" rx="1.5" stroke="currentColor" stroke-width="1.6"/><rect x="14" y="3" width="7" height="5" rx="1.5" stroke="currentColor" stroke-width="1.6"/><rect x="14" y="12" width="7" height="9" rx="1.5" stroke="currentColor" stroke-width="1.6"/><rect x="3" y="16" width="7" height="5" rx="1.5" stroke="currentColor" stroke-width="1.6"/></svg>
          </span>
          <span class="nav-text">实时监控</span>
        </router-link>
        <router-link to="/history" class="nav-item" active-class="active">
          <span class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.6"/><path d="M12 7v5l3.5 3.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </span>
          <span class="nav-text">历史轨迹</span>
        </router-link>
        <router-link to="/alerts" class="nav-item" active-class="active">
          <span class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none"><path d="M12 2L3 20h18L12 2z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M12 9v5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="12" cy="17" r="0.8" fill="currentColor"/></svg>
          </span>
          <span class="nav-text">告警中心</span>
        </router-link>
      </div>

      <div class="nav-section">
        <div class="nav-section-title">管理</div>
        <router-link to="/devices" class="nav-item" active-class="active">
          <span class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none"><rect x="7" y="2" width="10" height="18" rx="2.5" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="17.5" r="1" fill="currentColor"/><path d="M10 5.5h4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
          </span>
          <span class="nav-text">设备管理</span>
        </router-link>
        <router-link to="/logs" class="nav-item" active-class="active">
          <span class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none"><path d="M14 3H6a2 2 0 00-2 2v14a2 2 0 002 2h12a2 2 0 002-2V9l-6-6z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M14 3v6h6M8 13h8M8 17h5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
          </span>
          <span class="nav-text">交互日志</span>
        </router-link>
      </div>
    </nav>

    <div class="sidebar-footer">
      <div class="status-row">
        <span class="status-dot online"></span>
        <span class="status-text">系统在线</span>
      </div>
      <div class="version">v 1.0.0</div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const isExpanded = ref(false)
</script>

<style scoped>
.sidebar {
  width: 64px;
  height: 100vh;
  background: #0f172a;
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 200;
  box-shadow: 2px 0 20px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  transition: width 0.28s cubic-bezier(0.4, 0, 0.2, 1);
  border-right: 1px solid rgba(255,255,255,0.05);
}

.sidebar.expanded {
  width: 216px;
}

/* ── 隐藏/显示文字 ── */
.logo-text,
.subtitle,
.nav-section-title,
.nav-text,
.status-text,
.version {
  opacity: 0;
  overflow: hidden;
  white-space: nowrap;
  max-width: 0;
  transition: opacity 0.15s ease 0s, max-width 0.28s ease;
}

.sidebar.expanded .logo-text,
.sidebar.expanded .subtitle,
.sidebar.expanded .nav-section-title,
.sidebar.expanded .nav-text,
.sidebar.expanded .status-text,
.sidebar.expanded .version {
  opacity: 1;
  max-width: 160px;
  transition: opacity 0.18s ease 0.12s, max-width 0.28s ease;
}

/* ── Header ── */
.sidebar-header {
  padding: 18px 14px 16px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-icon-wrap {
  width: 34px;
  height: 34px;
  flex-shrink: 0;
  background: rgba(59,130,246,0.12);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(59,130,246,0.25);
}

.logo-icon-wrap svg {
  width: 20px;
  height: 20px;
}

.logo-text {
  font-size: 16px;
  font-weight: 700;
  color: #f1f5f9;
  letter-spacing: 0.03em;
}

.subtitle {
  font-size: 10px;
  color: rgba(148,163,184,0.5);
  margin-top: 5px;
  padding-left: 44px;
  letter-spacing: 0.04em;
}

/* ── Nav ── */
.sidebar-nav {
  flex: 1;
  padding: 12px 0;
  overflow-y: auto;
  overflow-x: hidden;
}

.sidebar-nav::-webkit-scrollbar { width: 0; }

.nav-section {
  margin-bottom: 4px;
}

.nav-section-title {
  padding: 8px 20px 4px;
  font-size: 10px;
  font-weight: 600;
  color: rgba(148,163,184,0.35);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 15px;
  margin: 1px 6px;
  color: rgba(148,163,184,0.7);
  text-decoration: none;
  border-radius: 9px;
  transition: background 0.18s ease, color 0.18s ease;
  position: relative;
}

.nav-item:hover {
  background: rgba(255,255,255,0.06);
  color: #e2e8f0;
}

.nav-item.active {
  background: rgba(59,130,246,0.18);
  color: #93c5fd;
}

.nav-item.active::before {
  content: '';
  position: absolute;
  left: -6px;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 20px;
  background: #3b82f6;
  border-radius: 0 2px 2px 0;
}

.nav-icon {
  width: 34px;
  height: 34px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-icon svg {
  width: 18px;
  height: 18px;
}

.nav-text {
  font-size: 13.5px;
  font-weight: 500;
}

/* ── Footer ── */
.sidebar-footer {
  padding: 14px 15px;
  border-top: 1px solid rgba(255,255,255,0.06);
}

.status-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}

.status-dot.online {
  background: #22c55e;
  box-shadow: 0 0 7px rgba(34,197,94,0.7);
  animation: pulse 2.5s infinite;
}

.status-text {
  font-size: 12px;
  color: rgba(148,163,184,0.6);
}

.version {
  font-size: 10px;
  color: rgba(148,163,184,0.28);
  padding-left: 15px;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.35; }
}
</style>
