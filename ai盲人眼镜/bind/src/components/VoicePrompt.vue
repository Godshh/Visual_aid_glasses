<!-- src/components/VoicePrompt.vue -->
<template>
  <div class="voice-panel">
    <div class="voice-display">
      <div class="current-prompt" :class="{ active: currentPrompt }">
        <div class="prompt-content">
          <div class="prompt-icon" :class="{ speaking: isSpeaking }">
            <span class="icon">🔊</span>
            <div class="sound-waves" v-if="isSpeaking">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
          <div class="prompt-text">
            <p v-if="currentPrompt">{{ currentPrompt }}</p>
            <p v-else class="placeholder">等待语音提示...</p>
          </div>
        </div>
      </div>
    </div>

    <div class="voice-controls">
      <button class="control-btn" @click="toggleMute" :class="{ muted: isMuted }">
        <span class="icon">{{ isMuted ? '🔇' : '🔊' }}</span>
      </button>
      <button class="control-btn" @click="adjustVolume(-1)">
        <span class="icon">🔉</span>
      </button>
      <div class="volume-indicator">
        <div class="volume-bar">
          <div class="volume-fill" :style="{ width: volumeLevel + '%' }"></div>
        </div>
        <span class="volume-text">{{ volumeLevel }}%</span>
      </div>
      <button class="control-btn" @click="adjustVolume(1)">
        <span class="icon">🔊</span>
      </button>
    </div>

    <div class="history-container">
      <div class="history-header">
        <span class="history-title">历史记录</span>
        <button class="clear-btn" @click="clearHistory">清空</button>
      </div>
      <div class="history-list">
        <div 
          v-for="(msg, i) in history" 
          :key="i" 
          class="history-item"
          :class="msg.type"
          @click="playHistoryMessage(msg)"
        >
          <div class="history-time">{{ msg.time }}</div>
          <div class="history-text">{{ msg.text }}</div>
          <div class="history-type">{{ getTypeLabel(msg.type) }}</div>
        </div>
      </div>
    </div>
    
    <!-- 添加测试按钮 -->
    <div class="test-controls">
      <button class="test-btn" @click="testNewMessage">测试新提示</button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, inject } from 'vue'

const currentPrompt = ref('前方30cm有行人，请注意避让')
const isSpeaking = ref(false)
const isMuted = ref(false)
const volumeLevel = ref(75)

// 注入事件总线
const eventBus = inject('eventBus')

// 模拟历史语音记录
const history = ref([
  { text: '已进入盲道跟随模式', time: '14:32', type: 'success' },
  { text: '红灯，请停下', time: '14:31', type: 'danger' },
  { text: '检测到地面有背包', time: '14:30', type: 'warning' },
  { text: '盲道正常', time: '14:29', type: 'success' },
])

// 测试消息列表
const testMessages = [
  { text: '前方有障碍物，请注意', type: 'danger' },
  { text: '绿灯，可以通行', type: 'success' },
  { text: '检测到台阶，请小心', type: 'warning' },
  { text: '已到达目的地', type: 'success' },
  { text: '左侧有车辆靠近', type: 'danger' },
  { text: '前方路况良好', type: 'info' },
]

let messageIndex = 0

// 模拟"正在说话"状态
watch(currentPrompt, (newVal) => {
  if (newVal && newVal.trim()) {
    isSpeaking.value = true
    
    // 发送事件到RealTimeVideo组件
    if (eventBus) {
      // 确定提示类型
      let promptType = 'info'
      if (newVal.includes('警告') || newVal.includes('危险') || newVal.includes('停下') || newVal.includes('障碍物') || newVal.includes('车辆')) {
        promptType = 'danger'
      } else if (newVal.includes('注意') || newVal.includes('检测到') || newVal.includes('台阶') || newVal.includes('小心')) {
        promptType = 'warning'
      } else if (newVal.includes('正常') || newVal.includes('已进入') || newVal.includes('绿灯') || newVal.includes('到达')) {
        promptType = 'success'
      }
      
      eventBus.emit('voice-prompt', {
        text: newVal,
        type: promptType
      })
    }
    
    setTimeout(() => {
      isSpeaking.value = false
    }, 3000)
  }
})

const toggleMute = () => {
  isMuted.value = !isMuted.value
}

const adjustVolume = (delta) => {
  volumeLevel.value = Math.max(0, Math.min(100, volumeLevel.value + delta * 10))
}

const clearHistory = () => {
  history.value = []
}

const getTypeLabel = (type) => {
  switch (type) {
    case 'success': return '正常'
    case 'danger': return '警告'
    case 'warning': return '提醒'
    default: return '信息'
  }
}

// 播放历史消息
const playHistoryMessage = (msg) => {
  currentPrompt.value = msg.text
}

