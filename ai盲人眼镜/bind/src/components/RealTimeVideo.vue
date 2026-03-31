<!-- src/components/RealTimeVideo.vue -->
<template>
  <div class="video-wrapper">
    <div class="video-container">
      <div class="video-controls-top">
        <button
          class="multi-view-btn"
          @click="toggleMultiView"
          :class="{ active: isMultiView }"
          title="多路模式"
        >
          <span class="multi-view-icon">📹</span>
          <span class="multi-view-text">{{ isMultiView ? '单路' : '多路' }}</span>
        </button>
        <div class="view-selector" v-if="isMultiView">
          <button
            class="view-btn"
            :class="{ active: viewMode === '4' }"
            @click="setViewMode('4')"
          >
            2×2
          </button>
          <button
            class="view-btn"
            :class="{ active: viewMode === '9' }"
            @click="setViewMode('9')"
          >
            3×3
          </button>
        </div>
      </div>

      <div v-if="!isMultiView" class="single-view">
        <img 
          :src="currentFrameUrl" 
          alt="实时视频流" 
          class="video-img"
          :class="{ loading: isLoading }"
        />
        
        <div class="video-info-overlay">
          <div class="video-status">
            <span class="status-dot" :class="{ online: isConnected, offline: !isConnected }"></span>
            <span class="status-text">{{ isConnected ? '在线' : '离线' }}</span>
          </div>
          <div class="video-fps">FPS: 30</div>
        </div>
      </div>

      <div v-else class="multi-view" :class="`view-${viewMode}`">
        <div
          v-for="(device, index) in visibleDevices"
          :key="device.id"
          class="video-grid-item"
          :class="{ active: device.id === currentDeviceId }"
          @click="selectDevice(device)"
        >
          <div class="video-placeholder">
            <div class="device-label">{{ device.name }} #{{ device.id }}</div>
            <div class="device-status">
              <span class="status-dot" :class="{ online: device.online, offline: !device.online }"></span>
              <span>{{ device.online ? '在线' : '离线' }}</span>
            </div>
          </div>
          <div v-if="device.id === currentDeviceId" class="selected-badge">主画面</div>
        </div>
      </div>
      
      <div class="video-popups-left">
        <TransitionGroup name="video-popup" tag="div">
          <div
            v-for="popup in leftPopups"
            :key="popup.id"
            :class="['video-popup', 'left']"
            @click="removePopup(popup.id)"
          >
            <div class="popup-icon">
              <span v-if="popup.type === 'danger'">⚠️</span>
              <span v-else-if="popup.type === 'warning'">⚡</span>
              <span v-else>ℹ️</span>
            </div>
            <div class="popup-content">
              <div class="popup-text">{{ popup.text }}</div>
              <div class="popup-time">{{ popup.time }}</div>
            </div>
          </div>
        </TransitionGroup>
      </div>

      <div class="video-popups-right">
        <TransitionGroup name="video-popup" tag="div">
          <div
            v-for="popup in rightPopups"
            :key="popup.id"
            :class="['video-popup', 'right']"
            @click="removePopup(popup.id)"
          >
            <div class="popup-icon">
              <span v-if="popup.type === 'danger'">⚠️</span>
              <span v-else-if="popup.type === 'warning'">⚡</span>
              <span v-else>ℹ️</span>
            </div>
            <div class="popup-content">
              <div class="popup-text">{{ popup.text }}</div>
              <div class="popup-time">{{ popup.time }}</div>
            </div>
          </div>
        </TransitionGroup>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, inject, computed, watch } from 'vue'

const WS_URL = 'ws://121.43.195.181:5001/ws/cam/'

const currentFrameUrl = ref('')
const isLoading = ref(true)
const isConnected = ref(false)
const popups = ref([])
const leftPopups = ref([])
const rightPopups = ref([])
const isMultiView = ref(false)
const viewMode = ref('4')
const currentDeviceId = ref('001')

const devices = ref([
  { id: '001', name: '智能盲人眼镜', online: true },
  { id: '002', name: '智能盲人眼镜', online: true },
  { id: '003', name: '智能盲人眼镜', online: true },
  { id: '004', name: '智能盲人眼镜', online: false },
  { id: '005', name: '智能盲人眼镜', online: true },
  { id: '006', name: '智能盲人眼镜', online: true },
  { id: '007', name: '智能盲人眼镜', online: true },
  { id: '008', name: '智能盲人眼镜', online: true },
  { id: '009', name: '智能盲人眼镜', online: true }
])

const visibleDevices = computed(() => {
  const count = viewMode.value === '4' ? 4 : 9
  return devices.value.slice(0, count)
})

let ws = null
let pendingUrl = null
let popupIdCounter = 0

const eventBus = inject('eventBus')

const handleVoicePrompt = data => {
  addPopup(data.text, data.type)
}

