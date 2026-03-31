<template>
  <div class="device-switcher" :class="{ collapsed: isCollapsed }">
    <div class="switcher-header">
      <span class="switcher-title">📱 设备切换</span>
      <div class="header-actions">
        <button class="collapse-btn" @click="toggleCollapse" :title="isCollapsed ? '展开' : '收起'">
          <span class="collapse-icon">{{ isCollapsed ? '▶' : '▼' }}</span>
        </button>
        <button class="refresh-btn" @click="refreshDevices" :disabled="loading">
          <span class="refresh-icon" :class="{ spinning: loading }">🔄</span>
        </button>
      </div>
    </div>

    <div class="switcher-content" v-show="!isCollapsed">
      <div class="search-box">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索设备..."
          class="search-input"
          @input="filterDevices"
        />
        <span class="search-icon">🔍</span>
      </div>

      <div class="device-list">
        <div
          v-for="device in filteredDevices"
          :key="device.id"
          class="device-item"
          :class="{ active: device.id === currentDeviceId }"
          @click="switchDevice(device)"
        >
          <div class="device-info">
            <div class="device-name">{{ device.name }}</div>
            <div class="device-id">#{{ device.id }}</div>
          </div>
          <div class="device-status">
            <span
              class="status-dot"
              :class="{
                online: device.status === 'online',
                offline: device.status === 'offline',
                warning: device.status === 'warning'
              }"
            ></span>
            <span class="status-text">{{ getStatusText(device.status) }}</span>
          </div>
          <div class="device-battery">
            <span class="battery-icon">🔋</span>
            <span class="battery-level">{{ device.battery }}%</span>
          </div>
        </div>
      </div>

      <div class="switcher-footer">
        <span class="device-count">共 {{ devices.length }} 台设备</span>
        <button class="add-device-btn" @click="addDevice">
          <span class="add-icon">➕</span>
          <span>添加设备</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject } from 'vue'

const eventBus = inject('eventBus')

const searchQuery = ref('')
const loading = ref(false)
const currentDeviceId = ref('001')
const isCollapsed = ref(false)

const devices = ref([
  { id: '001', name: '智能盲人眼镜', status: 'online', battery: 85 },
  { id: '002', name: '智能盲人眼镜', status: 'online', battery: 62 },
  { id: '003', name: '智能盲人眼镜', status: 'warning', battery: 23 },
  { id: '004', name: '智能盲人眼镜', status: 'offline', battery: 0 },
  { id: '005', name: '智能盲人眼镜', status: 'online', battery: 91 }
])

const filteredDevices = computed(() => {
  if (!searchQuery.value) {
    return devices.value
  }
  const query = searchQuery.value.toLowerCase()
  return devices.value.filter(
    device =>
      device.name.toLowerCase().includes(query) ||
      device.id.includes(query)
  )
})

const getStatusText = status => {
  const statusMap = {
    online: '在线',
    offline: '离线',
    warning: '低电'
  }
  return statusMap[status] || status
}

const switchDevice = device => {
  currentDeviceId.value = device.id
  if (eventBus) {
    eventBus.emit('device-switched', device)
  }
}

const refreshDevices = async () => {
  loading.value = true
  await new Promise(resolve => setTimeout(resolve, 1000))
  loading.value = false
}

const filterDevices = () => {}

const addDevice = () => {
  alert('添加设备功能')
}

const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value
}

onMounted(() => {
  if (eventBus) {
    eventBus.on('device-status-update', updateDeviceStatus)
  }
})

const updateDeviceStatus = data => {
  const device = devices.value.find(d => d.id === data.id)
  if (device) {
    Object.assign(device, data)
  }
}
</script>

<style scoped>
.device-switcher {
  padding: 16px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 12px;
  margin: 12px;
  border: 1px solid rgba(59, 130, 246, 0.2);
  transition: all 0.3s ease;
}

.device-switcher.collapsed {
  padding: 12px 16px;
}

.switcher-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.switcher-title {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.collapse-btn {
  width: 28px;
  height: 28px;
  border: none;
  border-radius: 6px;
  background: rgba(59, 130, 246, 0.1);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.collapse-btn:hover {
  background: rgba(59, 130, 246, 0.2);
  transform: scale(1.1);
}

.collapse-icon {
  font-size: 12px;
  transition: transform 0.3s ease;
}

.device-switcher.collapsed .collapse-icon {
  transform: rotate(-90deg);
}

.switcher-content {
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.refresh-btn {
  width: 28px;
  height: 28px;
  border: none;
  border-radius: 6px;
  background: rgba(59, 130, 246, 0.1);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.refresh-btn:hover:not(:disabled) {
  background: rgba(59, 130, 246, 0.2);
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.refresh-icon {
  font-size: 14px;
  transition: transform 0.3s ease;
}

.refresh-icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.search-box {
  position: relative;
  margin-bottom: 12px;
}

.search-input {
  width: 100%;
  padding: 8px 32px 8px 12px;
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 8px;
  font-size: 13px;
  background: rgba(255, 255, 255, 0.8);
  color: #1e293b;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.search-icon {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 14px;
  color: #64748b;
}

.device-list {
  max-height: 280px;
  overflow-y: auto;
  margin-bottom: 12px;
}

.device-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 8px;
  margin-bottom: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.device-item:hover {
  background: rgba(59, 130, 246, 0.1);
  transform: translateX(4px);
}

.device-item.active {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  border-color: #3b82f6;
}

.device-info {
  flex: 1;
}

.device-name {
  font-size: 13px;
  font-weight: 500;
  color: #1e293b;
  margin-bottom: 2px;
}

.device-id {
  font-size: 11px;
  color: #64748b;
}

.device-status {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-right: 12px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-dot.online {
  background: #22c55e;
  box-shadow: 0 0 6px rgba(34, 197, 94, 0.6);
}

.status-dot.offline {
  background: #ef4444;
  box-shadow: 0 0 6px rgba(239, 68, 68, 0.6);
}

.status-dot.warning {
  background: #f59e0b;
  box-shadow: 0 0 6px rgba(245, 158, 11, 0.6);
}

.status-text {
  font-size: 11px;
  color: #64748b;
}

.device-battery {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  background: rgba(59, 130, 246, 0.1);
  border-radius: 6px;
}

.battery-icon {
  font-size: 12px;
}

.battery-level {
  font-size: 11px;
  font-weight: 600;
  color: #3b82f6;
}

.switcher-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid rgba(59, 130, 246, 0.2);
}

.device-count {
  font-size: 12px;
  color: #64748b;
}

.add-device-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: #ffffff;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-device-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.add-icon {
  font-size: 14px;
}
</style>
