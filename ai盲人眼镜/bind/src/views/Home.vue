<!-- src/views/Home.vue  —— 主页面 -->
<template>
  <div class="home-container">
    <!-- 主内容区：三列布局 -->
    <div class="main-grid">
      <!-- 左侧：地图 -->
      <section class="map-box">
        <div class="panel-header">
          <div class="panel-title">
            <span class="panel-icon">🗺️</span>
            <span>导航地图</span>
          </div>
          <div class="panel-status">
            <span class="status-indicator active"></span>
            <span>定位中</span>
          </div>
        </div>
        <MapView />
      </section>
      
      <!-- 中间：视频区域 -->
      <section class="video-box">
        <div class="panel-header">
          <div class="panel-title">
            <span class="panel-icon">📹</span>
            <span>实时视频</span>
          </div>
          <div class="panel-status">
            <span class="status-indicator live"></span>
            <span>实时</span>
          </div>
        </div>
        <RealTimeVideo />
      </section>
      
      <!-- 右侧：语音提示区域 -->
      <section class="voice-box">
        <div class="panel-header">
          <div class="panel-title">
            <span class="panel-icon">🔊</span>
            <span>语音提示</span>
          </div>
          <div class="panel-status">
            <span class="status-indicator" :class="{ active: isVoiceActive }"></span>
            <span>{{ isVoiceActive ? '播放中' : '待机' }}</span>
          </div>
        </div>
        <VoicePrompt />
      </section>
    </div>
  </div>
</template>

<script setup>
import RealTimeVideo from '../components/RealTimeVideo.vue'
import VoicePrompt from '../components/VoicePrompt.vue'
import FeedbackBar from '../components/FeedbackBar.vue'
import MapView from '../components/MapView.vue'
import { ref } from 'vue'

const isVoiceActive = ref(false)

setInterval(() => {
  isVoiceActive.value = Math.random() > 0.7
}, 3000)
</script>

<style scoped>
.home-container {
  padding: 20px 20px 20px 24px;
  background: #f1f5f9;
  min-height: calc(100vh - 52px);
  display: flex;
  flex-direction: column;
}

.main-grid {
  display: grid;
  grid-template-columns: 1fr 1.6fr 0.75fr;
  gap: 16px;
  flex: 1;
  min-height: 0;
}

.map-box,
.video-box,
.voice-box {
  display: flex;
  flex-direction: column;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.06);
  background: #ffffff;
  transition: box-shadow 0.25s ease, transform 0.25s ease;
}

.map-box:hover,
.video-box:hover,
.voice-box:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.12);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 13px 18px;
  background: #ffffff;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  flex-shrink: 0;
}

.panel-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

.panel-icon {
  font-size: 16px;
}

.panel-status {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #64748b;
  background: #f8fafc;
  padding: 4px 10px;
  border-radius: 20px;
}

.status-indicator {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #94a3b8;
}

.status-indicator.active {
  background: #10b981;
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.6);
  animation: pulse 2s infinite;
}

.status-indicator.live {
  background: #ef4444;
  box-shadow: 0 0 8px rgba(239, 68, 68, 0.6);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}
</style>
