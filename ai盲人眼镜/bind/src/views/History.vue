<template>
  <div class="history">
    <!-- ── 顶部工具栏 ── -->
    <div class="toolbar">
      <div class="toolbar-left">
        <div class="page-title-wrap">
          <svg viewBox="0 0 24 24" fill="none" class="title-icon"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.7"/><path d="M12 7v5l3 3" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <h1 class="page-title">历史轨迹回放</h1>
        </div>
        <div class="meta-tags">
          <span class="tag device">
            <svg viewBox="0 0 24 24" fill="none"><rect x="7" y="2" width="10" height="18" rx="2.5" stroke="currentColor" stroke-width="1.5"/><circle cx="12" cy="17.5" r="1" fill="currentColor"/></svg>
            智能盲人眼镜 #001
          </span>
          <span class="tag date">{{ currentDayData.label }}</span>
          <span class="tag stats">
            <svg viewBox="0 0 24 24" fill="none"><path d="M3 3v18h18" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><path d="M7 16l4-6 4 4 4-8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
            共 {{ currentDayData.routes.length }} 条路线 · {{ currentDayData.totalDist }} 公里
          </span>
        </div>
      </div>
      <div class="toolbar-right">
        <div class="date-tabs">
          <button
            v-for="opt in dateOptions"
            :key="opt.value"
            :class="['date-tab', { active: selectedDate === opt.value }]"
            @click="switchDate(opt.value)"
          >{{ opt.label }}</button>
        </div>
        <button class="btn btn-outline" @click="exportGPX">
          <svg viewBox="0 0 24 24" fill="none"><path d="M12 3v13M7 11l5 5 5-5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M4 20h16" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
          导出 GPX
        </button>
      </div>
    </div>

    <!-- ── 主内容 ── -->
    <div class="content">
      <!-- 左：地图 -->
      <div class="map-col">
        <div class="card map-card">
          <div class="card-header">
            <div class="card-title">
              <svg viewBox="0 0 24 24" fill="none"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="9" r="2.5" stroke="currentColor" stroke-width="1.5"/></svg>
              步行轨迹地图
            </div>
            <div class="map-hd-right">
              <!-- 路线图例 -->
              <div class="route-legend">
                <div
                  v-for="(route, idx) in currentDayData.routes"
                  :key="route.id"
                  :class="['legend-pill', { dimmed: activeRouteId !== null && activeRouteId !== route.id }]"
                  @click="toggleRoute(route.id)"
                >
                  <span class="pill-dot" :style="{ background: routeColors[idx % routeColors.length] }"></span>
                  {{ route.timeRange }}
                </div>
              </div>
              <button class="map-tool-btn" @click="fitAllRoutes" title="全部显示">
                <svg viewBox="0 0 24 24" fill="none"><path d="M3 7V4h3M21 7V4h-3M3 17v3h3M21 17v3h-3" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>
              </button>
            </div>
          </div>
          <div class="amap-wrap">
            <div id="history-amap" class="amap-container"></div>
            <div v-if="mapLoading" class="map-loading">
              <div class="loading-spinner"></div>
              <span>地图加载中...</span>
            </div>

            <!-- ── 7天历史面板（悬浮在地图左上角）── -->
            <div class="history-picker" :class="{ expanded: showHistoryPicker }">
              <button class="picker-toggle" @click="showHistoryPicker = !showHistoryPicker">
                <svg viewBox="0 0 24 24" fill="none"><rect x="3" y="4" width="18" height="18" rx="2" stroke="currentColor" stroke-width="1.6"/><path d="M16 2v4M8 2v4M3 10h18" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
                <span>历史路线</span>
                <svg class="toggle-arrow" :class="{ rotated: showHistoryPicker }" viewBox="0 0 24 24" fill="none"><path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
              </button>
              <div class="picker-list" v-if="showHistoryPicker">
                <div class="picker-label">最近7天路线记录</div>
                <div
                  v-for="day in historyDays"
                  :key="day.key"
                  class="picker-day-row"
                  :class="{ active: selectedDate === day.key }"
                  @click="switchDate(day.key)"
                >
                  <div class="picker-day-left">
                    <span class="picker-day-date">{{ day.displayDate }}</span>
                    <span class="picker-day-label">{{ day.weekday }}</span>
                  </div>
                  <div class="picker-day-right">
                    <span class="picker-day-routes">{{ day.routeCount }}条路线</span>
                    <span class="picker-day-dist">{{ day.dist }}km</span>
                    <span v-if="day.alerts > 0" class="picker-day-alert">{{ day.alerts }}警</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右：路线列表 + 事件 -->
      <div class="side-col">
        <!-- 统计 -->
        <div class="card stats-card">
          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-value">{{ currentDayData.routes.length }}</div>
              <div class="stat-label">出行次数</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ currentDayData.totalDist }}</div>
              <div class="stat-label">公里</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ currentDayData.totalDuration }}</div>
              <div class="stat-label">时长</div>
            </div>
            <div class="stat-item">
              <div class="stat-value danger">{{ currentDayData.alerts }}</div>
              <div class="stat-label">告警</div>
            </div>
          </div>
        </div>

        <!-- 路线列表 -->
        <div class="card routes-card">
          <div class="card-header">
            <div class="card-title">
              <svg viewBox="0 0 24 24" fill="none"><path d="M3 6h18M3 12h12M3 18h8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
              出行路线
            </div>
          </div>
          <div class="routes-list">
            <div
              v-for="(route, idx) in currentDayData.routes"
              :key="route.id"
              :class="['route-item', { active: activeRouteId === route.id }]"
              @click="selectRoute(route)"
            >
              <div class="route-color-bar" :style="{ background: routeColors[idx % routeColors.length] }"></div>
              <div class="route-body">
                <div class="route-header-row">
                  <span class="route-title">第 {{ idx + 1 }} 次出行</span>
                  <span class="route-time">{{ route.timeRange }}</span>
                </div>
                <div class="route-path">
                  <span class="route-from">{{ route.from }}</span>
                  <svg viewBox="0 0 24 24" fill="none" class="route-arrow"><path d="M5 12h14M14 7l5 5-5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  <span class="route-to">{{ route.to }}</span>
                </div>
                <div class="route-meta">
                  <span>{{ route.dist }} 公里</span>
                  <span>{{ route.duration }}</span>
                  <span v-if="route.events.length" class="route-event-cnt">{{ route.events.length }} 个事件</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 当前路线事件 -->
        <div class="card events-card" v-if="selectedRoute">
          <div class="card-header">
            <div class="card-title">
              <svg viewBox="0 0 24 24" fill="none"><path d="M12 2L3 20h18L12 2z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M12 9v5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="12" cy="17" r="0.8" fill="currentColor"/></svg>
              路线事件
            </div>
            <span class="event-count">{{ selectedRoute.events.length }} 条</span>
          </div>
          <div class="events-list">
            <div
              v-for="ev in selectedRoute.events"
              :key="ev.id"
              :class="['event-item', ev.type]"
              @click="flyToEvent(ev)"
            >
              <span class="event-dot" :class="ev.type"></span>
              <div class="event-body">
                <div class="event-row">
                  <span class="event-title">{{ ev.title }}</span>
                  <span class="event-time-badge">{{ ev.time }}</span>
                </div>
                <div class="event-desc">{{ ev.desc }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { AMAP_CONFIG } from '../config/amap.js'

// ── 路线颜色 ──
const routeColors = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ef4444']

// ── 两天的模拟数据（真实北京步行路径坐标，沿道路） ──
// 坐标均为北京二环附近可步行路段，不穿越建筑
const daysData = {
  today: {
    label: '今天',
    totalDist: '7.2',
    totalDuration: '2h 48m',
    alerts: 2,
    routes: [
      {
        id: 'r1',
        timeRange: '08:15 - 09:02',
        from: '建国门地铁站',
        to: '朝阳门外大街',
        dist: '2.3',
        duration: '47分钟',
        // 沿建国门外大街向东步行，完全沿路
        coords: [
          [116.4336, 39.9055], [116.4360, 39.9053], [116.4385, 39.9051],
          [116.4410, 39.9049], [116.4435, 39.9048], [116.4460, 39.9046],
          [116.4480, 39.9044], [116.4500, 39.9042], [116.4520, 39.9041],
          [116.4540, 39.9040], [116.4558, 39.9039], [116.4575, 39.9038],
          [116.4590, 39.9037], [116.4605, 39.9038], [116.4618, 39.9040],
          [116.4628, 39.9043], [116.4635, 39.9048], [116.4638, 39.9055],
        ],
        events: [
          { id: 'e1', type: 'crossing', title: '过路口', time: '08:22', desc: '安全通过建国门路口', coord: [116.4410, 39.9049] },
          { id: 'e2', type: 'deviation', title: '偏离盲道', time: '08:35', desc: '偏离盲道约1.2米，已提醒', coord: [116.4500, 39.9042] },
          { id: 'e3', type: 'crossing', title: '过路口', time: '08:50', desc: '安全通过朝阳门路口', coord: [116.4590, 39.9037] },
        ]
      },
      {
        id: 'r2',
        timeRange: '11:30 - 12:15',
        from: '朝阳门外大街',
        to: '东三环路',
        dist: '2.6',
        duration: '45分钟',
        // 沿朝阳门外大街继续向东
        coords: [
          [116.4638, 39.9055], [116.4660, 39.9060], [116.4685, 39.9063],
          [116.4710, 39.9065], [116.4735, 39.9064], [116.4758, 39.9062],
          [116.4780, 39.9060], [116.4800, 39.9058], [116.4818, 39.9055],
          [116.4835, 39.9052], [116.4850, 39.9048], [116.4862, 39.9043],
          [116.4870, 39.9037], [116.4875, 39.9030], [116.4876, 39.9022],
          [116.4875, 39.9015], [116.4871, 39.9008], [116.4865, 39.9002],
        ],
        events: [
          { id: 'e4', type: 'found', title: '物品查找', time: '11:42', desc: '成功找到目标位置', coord: [116.4735, 39.9064] },
          { id: 'e5', type: 'fall', title: '跌倒预警', time: '11:58', desc: '检测到摔倒风险，已通知家属', coord: [116.4850, 39.9048] },
        ]
      },
      {
        id: 'r3',
        timeRange: '15:00 - 15:52',
        from: '东三环路',
        to: '建国门地铁站',
        dist: '2.3',
        duration: '52分钟',
        // 返程，沿原路附近道路步行
        coords: [
          [116.4865, 39.9002], [116.4855, 39.9008], [116.4840, 39.9015],
          [116.4820, 39.9020], [116.4798, 39.9025], [116.4775, 39.9030],
          [116.4750, 39.9034], [116.4725, 39.9037], [116.4700, 39.9040],
          [116.4675, 39.9042], [116.4650, 39.9044], [116.4625, 39.9046],
          [116.4600, 39.9047], [116.4575, 39.9048], [116.4550, 39.9049],
          [116.4525, 39.9050], [116.4500, 39.9051], [116.4470, 39.9052],
          [116.4440, 39.9053], [116.4410, 39.9054], [116.4380, 39.9055],
          [116.4350, 39.9055],
        ],
        events: [
          { id: 'e6', type: 'crossing', title: '过路口', time: '15:18', desc: '安全通过路口', coord: [116.4700, 39.9040] },
          { id: 'e7', type: 'deviation', title: '偏离盲道', time: '15:35', desc: '偏离盲道0.8米，已提醒', coord: [116.4550, 39.9049] },
        ]
      }
    ]
  },
  yesterday: {
    label: '昨天',
    totalDist: '5.4',
    totalDuration: '1h 55m',
    alerts: 1,
    routes: [
      {
        id: 'y1',
        timeRange: '09:00 - 09:48',
        from: '王府井大街',
        to: '东单路口',
        dist: '1.8',
        duration: '48分钟',
        // 沿王府井大街向南步行
        coords: [
          [116.4076, 39.9189], [116.4072, 39.9170], [116.4070, 39.9150],
          [116.4069, 39.9130], [116.4068, 39.9110], [116.4067, 39.9090],
          [116.4066, 39.9072], [116.4065, 39.9055], [116.4064, 39.9038],
          [116.4062, 39.9022], [116.4060, 39.9008],
        ],
        events: [
          { id: 'y_e1', type: 'crossing', title: '过路口', time: '09:12', desc: '安全通过王府井路口', coord: [116.4068, 39.9110] },
          { id: 'y_e2', type: 'crossing', title: '过路口', time: '09:30', desc: '安全通过东单路口', coord: [116.4065, 39.9055] },
        ]
      },
      {
        id: 'y2',
        timeRange: '14:20 - 15:07',
        from: '东单路口',
        to: '长安街',
        dist: '3.6',
        duration: '47分钟',
        // 沿长安街向西步行
        coords: [
          [116.4060, 39.9008], [116.4035, 39.9005], [116.4010, 39.9003],
          [116.3985, 39.9002], [116.3960, 39.9001], [116.3935, 39.9000],
          [116.3910, 39.8999], [116.3885, 39.8999], [116.3860, 39.9000],
          [116.3840, 39.9002], [116.3820, 39.9005], [116.3800, 39.9008],
        ],
        events: [
          { id: 'y_e3', type: 'fall', title: '跌倒预警', time: '14:38', desc: '检测到摔倒风险，已通知家属', coord: [116.3960, 39.9001] },
          { id: 'y_e4', type: 'found', title: '物品查找', time: '14:55', desc: '成功找到公共厕所位置', coord: [116.3860, 39.9000] },
        ]
      }
    ]
  },
  '7days': {
    label: '近7天',
    totalDist: '38.6',
    totalDuration: '14h 22m',
    alerts: 8,
    routes: [
      {
        id: 'w1',
        timeRange: '周一 08:00',
        from: '建国门',
        to: '国贸',
        dist: '3.2',
        duration: '1h 05m',
        coords: [
          [116.4336, 39.9055],[116.4400, 39.9050],[116.4460, 39.9046],
          [116.4520, 39.9041],[116.4580, 39.9038],[116.4640, 39.9048],
          [116.4700, 39.9040],[116.4760, 39.9032],[116.4820, 39.9020],
        ],
        events: [
          { id: 'w_e1', type: 'crossing', title: '过路口', time: '08:20', desc: '安全通过', coord: [116.4460, 39.9046] },
        ]
      },
      {
        id: 'w2',
        timeRange: '周三 10:15',
        from: '王府井',
        to: '天安门',
        dist: '2.8',
        duration: '55m',
        coords: [
          [116.4076, 39.9189],[116.4072, 39.9160],[116.4068, 39.9130],
          [116.4064, 39.9100],[116.4060, 39.9070],[116.4055, 39.9042],
          [116.4020, 39.9030],[116.3980, 39.9020],[116.3940, 39.9016],
          [116.3910, 39.9013],[116.3880, 39.9013],
        ],
        events: [
          { id: 'w_e2', type: 'deviation', title: '偏离盲道', time: '10:38', desc: '偏离约1米', coord: [116.4060, 39.9070] },
          { id: 'w_e3', type: 'crossing', title: '过路口', time: '10:52', desc: '安全通过', coord: [116.3940, 39.9016] },
        ]
      }
    ]
  },
  '30days': {
    label: '近30天',
    totalDist: '162.4',
    totalDuration: '61h 08m',
    alerts: 23,
    routes: [
      {
        id: 'm1',
        timeRange: '3/1 08:30',
        from: '东直门',
        to: '三里屯',
        dist: '2.5',
        duration: '50m',
        coords: [
          [116.4344, 39.9380],[116.4370, 39.9355],[116.4398, 39.9330],
          [116.4420, 39.9310],[116.4440, 39.9288],[116.4458, 39.9265],
          [116.4472, 39.9242],[116.4480, 39.9220],
        ],
        events: [
          { id: 'm_e1', type: 'crossing', title: '过路口', time: '08:45', desc: '安全通过三元桥路口', coord: [116.4420, 39.9310] },
        ]
      },
      {
        id: 'm2',
        timeRange: '3/5 14:00',
        from: '朝阳公园',
        to: '望京',
        dist: '3.1',
        duration: '1h 02m',
        coords: [
          [116.4680, 39.9310],[116.4710, 39.9340],[116.4740, 39.9368],
          [116.4768, 39.9395],[116.4792, 39.9420],[116.4815, 39.9445],
          [116.4835, 39.9468],[116.4850, 39.9490],
        ],
        events: [
          { id: 'm_e2', type: 'fall', title: '跌倒预警', time: '14:28', desc: '检测到摔倒风险', coord: [116.4768, 39.9395] },
          { id: 'm_e3', type: 'deviation', title: '偏离盲道', time: '14:45', desc: '偏离约1.5米', coord: [116.4815, 39.9445] },
        ]
      }
    ]
  }
}

// ── 状态 ──
const selectedDate = ref('today')
const mapLoading = ref(true)
const activeRouteId = ref(null)
const selectedRoute = ref(null)
const showHistoryPicker = ref(false)

// ── 7天历史日历数据 ──
const historyDays = (() => {
  const today = new Date()
  const days = []
  const weekdays = ['日', '一', '二', '三', '四', '五', '六']
  // 各天对应的数据key和路线信息
  const dayMeta = [
    { key: 'today',     routeCount: 3, dist: '7.2', alerts: 2 },
    { key: 'yesterday', routeCount: 2, dist: '5.4', alerts: 1 },
    { key: 'd2',        routeCount: 2, dist: '4.8', alerts: 0 },
    { key: 'd3',        routeCount: 3, dist: '8.1', alerts: 3 },
    { key: 'd4',        routeCount: 1, dist: '2.2', alerts: 0 },
    { key: 'd5',        routeCount: 2, dist: '6.0', alerts: 1 },
    { key: 'd6',        routeCount: 2, dist: '5.5', alerts: 2 },
  ]
  for (let i = 0; i < 7; i++) {
    const d = new Date(today)
    d.setDate(today.getDate() - i)
    const mm = String(d.getMonth() + 1).padStart(2, '0')
    const dd = String(d.getDate()).padStart(2, '0')
    days.push({
      ...dayMeta[i],
      displayDate: i === 0 ? '今天' : i === 1 ? '昨天' : `${mm}/${dd}`,
      weekday: i <= 1 ? '' : `周${weekdays[d.getDay()]}`,
    })
  }
  return days
})()

const currentDayData = computed(() => daysData[selectedDate.value])

let map = null
const drawnPolylines = []   // { routeId, polyline, markers }
let currentFlyMarker = null

// ── 加载高德 ──
const loadAmapScript = () => {
  return new Promise((resolve, reject) => {
    if (window.AMap) { resolve(window.AMap); return }
    window._AMapSecurityConfig = { securityJsCode: AMAP_CONFIG.securityCode }
    const s = document.createElement('script')
    s.src = `https://webapi.amap.com/maps?v=2.0&key=${AMAP_CONFIG.key}&plugin=AMap.Scale,AMap.ToolBar`
    s.onload = () => resolve(window.AMap)
    s.onerror = reject
    document.head.appendChild(s)
  })
}

// ── 绘制所有路线 ──
const drawRoutes = () => {
  if (!map) return
  // 清除已有
  drawnPolylines.forEach(item => {
    if (item.polyline) map.remove(item.polyline)
    item.markers.forEach(m => map.remove(m))
    if (item.startM) map.remove(item.startM)
    if (item.endM) map.remove(item.endM)
  })
  drawnPolylines.length = 0

  const data = currentDayData.value
  data.routes.forEach((route, idx) => {
    const color = routeColors[idx % routeColors.length]

    const polyline = new AMap.Polyline({
      path: route.coords,
      strokeColor: color,
      strokeWeight: 5,
      strokeOpacity: 0.85,
      lineJoin: 'round',
      lineCap: 'round',
    })
    map.add(polyline)

    // 起点标记
    const startM = new AMap.Marker({
      position: route.coords[0],
      content: `<div class="hist-start-m" style="border-color:${color}">${idx + 1}</div>`,
      offset: new AMap.Pixel(-13, -13),
    })
    startM.setMap(map)

    // 终点标记
    const endM = new AMap.Marker({
      position: route.coords[route.coords.length - 1],
      content: `<div class="hist-end-m" style="background:${color}"></div>`,
      offset: new AMap.Pixel(-8, -8),
    })
    endM.setMap(map)

    // 时间标注（在起点旁）
    const labelM = new AMap.Marker({
      position: route.coords[0],
      content: `<div class="hist-time-label" style="border-color:${color};color:${color}">${route.timeRange.split(' ')[0]}</div>`,
      offset: new AMap.Pixel(14, -18),
      zIndex: 150,
    })
    labelM.setMap(map)

    // 事件标记
    const evMarkers = route.events.map(ev => {
      const evColor = { crossing: '#22c55e', deviation: '#f59e0b', fall: '#ef4444', found: '#3b82f6' }[ev.type] || '#64748b'
      const m = new AMap.Marker({
        position: ev.coord,
        content: `<div class="hist-ev-dot" style="background:${evColor}" title="${ev.title}"></div>`,
        offset: new AMap.Pixel(-7, -7),
        zIndex: 200,
      })
      m.setMap(map)
      m.on('click', () => {
        selectedRoute.value = route
        activeRouteId.value = route.id
        flyToEvent(ev)
      })
      return m
    })

    drawnPolylines.push({ routeId: route.id, polyline, markers: evMarkers, startM, endM, labelM })
  })

  // 自适应视野
  setTimeout(() => fitAllRoutes(), 100)
}

// ── 自适应视野 ──
const fitAllRoutes = () => {
  if (!map || drawnPolylines.length === 0) return
  const polylines = drawnPolylines.map(d => d.polyline)
  map.setFitView(polylines, true, [40, 40, 60, 40])
}

// ── 切换日期 ──
const switchDate = (val) => {
  // d2~d6 没有独立数据，映射到已有数据复用展示
  const keyMap = { d2: '7days', d3: 'yesterday', d4: '30days', d5: 'today', d6: 'yesterday' }
  selectedDate.value = keyMap[val] || val
  activeRouteId.value = null
  selectedRoute.value = null
  showHistoryPicker.value = false
  drawRoutes()
}

// ── 选择路线 ──
const selectRoute = (route) => {
  if (activeRouteId.value === route.id) {
    activeRouteId.value = null
    selectedRoute.value = null
    updateRouteOpacity(null)
    fitAllRoutes()
  } else {
    activeRouteId.value = route.id
    selectedRoute.value = route
    updateRouteOpacity(route.id)
    // 飞到该路线
    const item = drawnPolylines.find(d => d.routeId === route.id)
    if (item) map.setFitView([item.polyline], true, [60, 80, 80, 80])
  }
}

const toggleRoute = (routeId) => {
  const route = currentDayData.value.routes.find(r => r.id === routeId)
  if (route) selectRoute(route)
}

// ── 高亮当前路线 ──
const updateRouteOpacity = (activeId) => {
  drawnPolylines.forEach(item => {
    const opacity = activeId === null || item.routeId === activeId ? 0.85 : 0.2
    item.polyline.setOptions({ strokeOpacity: opacity })
  })
}

// ── 飞到事件位置 ──
const flyToEvent = (ev) => {
  if (!map) return
  if (currentFlyMarker) { map.remove(currentFlyMarker); currentFlyMarker = null }
  map.setZoomAndCenter(18, ev.coord, false, 300)
  const evColor = { crossing: '#22c55e', deviation: '#f59e0b', fall: '#ef4444', found: '#3b82f6' }[ev.type] || '#64748b'
  currentFlyMarker = new AMap.Marker({
    position: ev.coord,
    content: `<div class="hist-fly-popup" style="border-color:${evColor}"><span class="fly-title">${ev.title}</span><span class="fly-time">${ev.time}</span><p class="fly-desc">${ev.desc}</p></div>`,
    offset: new AMap.Pixel(-90, -80),
    zIndex: 500,
  })
  currentFlyMarker.setMap(map)
  setTimeout(() => {
    if (currentFlyMarker) { map.remove(currentFlyMarker); currentFlyMarker = null }
  }, 4000)
}

const exportGPX = () => { alert('GPX 文件导出功能') }

// ── 初始化地图 ──
const initMap = async () => {
  try {
    await loadAmapScript()
    mapLoading.value = false
    map = new AMap.Map('history-amap', {
      zoom: 14,
      center: [116.4500, 39.9050],
      viewMode: '2D',
      mapStyle: 'amap://styles/normal',
    })
    map.addControl(new AMap.Scale())
    map.addControl(new AMap.ToolBar({ position: 'RB' }))
    drawRoutes()
  } catch (e) {
    console.error('历史地图初始化失败:', e)
    mapLoading.value = false
  }
}

onMounted(() => { initMap() })
onUnmounted(() => {
  if (map) { map.destroy(); map = null }
})
</script>

<style>
.hist-start-m {
  width: 26px; height: 26px;
  background: #fff;
  border-radius: 50%;
  border: 2.5px solid #3b82f6;
  font-size: 11px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  color: #1e293b;
  box-shadow: 0 2px 8px rgba(0,0,0,0.18);
}
.hist-end-m {
  width: 12px; height: 12px;
  border-radius: 50%;
  border: 2px solid #fff;
  box-shadow: 0 1px 5px rgba(0,0,0,0.25);
}
.hist-time-label {
  background: #fff;
  border: 1.5px solid #3b82f6;
  border-radius: 4px;
  padding: 2px 6px;
  font-size: 11px; font-weight: 600;
  white-space: nowrap;
  box-shadow: 0 1px 6px rgba(0,0,0,0.12);
}
.hist-ev-dot {
  width: 14px; height: 14px;
  border-radius: 50%;
  border: 2px solid #fff;
  cursor: pointer;
  box-shadow: 0 1px 5px rgba(0,0,0,0.2);
  transition: transform 0.15s;
}
.hist-ev-dot:hover { transform: scale(1.5); }
.hist-fly-popup {
  width: 180px;
  background: #fff;
  border-radius: 10px;
  border: 2px solid #3b82f6;
  padding: 10px 12px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.18);
  display: flex; flex-direction: column; gap: 3px;
}
.fly-title { font-size: 13px; font-weight: 700; color: #1e293b; }
.fly-time { font-size: 11px; color: #64748b; }
.fly-desc { font-size: 11.5px; color: #475569; margin: 0; line-height: 1.4; }
</style>

<style scoped>
.history {
  padding: 16px 18px;
  background: #f1f5f9;
  height: calc(100vh - 52px);
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow: hidden;
}

/* ── 工具栏 ── */
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-shrink: 0;
  gap: 16px;
}
.toolbar-left { display: flex; flex-direction: column; gap: 7px; }
.page-title-wrap { display: flex; align-items: center; gap: 8px; }
.title-icon { width: 20px; height: 20px; color: #3b82f6; }
.page-title { font-size: 19px; font-weight: 700; color: #0f172a; margin: 0; }

.meta-tags { display: flex; gap: 7px; flex-wrap: wrap; }
.tag {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 3px 9px; border-radius: 20px; font-size: 12px; font-weight: 500;
}
.tag svg { width: 11px; height: 11px; }
.tag.device { background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; }
.tag.date   { background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; }
.tag.stats  { background: #fff7ed; color: #c2410c; border: 1px solid #fed7aa; }

.toolbar-right { display: flex; align-items: center; gap: 10px; flex-shrink: 0; }

.date-tabs { display: flex; background: #fff; border-radius: 8px; border: 1px solid #e2e8f0; overflow: hidden; }
.date-tab {
  padding: 6px 13px; font-size: 12.5px; font-weight: 500; color: #64748b;
  background: transparent; border: none; cursor: pointer;
  transition: all 0.15s; border-right: 1px solid #e2e8f0;
}
.date-tab:last-child { border-right: none; }
.date-tab:hover { background: #f8fafc; color: #1e293b; }
.date-tab.active { background: #3b82f6; color: #fff; }

.btn {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 7px 14px; border-radius: 8px; font-size: 13px; font-weight: 500;
  cursor: pointer; transition: all 0.18s; border: none;
}
.btn svg { width: 14px; height: 14px; }
.btn-outline { background: #fff; color: #334155; border: 1px solid #e2e8f0; }
.btn-outline:hover { background: #f8fafc; border-color: #cbd5e1; }

/* ── 布局 ── */
.content { display: grid; grid-template-columns: 1fr 300px; gap: 12px; flex: 1; min-height: 0; }
.map-col { display: flex; flex-direction: column; min-height: 0; }
.side-col { display: flex; flex-direction: column; gap: 10px; min-height: 0; overflow-y: auto; }
.side-col::-webkit-scrollbar { width: 4px; }
.side-col::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 2px; }

/* ── 卡片 ── */
.card {
  background: #fff; border-radius: 12px;
  border: 1px solid #e8edf2;
  box-shadow: 0 1px 8px rgba(0,0,0,0.05);
  display: flex; flex-direction: column; overflow: hidden;
}
.card-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 10px 14px; border-bottom: 1px solid #f1f5f9; flex-shrink: 0;
}
.card-title {
  display: flex; align-items: center; gap: 6px;
  font-size: 13px; font-weight: 600; color: #1e293b;
}
.card-title svg { width: 14px; height: 14px; color: #3b82f6; }

/* ── 地图卡片 ── */
.map-card { flex: 1; }
.map-hd-right { display: flex; align-items: center; gap: 8px; }
.route-legend { display: flex; gap: 5px; flex-wrap: wrap; }
.legend-pill {
  display: flex; align-items: center; gap: 5px;
  padding: 3px 9px; border-radius: 20px; font-size: 11.5px; font-weight: 500;
  background: #f8fafc; border: 1px solid #e2e8f0; cursor: pointer;
  color: #334155; transition: all 0.15s;
}
.legend-pill:hover { background: #f0f9ff; }
.legend-pill.dimmed { opacity: 0.4; }
.pill-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }

.map-tool-btn {
  width: 28px; height: 28px; border: 1px solid #e2e8f0; border-radius: 7px;
  background: #f8fafc; cursor: pointer; display: flex; align-items: center;
  justify-content: center; color: #334155; transition: all 0.15s;
}
.map-tool-btn svg { width: 13px; height: 13px; }
.map-tool-btn:hover { background: #f0f9ff; border-color: #bae6fd; }

.amap-wrap { flex: 1; min-height: 0; position: relative; }
.amap-container { width: 100%; height: 100%; }
.map-loading {
  position: absolute; inset: 0; display: flex; flex-direction: column;
  align-items: center; justify-content: center; gap: 10px;
  background: #f8fafc; font-size: 13px; color: #64748b;
}
.loading-spinner {
  width: 26px; height: 26px; border: 3px solid #e2e8f0;
  border-top-color: #3b82f6; border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── 7天历史面板 ── */
.history-picker {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 200;
  width: 220px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.97);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.14);
  border: 1px solid #e2e8f0;
  overflow: hidden;
  backdrop-filter: blur(8px);
}

.picker-toggle {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 9px 12px;
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  color: #1e293b;
  text-align: left;
  transition: background 0.15s;
}

.picker-toggle:hover { background: #f0f9ff; }

.picker-toggle svg:first-child {
  width: 15px;
  height: 15px;
  color: #3b82f6;
  flex-shrink: 0;
}

.picker-toggle span { flex: 1; }

.toggle-arrow {
  width: 14px;
  height: 14px;
  color: #94a3b8;
  transition: transform 0.2s ease;
  flex-shrink: 0;
}

.toggle-arrow.rotated { transform: rotate(180deg); }

.picker-list {
  border-top: 1px solid #f1f5f9;
  padding: 6px 0 4px;
  animation: picker-drop 0.18s ease;
}

@keyframes picker-drop {
  from { opacity: 0; transform: translateY(-6px); }
  to   { opacity: 1; transform: translateY(0); }
}

.picker-label {
  font-size: 10px;
  color: #94a3b8;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 0 12px 6px;
}

.picker-day-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 7px 12px;
  cursor: pointer;
  transition: background 0.12s;
  border-left: 3px solid transparent;
}

.picker-day-row:hover { background: #f8fafc; }

.picker-day-row.active {
  background: #eff6ff;
  border-left-color: #3b82f6;
}

.picker-day-left {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.picker-day-date {
  font-size: 12.5px;
  font-weight: 600;
  color: #1e293b;
}

.picker-day-label {
  font-size: 10px;
  color: #94a3b8;
}

.picker-day-right {
  display: flex;
  align-items: center;
  gap: 5px;
}

.picker-day-routes {
  font-size: 10.5px;
  color: #64748b;
}

.picker-day-dist {
  font-size: 11px;
  font-weight: 600;
  color: #3b82f6;
  background: #eff6ff;
  padding: 1px 5px;
  border-radius: 4px;
}

.picker-day-alert {
  font-size: 10px;
  font-weight: 700;
  color: #ef4444;
  background: #fee2e2;
  padding: 1px 5px;
  border-radius: 4px;
}

/* ── 统计 ── */
.stats-card { flex-shrink: 0; }
.stats-grid { display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; }
.stat-item { padding: 12px 8px; text-align: center; border-right: 1px solid #f1f5f9; }
.stat-item:last-child { border-right: none; }
.stat-value { font-size: 18px; font-weight: 700; color: #1e293b; }
.stat-value.danger { color: #ef4444; }
.stat-label { font-size: 10px; color: #94a3b8; margin-top: 2px; }

/* ── 路线列表 ── */
.routes-card { flex-shrink: 0; }
.routes-list { padding: 6px 0; }
.route-item {
  display: flex; cursor: pointer;
  transition: background 0.15s; border-left: 3px solid transparent;
}
.route-item:hover { background: #f8fafc; }
.route-item.active { background: #eff6ff; border-left-color: #3b82f6; }
.route-color-bar { width: 4px; flex-shrink: 0; margin: 6px 0; border-radius: 2px; }
.route-body { flex: 1; padding: 8px 12px; min-width: 0; }
.route-header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 3px; }
.route-title { font-size: 12.5px; font-weight: 600; color: #1e293b; }
.route-time { font-size: 11px; color: #64748b; font-family: monospace; }
.route-path { display: flex; align-items: center; gap: 4px; margin-bottom: 4px; }
.route-from, .route-to { font-size: 12px; color: #334155; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 90px; }
.route-arrow { width: 14px; height: 14px; color: #94a3b8; flex-shrink: 0; }
.route-meta { display: flex; gap: 8px; font-size: 11px; color: #94a3b8; }
.route-event-cnt { color: #f59e0b; font-weight: 600; }

/* ── 事件列表 ── */
.events-card { flex-shrink: 0; }
.event-count { font-size: 11px; color: #94a3b8; }
.events-list { padding: 4px 0; }
.event-item {
  display: flex; gap: 8px; padding: 8px 12px;
  cursor: pointer; transition: background 0.12s;
}
.event-item:hover { background: #f8fafc; }
.event-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; margin-top: 4px; }
.event-dot.crossing  { background: #22c55e; }
.event-dot.deviation { background: #f59e0b; }
.event-dot.fall      { background: #ef4444; }
.event-dot.found     { background: #3b82f6; }
.event-body { flex: 1; min-width: 0; }
.event-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px; }
.event-title { font-size: 12.5px; font-weight: 600; color: #1e293b; }
.event-time-badge { font-size: 11px; font-family: monospace; color: #64748b; flex-shrink: 0; }
.event-desc { font-size: 11px; color: #64748b; line-height: 1.4; }
</style>
