<template>
  <header class="global-status-bar">
    <div class="status-left">
      <div class="system-status">
        <span class="status-dot" :class="{ online: isOnline, offline: !isOnline }"></span>
        <span class="status-text">{{ isOnline ? '系统在线' : '系统离线' }}</span>
      </div>
      <div class="time-display">
        <svg class="icon" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.6"/><path d="M12 7v5l3 3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
        <span class="time-text">{{ currentTime }}</span>
      </div>
    </div>

    <div class="status-center">
        <div class="device-selector" ref="deviceSelectorRef">
          <button class="device-selector-btn" @click="toggleDeviceDropdown" :class="{ active: showDeviceDropdown }">
            <svg class="icon" viewBox="0 0 24 24" fill="none"><rect x="7" y="2" width="10" height="18" rx="2.5" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="17.5" r="1" fill="currentColor"/><path d="M10 5.5h4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
            <span class="device-selector-text">{{ currentDevice.name }} #{{ currentDevice.id }}</span>
            <svg class="arrow-icon" :class="{ rotated: showDeviceDropdown }" viewBox="0 0 24 24" fill="none"><path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </button>

          <teleport to="body">
            <div
              class="device-dropdown"
              v-if="showDeviceDropdown"
              :style="dropdownStyle"
            >
              <div
                v-for="device in devices"
                :key="device.id"
                class="device-dropdown-item"
                :class="{ active: device.id === currentDevice.id }"
                @click="selectDevice(device)"
              >
                <div class="dropdown-device-info">
                  <span class="dropdown-device-name">{{ device.name }} #{{ device.id }}</span>
                  <span class="dropdown-device-status" :class="device.status">
                    {{ getStatusText(device.status) }}
                  </span>
                </div>
                <div class="dropdown-device-battery">
                  <svg viewBox="0 0 24 24" fill="none" style="width:13px;height:13px"><rect x="2" y="7" width="16" height="10" rx="2" stroke="currentColor" stroke-width="1.5"/><path d="M20 10v4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><rect x="4" y="9" width="10" height="6" rx="1" fill="currentColor" opacity="0.5"/></svg>
                  <span class="battery-level">{{ device.battery }}%</span>
                </div>
              </div>
            </div>
          </teleport>
        </div>

      <div class="active-devices">
        <svg class="icon" viewBox="0 0 24 24" fill="none"><circle cx="9" cy="8" r="3" stroke="currentColor" stroke-width="1.5"/><circle cx="17" cy="9" r="2.5" stroke="currentColor" stroke-width="1.5"/><path d="M3 20c0-3.314 2.686-6 6-6s6 2.686 6 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><path d="M17 14c1.657 0 3 1.343 3 3v1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
        <span class="devices-count">{{ activeDevices }}/{{ totalDevices }}</span>
        <span class="devices-label">在线</span>
      </div>
      <div class="alert-summary">
        <svg class="icon" viewBox="0 0 24 24" fill="none"><path d="M12 2L3 20h18L12 2z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M12 9v5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="12" cy="17" r="0.8" fill="currentColor"/></svg>
        <span class="alert-count critical">{{ criticalAlerts }}</span>
        <span class="alert-count warning">{{ warningAlerts }}</span>
        <span class="alert-label">告警</span>
      </div>
    </div>

    <div class="status-right">
      <div class="weather-info">
        <svg class="icon" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="4" stroke="#f59e0b" stroke-width="1.6"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41" stroke="#f59e0b" stroke-width="1.6" stroke-linecap="round"/></svg>
        <span class="weather-text">{{ weatherText }}</span>
      </div>
      <button class="notification-btn" @click="showNotifications">
        <svg viewBox="0 0 24 24" fill="none"><path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M13.73 21a2 2 0 01-3.46 0" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
        <span class="notification-badge" v-if="unreadCount > 0">{{ unreadCount }}</span>
      </button>
      <div class="user-profile">
        <div class="user-avatar-wrap">
          <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="8" r="4" stroke="currentColor" stroke-width="1.6"/><path d="M4 20c0-4 3.582-7 8-7s8 3 8 7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
        </div>
        <span class="user-name">{{ userName }}</span>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted, inject, computed, nextTick } from 'vue'

const eventBus = inject('eventBus')

const isOnline = ref(true)
const currentTime = ref('')
const showDeviceDropdown = ref(false)
const currentDeviceId = ref('001')
const deviceSelectorRef = ref(null)
const dropdownPosition = ref({ top: 0, left: 0 })

