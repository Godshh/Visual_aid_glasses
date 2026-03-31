<template>
  <div class="dashboard">
    <div class="dash-header">
      <div class="header-left">
        <h1 class="page-title">实时监控仪表盘</h1>
        <div class="device-tag">
          <span class="pulse-dot"></span>
          <span class="device-name">智能盲人眼镜 #{{ currentDeviceId }}</span>
          <span class="device-badge online">在线</span>
        </div>
      </div>
      <div class="header-right">
        <button class="action-btn call-btn" @click="handleRemoteCall">
          <svg viewBox="0 0 24 24" fill="none"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.63 10.8a19.79 19.79 0 01-3.07-8.67A2 2 0 012.52 0h3a2 2 0 012 1.72c.13 1 .36 1.97.71 2.9a2 2 0 01-.45 2.11L6.91 7.91a16 16 0 006.18 6.18l1.18-.87a2 2 0 012.11-.45c.93.35 1.9.58 2.9.71A2 2 0 0122 16.92z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
          远程喊话
        </button>
        <button class="action-btn emergency-btn" @click="handleEmergencyCall">
          <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.6"/><path d="M12 8v5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="12" cy="16" r="0.8" fill="currentColor"/></svg>
          紧急呼叫
        </button>
      </div>
    </div>

    <div class="dash-body">
      <!-- 左列：视频 + 地图 -->
      <div class="left-col">
        <!-- 实时视角面板 -->
        <div class="panel video-panel">
          <div class="panel-head">
            <div class="panel-head-left">
              <svg viewBox="0 0 24 24" fill="none"><rect x="2" y="7" width="15" height="10" rx="2" stroke="currentColor" stroke-width="1.6"/><path d="M17 9l4-2v10l-4-2V9z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>
              <span>实时第一视角</span>
            </div>
            <div class="panel-head-right">
              <span class="fps-tag">
                <span class="fps-dot"></span>
                LIVE · 30fps
              </span>
              <button class="icon-btn" @click="toggleFullscreen" title="全屏">
                <svg viewBox="0 0 24 24" fill="none"><path d="M8 3H5a2 2 0 00-2 2v3M16 3h3a2 2 0 012 2v3M8 21H5a2 2 0 01-2-2v-3M16 21h3a2 2 0 002-2v-3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
              </button>
            </div>
          </div>
          <div class="video-body">
            <!-- 模拟摄像头画面 -->
            <div class="video-sim">
              <div class="video-scanline"></div>
              <div class="ai-box box-road" :style="{ left: boxRoad.x+'%', top: boxRoad.y+'%', width: boxRoad.w+'%', height: boxRoad.h+'%' }">
                <span class="ai-label road">盲道 97%</span>
              </div>
              <div class="ai-box box-obstacle" v-if="showObstacle" :style="{ left: '60%', top: '35%', width: '18%', height: '25%' }">
                <span class="ai-label obstacle">障碍物 89%</span>
              </div>
              <div class="ai-box box-cross" :style="{ left: crossBox.x+'%', top: crossBox.y+'%', width: crossBox.w+'%', height: crossBox.h+'%' }">
                <span class="ai-label cross">斑马线 94%</span>
              </div>
              <div class="hud-bottom">
                <span class="hud-item">
                  <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.5"/><path d="M12 7v5l3 2.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
                  {{ liveTime }}
                </span>
                <span class="hud-item rec">
                  <span class="rec-dot"></span>
                  REC
                </span>
                <span class="hud-item">
                  <svg viewBox="0 0 24 24" fill="none"><path d="M1 6l8.19 6L1 18" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><path d="M9 6l8.19 6L9 18" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><path d="M17 6h6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><path d="M17 18h6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
                  前置镜头
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 实时位置地图 -->
        <div class="panel map-panel">
          <div class="panel-head">
            <div class="panel-head-left">
              <svg viewBox="0 0 24 24" fill="none"><path d="M12 22s-8-6.686-8-12a8 8 0 0116 0c0 5.314-8 12-8 12z" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="10" r="2.5" stroke="currentColor" stroke-width="1.5"/></svg>
              <span>实时位置</span>
            </div>
            <div class="panel-head-right">
              <span class="coord-tag">{{ lngLat[0].toFixed(4) }}, {{ lngLat[1].toFixed(4) }}</span>
              <button class="icon-btn" @click="centerMap" title="居中">
                <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="1.6"/><path d="M12 2v4M12 18v4M2 12h4M18 12h4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
              </button>
            </div>
          </div>
          <div id="dash-map" class="map-body"></div>
        </div>
      </div>

      <!-- 右列：设备状态 + 日志 -->
      <div class="right-col">
        <!-- 设备状态 -->
        <div class="panel status-panel">
          <div class="panel-head">
            <div class="panel-head-left">
              <svg viewBox="0 0 24 24" fill="none"><rect x="7" y="2" width="10" height="18" rx="2.5" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="17.5" r="1" fill="currentColor"/><path d="M10 5.5h4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
              <span>设备状态</span>
            </div>
            <div class="heartbeat-tag">
              <span class="heart-dot"></span>
              心跳正常
            </div>
          </div>
          <div class="status-body">
            <div class="status-row-item">
              <div class="status-icon-wrap battery">
                <svg viewBox="0 0 24 24" fill="none"><rect x="2" y="7" width="16" height="10" rx="2" stroke="currentColor" stroke-width="1.5"/><path d="M20 10v4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><rect x="4" y="9" :width="(batteryLevel/100)*12" height="6" rx="1" fill="currentColor"/></svg>
              </div>
              <div class="status-text-col">
                <span class="status-label">电量</span>
                <span class="status-val">{{ batteryLevel }}%</span>
              </div>
              <div class="status-bar-wrap">
                <div class="status-bar-track">
                  <div class="status-bar-fill" :class="batteryLevel < 20 ? 'low' : batteryLevel < 50 ? 'mid' : 'ok'" :style="{ width: batteryLevel + '%' }"></div>
                </div>
              </div>
            </div>

            <div class="status-row-item">
              <div class="status-icon-wrap network">
                <svg viewBox="0 0 24 24" fill="none"><path d="M1 6s5-4 11-4 11 4 11 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><path d="M5 10s3.5-3 7-3 7 3 7 3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><path d="M9 14s1.5-1.5 3-1.5 3 1.5 3 1.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="12" cy="17.5" r="1" fill="currentColor"/></svg>
              </div>
              <div class="status-text-col">
                <span class="status-label">网络信号</span>
                <span class="status-val">4G · 强</span>
              </div>
              <div class="status-bar-wrap">
                <div class="status-bar-track">
                  <div class="status-bar-fill ok" style="width: 88%"></div>
                </div>
              </div>
            </div>

            <div class="status-row-item">
              <div class="status-icon-wrap sensor">
                <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="1.5"/><path d="M12 2v4M12 18v4M2 12h4M18 12h4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
              </div>
              <div class="status-text-col">
                <span class="status-label">俯仰角</span>
                <span class="status-val">{{ pitchAngle.toFixed(1) }}°</span>
              </div>
              <div class="angle-badge">前倾</div>
            </div>

            <div class="status-row-item">
              <div class="status-icon-wrap compass">
                <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.5"/><path d="M16.24 7.76l-2.12 6.36-6.36 2.12 2.12-6.36 6.36-2.12z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg>
              </div>
              <div class="status-text-col">
                <span class="status-label">偏航角</span>
                <span class="status-val">{{ yawAngle.toFixed(1) }}°</span>
              </div>
              <div class="angle-badge">东南</div>
            </div>

            <div class="status-row-item">
              <div class="status-icon-wrap speed">
                <svg viewBox="0 0 24 24" fill="none"><path d="M12 2a10 10 0 100 20A10 10 0 0012 2z" stroke="currentColor" stroke-width="1.5"/><path d="M12 12L8 8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/></svg>
              </div>
              <div class="status-text-col">
                <span class="status-label">当前速度</span>
                <span class="status-val">{{ walkSpeed.toFixed(1) }} km/h</span>
              </div>
              <div class="angle-badge">步行</div>
            </div>
          </div>
        </div>

        <!-- 语音提示日志 -->
        <div class="panel logs-panel">
          <div class="panel-head">
            <div class="panel-head-left">
              <svg viewBox="0 0 24 24" fill="none"><path d="M14 3H6a2 2 0 00-2 2v14a2 2 0 002 2h12a2 2 0 002-2V9l-6-6z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M14 3v6h6M8 13h8M8 17h5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
              <span>语音提示日志</span>
            </div>
            <span class="log-count-tag">实时更新</span>
          </div>
          <div class="logs-body">
            <div
              v-for="log in voiceLogs"
              :key="log.id"
              class="log-item"
              :class="{ 'log-new': log.isNew, ['log-' + log.type]: true }"
            >
              <div class="log-type-dot" :class="'dot-' + log.type"></div>
              <div class="log-main">
                <span class="log-content">{{ log.content }}</span>
                <span class="log-time">{{ log.time }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 告警摘要 -->
        <div class="panel alerts-summary-panel">
          <div class="panel-head">
            <div class="panel-head-left">
              <svg viewBox="0 0 24 24" fill="none"><path d="M12 2L3 20h18L12 2z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M12 9v5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="12" cy="17" r="0.8" fill="currentColor"/></svg>
              <span>今日告警摘要</span>
            </div>
          </div>
          <div class="alerts-summary-body">
            <div class="alert-stat-item critical">
              <span class="astat-num">2</span>
              <span class="astat-label">严重</span>
            </div>
            <div class="alert-stat-div"></div>
            <div class="alert-stat-item warning">
              <span class="astat-num">3</span>
              <span class="astat-label">警告</span>
            </div>
            <div class="alert-stat-div"></div>
            <div class="alert-stat-item info">
              <span class="astat-num">8</span>
              <span class="astat-label">提示</span>
            </div>
            <div class="alert-stat-div"></div>
            <div class="alert-stat-item resolved">
              <span class="astat-num">11</span>
              <span class="astat-label">已处理</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { AMAP_CONFIG } from '../config/amap.js'

// ── 响应式状态 ──────────────────────────────────────
const currentDeviceId = ref('001')
const batteryLevel = ref(85)
const pitchAngle = ref(5.2)
const yawAngle = ref(127.8)
const walkSpeed = ref(3.4)
const liveTime = ref('')
const lngLat = ref([116.4074, 39.9042])
const showObstacle = ref(false)

const boxRoad = ref({ x: 20, y: 55, w: 60, h: 30 })
const crossBox = ref({ x: 25, y: 68, w: 50, h: 18 })

let mapInstance = null
let liveMarker = null
let trailPolyline = null
let animTimer = null
let logTimer = null
let mapLoaded = false

// 行走路径（建国门外大街附近）
const walkPath = [
  [116.4320, 39.9082],
  [116.4335, 39.9080],
  [116.4350, 39.9078],
  [116.4362, 39.9075],
  [116.4375, 39.9072],
  [116.4388, 39.9070],
  [116.4400, 39.9068],
  [116.4412, 39.9066],
  [116.4425, 39.9064],
  [116.4438, 39.9062],
  [116.4450, 39.9060],
  [116.4462, 39.9058],
  [116.4474, 39.9056],
  [116.4485, 39.9055],
  [116.4496, 39.9054],
]

let pathIndex = ref(4)
const trailCoords = ref(walkPath.slice(0, 5))

// ── 语音日志数据 ────────────────────────────────────
let logIdCounter = 100
const voiceLogs = ref([
  { id: 1, type: 'warn', content: '前方 10 米有障碍物', time: '14:32:15', isNew: false },
  { id: 2, type: 'nav', content: '请沿盲道直行', time: '14:31:58', isNew: false },
  { id: 3, type: 'nav', content: '前方 50 米到达目的地', time: '14:31:42', isNew: false },
  { id: 4, type: 'warn', content: '注意左侧来车', time: '14:31:20', isNew: false },
  { id: 5, type: 'nav', content: '前方是斑马线，请注意安全', time: '14:30:55', isNew: false },
  { id: 6, type: 'info', content: '已进入建国门外大街路段', time: '14:30:30', isNew: false },
])

const logMessages = [
  { type: 'warn', content: '前方 8 米检测到障碍物' },
  { type: 'nav', content: '请保持直行方向' },
  { type: 'nav', content: '前方路口，请注意来车' },
  { type: 'warn', content: '检测到路面不平，请小心' },
  { type: 'info', content: '已识别周边商户：建设银行' },
  { type: 'nav', content: '前方是斑马线' },
  { type: 'warn', content: '注意右侧自行车道' },
  { type: 'info', content: '当前位置：建国路88号附近' },
  { type: 'nav', content: '请在前方路口左转' },
  { type: 'info', content: '已到达设定目标区域' },
]

// ── 时间更新 ────────────────────────────────────────
const updateTime = () => {
  const now = new Date()
  liveTime.value = now.toLocaleTimeString('zh-CN', { hour12: false })
}

// ── AMap 初始化 ─────────────────────────────────────
const loadAMap = () => {
  return new Promise((resolve) => {
    if (window.AMap) { resolve(); return }
    window._AMapSecurityConfig = { securityJsCode: AMAP_CONFIG.securityCode }
    const script = document.createElement('script')
    script.src = `https://webapi.amap.com/maps?v=2.0&key=${AMAP_CONFIG.key}`
    script.onload = () => resolve()
    document.head.appendChild(script)
  })
}

const initMap = async () => {
  await loadAMap()
  mapLoaded = true

  const startCoord = walkPath[4]
  mapInstance = new window.AMap.Map('dash-map', {
    zoom: 16,
    center: startCoord,
    mapStyle: 'amap://styles/normal',
  })

  mapInstance.addControl(new window.AMap.Scale())

  // 轨迹折线
  trailPolyline = new window.AMap.Polyline({
    path: trailCoords.value.map(c => new window.AMap.LngLat(c[0], c[1])),
    strokeColor: '#3b82f6',
    strokeWeight: 4,
    strokeOpacity: 0.8,
    showDir: true,
  })
  mapInstance.add(trailPolyline)

  // 当前位置标记
  const markerContent = `<div style="
    width:18px;height:18px;border-radius:50%;
    background:#3b82f6;border:3px solid #fff;
    box-shadow:0 0 0 4px rgba(59,130,246,0.3);
    animation:dash-pulse 2s infinite;
  "></div>`

  const styleEl = document.createElement('style')
  styleEl.textContent = `@keyframes dash-pulse{0%,100%{box-shadow:0 0 0 4px rgba(59,130,246,0.3)}50%{box-shadow:0 0 0 8px rgba(59,130,246,0.15)}}`
  document.head.appendChild(styleEl)

  liveMarker = new window.AMap.Marker({
    position: new window.AMap.LngLat(startCoord[0], startCoord[1]),
    content: markerContent,
    offset: new window.AMap.Pixel(-9, -9),
  })
  mapInstance.add(liveMarker)
  lngLat.value = [startCoord[0], startCoord[1]]
}

const centerMap = () => {
  if (mapInstance && liveMarker) {
    mapInstance.setCenter(liveMarker.getPosition())
    mapInstance.setZoom(16)
  }
}

// ── 位置移动模拟 ────────────────────────────────────
const moveLiveMarker = () => {
  if (!mapLoaded || pathIndex.value >= walkPath.length - 1) {
    pathIndex.value = 0
    trailCoords.value = [walkPath[0]]
    return
  }
  pathIndex.value++
  const coord = walkPath[pathIndex.value]
  lngLat.value = [coord[0], coord[1]]
  trailCoords.value.push(coord)

  if (liveMarker) {
    liveMarker.setPosition(new window.AMap.LngLat(coord[0], coord[1]))
  }
  if (trailPolyline) {
    trailPolyline.setPath(trailCoords.value.map(c => new window.AMap.LngLat(c[0], c[1])))
  }

  // 随机更新传感器数据
  batteryLevel.value = Math.max(0, batteryLevel.value - 0.05)
  pitchAngle.value = 4 + Math.random() * 4
  yawAngle.value = 120 + Math.random() * 20
  walkSpeed.value = 2.8 + Math.random() * 1.5
  showObstacle.value = Math.random() > 0.7
}

// ── 日志自动追加 ────────────────────────────────────
const appendLog = () => {
  const msg = logMessages[Math.floor(Math.random() * logMessages.length)]
  const now = new Date()
  const timeStr = now.toLocaleTimeString('zh-CN', { hour12: false })

  voiceLogs.value.unshift({
    id: ++logIdCounter,
    type: msg.type,
    content: msg.content,
    time: timeStr,
    isNew: true,
  })

  // 最多保留 20 条
  if (voiceLogs.value.length > 20) voiceLogs.value.pop()

  // 新消息 2s 后去掉高亮
  setTimeout(() => {
    const entry = voiceLogs.value.find(l => l.id === logIdCounter)
    if (entry) entry.isNew = false
  }, 2000)
}

// ── 操作按钮 ────────────────────────────────────────
const handleRemoteCall = () => {
  window.alert('远程喊话：将打开语音输入界面')
}
const handleEmergencyCall = () => {
  if (window.confirm('确定要发起紧急呼叫吗？')) {
    window.alert('紧急呼叫已发送')
  }
}
const toggleFullscreen = () => {
  const el = document.querySelector('.video-sim')
  if (el) {
    if (!document.fullscreenElement) el.requestFullscreen?.()
    else document.exitFullscreen?.()
  }
}

// ── 生命周期 ────────────────────────────────────────
onMounted(() => {
  updateTime()
  const clockTimer = setInterval(updateTime, 1000)
  initMap()

  animTimer = setInterval(moveLiveMarker, 2000)
  logTimer = setInterval(appendLog, 6000)

  onUnmounted(() => {
    clearInterval(clockTimer)
    clearInterval(animTimer)
    clearInterval(logTimer)
    if (mapInstance) mapInstance.destroy()
  })
})
</script>

<style scoped>
/* ── 整体布局 ── */
.dashboard {
  padding: 20px 20px 16px 24px;
  background: #f1f5f9;
  height: calc(100vh - 52px);
  display: flex;
  flex-direction: column;
  gap: 14px;
  overflow: hidden;
}

.dash-header {
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

.device-tag {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 12px;
  background: #fff;
  border-radius: 20px;
  border: 1px solid #e2e8f0;
  font-size: 13px;
  color: #334155;
}

.pulse-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #22c55e;
  box-shadow: 0 0 0 3px rgba(34,197,94,0.2);
  animation: pulse-anim 2s infinite;
}

.device-name { font-weight: 500; }

.device-badge {
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 600;
}
.device-badge.online { background: #dcfce7; color: #166534; }

.header-right {
  display: flex;
  gap: 10px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 8px 16px;
  border: none;
  border-radius: 9px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

.call-btn {
  background: #3b82f6;
  color: #fff;
}
.call-btn:hover {
  background: #2563eb;
  box-shadow: 0 4px 12px rgba(59,130,246,0.35);
  transform: translateY(-1px);
}

.emergency-btn {
  background: #ef4444;
  color: #fff;
}
.emergency-btn:hover {
  background: #dc2626;
  box-shadow: 0 4px 12px rgba(239,68,68,0.35);
  transform: translateY(-1px);
}

/* ── 主体两列 ── */
.dash-body {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 14px;
  flex: 1;
  min-height: 0;
}

.left-col {
  display: flex;
  flex-direction: column;
  gap: 14px;
  min-height: 0;
}

.right-col {
  display: flex;
  flex-direction: column;
  gap: 14px;
  min-height: 0;
  overflow-y: auto;
}

.right-col::-webkit-scrollbar { width: 4px; }
.right-col::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 2px; }

/* ── 面板通用 ── */
.panel {
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.video-panel { flex: 1; min-height: 0; }
.map-panel { flex: 1; min-height: 0; }

.panel-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 11px 16px;
  border-bottom: 1px solid #f1f5f9;
  flex-shrink: 0;
}

.panel-head-left {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13.5px;
  font-weight: 600;
  color: #1e293b;
}

.panel-head-left svg {
  width: 16px;
  height: 16px;
  color: #64748b;
}

.panel-head-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.fps-tag {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  font-weight: 600;
  color: #22c55e;
  background: #f0fdf4;
  padding: 3px 8px;
  border-radius: 6px;
  border: 1px solid #bbf7d0;
}

.fps-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #22c55e;
  animation: pulse-anim 1.5s infinite;
}

.icon-btn {
  width: 30px;
  height: 30px;
  border: 1px solid #e2e8f0;
  border-radius: 7px;
  background: #f8fafc;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  transition: all 0.2s ease;
}

.icon-btn svg { width: 15px; height: 15px; }

.icon-btn:hover {
  background: #f0f9ff;
  border-color: #bae6fd;
  color: #0369a1;
}

.coord-tag {
  font-size: 11px;
  font-family: 'Consolas', monospace;
  color: #64748b;
  background: #f8fafc;
  padding: 3px 8px;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
}

/* ── 视频模拟区 ── */
.video-body {
  flex: 1;
  min-height: 0;
  position: relative;
}

.video-sim {
  width: 100%;
  height: 100%;
  background: linear-gradient(170deg, #1a2035 0%, #0f1629 40%, #1a2a20 100%);
  position: relative;
  overflow: hidden;
}

.video-scanline {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(255,255,255,0.012) 2px,
    rgba(255,255,255,0.012) 4px
  );
  pointer-events: none;
  z-index: 1;
}

.ai-box {
  position: absolute;
  border: 1.5px solid;
  border-radius: 3px;
  z-index: 2;
}

.box-road { border-color: rgba(34,197,94,0.8); }
.box-obstacle { border-color: rgba(239,68,68,0.9); }
.box-cross { border-color: rgba(59,130,246,0.8); }

.ai-label {
  position: absolute;
  top: -20px;
  left: 0;
  font-size: 10px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 3px;
  white-space: nowrap;
}

.ai-label.road { background: rgba(34,197,94,0.9); color: #fff; }
.ai-label.obstacle { background: rgba(239,68,68,0.9); color: #fff; }
.ai-label.cross { background: rgba(59,130,246,0.9); color: #fff; }

.hud-bottom {
  position: absolute;
  bottom: 12px;
  left: 12px;
  right: 12px;
  display: flex;
  align-items: center;
  gap: 12px;
  z-index: 3;
}

.hud-item {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  font-weight: 500;
  color: rgba(255,255,255,0.8);
  background: rgba(0,0,0,0.45);
  padding: 4px 8px;
  border-radius: 5px;
  backdrop-filter: blur(4px);
}

.hud-item svg { width: 12px; height: 12px; }

.hud-item.rec { color: #ef4444; }

.rec-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #ef4444;
  animation: pulse-anim 1s infinite;
}

/* ── 地图 ── */
.map-body {
  flex: 1;
  min-height: 0;
}

/* ── 设备状态 ── */
.status-panel { flex-shrink: 0; }

.heartbeat-tag {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  font-weight: 600;
  color: #22c55e;
}

.heart-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #22c55e;
  animation: pulse-anim 1.5s infinite;
}

.status-body {
  padding: 8px 14px 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.status-row-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  background: #f8fafc;
  border-radius: 9px;
}

.status-icon-wrap {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.status-icon-wrap svg { width: 18px; height: 18px; }

.battery { background: #dbeafe; color: #2563eb; }
.network { background: #dcfce7; color: #16a34a; }
.sensor  { background: #fef3c7; color: #d97706; }
.compass { background: #ede9fe; color: #7c3aed; }
.speed   { background: #fce7f3; color: #db2777; }

.status-text-col {
  display: flex;
  flex-direction: column;
  gap: 1px;
  flex: 1;
  min-width: 0;
}

.status-label {
  font-size: 11px;
  color: #94a3b8;
}

.status-val {
  font-size: 13px;
  font-weight: 700;
  color: #1e293b;
}

.status-bar-wrap {
  width: 70px;
  flex-shrink: 0;
}

.status-bar-track {
  height: 5px;
  background: #e2e8f0;
  border-radius: 3px;
  overflow: hidden;
}

.status-bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}

.status-bar-fill.ok  { background: #22c55e; }
.status-bar-fill.mid { background: #f59e0b; }
.status-bar-fill.low { background: #ef4444; }

.angle-badge {
  font-size: 11px;
  font-weight: 600;
  padding: 2px 7px;
  background: #f1f5f9;
  border-radius: 6px;
  color: #64748b;
  flex-shrink: 0;
}

/* ── 日志面板 ── */
.logs-panel { flex: 1; min-height: 0; }

.log-count-tag {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  color: #3b82f6;
  font-weight: 600;
}

.logs-body {
  flex: 1;
  overflow-y: auto;
  min-height: 0;
  padding: 6px 0;
}

.logs-body::-webkit-scrollbar { width: 3px; }
.logs-body::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 2px; }

.log-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 8px 16px;
  border-bottom: 1px solid #f8fafc;
  transition: background 0.2s ease;
}

.log-item:hover { background: #f8fafc; }

.log-item.log-new {
  background: #eff6ff;
  animation: log-flash 0.4s ease;
}

@keyframes log-flash {
  from { background: #dbeafe; }
  to   { background: #eff6ff; }
}

.log-type-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  margin-top: 5px;
  flex-shrink: 0;
}

.dot-warn { background: #f59e0b; }
.dot-nav  { background: #3b82f6; }
.dot-info { background: #22c55e; }

.log-main {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex: 1;
  gap: 8px;
}

.log-content {
  font-size: 13px;
  color: #1e293b;
  line-height: 1.4;
}

.log-time {
  font-size: 11px;
  color: #94a3b8;
  font-family: 'Consolas', monospace;
  flex-shrink: 0;
}

/* ── 告警摘要 ── */
.alerts-summary-panel { flex-shrink: 0; }

.alerts-summary-body {
  display: flex;
  align-items: center;
  padding: 14px 16px;
  gap: 0;
}

.alert-stat-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
}

.astat-num {
  font-size: 22px;
  font-weight: 700;
}

.astat-label {
  font-size: 11px;
  color: #94a3b8;
}

.alert-stat-item.critical .astat-num { color: #ef4444; }
.alert-stat-item.warning  .astat-num { color: #f59e0b; }
.alert-stat-item.info     .astat-num { color: #3b82f6; }
.alert-stat-item.resolved .astat-num { color: #22c55e; }

.alert-stat-div {
  width: 1px;
  height: 32px;
  background: #e2e8f0;
}

@keyframes pulse-anim {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}
</style>