// 测试新消息
const testNewMessage = () => {
  const message = testMessages[messageIndex % testMessages.length]
  currentPrompt.value = message.text
  messageIndex++
  
  // 添加到历史记录
  const now = new Date()
  const time = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`
  history.value.unshift({
    text: message.text,
    time,
    type: message.type
  })
}
</script>

<style scoped>
.voice-panel {
  background: transparent;
  backdrop-filter: blur(10px);
  border-radius: 0 0 18px 18px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 100%;
  border: none;
}

.voice-display {
  flex: 1;
  padding: clamp(8px, 1.5vh, 20px);
  display: flex;
  justify-content: center;
  align-items: center;
}

.current-prompt {
  width: 100%;
  max-width: 90%;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 16px;
  padding: clamp(10px, 2vh, 24px);
  transition: all 0.3s ease;
  border: 1px solid rgba(0,0,0,0.08);
}

.current-prompt.active {
  background: rgba(255, 68, 68, 0.2);
  border-color: rgba(255, 68, 68, 0.3);
  animation: pulse 2s infinite;
}

.prompt-content {
  display: flex;
  align-items: center;
  gap: clamp(15px, 3vw, 20px);
}

.prompt-icon {
  position: relative;
  width: clamp(45px, 6vw, 60px);
  height: clamp(45px, 6vw, 60px);
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 50%;
  flex-shrink: 0;
}

.prompt-icon.speaking {
  background: rgba(16, 185, 129, 0.2);
}

.icon {
  font-size: clamp(20px, 3vw, 28px);
  z-index: 2;
}

.sound-waves {
  position: absolute;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 4px;
}

.sound-waves span {
  width: 4px;
  height: clamp(15px, 3vw, 20px);
  background: rgba(16, 185, 129, 0.8);
  border-radius: 2px;
  animation: soundWave 1s infinite ease-in-out;
}

.sound-waves span:nth-child(2) {
  animation-delay: 0.2s;
  height: clamp(22px, 3.5vw, 30px);
}

.sound-waves span:nth-child(3) {
  animation-delay: 0.4s;
  height: clamp(18px, 3vw, 25px);
}

.prompt-text {
  flex: 1;
}

.prompt-text p {
  font-size: clamp(16px, 2vw, 1.4em);
  font-weight: 600;
  color: #1e293b;
  line-height: 1.5;
  margin: 0;
}

.placeholder {
  color: rgba(30, 41, 59, 0.5);
  font-style: italic;
}

.voice-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(8px, 1.5vw, 12px);
  padding: clamp(12px, 2vh, 16px);
  background: rgba(248, 250, 252, 0.8);
  border-top: 1px solid rgba(0,0,0,0.08);
}

.control-btn {
  width: clamp(32px, 4vw, 40px);
  height: clamp(32px, 4vw, 40px);
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0,0,0,0.1);
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.control-btn:hover {
  background: rgba(0, 0, 0, 0.1);
  transform: scale(1.05);
}

.control-btn.muted {
  background: rgba(255, 68, 68, 0.2);
  border-color: rgba(255, 68, 68, 0.3);
}

.control-btn .icon {
  font-size: clamp(14px, 2vw, 18px);
}

.volume-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.volume-bar {
  width: clamp(80px, 10vw, 100px);
  height: 6px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.volume-fill {
  height: 100%;
  background: linear-gradient(90deg, #10b981, #f59e0b, #ef4444);
  transition: width 0.2s ease;
}

.volume-text {
  font-size: clamp(10px, 1.5vw, 12px);
  color: rgba(30, 41, 59, 0.7);
}

.history-container {
  background: rgba(248, 250, 252, 0.8);
  border-top: 1px solid rgba(0,0,0,0.08);
  max-height: 200px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: clamp(10px, 2vh, 12px) clamp(12px, 2vw, 16px);
  background: rgba(241, 245, 249, 0.9);
  border-bottom: 1px solid rgba(0,0,0,0.08);
}

.history-title {
  font-size: clamp(14px, 2vw, 16px);
  font-weight: 600;
  color: #1e293b;
}

.clear-btn {
  background: none;
  border: none;
  color: rgba(30, 41, 59, 0.7);
  cursor: pointer;
  font-size: clamp(12px, 1.5vw, 14px);
  transition: color 0.2s ease;
}

.clear-btn:hover {
  color: #ef4444;
}

.history-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px 0;
}

.history-item {
  display: flex;
  align-items: center;
  padding: clamp(8px, 1.5vh, 10px) clamp(12px, 2vw, 16px);
  border-bottom: 1px solid rgba(0,0,0,0.05);
  transition: background 0.2s ease;
  cursor: pointer;
}

.history-item:hover {
  background: rgba(0, 0, 0, 0.05);
}

.history-item:last-child {
  border-bottom: none;
}

.history-time {
  width: clamp(40px, 5vw, 50px);
  font-size: clamp(10px, 1.5vw, 12px);
  color: rgba(30, 41, 59, 0.5);
  flex-shrink: 0;
}

.history-text {
  flex: 1;
  font-size: clamp(12px, 1.5vw, 14px);
  color: #1e293b;
  margin: 0 clamp(8px, 1.5vw, 12px);
}

.history-type {
  padding: 2px 8px;
  border-radius: 10px;
  font-size: clamp(10px, 1.5vw, 12px);
  font-weight: 600;
  flex-shrink: 0;
}

.history-item.success .history-type {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.history-item.danger .history-type {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.history-item.warning .history-type {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}

.test-controls {
  padding: 10px;
  background: rgba(241, 245, 249, 0.9);
  border-top: 1px solid rgba(0,0,0,0.08);
  display: flex;
  justify-content: center;
}

.test-btn {
  padding: 8px 16px;
  background: rgba(59, 130, 246, 0.15);
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 8px;
  color: #3b82f6;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.test-btn:hover {
  background: rgba(59, 130, 246, 0.25);
  transform: translateY(-2px);
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(255,68,68,0.4); }
  70% { box-shadow: 0 0 0 10px rgba(255,68,68,0); }
  100% { box-shadow: 0 0 0 0 rgba(255,68,68,0); }
}

@keyframes soundWave {
  0% { transform: scaleY(0.5); opacity: 0.7; }
  50% { transform: scaleY(1); opacity: 1; }
  100% { transform: scaleY(0.5); opacity: 0.7; }
}

/* 自定义滚动条 */
.history-list::-webkit-scrollbar {
  width: 6px;
}

.history-list::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
}

.history-list::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

.history-list::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}
</style>