const addPopup = (text, type = 'info') => {
  const id = ++popupIdCounter
  const time = new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  
  const position = Math.random() < 0.5 ? 'left' : 'right'
  
  const popup = {
    id,
    text,
    type,
    time,
    timestamp: Date.now()
  }
  
  if (position === 'left') {
    leftPopups.value.push(popup)
  } else {
    rightPopups.value.push(popup)
  }
  
  setTimeout(() => {
    removePopup(id)
  }, 8000)
}

const removePopup = id => {
  const leftIndex = leftPopups.value.findIndex(popup => popup.id === id)
  if (leftIndex !== -1) {
    leftPopups.value.splice(leftIndex, 1)
    return
  }
  
  const rightIndex = rightPopups.value.findIndex(popup => popup.id === id)
  if (rightIndex !== -1) {
    rightPopups.value.splice(rightIndex, 1)
    return
  }
}

const revokeUrl = () => {
  if (pendingUrl) {
    URL.revokeObjectURL(pendingUrl)
    pendingUrl = null
  }
}

const connect = () => {
  isLoading.value = true
  isConnected.value = false
  
  if (ws) {
    ws.onclose = null
    ws.close()
  }

  ws = new WebSocket(WS_URL)
  ws.binaryType = 'blob'

  ws.onopen = () => {
    isLoading.value = false
    isConnected.value = true
  }

  ws.onmessage = e => {
    if (e.data instanceof Blob) {
      revokeUrl()
      const url = URL.createObjectURL(e.data)
      pendingUrl = url
      currentFrameUrl.value = url + '#' + Date.now()
      setTimeout(revokeUrl, 100)
    }
  }

  ws.onclose = () => {
    isLoading.value = true
    isConnected.value = false
    setTimeout(connect, 2000)
  }

  ws.onerror = () => {
    isLoading.value = true
    isConnected.value = false
    ws?.close()
  }
}

const toggleMultiView = () => {
  isMultiView.value = !isMultiView.value
}

const setViewMode = mode => {
  viewMode.value = mode
}

const selectDevice = device => {
  currentDeviceId.value = device.id
  if (eventBus) {
    eventBus.emit('device-switched', device)
  }
}

const toggleFullscreen = () => {
  const elem = document.querySelector('.video-img')
  if (elem.requestFullscreen) {
    elem.requestFullscreen()
  }
}

const takeSnapshot = () => {
  if (!currentFrameUrl.value) return
  
  const link = document.createElement('a')
  link.href = currentFrameUrl.value
  link.download = `snapshot_${Date.now()}.jpg`
  link.click()
}

const sortedPopups = computed(() => {
  const allPopups = [
    ...leftPopups.value.map(popup => ({ ...popup, position: 'left' })),
    ...rightPopups.value.map(popup => ({ ...popup, position: 'right' }))
  ];
  
  return allPopups.sort((a, b) => a.timestamp - b.timestamp);
});

watch(() => eventBus?.value?.on, (newHandler) => {
  if (newHandler && eventBus.value) {
    eventBus.value.on('device-switched', device => {
      currentDeviceId.value = device.id
    })
  }
}, { immediate: true })

onMounted(() => {
  connect()
  if (eventBus) {
    eventBus.on('voice-prompt', handleVoicePrompt)
    eventBus.on('device-switched', device => {
      currentDeviceId.value = device.id
    })
  }
})

onUnmounted(() => {
  revokeUrl()
  if (ws) {
    ws.onclose = null
    ws.close()
  }
  if (eventBus) {
    eventBus.off('voice-prompt', handleVoicePrompt)
    eventBus.off('device-switched', device => {
      currentDeviceId.value = device.id
    })
  }
})
</script>

<style scoped>
.video-wrapper {
  width: 100%;
  height: 100%;
  background: transparent;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

.video-container {
  width: 100%;
  flex: 4;
  position: relative;
  overflow: hidden;
  border-radius: 0 0 18px 18px;
}

.video-controls-top {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 20;
  display: flex;
  align-items: center;
  gap: 8px;
}

.multi-view-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.multi-view-btn:hover {
  background: rgba(59, 130, 246, 0.1);
  transform: translateY(-2px);
}

.multi-view-btn.active {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: #ffffff;
  border-color: #3b82f6;
}

.multi-view-icon {
  font-size: 16px;
}

.multi-view-text {
  font-size: 13px;
  font-weight: 500;
}

.view-selector {
  display: flex;
  gap: 4px;
  background: rgba(255, 255, 255, 0.95);
  padding: 4px;
  border-radius: 8px;
  border: 1px solid rgba(59, 130, 246, 0.3);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.view-btn {
  padding: 6px 12px;
  background: transparent;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  color: #64748b;
  transition: all 0.3s ease;
}

.view-btn:hover {
  background: rgba(59, 130, 246, 0.1);
}

.view-btn.active {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: #ffffff;
}

.single-view {
  width: 100%;
  height: 100%;
  position: relative;
}

.video-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: opacity 0.3s ease;
}

.video-img.loading {
  opacity: 0.7;
}

.video-info-overlay {
  position: absolute;
  bottom: 12px;
  left: 12px;
  right: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(10px);
  border-radius: 8px;
  color: #ffffff;
}

.video-status {
  display: flex;
  align-items: center;
  gap: 6px;
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

.status-text {
  font-size: 12px;
  font-weight: 500;
}

.video-fps {
  font-size: 12px;
  font-weight: 600;
}

.multi-view {
  width: 100%;
  height: 100%;
  display: grid;
  gap: 8px;
  padding: 8px;
  background: rgba(0, 0, 0, 0.3);
}

.multi-view.view-4 {
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);
}

.multi-view.view-9 {
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(3, 1fr);
}

.video-grid-item {
  position: relative;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.video-grid-item:hover {
  transform: scale(1.02);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.video-grid-item.active {
  border-color: #3b82f6;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2);
}

.video-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  color: #ffffff;
}

.device-label {
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 4px;
}

.device-status {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  opacity: 0.8;
}

.selected-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  padding: 4px 8px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: #ffffff;
  font-size: 10px;
  font-weight: 600;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.4);
}

