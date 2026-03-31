<template>
  <div class="devices-page">
    <!-- 页头 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">设备管理</h1>
        <div class="summary-chips">
          <div class="chip green">
            <span class="chip-dot"></span>
            <span class="chip-num">{{ onlineCount }}</span>
            <span class="chip-label">在线</span>
          </div>
          <div class="chip red">
            <span class="chip-dot"></span>
            <span class="chip-num">{{ offlineCount }}</span>
            <span class="chip-label">离线</span>
          </div>
          <div class="chip blue">
            <span class="chip-num">{{ devices.length }}</span>
            <span class="chip-label">全部设备</span>
          </div>
        </div>
      </div>
      <div class="header-right">
        <div class="search-wrap">
          <svg viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="1.6"/><path d="M21 21l-4.35-4.35" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
          <input type="text" v-model="searchQuery" placeholder="搜索设备..." />
        </div>
        <button class="add-btn" @click="showAddModal = true">
          <svg viewBox="0 0 24 24" fill="none"><path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
          添加设备
        </button>
      </div>
    </div>

    <!-- 主体 -->
    <div class="devices-body">
      <!-- 设备卡片列表 -->
      <div class="devices-grid">
        <div
          v-for="device in filteredDevices"
          :key="device.id"
          class="device-card"
          :class="{ offline: !device.online, selected: selectedDevice?.id === device.id }"
          @click="selectDevice(device)"
        >
          <div class="dcard-head">
            <div class="dcard-avatar" :class="device.online ? 'av-online' : 'av-offline'">
              <svg viewBox="0 0 24 24" fill="none"><rect x="7" y="2" width="10" height="18" rx="2.5" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="17.5" r="1" fill="currentColor"/><path d="M10 5.5h4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
            </div>
            <div class="dcard-info">
              <div class="dcard-name">{{ device.name }}</div>
              <div class="dcard-id">{{ device.id }}</div>
            </div>
            <div class="dcard-status-badge" :class="device.online ? 'online' : 'offline'">
              <span class="status-dot-sm"></span>
              {{ device.online ? '在线' : '离线' }}
            </div>
          </div>

          <div class="dcard-stats">
            <div class="dstat-item">
              <div class="dstat-icon battery-icon">
                <svg viewBox="0 0 24 24" fill="none"><rect x="2" y="7" width="16" height="10" rx="2" stroke="currentColor" stroke-width="1.5"/><path d="M20 10v4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><rect x="4" y="9" :width="(device.battery/100)*12" height="6" rx="1" fill="currentColor"/></svg>
              </div>
              <div class="dstat-body">
                <span class="dstat-label">电量</span>
                <span class="dstat-val" :class="device.battery < 20 ? 'val-red' : device.battery < 50 ? 'val-yellow' : 'val-green'">{{ device.battery }}%</span>
              </div>
              <div class="dstat-bar">
                <div class="dstat-fill" :class="device.battery < 20 ? 'fill-red' : device.battery < 50 ? 'fill-yellow' : 'fill-green'" :style="{ width: device.battery + '%' }"></div>
              </div>
            </div>
            <div class="dstat-item">
              <div class="dstat-icon signal-icon">
                <svg viewBox="0 0 24 24" fill="none"><path d="M1 6s5-4 11-4 11 4 11 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><path d="M5 10s3.5-3 7-3 7 3 7 3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><path d="M9 14s1.5-1.5 3-1.5 3 1.5 3 1.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="12" cy="17.5" r="1" fill="currentColor"/></svg>
              </div>
              <div class="dstat-body">
                <span class="dstat-label">网络</span>
                <span class="dstat-val">{{ device.signal }}</span>
              </div>
            </div>
            <div class="dstat-item">
              <div class="dstat-icon storage-icon">
                <svg viewBox="0 0 24 24" fill="none"><ellipse cx="12" cy="5" rx="9" ry="3" stroke="currentColor" stroke-width="1.5"/><path d="M3 5v14c0 1.66 4.03 3 9 3s9-1.34 9-3V5" stroke="currentColor" stroke-width="1.5"/><path d="M3 12c0 1.66 4.03 3 9 3s9-1.34 9-3" stroke="currentColor" stroke-width="1.5"/></svg>
              </div>
              <div class="dstat-body">
                <span class="dstat-label">存储</span>
                <span class="dstat-val">{{ device.storage }}</span>
              </div>
            </div>
          </div>

          <div class="dcard-sensors">
            <div
              v-for="sensor in sensorList"
              :key="sensor.key"
              class="sensor-chip"
              :class="device.sensors[sensor.key] ? 'sensor-ok' : 'sensor-err'"
            >
              <component :is="'svg'" viewBox="0 0 24 24" fill="none" v-html="sensor.icon"></component>
              {{ sensor.label }}
            </div>
          </div>

          <div class="dcard-actions">
            <button class="daction-btn" @click.stop="goToDashboard(device)" title="实时监控">
              <svg viewBox="0 0 24 24" fill="none"><rect x="3" y="3" width="7" height="9" rx="1.5" stroke="currentColor" stroke-width="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5" stroke="currentColor" stroke-width="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5" stroke="currentColor" stroke-width="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5" stroke="currentColor" stroke-width="1.5"/></svg>
            </button>
            <button class="daction-btn" @click.stop="sendVoice(device)" title="远程喊话">
              <svg viewBox="0 0 24 24" fill="none"><path d="M12 1a3 3 0 013 3v7a3 3 0 01-6 0V4a3 3 0 013-3z" stroke="currentColor" stroke-width="1.5"/><path d="M19 10v1a7 7 0 01-14 0v-1M12 18v4M8 22h8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
            </button>
            <button class="daction-btn" @click.stop="restartDevice(device)" title="重启设备">
              <svg viewBox="0 0 24 24" fill="none"><path d="M23 4v6h-6M1 20v-6h6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </button>
            <button class="daction-btn" @click.stop="openEditModal(device)" title="编辑设备">
              <svg viewBox="0 0 24 24" fill="none"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </button>
          </div>
        </div>

        <div class="empty-state" v-if="filteredDevices.length === 0">
          <svg viewBox="0 0 24 24" fill="none"><rect x="7" y="2" width="10" height="18" rx="2.5" stroke="#cbd5e1" stroke-width="1.5"/><circle cx="12" cy="17.5" r="1" fill="#cbd5e1"/></svg>
          <span>未找到匹配的设备</span>
        </div>
      </div>

      <!-- 设备详情面板 -->
      <div class="detail-panel" v-if="selectedDevice">
        <div class="detail-head">
          <div class="detail-head-left">
            <div class="detail-avatar" :class="selectedDevice.online ? 'av-online' : 'av-offline'">
              <svg viewBox="0 0 24 24" fill="none"><rect x="7" y="2" width="10" height="18" rx="2.5" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="17.5" r="1" fill="currentColor"/><path d="M10 5.5h4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
            </div>
            <div>
              <div class="detail-name">{{ selectedDevice.name }}</div>
              <div class="detail-id-tag">{{ selectedDevice.id }}</div>
            </div>
          </div>
          <button class="close-btn" @click="selectedDevice = null">
            <svg viewBox="0 0 24 24" fill="none"><path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
          </button>
        </div>

        <div class="detail-scroll">
          <!-- 基本信息 -->
          <div class="detail-section">
            <div class="section-title">基本信息</div>
            <div class="info-grid">
              <div class="info-item">
                <span class="info-label">绑定用户</span>
                <span class="info-val">{{ selectedDevice.user }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">设备状态</span>
                <span class="info-val" :class="selectedDevice.online ? 'text-green' : 'text-red'">{{ selectedDevice.online ? '在线' : '离线' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">固件版本</span>
                <span class="info-val">{{ selectedDevice.firmware }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">最后在线</span>
                <span class="info-val">{{ selectedDevice.lastSeen }}</span>
              </div>
            </div>
          </div>

          <!-- 状态监控 -->
          <div class="detail-section">
            <div class="section-title">状态监控</div>
            <div class="monitor-list">
              <div class="monitor-row">
                <div class="monitor-icon battery-icon">
                  <svg viewBox="0 0 24 24" fill="none"><rect x="2" y="7" width="16" height="10" rx="2" stroke="currentColor" stroke-width="1.5"/><path d="M20 10v4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><rect x="4" y="9" :width="(selectedDevice.battery/100)*12" height="6" rx="1" fill="currentColor"/></svg>
                </div>
                <div class="monitor-info">
                  <span class="monitor-label">电量</span>
                  <span class="monitor-val">{{ selectedDevice.battery }}%</span>
                </div>
                <div class="monitor-bar-wrap">
                  <div class="monitor-bar-track">
                    <div class="monitor-bar-fill"
                      :class="selectedDevice.battery < 20 ? 'fill-red' : selectedDevice.battery < 50 ? 'fill-yellow' : 'fill-green'"
                      :style="{ width: selectedDevice.battery + '%' }"></div>
                  </div>
                </div>
              </div>
              <div class="monitor-row">
                <div class="monitor-icon signal-icon">
                  <svg viewBox="0 0 24 24" fill="none"><path d="M1 6s5-4 11-4 11 4 11 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><path d="M5 10s3.5-3 7-3 7 3 7 3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><path d="M9 14s1.5-1.5 3-1.5 3 1.5 3 1.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="12" cy="17.5" r="1" fill="currentColor"/></svg>
                </div>
                <div class="monitor-info">
                  <span class="monitor-label">网络信号</span>
                  <span class="monitor-val">{{ selectedDevice.signal }}</span>
                </div>
                <div class="monitor-bar-wrap">
                  <div class="monitor-bar-track">
                    <div class="monitor-bar-fill fill-green" :style="{ width: getSignalPct(selectedDevice.signal) + '%' }"></div>
                  </div>
                </div>
              </div>
              <div class="monitor-row">
                <div class="monitor-icon storage-icon">
                  <svg viewBox="0 0 24 24" fill="none"><ellipse cx="12" cy="5" rx="9" ry="3" stroke="currentColor" stroke-width="1.5"/><path d="M3 5v14c0 1.66 4.03 3 9 3s9-1.34 9-3V5" stroke="currentColor" stroke-width="1.5"/><path d="M3 12c0 1.66 4.03 3 9 3s9-1.34 9-3" stroke="currentColor" stroke-width="1.5"/></svg>
                </div>
                <div class="monitor-info">
                  <span class="monitor-label">存储空间</span>
                  <span class="monitor-val">{{ selectedDevice.storage }}</span>
                </div>
                <div class="monitor-bar-wrap">
                  <div class="monitor-bar-track">
                    <div class="monitor-bar-fill" :class="getStoragePct(selectedDevice.storage) > 80 ? 'fill-red' : 'fill-blue'" :style="{ width: getStoragePct(selectedDevice.storage) + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 传感器状态 -->
          <div class="detail-section">
            <div class="section-title">传感器状态</div>
            <div class="sensor-grid">
              <div
                v-for="sensor in sensorList"
                :key="sensor.key"
                class="sensor-card"
                :class="selectedDevice.sensors[sensor.key] ? 'card-ok' : 'card-err'"
              >
                <div class="sensor-card-icon">
                  <svg viewBox="0 0 24 24" fill="none" v-html="sensor.icon"></svg>
                </div>
                <span class="sensor-card-name">{{ sensor.label }}</span>
                <span class="sensor-card-status">{{ selectedDevice.sensors[sensor.key] ? '正常' : '异常' }}</span>
              </div>
            </div>
          </div>

          <!-- 远程控制 -->
          <div class="detail-section">
            <div class="section-title">远程控制</div>
            <div class="ctrl-grid">
              <button class="ctrl-card" @click="sendVoice(selectedDevice)">
                <div class="ctrl-icon mic-bg">
                  <svg viewBox="0 0 24 24" fill="none"><path d="M12 1a3 3 0 013 3v7a3 3 0 01-6 0V4a3 3 0 013-3z" stroke="currentColor" stroke-width="1.5"/><path d="M19 10v1a7 7 0 01-14 0v-1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
                </div>
                <span class="ctrl-label">远程喊话</span>
                <span class="ctrl-desc">发送语音指令</span>
              </button>
              <button class="ctrl-card" @click="restartDevice(selectedDevice)">
                <div class="ctrl-icon restart-bg">
                  <svg viewBox="0 0 24 24" fill="none"><path d="M23 4v6h-6M1 20v-6h6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </div>
                <span class="ctrl-label">远程重启</span>
                <span class="ctrl-desc">重启设备系统</span>
              </button>
              <button class="ctrl-card" @click="updateFirmware(selectedDevice)">
                <div class="ctrl-icon update-bg">
                  <svg viewBox="0 0 24 24" fill="none"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M17 8l-5-5-5 5M12 3v12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </div>
                <span class="ctrl-label">固件升级</span>
                <span class="ctrl-desc">更新到最新版本</span>
              </button>
              <button class="ctrl-card" @click="clearStorage(selectedDevice)">
                <div class="ctrl-icon trash-bg">
                  <svg viewBox="0 0 24 24" fill="none"><polyline points="3 6 5 6 21 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><path d="M19 6l-1 14a2 2 0 01-2 2H8a2 2 0 01-2-2L5 6M10 11v6M14 11v6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><path d="M9 6V4a1 1 0 011-1h4a1 1 0 011 1v2" stroke="currentColor" stroke-width="1.5"/></svg>
                </div>
                <span class="ctrl-label">清理存储</span>
                <span class="ctrl-desc">清理设备缓存</span>
              </button>
            </div>
          </div>

          <!-- 今日统计 -->
          <div class="detail-section">
            <div class="section-title">今日使用统计</div>
            <div class="today-stats">
              <div class="today-stat-item">
                <span class="ts-num">{{ selectedDevice.todaySteps }}</span>
                <span class="ts-label">步数</span>
              </div>
              <div class="ts-div"></div>
              <div class="today-stat-item">
                <span class="ts-num">{{ selectedDevice.todayDist }}</span>
                <span class="ts-label">公里</span>
              </div>
              <div class="ts-div"></div>
              <div class="today-stat-item">
                <span class="ts-num">{{ selectedDevice.todayVoice }}</span>
                <span class="ts-label">语音交互</span>
              </div>
              <div class="ts-div"></div>
              <div class="today-stat-item">
                <span class="ts-num" style="color:#ef4444">{{ selectedDevice.todayAlerts }}</span>
                <span class="ts-label">告警</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加设备弹窗 -->
    <div class="modal-wrap" v-if="showAddModal" @click.self="showAddModal = false">
      <div class="modal-box">
        <div class="modal-head">
          <span>添加设备</span>
          <button class="close-btn" @click="showAddModal = false">
            <svg viewBox="0 0 24 24" fill="none"><path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="form-field">
            <label>设备名称</label>
            <input type="text" v-model="newDevice.name" placeholder="例：张三的眼镜" />
          </div>
          <div class="form-field">
            <label>设备编号</label>
            <input type="text" v-model="newDevice.id" placeholder="例：智能盲人眼镜 #006" />
          </div>
          <div class="form-field">
            <label>绑定用户</label>
            <input type="text" v-model="newDevice.user" placeholder="输入用户姓名" />
          </div>
        </div>
        <div class="modal-foot">
          <button class="modal-btn cancel" @click="showAddModal = false">取消</button>
          <button class="modal-btn confirm" @click="doAddDevice">确认添加</button>
        </div>
      </div>
    </div>

    <!-- 编辑设备弹窗 -->
    <div class="modal-wrap" v-if="showEditModal" @click.self="showEditModal = false">
      <div class="modal-box">
        <div class="modal-head">
          <span>编辑设备</span>
          <button class="close-btn" @click="showEditModal = false">
            <svg viewBox="0 0 24 24" fill="none"><path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="form-field">
            <label>设备名称</label>
            <input type="text" v-model="editingDevice.name" />
          </div>
          <div class="form-field">
            <label>绑定用户</label>
            <input type="text" v-model="editingDevice.user" />
          </div>
        </div>
        <div class="modal-foot">
          <button class="modal-btn cancel" @click="showEditModal = false">取消</button>
          <button class="modal-btn confirm" @click="doSaveEdit">保存修改</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const searchQuery = ref('')
const showAddModal = ref(false)
const showEditModal = ref(false)
const selectedDevice = ref(null)
const newDevice = ref({ name: '', id: '', user: '' })
const editingDevice = ref(null)

const sensorList = [
  { key: 'camera',     label: '摄像头', icon: '<rect x="2" y="7" width="15" height="10" rx="2" stroke="currentColor" stroke-width="1.5"/><path d="M17 9l4-2v10l-4-2V9z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>' },
  { key: 'microphone', label: '麦克风', icon: '<path d="M12 1a3 3 0 013 3v7a3 3 0 01-6 0V4a3 3 0 013-3z" stroke="currentColor" stroke-width="1.5"/><path d="M19 10v1a7 7 0 01-14 0v-1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>' },
  { key: 'gps',        label: 'GPS',   icon: '<path d="M12 22s-8-6.686-8-12a8 8 0 0116 0c0 5.314-8 12-8 12z" stroke="currentColor" stroke-width="1.5"/><circle cx="12" cy="10" r="2.5" stroke="currentColor" stroke-width="1.4"/>' },
  { key: 'gyroscope',  label: '陀螺仪', icon: '<circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.5"/><ellipse cx="12" cy="12" rx="10" ry="4" stroke="currentColor" stroke-width="1.3"/><line x1="12" y1="2" x2="12" y2="22" stroke="currentColor" stroke-width="1.3"/>' },
]

const devices = ref([
  {
    id: '智能盲人眼镜 #001', name: '张三的眼镜', user: '张三',
    online: true, battery: 85, signal: '4G', storage: '12/32 GB', firmware: 'v2.1.0',
    lastSeen: '刚刚', todaySteps: 8432, todayDist: '6.2', todayVoice: 47, todayAlerts: 2,
    sensors: { camera: true, microphone: true, gps: true, gyroscope: true }
  },
  {
    id: '智能盲人眼镜 #002', name: '李四的眼镜', user: '李四',
    online: true, battery: 62, signal: 'WiFi', storage: '18/32 GB', firmware: 'v2.0.8',
    lastSeen: '3分钟前', todaySteps: 5210, todayDist: '3.8', todayVoice: 31, todayAlerts: 1,
    sensors: { camera: true, microphone: true, gps: true, gyroscope: false }
  },
  {
    id: '智能盲人眼镜 #003', name: '王五的眼镜', user: '王五',
    online: false, battery: 23, signal: '-', storage: '28/32 GB', firmware: 'v2.1.0',
    lastSeen: '2小时前', todaySteps: 1200, todayDist: '0.9', todayVoice: 8, todayAlerts: 0,
    sensors: { camera: true, microphone: true, gps: false, gyroscope: true }
  },
  {
    id: '智能盲人眼镜 #004', name: '赵六的眼镜', user: '赵六',
    online: true, battery: 91, signal: '5G', storage: '5/32 GB', firmware: 'v2.1.0',
    lastSeen: '刚刚', todaySteps: 12050, todayDist: '8.8', todayVoice: 63, todayAlerts: 3,
    sensors: { camera: true, microphone: true, gps: true, gyroscope: true }
  },
])

const onlineCount  = computed(() => devices.value.filter(d => d.online).length)
const offlineCount = computed(() => devices.value.filter(d => !d.online).length)

const filteredDevices = computed(() => {
  if (!searchQuery.value) return devices.value
  const q = searchQuery.value.toLowerCase()
  return devices.value.filter(d =>
    d.name.toLowerCase().includes(q) || d.id.toLowerCase().includes(q) || d.user.toLowerCase().includes(q)
  )
})

const selectDevice = (device) => {
  selectedDevice.value = selectedDevice.value?.id === device.id ? null : device
}

const getSignalPct = (signal) => ({ '5G': 100, '4G': 88, '3G': 65, 'WiFi': 93, '-': 0 }[signal] || 50)

const getStoragePct = (storage) => {
  const parts = storage.replace(' GB', '').split('/')
  return Math.round((parseInt(parts[0]) / parseInt(parts[1])) * 100)
}

const goToDashboard = (device) => {
  window.alert(`跳转到 ${device.name} 的实时监控仪表盘`)
}

const sendVoice = (device) => {
  window.alert(`向 ${device.name} 发送远程语音指令`)
}

const restartDevice = (device) => {
  if (window.confirm(`确定要重启 ${device.name} 吗？`)) {
    window.alert(`已发送重启指令到 ${device.name}`)
  }
}

const openEditModal = (device) => {
  editingDevice.value = { ...device }
  showEditModal.value = true
}

const doSaveEdit = () => {
  const idx = devices.value.findIndex(d => d.id === editingDevice.value.id)
  if (idx !== -1) {
    devices.value[idx].name = editingDevice.value.name
    devices.value[idx].user = editingDevice.value.user
    if (selectedDevice.value?.id === editingDevice.value.id) {
      selectedDevice.value = devices.value[idx]
    }
  }
  showEditModal.value = false
}

const updateFirmware = (device) => {
  window.alert(`已向 ${device.name} 推送固件升级包，请保持设备在线`)
}

const clearStorage = (device) => {
  if (window.confirm(`确定要清理 ${device.name} 的存储缓存吗？`)) {
    window.alert('存储清理指令已发送')
  }
}

const doAddDevice = () => {
  const { name, id, user } = newDevice.value
  if (!name || !id || !user) return
  devices.value.push({
    id, name, user,
    online: false, battery: 0, signal: '-', storage: '0/32 GB', firmware: 'v1.0.0',
    lastSeen: '从未', todaySteps: 0, todayDist: '0', todayVoice: 0, todayAlerts: 0,
    sensors: { camera: false, microphone: false, gps: false, gyroscope: false }
  })
  showAddModal.value = false
  newDevice.value = { name: '', id: '', user: '' }
}
</script>

<style scoped>
/* ── 整体 ── */
.devices-page {
  padding: 20px 20px 16px 24px;
  background: #f1f5f9;
  min-height: calc(100vh - 52px);
  display: flex;
  flex-direction: column;
  gap: 14px;
}

/* ── 页头 ── */
.page-header {
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

.summary-chips {
  display: flex;
  gap: 8px;
}

.chip {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 5px 11px;
  border-radius: 20px;
  font-size: 12px;
  border: 1px solid;
}

.chip-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}

.chip-num { font-size: 14px; font-weight: 700; }
.chip-label { color: #64748b; }

.chip.green  { background: #f0fdf4; border-color: #bbf7d0; color: #15803d; }
.chip.green .chip-dot { background: #22c55e; }
.chip.red    { background: #fef2f2; border-color: #fca5a5; color: #dc2626; }
.chip.red .chip-dot { background: #ef4444; }
.chip.blue   { background: #eff6ff; border-color: #93c5fd; color: #2563eb; }

.header-right {
  display: flex;
  gap: 10px;
  align-items: center;
}

.search-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 7px 12px;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 9px;
}

.search-wrap svg { width: 15px; height: 15px; color: #94a3b8; flex-shrink: 0; }

.search-wrap input {
  border: none;
  outline: none;
  font-size: 13px;
  color: #1e293b;
  width: 180px;
  background: transparent;
}

.add-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  background: #3b82f6;
  color: #fff;
  border: none;
  border-radius: 9px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.add-btn svg { width: 16px; height: 16px; }
.add-btn:hover { background: #2563eb; box-shadow: 0 3px 10px rgba(59,130,246,0.35); }

/* ── 主体 ── */
.devices-body {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 14px;
  flex: 1;
  min-height: 0;
}

/* ── 设备网格 ── */
.devices-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 12px;
  align-content: start;
  overflow-y: auto;
}

.devices-grid::-webkit-scrollbar { width: 4px; }
.devices-grid::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 2px; }

.device-card {
  background: #fff;
  border-radius: 14px;
  padding: 16px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.06);
  cursor: pointer;
  transition: box-shadow 0.2s, transform 0.15s;
  border: 2px solid transparent;
}

.device-card:hover {
  box-shadow: 0 6px 20px rgba(0,0,0,0.1);
  transform: translateY(-2px);
}

.device-card.selected { border-color: #3b82f6; }
.device-card.offline { opacity: 0.7; }

/* ── 卡片头 ── */
.dcard-head {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
}

.dcard-avatar {
  width: 40px;
  height: 40px;
  border-radius: 11px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.dcard-avatar svg { width: 22px; height: 22px; }
.av-online { background: #dbeafe; color: #2563eb; }
.av-offline { background: #f1f5f9; color: #94a3b8; }

.dcard-info { flex: 1; min-width: 0; }

.dcard-name {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 2px;
}

.dcard-id {
  font-size: 11px;
  color: #94a3b8;
}

.dcard-status-badge {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 3px 8px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 600;
  flex-shrink: 0;
}

.status-dot-sm {
  width: 5px;
  height: 5px;
  border-radius: 50%;
}

.dcard-status-badge.online  { background: #dcfce7; color: #166534; }
.dcard-status-badge.online .status-dot-sm { background: #22c55e; }
.dcard-status-badge.offline { background: #f1f5f9; color: #64748b; }
.dcard-status-badge.offline .status-dot-sm { background: #94a3b8; }

/* ── 卡片统计 ── */
.dcard-stats {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 12px;
}

.dstat-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.dstat-icon {
  width: 26px;
  height: 26px;
  border-radius: 7px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.dstat-icon svg { width: 15px; height: 15px; }
.battery-icon { background: #dbeafe; color: #2563eb; }
.signal-icon  { background: #dcfce7; color: #16a34a; }
.storage-icon { background: #fef3c7; color: #d97706; }

.dstat-body { display: flex; gap: 6px; align-items: center; flex-shrink: 0; min-width: 0; }
.dstat-label { font-size: 11px; color: #94a3b8; min-width: 28px; }
.dstat-val { font-size: 12px; font-weight: 600; color: #1e293b; }

.val-green { color: #16a34a; }
.val-yellow { color: #d97706; }
.val-red { color: #dc2626; }

.dstat-bar { flex: 1; height: 4px; background: #e2e8f0; border-radius: 2px; overflow: hidden; }
.dstat-fill { height: 100%; border-radius: 2px; transition: width 0.4s; }
.fill-green  { background: #22c55e; }
.fill-yellow { background: #f59e0b; }
.fill-red    { background: #ef4444; }
.fill-blue   { background: #3b82f6; }

/* ── 传感器芯片 ── */
.dcard-sensors {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-bottom: 12px;
}

.sensor-chip {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 2px 8px;
  border-radius: 5px;
  font-size: 11px;
  font-weight: 500;
}

.sensor-chip svg { width: 11px; height: 11px; }
.sensor-ok  { background: #dcfce7; color: #166534; }
.sensor-err { background: #fee2e2; color: #991b1b; }

/* ── 卡片操作 ── */
.dcard-actions {
  display: flex;
  gap: 7px;
  border-top: 1px solid #f1f5f9;
  padding-top: 10px;
}

.daction-btn {
  flex: 1;
  height: 32px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 7px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  transition: all 0.15s;
}

.daction-btn svg { width: 14px; height: 14px; }

.daction-btn:hover {
  background: #eff6ff;
  border-color: #bae6fd;
  color: #0369a1;
}

.empty-state {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 60px 24px;
  color: #94a3b8;
  font-size: 14px;
}
.empty-state svg { width: 48px; height: 48px; }

/* ── 详情面板 ── */
.detail-panel {
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.06);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: sticky;
  top: 0;
  max-height: calc(100vh - 106px);
}

.detail-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 16px;
  border-bottom: 1px solid #f1f5f9;
  flex-shrink: 0;
}

.detail-head-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.detail-avatar {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.detail-avatar svg { width: 20px; height: 20px; }

.detail-name { font-size: 14px; font-weight: 700; color: #1e293b; }
.detail-id-tag { font-size: 10.5px; color: #94a3b8; margin-top: 1px; }

.close-btn {
  width: 28px;
  height: 28px;
  border: 1px solid #e2e8f0;
  border-radius: 7px;
  background: #f8fafc;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  transition: all 0.15s;
}

.close-btn svg { width: 13px; height: 13px; }
.close-btn:hover { background: #fee2e2; border-color: #fca5a5; color: #dc2626; }

.detail-scroll {
  overflow-y: auto;
  flex: 1;
  padding: 14px 16px;
}

.detail-scroll::-webkit-scrollbar { width: 3px; }
.detail-scroll::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 2px; }

.detail-section { margin-bottom: 18px; }
.detail-section:last-child { margin-bottom: 0; }

.section-title {
  font-size: 12px;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-bottom: 10px;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 8px 10px;
  background: #f8fafc;
  border-radius: 8px;
}

.info-label { font-size: 10.5px; color: #94a3b8; }
.info-val { font-size: 13px; font-weight: 600; color: #1e293b; }
.text-green { color: #16a34a; }
.text-red { color: #dc2626; }

/* 监控列表 */
.monitor-list { display: flex; flex-direction: column; gap: 8px; }

.monitor-row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 7px 10px;
  background: #f8fafc;
  border-radius: 8px;
}

.monitor-icon {
  width: 28px;
  height: 28px;
  border-radius: 7px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.monitor-icon svg { width: 15px; height: 15px; }

.monitor-info {
  display: flex;
  flex-direction: column;
  gap: 1px;
  min-width: 60px;
}

.monitor-label { font-size: 10px; color: #94a3b8; }
.monitor-val { font-size: 12px; font-weight: 700; color: #1e293b; }

.monitor-bar-wrap { flex: 1; }
.monitor-bar-track { height: 5px; background: #e2e8f0; border-radius: 3px; overflow: hidden; }
.monitor-bar-fill { height: 100%; border-radius: 3px; transition: width 0.4s; }

/* 传感器卡片 */
.sensor-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.sensor-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 12px 8px;
  border-radius: 10px;
  border: 1.5px solid;
  text-align: center;
}

.sensor-card-icon {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sensor-card-icon svg { width: 20px; height: 20px; }
.sensor-card-name { font-size: 11px; font-weight: 600; color: #1e293b; }
.sensor-card-status { font-size: 10px; }

.card-ok  { background: #f0fdf4; border-color: #86efac; color: #16a34a; }
.card-ok .sensor-card-status { color: #16a34a; }
.card-err { background: #fef2f2; border-color: #fca5a5; color: #dc2626; }
.card-err .sensor-card-status { color: #dc2626; }

/* 远程控制 */
.ctrl-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.ctrl-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  padding: 14px 8px;
  background: #f8fafc;
  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  cursor: pointer;
  text-align: center;
  transition: all 0.2s;
}

.ctrl-card:hover {
  background: #f0f9ff;
  border-color: #bae6fd;
  transform: translateY(-1px);
  box-shadow: 0 3px 10px rgba(0,0,0,0.07);
}

.ctrl-icon {
  width: 32px;
  height: 32px;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ctrl-icon svg { width: 17px; height: 17px; }
.mic-bg     { background: #dbeafe; color: #2563eb; }
.restart-bg { background: #dcfce7; color: #16a34a; }
.update-bg  { background: #ede9fe; color: #7c3aed; }
.trash-bg   { background: #fee2e2; color: #dc2626; }

.ctrl-label { font-size: 12px; font-weight: 600; color: #1e293b; }
.ctrl-desc  { font-size: 10px; color: #94a3b8; }

/* 今日统计 */
.today-stats {
  display: flex;
  align-items: center;
  padding: 12px 8px;
  background: #f8fafc;
  border-radius: 10px;
}

.today-stat-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
}

.ts-num { font-size: 18px; font-weight: 700; color: #1e293b; }
.ts-label { font-size: 10px; color: #94a3b8; }
.ts-div { width: 1px; height: 28px; background: #e2e8f0; }

/* ── 弹窗 ── */
.modal-wrap {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  backdrop-filter: blur(3px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-box {
  width: 480px;
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.15);
  animation: modal-in 0.22s ease;
}

@keyframes modal-in {
  from { opacity: 0; transform: scale(0.94) translateY(12px); }
  to   { opacity: 1; transform: scale(1)   translateY(0); }
}

.modal-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
  border-bottom: 1px solid #f1f5f9;
}

.modal-body { padding: 20px; display: flex; flex-direction: column; gap: 14px; }

.form-field { display: flex; flex-direction: column; gap: 5px; }

.form-field label { font-size: 12.5px; font-weight: 600; color: #475569; }

.form-field input {
  padding: 9px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 13.5px;
  color: #1e293b;
  outline: none;
  transition: border-color 0.15s;
}

.form-field input:focus { border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59,130,246,0.1); }

.modal-foot {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  padding: 14px 20px;
  border-top: 1px solid #f1f5f9;
}

.modal-btn {
  padding: 8px 18px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.15s;
}

.modal-btn.cancel { background: #f1f5f9; color: #64748b; }
.modal-btn.cancel:hover { background: #e2e8f0; }
.modal-btn.confirm { background: #3b82f6; color: #fff; }
.modal-btn.confirm:hover { background: #2563eb; box-shadow: 0 3px 10px rgba(59,130,246,0.3); }
</style>
