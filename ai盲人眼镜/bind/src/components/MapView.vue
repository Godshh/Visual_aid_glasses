<!-- src/components/MapView.vue  —— 地图组件 -->
<template>
  <div class="map-container">
    <div class="nav-panel">
      <div class="nav-title">目的地导航</div>
      <div class="nav-controls">
        <input
          v-model="destination"
          type="text"
          class="nav-input"
          placeholder="请输入目的地，如：南京南站"
        />
        <button @click="startNavigation" class="nav-btn">开始导航</button>
      </div>
      <div v-if="totalDistanceKm" class="nav-summary">
        全程距离约 {{ totalDistanceKm }} 公里，预计 {{ totalTimeMin }} 分钟
      </div>
      <div v-if="remainingDistanceKm" class="nav-summary secondary">
        当前剩余约 {{ remainingDistanceKm }} 公里，预计 {{ remainingTimeMin }} 分钟
      </div>
      <div v-if="routeSummary" class="nav-summary">
        {{ routeSummary }}
      </div>
      <div v-if="totalDistanceKm" class="nav-view-buttons">
        <button @click="showFullRoute" class="nav-toggle-btn">查看全程</button>
        <button @click="showCurrentView" class="nav-toggle-btn secondary">回到当前路况</button>
      </div>
    </div>
    <div class="map-wrapper">
      <div id="amap-container" class="amap-container"></div>
      <div class="map-overlay">
        <div class="map-coords">
          <div class="coord-item">纬度: {{ currentLat || '--' }}</div>
          <div class="coord-item">经度: {{ currentLng || '--' }}</div>
        </div>
        <div class="map-controls">
          <button @click="resetView" class="control-btn">重置视角</button>
          <button @click="toggle3D" class="control-btn">{{ is3D ? '2D视图' : '3D视图' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, inject } from 'vue'
import { AMAP_CONFIG, getCurrentPosition } from '../config/amap.js'

// 1. 注入事件总线 (用于接收 ChatAssistant 的语音指令)
const eventBus = inject('eventBus')

const currentLat = ref('39.9042')
const currentLng = ref('116.4074')
const is3D = ref(true)
const destination = ref('')
const routeSummary = ref('')
const totalDistanceKm = ref('')
const remainingDistanceKm = ref('')
const totalTimeMin = ref('')
const remainingTimeMin = ref('')

let map = null
let marker = null
let geocoder = null
let driving = null
let destinationLngLat = null
let destinationMarker = null
let lastRoute = null

// 加载高德地图API
const loadAmapScript = () => {
  return new Promise((resolve, reject) => {
    if (window.AMap) {
      resolve(window.AMap)
      return
    }
    window._AMapSecurityConfig = {
      securityJsCode: AMAP_CONFIG.securityCode
    }
    const script = document.createElement('script')
    script.type = 'text/javascript'
    script.async = true
    script.src = `https://webapi.amap.com/maps?v=2.0&key=${AMAP_CONFIG.key}&plugin=AMap.Scale,AMap.ToolBar,AMap.ControlBar,AMap.HawkEye,AMap.MapType,AMap.Geolocation,AMap.Driving,AMap.Geocoder`
    
    script.onerror = (error) => {
      console.error('高德地图加载失败:', error)
      reject(error)
    }
    script.onload = () => {
      resolve(window.AMap)
    }
    document.head.appendChild(script)
  })
}

const initMap = async () => {
  try {
    try {
      const position = await getCurrentPosition()
      currentLng.value = position.longitude.toFixed(4)
      currentLat.value = position.latitude.toFixed(4)
    } catch (error) {
      console.warn('获取当前位置失败，使用默认位置:', error)
      currentLng.value = AMAP_CONFIG.defaultCenter[0].toFixed(4)
      currentLat.value = AMAP_CONFIG.defaultCenter[1].toFixed(4)
    }
    
    const AMap = await loadAmapScript()
    
    map = new AMap.Map('amap-container', {
      zoom: AMAP_CONFIG.defaultZoom,
      center: [currentLng.value, currentLat.value],
      viewMode: AMAP_CONFIG.viewMode,
      pitch: AMAP_CONFIG.pitch,
      rotation: AMAP_CONFIG.rotation,
      showLabel: AMAP_CONFIG.showLabel,
      showBuildingBlock: AMAP_CONFIG.showBuildingBlock,
      buildingAnimation: AMAP_CONFIG.buildingAnimation,
      expandZoomRange: true,
      zooms: AMAP_CONFIG.zooms,
      mapStyle: AMAP_CONFIG.mapStyle,
      features: ['bg', 'road', 'building', 'point'],
      skyColor: AMAP_CONFIG.skyColor
    })
    
    map.addControl(new AMap.Scale())
    map.addControl(new AMap.ToolBar({ position: 'RB' }))
    map.addControl(new AMap.ControlBar({ position: { top: '10px', right: '10px' } }))
    map.addControl(new AMap.Geolocation({ position: 'LB' }))
    
    marker = new AMap.Marker({
      position: [currentLng.value, currentLat.value],
      title: '当前位置',
      animation: 'AMAP_ANIMATION_DROP'
    })
    
    map.add(marker)
    geocoder = new AMap.Geocoder()
    driving = new AMap.Driving({
      map,
      showTraffic: true,
      hideMarkers: false, // 改为 false，让 Driving 插件自动处理起点/终点标记，适应"从A到B"场景
      autoFitView: false
    })
    
    setInterval(() => {
      updatePosition()
    }, 3000)
    
  } catch (error) {
    console.error('地图初始化失败:', error)
    showFallbackMap()
  }
}

const handleRouteResult = (driveStatus, driveResult, isInitial) => {
  if (driveStatus === 'complete' && driveResult && driveResult.routes && driveResult.routes.length) {
    const route = driveResult.routes[0]
    lastRoute = route
    const distanceKm = (route.distance / 1000).toFixed(1)
    const timeMin = Math.round(route.time / 60)

    remainingDistanceKm.value = distanceKm
    remainingTimeMin.value = timeMin

    if (isInitial || !totalDistanceKm.value) {
      totalDistanceKm.value = distanceKm
      totalTimeMin.value = timeMin
    }

    routeSummary.value = `全程约 ${totalDistanceKm.value} 公里，当前剩余约 ${remainingDistanceKm.value} 公里，预计耗时约 ${remainingTimeMin.value} 分钟`
  } else {
    routeSummary.value = '规划路线失败，请检查网络或目的地'
  }
}

const updatePosition = () => {
  if (!map || !marker) return
  
  const lat = parseFloat(currentLat.value)
  const lng = parseFloat(currentLng.value)
  // 模拟微小移动
  const newLat = lat + (Math.random() - 0.5) * 0.0001
  const newLng = lng + (Math.random() - 0.5) * 0.0001
  
  currentLat.value = newLat.toFixed(4)
  currentLng.value = newLng.toFixed(4)
  
  marker.setPosition([newLng, newLat])
  
  // 如果当前处于导航模式且有目的地坐标（仅针对"当前位置->目的地"模式的更新）
  if (destinationLngLat && driving && !routeSummary.value.includes('全程')) {
    const origin = new AMap.LngLat(newLng, newLat)
    driving.search(origin, destinationLngLat, (driveStatus, driveResult) => {
      handleRouteResult(driveStatus, driveResult, false)
    })
  }
}

// 核心功能 1: 执行路径规划 (支持 关键字->关键字 或 坐标->关键字)
const executeRouting = (startKeyword, endKeyword) => {
  if (!map || !driving) return

  // 重置状态
  totalDistanceKm.value = ''
  remainingDistanceKm.value = ''
  routeSummary.value = '正在规划路线...'
  lastRoute = null
  
  // 清理之前的覆盖物 (Driving 插件会自动清理它生成的，但我们需要清理手动添加的)
  if (destinationMarker) {
    map.remove(destinationMarker)
    destinationMarker = null
  }
  
  // 构造查询参数
  // AMap.Driving 支持 [{keyword: '起点'}, {keyword: '终点'}] 这种格式
  const points = []
  
  if (startKeyword) {
    // 场景 A: 语音指令 "从 [北京南站] 去 [天安门]"
    points.push({ keyword: startKeyword })
  } else {
    // 场景 B: 语音指令 "去 [天安门]" (默认从当前位置出发)
    points.push(new AMap.LngLat(parseFloat(currentLng.value), parseFloat(currentLat.value)))
  }
  
  // 终点
  points.push({ keyword: endKeyword })

  // 调用高德 API
  driving.search(points, (status, result) => {
    if (status === 'complete') {
      // 如果是普通导航，记录一下终点坐标，以便 updatePosition 更新剩余距离
      if (!startKeyword && result.routes && result.routes[0]) {
         // 注意：Driving 插件自动返回的结构里解析终点坐标比较复杂，
         // 这里简化处理，直接交给 handleRouteResult 展示文本
      }
      handleRouteResult(status, result, true)
      showFullRoute() // 自动缩放视野
    } else {
      routeSummary.value = `无法规划路线: 未找到 "${startKeyword || '当前位置'}" 或 "${endKeyword}"`
      console.warn('规划失败', result)
    }
  })
}

// 核心功能 2: 处理语音指令
const handleVoiceCommand = (text) => {
  if (!text) return
  console.log('地图收到语音指令:', text)
  
  // 移除标点符号，防止正则匹配失败
  const cleanText = text.replace(/[，。！？,.!?]/g, ' ').trim()

  // 正则匹配策略
  // 模式 1: "从 A 到 B"
  const patternFull = /(?:从|from)\s*(\S+)\s*(?:去|到|navigate to)\s*(\S+)/i
  // 模式 2: "去 B" / "导航到 B"
  const patternDestOnly = /(?:去|到|导航到|navigate to)\s*(\S+)/i

  const matchFull = cleanText.match(patternFull)
  const matchDest = cleanText.match(patternDestOnly)

  if (matchFull) {
    const startPoint = matchFull[1].trim()
    const endPoint = matchFull[2].trim()
    destination.value = endPoint // 更新输入框显示
    executeRouting(startPoint, endPoint)
  } else if (matchDest) {
    const endPoint = matchDest[1].trim()
    destination.value = endPoint
    executeRouting(null, endPoint)
  }
}

// 按钮点击触发的导航（保持兼容）
const startNavigation = () => {
  if (!destination.value.trim()) return
  executeRouting(null, destination.value)
}

const resetView = () => {
  if (!map) return
  map.setZoomAndCenter(AMAP_CONFIG.defaultZoom, [currentLng.value, currentLat.value])
  map.setPitch(is3D.value ? AMAP_CONFIG.pitch : 0)
  map.setRotation(AMAP_CONFIG.rotation)
}

const toggle3D = () => {
  if (!map) return
  is3D.value = !is3D.value
  map.setViewMode(is3D.value ? '3D' : '2D')
  map.setPitch(is3D.value ? AMAP_CONFIG.pitch : 0)
}

const showFullRoute = () => {
  if (!map || !lastRoute) return
  const path = []
  lastRoute.steps.forEach((step) => {
    if (step.path && step.path.length) {
      path.push(...step.path)
    }
  })
  if (path.length) {
    map.setFitView(path)
  }
}

const showCurrentView = () => {
  resetView()
}

const showFallbackMap = () => {
  const container = document.getElementById('amap-container')
  if (container) {
    container.innerHTML = `
      <div class="fallback-map">
        <div class="map-icon">🗺️</div>
        <div class="map-text">地图加载失败，显示模拟地图</div>
        <div class="map-coords">
          <div class="coord-item">纬度: ${currentLat.value}</div>
          <div class="coord-item">经度: ${currentLng.value}</div>
        </div>
      </div>
    `
  }
}

onMounted(() => {
  initMap()
  // 注册事件监听
  if (eventBus) {
    eventBus.on('send-text-cmd', handleVoiceCommand)
  }
})

onUnmounted(() => {
  if (map) {
    map.destroy()
  }
  // 销毁事件监听
  if (eventBus) {
    eventBus.off('send-text-cmd', handleVoiceCommand)
  }
})
</script>
<style scoped>
.map-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: transparent;
  border-radius: 12px;
  overflow: hidden;
}

