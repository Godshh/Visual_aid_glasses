<template>
  <div class="app-container">
    <Sidebar />
    <GlobalStatusBar />
    <div class="main-content" :class="{ 'with-sidebar': isAdminPage }">
      <router-view />
    </div>
    <ChatAssistant />
  </div>
</template>

<script setup>
import { provide, computed } from 'vue'
import { useRoute } from 'vue-router'
import eventBus from './utils/eventBus'
import Sidebar from './components/Sidebar.vue'
import GlobalStatusBar from './components/GlobalStatusBar.vue'
import ChatAssistant from './components/ChatAssistant.vue'

const route = useRoute()

const adminPages = ['/dashboard', '/history', '/alerts', '/devices', '/logs', '/']

const isAdminPage = computed(() => {
  return adminPages.includes(route.path)
})

provide('eventBus', eventBus.value)
</script>

<style>
/* === 全局重置和基础样式 (保持你之前的样式不变) === */
* { 
  margin: 0; 
  padding: 0; 
  box-sizing: border-box;
}

html, body, #app, .app-container {
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  font-family: "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial, sans-serif;
}

body {
  overflow-x: auto;
}

/* 整体容器 */
.app-container {
  display: flex;
  background: #f8fafc;
  color: #1e293b;
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

.main-content {
  flex: 1;
  margin-left: 64px;
  overflow-y: auto;
  margin-top: 52px;
  position: relative;
}

.main-content.with-sidebar {
  margin-left: 64px;
}

/* 背景装饰及动画 (保持你之前的样式不变) ... */
.app-container::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.03) 0%, transparent 70%);
  animation: rotate 30s linear infinite;
}

.app-container::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 20%, rgba(139, 92, 246, 0.02) 0%, transparent 50%),
    radial-gradient(circle at 50% 50%, rgba(16, 185, 129, 0.02) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(59, 130, 246, 0.02) 0%, transparent 50%);
  pointer-events: none;
}

@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

@keyframes rotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>