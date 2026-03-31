<template>
  <div class="asr-container">
    <div class="asr-header">
      <h2>智能指令中枢</h2>
      <div class="header-controls">
        <div class="network-status" :class="{ online: isOnline, offline: !isOnline }">
          <div class="status-dot"></div>
          <span>{{ isOnline ? '大脑已连接' : '网络离线' }}</span>
        </div>
        <div class="status-indicator" :class="{ active: isRecording, thinking: isThinking }">
          <div class="led"></div>
          <span>{{ getStatusText() }}</span>
        </div>
      </div>
    </div>

    <div class="asr-content">
      <div class="conversation-area">
        <div class="messages" ref="messagesContainer">
          <div v-if="messages.length === 0" class="empty-state">
            长按下方按钮或点击悬浮球开始对话
          </div>
          <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.role]">
            <div class="message-content">
              <div class="message-text">{{ msg.content }}</div>
              <div class="message-time">{{ msg.time }}</div>
            </div>
          </div>
          <div v-if="streamingContent" class="message bot">
            <div class="message-content">
              <div class="message-text">{{ streamingContent }}<span class="cursor">|</span></div>
              <div class="message-time">正在回复...</div>
            </div>
          </div>
        </div>
      </div>

      <div class="controls">
        <button 
          @mousedown="startRecording" 
          @mouseup="stopRecording"
          @mouseleave="stopRecording"
          @touchstart.prevent="startRecording"
          @touchend.prevent="stopRecording"
          :class="['mic-btn', { recording: isRecording, thinking: isThinking }]"
        >
          <div class="mic-icon-wrapper">
            <span v-if="!isRecording && !isThinking">🎤</span>
            <span v-if="isRecording">🔴</span>
            <span v-if="isThinking">⏳</span>
          </div>
          {{ getBtnText() }}
          <div class="ripple" v-if="isRecording"></div>
        </button>
        
        <button @click="clearHistory" class="reset-btn">清空对话</button>
      </div>

      <div class="settings-grid">
        <div class="setting-item">
          <label>语音引擎</label>
          <select v-model="engine"><option>Paraformer-V2 + Coze</option></select>
        </div>
        <div class="setting-item">
          <label>交互反馈</label>
          <div class="toggle-group">
            <span>AR弹窗</span><input type="checkbox" checked>
            <span>地图联动</span><input type="checkbox" checked>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, inject } from 'vue'

// 注入全局神经系统
const eventBus = inject('eventBus')

// 状态定义
const messages = ref([])
const streamingContent = ref('')
const isRecording = ref(false)
const isThinking = ref(false)
const isOnline = ref(true)
const messagesContainer = ref(null)
const engine = ref('Paraformer-V2 + Coze')

let mediaRecorder = null
let audioChunks = []

// --- 核心逻辑：对接后端统一大脑 ---
const sendAudioToBackend = async (audioBlob) => {
  isThinking.value = true
  const formData = new FormData()
  formData.append('audio', audioBlob, 'query.wav')

  try {
    // 1. 调用整合后的后端 5002 端口
    const response = await fetch('http://localhost:5002/api/assistant', {
      method: 'POST',
      body: formData
    })

    if (!response.ok) throw new Error('后端响应异常')

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    streamingContent.value = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const chunk = decoder.decode(value)
      
      // 2. 解析 USER_TEXT 协议，同步更新用户 UI
      if (chunk.includes('USER_TEXT:')) {
        const userText = chunk.split('USER_TEXT:')[1].split('\n\n')[0]
        addMessage('user', userText)
        // 联动：如果识别到导航意图，触发地图组件
        if (userText.includes('去') || userText.includes('导航')) {
            eventBus.emit('send-text-cmd', userText)
        }
      } else {
        // 3. 实时更新 AI 流式文字，并同步给视频弹窗
        streamingContent.value += chunk
        eventBus.emit('voice-prompt', { text: chunk, type: 'info' })
      }
      scrollToBottom()
    }

    // 回复结束，转入正式消息列表
    if (streamingContent.value) {
      addMessage('bot', streamingContent.value)
      streamingContent.value = ''
    }

  } catch (err) {
    console.error('通信失败:', err)
    addMessage('bot', '抱歉，大脑连接失败，请确保后端 5002 端口已启动。')
  } finally {
    isThinking.value = false
    scrollToBottom()
  }
}

// --- 录音控制 ---
const startRecording = async () => {
  if (isThinking.value) return
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder = new MediaRecorder(stream)
    audioChunks = []
    mediaRecorder.ondataavailable = e => audioChunks.push(e.data)
    mediaRecorder.start()
    isRecording.value = true
  } catch (err) {
    alert('无法访问麦克风，请检查权限')
  }
}

