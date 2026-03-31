<!-- src/components/FeedbackBar.vue -->
<template>
  <div class="feedback-panel">
    <div class="panel-header">
      <h3 class="panel-title">智能感知系统</h3>
      <div class="system-status" :class="{ active: systemActive }">
        <span class="status-dot"></span>
        <span class="status-text">{{ systemActive ? '运行中' : '待机' }}</span>
      </div>
    </div>
    
    <div class="feedback-grid">
      <div class="feedback-item" :class="{ active: obstacles }">
        <div class="item-icon">🚧</div>
        <div class="item-content">
          <h4>障碍物检测</h4>
          <p>{{ obstacles ? '前方有障碍物' : '无障碍物' }}</p>
          <div class="item-detail" v-if="obstacles">
            <span class="distance">距离: {{ obstacleDistance }}cm</span>
            <span class="direction">方向: {{ obstacleDirection }}</span>
          </div>
        </div>
        <div class="item-indicator" :class="{ warning: obstacles }"></div>
      </div>
      
      <div class="feedback-item" :class="{ active: blindRoad }">
        <div class="item-icon">🦯</div>
        <div class="item-content">
          <h4>盲道识别</h4>
          <p>{{ blindRoad ? '盲道正常' : '未检测到盲道' }}</p>
          <div class="item-detail" v-if="blindRoad">
            <span class="status">状态: 良好</span>
            <span class="direction">方向: 前方</span>
          </div>
        </div>
        <div class="item-indicator" :class="{ success: blindRoad }"></div>
      </div>
      
      <div class="feedback-item" :class="{ active: trafficLight }">
        <div class="item-icon">🚦</div>
        <div class="item-content">
          <h4>红绿灯</h4>
          <p>{{ trafficLight ? lightStatus : '未检测到信号灯' }}</p>
          <div class="item-detail" v-if="trafficLight">
            <span class="status">状态: {{ lightStatus }}</span>
            <span class="countdown">倒计时: {{ countdown }}s</span>
          </div>
        </div>
        <div class="item-indicator" :class="lightClass"></div>
      </div>
      
      <div class="feedback-item" :class="{ active: crosswalk }">
        <div class="item-icon">🚶</div>
        <div class="item-content">
          <h4>人行横道</h4>
          <p>{{ crosswalk ? '前方有人行横道' : '未检测到人行横道' }}</p>
          <div class="item-detail" v-if="crosswalk">
            <span class="status">状态: 安全</span>
            <span class="distance">距离: {{ crosswalkDistance }}m</span>
          </div>
        </div>
        <div class="item-indicator" :class="{ info: crosswalk }"></div>
      </div>
      
      <div class="feedback-item" :class="{ active: stairs }">
        <div class="item-icon">🪜</div>
        <div class="item-content">
          <h4>楼梯/台阶</h4>
          <p>{{ stairs ? '前方有楼梯' : '无楼梯' }}</p>
          <div class="item-detail" v-if="stairs">
            <span class="type">类型: {{ stairsType }}</span>
            <span class="count">数量: {{ stairsCount }}级</span>
          </div>
        </div>
        <div class="item-indicator" :class="{ warning: stairs }"></div>
      </div>
      
      <div class="feedback-item" :class="{ active: door }">
        <div class="item-icon">🚪</div>
        <div class="item-content">
          <h4>门/入口</h4>
          <p>{{ door ? '前方有门' : '无门' }}</p>
          <div class="item-detail" v-if="door">
            <span class="type">类型: {{ doorType }}</span>
            <span class="status">状态: {{ doorStatus }}</span>
          </div>
        </div>
        <div class="item-indicator" :class="{ info: door }"></div>
      </div>
    </div>
    
    <div class="system-info">
      <div class="info-item">
        <span class="info-label">处理延迟:</span>
        <span class="info-value">{{ latency }}ms</span>
      </div>
      <div class="info-item">
        <span class="info-label">识别准确率:</span>
        <span class="info-value">{{ accuracy }}%</span>
      </div>
      <div class="info-item">
        <span class="info-label">运行时长:</span>
        <span class="info-value">{{ runtime }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

// 模拟数据
const obstacles = ref(true)
const blindRoad = ref(true)
const trafficLight = ref(true)
const crosswalk = ref(false)
const stairs = ref(false)
const door = ref(false)

const obstacleDistance = ref(120)
const obstacleDirection = ref('右前方')
const lightStatus = ref('红灯')
const countdown = ref(25)
const crosswalkDistance = ref(0)
const stairsType = ref('上楼梯')
const stairsCount = ref(12)
const doorType = ref('推拉门')
const doorStatus = ref('关闭')

const systemActive = ref(true)
const latency = ref(32)
const accuracy = ref(96)
const runtime = ref('00:15:32')

// 计算红绿灯状态对应的样式类
const lightClass = computed(() => {
  if (!trafficLight.value) return ''
  switch (lightStatus.value) {
    case '红灯': return 'danger'
    case '绿灯': return 'success'
    case '黄灯': return 'warning'
    default: return ''
  }
})

// 模拟数据更新
let intervalId = null

onMounted(() => {
  // 模拟数据变化
  intervalId = setInterval(() => {
    // 随机更新一些数据
    if (Math.random() > 0.7) {
      obstacles.value = !obstacles.value
      if (obstacles.value) {
        obstacleDistance.value = Math.floor(Math.random() * 200) + 50
        obstacleDirection.value = ['前方', '左前方', '右前方', '左侧', '右侧'][Math.floor(Math.random() * 5)]
      }
    }
    
    if (Math.random() > 0.8) {
      blindRoad.value = !blindRoad.value
    }
    
    if (Math.random() > 0.9) {
      const lights = ['红灯', '绿灯', '黄灯']
      lightStatus.value = lights[Math.floor(Math.random() * lights.length)]
      countdown.value = Math.floor(Math.random() * 60) + 5
    }
    
    // 更新系统信息
    latency.value = Math.floor(Math.random() * 20) + 25
    accuracy.value = Math.floor(Math.random() * 5) + 94
  }, 3000)
  
  // 更新运行时间
  const startTime = Date.now()
  setInterval(() => {
    const elapsed = Date.now() - startTime
    const hours = Math.floor(elapsed / 3600000)
    const minutes = Math.floor((elapsed % 3600000) / 60000)
    const seconds = Math.floor((elapsed % 60000) / 1000)
    runtime.value = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
  }, 1000)
})

onUnmounted(() => {
  if (intervalId) {
    clearInterval(intervalId)
  }
})
</script>

<style scoped>
.feedback-panel {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 0 0 18px 18px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 100%;
  border: 1px solid rgba(0,0,0,0.08);
}

.panel-header {
  padding: clamp(4px, 0.8vh, 8px) clamp(8px, 1vw, 12px);
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(0,0,0,0.08);
  background: rgba(248, 250, 252, 0.9);
}

.panel-title {
  font-size: clamp(16px, 2vw, 18px);
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.system-status {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 16px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  font-size: clamp(12px, 1.5vw, 14px);
  color: rgba(30, 41, 59, 0.8);
  transition: all 0.3s ease;
}

.system-status.active {
  background: rgba(16, 185, 129, 0.15);
  border-color: rgba(16, 185, 129, 0.3);
  color: #10b981;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(30, 41, 59, 0.3);
}

.system-status.active .status-dot {
  background: #10b981;
  animation: pulse 2s infinite;
}

.status-text {
  font-weight: 500;
}

.feedback-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: clamp(8px, 1.5vh, 15px);
  padding: clamp(8px, 1.2vh, 15px);
  flex: 1;
  overflow-y: auto;
}

.feedback-item {
  background: rgba(0, 0, 0, 0.03);
  border-radius: 12px;
  padding: clamp(8px, 1.5vh, 15px);
  display: flex;
  align-items: center;
  gap: clamp(8px, 1.5vw, 12px);
  position: relative;
  border: 1px solid rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.feedback-item:hover {
  background: rgba(0, 0, 0, 0.05);
  transform: translateY(-2px);
}

.feedback-item.active {
  background: rgba(0, 0, 0, 0.05);
  border-color: rgba(0, 0, 0, 0.12);
}

.item-icon {
  font-size: clamp(20px, 3vw, 24px);
  flex-shrink: 0;
  width: clamp(40px, 5vw, 50px);
  height: clamp(40px, 5vw, 50px);
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 10px;
}

.item-content {
  flex: 1;
}

.item-content h4 {
  font-size: clamp(14px, 2vw, 16px);
  margin: 0 0 4px 0;
  color: #1e293b;
  font-weight: 600;
}

.item-content p {
  font-size: clamp(12px, 1.5vw, 14px);
  margin: 0 0 6px 0;
  color: rgba(30, 41, 59, 0.8);
}

.item-detail {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.item-detail span {
  font-size: clamp(10px, 1.5vw, 12px);
  padding: 2px 6px;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 4px;
  color: rgba(30, 41, 59, 0.7);
}

.item-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(30, 41, 59, 0.2);
  position: absolute;
  top: clamp(10px, 2vh, 15px);
  right: clamp(10px, 2vh, 15px);
}

.item-indicator.warning {
  background: #f59e0b;
  box-shadow: 0 0 10px rgba(245, 158, 11, 0.5);
}

.item-indicator.success {
  background: #10b981;
  box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
}

.item-indicator.danger {
  background: #ef4444;
  box-shadow: 0 0 10px rgba(239, 68, 68, 0.5);
}

.item-indicator.info {
  background: #0ea5e9;
  box-shadow: 0 0 10px rgba(14, 165, 233, 0.5);
}

.system-info {
  display: flex;
  justify-content: space-between;
  padding: clamp(10px, 2vh, 12px) clamp(15px, 2vw, 20px);
  background: rgba(248, 250, 252, 0.9);
  border-top: 1px solid rgba(0,0,0,0.08);
}

.info-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.info-label {
  font-size: clamp(10px, 1.5vw, 12px);
  color: rgba(30, 41, 59, 0.6);
}

.info-value {
  font-size: clamp(12px, 1.5vw, 14px);
  font-weight: 600;
  color: #1e293b;
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
  70% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
  100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

/* 自定义滚动条 */
.feedback-grid::-webkit-scrollbar {
  width: 6px;
}

.feedback-grid::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
}

.feedback-grid::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

.feedback-grid::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .feedback-grid {
    grid-template-columns: 1fr;
  }
}
</style>