const devices = ref([
  { id: '001', name: '智能盲人眼镜', status: 'online', battery: 85, alerts: { critical: 1, warning: 2 } },
  { id: '002', name: '智能盲人眼镜', status: 'online', battery: 62, alerts: { critical: 0, warning: 1 } },
  { id: '003', name: '智能盲人眼镜', status: 'warning', battery: 23, alerts: { critical: 1, warning: 2 } },
  { id: '004', name: '智能盲人眼镜', status: 'offline', battery: 0, alerts: { critical: 0, warning: 0 } },
  { id: '005', name: '智能盲人眼镜', status: 'online', battery: 91, alerts: { critical: 0, warning: 0 } }
])

const currentDevice = computed(() => {
  return devices.value.find(d => d.id === currentDeviceId.value) || devices.value[0]
})

const activeDevices = computed(() => {
  return devices.value.filter(d => d.status !== 'offline').length
})

const totalDevices = computed(() => {
  return devices.value.length
})

const criticalAlerts = computed(() => {
  return currentDevice.value.alerts.critical
})

const warningAlerts = computed(() => {
  return currentDevice.value.alerts.warning
})

const dropdownStyle = computed(() => {
  return {
    top: `${dropdownPosition.value.top}px`,
    left: `${dropdownPosition.value.left}px`
  }
})

const weatherIcon = ref('☀️')
const weatherText = ref('晴 25°C')
const unreadCount = ref(7)
const userName = ref('管理员')

let timeInterval = null

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

const showNotifications = () => {
  alert('查看通知')
}

const toggleDeviceDropdown = async () => {
  showDeviceDropdown.value = !showDeviceDropdown.value
  if (showDeviceDropdown.value) {
    await nextTick()
    updateDropdownPosition()
  }
}

const updateDropdownPosition = () => {
  if (deviceSelectorRef.value) {
    const rect = deviceSelectorRef.value.getBoundingClientRect()
    dropdownPosition.value = {
      top: rect.bottom + 8,
      left: rect.left
    }
  }
}

const selectDevice = device => {
  currentDeviceId.value = device.id
  showDeviceDropdown.value = false
  if (eventBus) {
    eventBus.emit('device-switched', device)
  }
}

const getStatusText = status => {
  const statusMap = {
    online: '在线',
    offline: '离线',
    warning: '低电'
  }
  return statusMap[status] || status
}

const handleClickOutside = event => {
  if (!event.target.closest('.device-selector') && !event.target.closest('.device-dropdown')) {
    showDeviceDropdown.value = false
  }
}

onMounted(() => {
  updateTime()
  timeInterval = setInterval(updateTime, 1000)
  
  if (eventBus) {
    eventBus.on('device-switched', device => {
      currentDeviceId.value = device.id
    })
  }
  
  document.addEventListener('click', handleClickOutside)
  window.addEventListener('scroll', updateDropdownPosition)
})

onUnmounted(() => {
  if (timeInterval) {
    clearInterval(timeInterval)
  }
  
  if (eventBus) {
    eventBus.off('device-switched', device => {
      currentDeviceId.value = device.id
    })
  }
  
  document.removeEventListener('click', handleClickOutside)
  window.removeEventListener('scroll', updateDropdownPosition)
})
</script>

<style scoped>
.global-status-bar {
  height: 52px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.07);
  box-shadow: 0 1px 12px rgba(0, 0, 0, 0.05);
  position: fixed;
  top: 0;
  left: 64px;
  right: 0;
  z-index: 90;
}

.icon {
  width: 15px;
  height: 15px;
  flex-shrink: 0;
  color: currentColor;
}

.status-left,
.status-center,
.status-right {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.status-right {
  gap: 8px;
}

/* ── 系统状态 ── */
.system-status {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 5px 11px;
  background: #f0fdf4;
  border-radius: 20px;
  border: 1px solid #bbf7d0;
}

.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}

.status-dot.online {
  background: #22c55e;
  box-shadow: 0 0 7px rgba(34,197,94,0.6);
  animation: pulse 2.5s infinite;
}

.status-dot.offline {
  background: #ef4444;
  box-shadow: 0 0 7px rgba(239,68,68,0.6);
}

.status-text {
  font-size: 12px;
  font-weight: 600;
  color: #15803d;
}

/* ── 时间 ── */
.time-display {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 11px;
  background: #f8fafc;
  border-radius: 20px;
  border: 1px solid #e2e8f0;
  color: #64748b;
}