.video-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, rgba(0,0,0,0.5) 0%, transparent 10%, transparent 90%, rgba(0,0,0,0.5) 100%);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: clamp(8px, 1.5vh, 15px);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.video-container:hover .video-overlay {
  opacity: 1;
}

.video-info {
  display: flex;
  gap: clamp(10px, 2vw, 20px);
  flex-wrap: wrap;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: clamp(10px, 1.2vw, 12px);
  color: rgba(255,255,255,0.7);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.info-value {
  font-size: clamp(12px, 1.5vw, 14px);
  font-weight: 600;
  color: white;
}

.info-value.connected {
  color: #00c851;
}

.info-value.disconnected {
  color: #ff4444;
}

.video-controls {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.control-btn {
  width: clamp(36px, 4vw, 40px);
  height: clamp(36px, 4vw, 40px);
  border-radius: 50%;
  background: rgba(255,255,255,0.1);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255,255,255,0.2);
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.control-btn:hover {
  background: rgba(255,255,255,0.2);
  transform: scale(1.1);
}

.icon {
  font-size: clamp(16px, 2vw, 18px);
}

.loading-indicator {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.7);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 20px;
  color: white;
}

.loading-spinner {
  width: clamp(40px, 5vw, 50px);
  height: clamp(40px, 5vw, 50px);
  border: 4px solid rgba(255,255,255,0.2);
  border-top: 4px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* 视频弹窗提示样式 */
.video-popups-left {
  position: absolute;
  top: 20px;
  left: 20px;
  right: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 40%;
  z-index: 10;
  pointer-events: none;
  align-items: flex-start;
}

.video-popups-right {
  position: absolute;
  top: 20px;
  right: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 40%;
  z-index: 10;
  pointer-events: none;
  align-items: flex-end;
}

.video-popup {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 18px 18px 4px 4px;
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0.95), rgba(248, 250, 252, 0.9));
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  color: #1e293b;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  position: relative;
  overflow: hidden;
  pointer-events: auto;
  width: 100%;
  margin-bottom: 10px;
  transform: translateY(20px);
  opacity: 0;
}

/* 弹窗入场动画 */
.video-popup-enter-active {
  transition: all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.video-popup-leave-active {
  transition: all 0.3s cubic-bezier(0.55, 0.055, 0.675, 0.19);
}

.video-popup-enter-from {
  transform: translateY(30px) scale(0.9);
  opacity: 0;
}

.video-popup-leave-to {
  transform: translateY(-20px) scale(0.95);
  opacity: 0;
}

.video-popup-enter-to {
  transform: translateY(0) scale(1);
  opacity: 1;
}

/* 弹窗位置样式 */
.video-popup.left {
  border-radius: 12px 12px 12px 4px;
}

.video-popup.right {
  border-radius: 12px 12px 4px 12px;
}

.popup-icon {
  font-size: 20px;
  margin-right: 8px;
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 50%;
}

.popup-content {
  flex: 1;
}

.popup-title {
  font-weight: 600;
  font-size: 14px;
  margin-bottom: 4px;
  color: #1e293b;
}

.popup-message {
  font-size: 13px;
  opacity: 0.9;
  color: rgba(30, 41, 59, 0.9);
  line-height: 1.4;
}

.popup-text {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 4px;
}

.popup-time {
  font-size: 12px;
  opacity: 0.6;
}

.popup-close {
  position: absolute;
  top: 5px;
  right: 5px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.1);
  border: none;
  color: #1e293b;
  font-size: 14px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.video-popup:hover .popup-close {
  opacity: 1;
}

.popup-close:hover {
  background: rgba(0, 0, 0, 0.2);
}

/* 弹窗动画 */
.popup-enter-active {
  transition: all 0.3s ease;
}

.popup-leave-active {
  transition: all 0.3s ease;
}

.popup-enter-from.left {
  opacity: 0;
  transform: translateX(-20px);
}

.popup-enter-from.right {
  opacity: 0;
  transform: translateX(20px);
}

.popup-leave-to.left {
  opacity: 0;
  transform: translateX(-20px);
}

.popup-leave-to.right {
  opacity: 0;
  transform: translateX(20px);
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>