const stopRecording = () => {
  if (!mediaRecorder || !isRecording.value) return
  mediaRecorder.stop()
  mediaRecorder.stream.getTracks().forEach(t => t.stop())
  isRecording.value = false
  mediaRecorder.onstop = () => {
    const blob = new Blob(audioChunks, { type: 'audio/wav' })
    sendAudioToBackend(blob)
  }
}

// --- 辅助功能 ---
const addMessage = (role, content) => {
  const time = new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  messages.value.push({ role, content, time })
  // 同步到语音播报历史记录
  if (role === 'bot') {
    eventBus.emit('add-voice-history', { text: content, type: 'info', time })
  }
}

const clearHistory = () => { messages.value = [] }

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const getStatusText = () => {
  if (isRecording.value) return '正在听...'
  if (isThinking.value) return '思考中...'
  return '待机中'
}

const getBtnText = () => {
  if (isRecording.value) return '松开 发送'
  if (isThinking.value) return '请稍候'
  return '按住 说话'
}

// 监听来自悬浮球的快捷指令
onMounted(() => {
  if (eventBus) {
    eventBus.on('send-text-cmd', (text) => {
      // 如果是快捷文本指令，逻辑可在此处直接调用 text 接口或模拟语音
      addMessage('user', text)
      // 提示用户正在处理
      eventBus.emit('voice-prompt', { text: `收到指令：${text}`, type: 'success' })
    })
  }
})
</script>

<style scoped>
.asr-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-radius: 18px;
  border: 1px solid rgba(0, 0, 0, 0.08);
}

.asr-header {
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  background: rgba(248, 250, 252, 0.9);
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.asr-header h2 { font-size: 1.2rem; color: #3b82f6; margin: 0; }

.header-controls { display: flex; gap: 15px; align-items: center; }

.status-dot { width: 8px; height: 8px; border-radius: 50%; background: #475569; }
.online .status-dot { background: #10b981; box-shadow: 0 0 10px #10b981; }

.status-indicator { display: flex; align-items: center; gap: 6px; font-size: 12px; }
.led { width: 8px; height: 8px; border-radius: 50%; background: #475569; }
.active .led { background: #ef4444; animation: blink 1s infinite; }
.thinking .led { background: #3b82f6; animation: pulse 1s infinite; }

.asr-content { flex: 1; padding: 20px; display: flex; flex-direction: column; overflow: hidden; }

.conversation-area { flex: 1; overflow-y: auto; margin-bottom: 20px; padding-right: 5px; }

.message { display: flex; margin-bottom: 15px; }
.message.user { justify-content: flex-end; }
.message-content { max-width: 80%; padding: 10px 15px; border-radius: 15px; position: relative; }
.user .message-content { background: #3b82f6; color: white; border-bottom-right-radius: 2px; }
.bot .message-content { background: rgba(0, 0, 0, 0.08); color: #1e293b; border-bottom-left-radius: 2px; }

.message-text { font-size: 14px; line-height: 1.5; }
.message-time { font-size: 10px; opacity: 0.5; margin-top: 5px; }

.controls { display: flex; align-items: center; gap: 20px; padding: 10px 0; }

.mic-btn {
  flex: 1;
  height: 60px;
  border-radius: 30px;
  border: none;
  background: rgba(59, 130, 246, 0.15);
  color: #1e293b;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
}

.mic-btn.recording { background: rgba(239, 68, 68, 0.2); transform: scale(0.98); }
.mic-btn.thinking { background: rgba(59, 130, 246, 0.25); }

.ripple {
  position: absolute;
  width: 100%; height: 100%; background: rgba(239, 68, 68, 0.15);
  animation: ripple 1.5s infinite; border-radius: 30px;
}

.reset-btn { background: none; border: 1px solid rgba(0,0,0,0.15); color: #64748b; padding: 8px 15px; border-radius: 20px; cursor: pointer; }

.settings-grid {
  display: grid; grid-template-columns: 1fr 1fr; gap: 15px;
  padding: 15px; background: rgba(248, 250, 252, 0.8); border-radius: 12px; margin-top: 10px;
}

.setting-item { display: flex; flex-direction: column; gap: 5px; font-size: 12px; }
.setting-item select { background: #fff; color: #1e293b; border: 1px solid rgba(0,0,0,0.15); padding: 5px; border-radius: 4px; }
.toggle-group { display: flex; gap: 8px; align-items: center; color: #64748b; }

@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
@keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.1); } 100% { transform: scale(1); } }
@keyframes ripple { 0% { transform: scale(1); opacity: 0.4; } 100% { transform: scale(2); opacity: 0; } }

.cursor { animation: blink 1s infinite; margin-left: 2px; font-weight: bold; color: #3b82f6; }

.empty-state {
  color: rgba(30, 41, 59, 0.5);
  text-align: center;
  padding: 40px 20px;
}
</style>