.time-text {
  font-size: 12.5px;
  font-weight: 500;
  color: #334155;
  font-family: 'Consolas', 'Monaco', monospace;
  letter-spacing: 0.02em;
}

/* ── 设备选择器 ── */
.device-selector { position: relative; }

.device-selector-btn {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 5px 12px;
  background: #f0f9ff;
  border: 1px solid #bae6fd;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #0369a1;
}

.device-selector-btn:hover {
  background: #e0f2fe;
  border-color: #7dd3fc;
}

.device-selector-btn.active {
  background: #0ea5e9;
  border-color: #0ea5e9;
  color: #fff;
}

.device-selector-btn .icon {
  color: currentColor;
}

.device-selector-text {
  font-size: 12.5px;
  font-weight: 600;
  color: inherit;
}

.arrow-icon {
  width: 14px;
  height: 14px;
  color: currentColor;
  opacity: 0.7;
  transition: transform 0.2s ease;
}

.arrow-icon.rotated {
  transform: rotate(180deg);
}

/* ── Dropdown ── */
.device-dropdown {
  position: fixed;
  min-width: 270px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.13);
  border: 1px solid #e2e8f0;
  padding: 6px;
  z-index: 9999;
  animation: dropdownSlide 0.2s ease;
}

@keyframes dropdownSlide {
  from { opacity: 0; transform: translateY(-6px); }
  to   { opacity: 1; transform: translateY(0); }
}

.device-dropdown-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 9px 10px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.15s ease;
  margin-bottom: 2px;
}

.device-dropdown-item:hover { background: #f0f9ff; }

.device-dropdown-item.active {
  background: #eff6ff;
  border: 1px solid #bfdbfe;
}

.dropdown-device-info {
  display: flex;
  flex-direction: column;
  gap: 3px;
  flex: 1;
}

.dropdown-device-name {
  font-size: 13px;
  font-weight: 600;
  color: #1e293b;
}

.dropdown-device-status {
  font-size: 11px;
  padding: 2px 7px;
  border-radius: 4px;
  display: inline-block;
  width: fit-content;
  font-weight: 500;
}

.dropdown-device-status.online  { background: #dcfce7; color: #166534; }
.dropdown-device-status.offline { background: #fee2e2; color: #991b1b; }
.dropdown-device-status.warning { background: #fef3c7; color: #92400e; }

.dropdown-device-battery {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 3px 8px;
  background: #f0f9ff;
  border-radius: 6px;
  color: #0369a1;
}

.battery-level {
  font-size: 11px;
  font-weight: 600;
}

/* ── 在线设备 ── */
.active-devices {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 5px 11px;
  background: #f0f9ff;
  border-radius: 20px;
  border: 1px solid #bae6fd;
  color: #0369a1;
}

.devices-count {
  font-size: 13px;
  font-weight: 700;
  color: #0369a1;
}

.devices-label {
  font-size: 12px;
  color: #64748b;
}

/* ── 告警 ── */
.alert-summary {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 11px;
  background: #fff7ed;
  border-radius: 20px;
  border: 1px solid #fed7aa;
  color: #c2410c;
}

.alert-count {
  font-size: 12px;
  font-weight: 700;
  padding: 1px 6px;
  border-radius: 5px;
  line-height: 1.5;
}

.alert-count.critical { background: #ef4444; color: #fff; }
.alert-count.warning  { background: #f59e0b; color: #fff; }

.alert-label {
  font-size: 12px;
  color: #c2410c;
  font-weight: 500;
}

/* ── 天气 ── */
.weather-info {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 11px;
  background: #fffbeb;
  border-radius: 20px;
  border: 1px solid #fde68a;
}

.weather-text {
  font-size: 12.5px;
  font-weight: 500;
  color: #92400e;
}

/* ── 通知 ── */
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
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 4px;
  border: 2px solid #fff;
}

/* ── 用户 ── */
.user-profile {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 12px;
  background: #f8fafc;
  border-radius: 20px;
  border: 1px solid #e2e8f0;
  cursor: pointer;
  transition: all 0.2s ease;
}

.user-profile:hover {
  background: #f0f9ff;
  border-color: #bae6fd;
}

.user-avatar-wrap {
  width: 26px;
  height: 26px;
  background: #dbeafe;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #2563eb;
}

.user-avatar-wrap svg {
  width: 15px;
  height: 15px;
}

.user-name {
  font-size: 12.5px;
  font-weight: 600;
  color: #1e293b;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}
</style>