.nav-panel {
  padding: 12px 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: rgba(255, 255, 255, 0.95);
  border-bottom: 1px solid rgba(59, 130, 246, 0.2);
}

.nav-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: #1e293b;
}

.nav-controls {
  display: flex;
  gap: 8px;
}

.nav-input {
  flex: 1;
  padding: 6px 10px;
  border-radius: 6px;
  border: 1px solid rgba(0, 0, 0, 0.15);
  background: rgba(255, 255, 255, 0.9);
  color: #1e293b;
  font-size: 0.9rem;
}

.nav-input::placeholder {
  color: rgba(100, 116, 139, 0.8);
}

.nav-btn {
  padding: 6px 14px;
  border-radius: 6px;
  border: none;
  background: rgba(34, 197, 94, 0.9);
  color: white;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-btn:hover {
  background: rgba(22, 163, 74, 1);
  transform: translateY(-1px);
}

.nav-btn:active {
  transform: translateY(0);
}

.nav-summary {
  font-size: 0.85rem;
  color: #475569;
}

.nav-summary.secondary {
  color: #6366f1;
}

.nav-view-buttons {
  display: flex;
  gap: 8px;
  margin-top: 4px;
}

.nav-toggle-btn {
  padding: 4px 10px;
  border-radius: 6px;
  border: 1px solid rgba(0, 0, 0, 0.15);
  background: transparent;
  color: #1e293b;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-toggle-btn:hover {
  background: rgba(59, 130, 246, 0.15);
  transform: translateY(-1px);
}

.nav-toggle-btn:active {
  transform: translateY(0);
}

.nav-toggle-btn.secondary {
  border-color: rgba(0, 0, 0, 0.1);
  background: rgba(248, 250, 252, 0.9);
}

.map-wrapper {
  flex: 1;
  position: relative;
  overflow: hidden;
}

.amap-container {
  width: 100%;
  height: 100%;
}

.map-overlay {
  position: absolute;
  bottom: 20px;
  left: 20px;
  z-index: 100;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.map-coords {
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: rgba(255, 255, 255, 0.9);
  padding: 12px 20px;
  border-radius: 8px;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.coord-item {
  font-size: 0.9rem;
  font-family: 'Courier New', monospace;
  color: #3b82f6;
}

.map-controls {
  display: flex;
  gap: 10px;
}

.control-btn {
  padding: 8px 16px;
  background: rgba(59, 130, 246, 0.8);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s ease;
  backdrop-filter: blur(5px);
}

.control-btn:hover {
  background: rgba(59, 130, 246, 1);
  transform: translateY(-2px);
}

.control-btn:active {
  transform: translateY(0);
}

/* 备用地图样式 */
.fallback-map {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
  background: linear-gradient(135deg, #e2e8f0 0%, #f8fafc 100%);
  color: #1e293b;
  text-align: center;
  padding: 20px;
}

.map-icon {
  font-size: 4rem;
  opacity: 0.8;
  animation: pulse 3s infinite ease-in-out;
}

.map-text {
  font-size: 1.2rem;
  font-weight: 500;
  opacity: 0.9;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.8; }
  50% { transform: scale(1.1); opacity: 1; }
}
</style>
