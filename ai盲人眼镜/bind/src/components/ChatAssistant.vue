<template>
  <div class="chat-assistant-container">
    <transition name="pop">
      <div v-if="isOpen" class="chat-bubble">
        <div class="bubble-header">
          <div class="status-box">
            <span class="status-dot" :class="{ active: isSystemActive, recording: isRecording }"></span>
            <span class="status-text">{{ statusText }}</span>
          </div>
          <button class="close-btn" @click="toggleChat">×</button>
        </div>

        <div class="bubble-content" ref="msgContainer">
          <div v-if="messages.length === 0" class="welcome-msg">
            您好，我是智能导航助手。请长按下方麦克风或输入文字调试。
          </div>
          <div v-for="(msg, index) in messages" :key="index" :class="['message-row', msg.role]">
            <div class="message-bubble">{{ msg.text }}</div>
          </div>
          <div v-if="streamingContent" class="message-row ai">
            <div class="message-bubble streaming">{{ streamingContent }}<span class="typing-cursor">|</span></div>
          </div>
        </div>

        <div class="bubble-footer">
          <div class="input-area">
            <input v-model="inputText" @keyup.enter="handleSendText" placeholder="输入调试文字..." :disabled="isThinking" />
            <button class="send-text-btn" @click="handleSendText" :disabled="isThinking || !inputText.trim()">发送</button>
          </div>

          <div class="control-bar">
            <button 
              class="mic-btn"
              :class="{ active: isRecording, thinking: isThinking }"
              @mousedown.prevent="startRecording"
              @mouseup.prevent="stopRecording"
              @mouseleave="stopRecording"
              @touchstart.prevent="startRecording"
              @touchend.prevent="stopRecording"
            >
              <span v-if="!isThinking">{{ isRecording ? '🔴' : '🎤' }}</span>
              <span v-else class="loading-icon">⏳</span>
            </button>
            <div class="mic-tip">{{ micTip }}</div>
          </div>
        </div>
      </div>
    </transition>

    <div class="floating-ball" @click="toggleChat" :class="{ hidden: isOpen }">
      <div class="ball-content">
        <span class="ball-icon">🤖</span>
        <div class="wave-ring"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject, nextTick, computed } from 'vue'
import Recorder from 'recorder-core' // 核心库
import 'recorder-core/src/engine/wav' // WAV 引擎

const isOpen = ref(false)
const isSystemActive = ref(true)
const messages = ref([])
const streamingContent = ref('')
const isRecording = ref(false)
const isThinking = ref(false)
const msgContainer = ref(null)
const inputText = ref('')

const eventBus = inject('eventBus')
let rec = null; // 录音机实例

const statusText = computed(() => isRecording.value ? '正在听...' : (isThinking.value ? '思考中...' : 'AI 助手已就绪'))
const micTip = computed(() => isRecording.value ? '松开发送' : (isThinking.value ? '正在处理...' : '长按说话'))

const toggleChat = () => { isOpen.value = !isOpen.value; if (isOpen.value) scrollToBottom(); }
const scrollToBottom = () => { nextTick(() => { if (msgContainer.value) msgContainer.value.scrollTop = msgContainer.value.scrollHeight; }) }

// --- 核心：流式处理 ---
const processStream = async (response) => {
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  streamingContent.value = '';
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const chunk = decoder.decode(value);
    if (chunk.includes('USER_TEXT:')) {
      const userText = chunk.split('USER_TEXT:')[1].split('\n\n')[0];
      if (!messages.value.find(m => m.role === 'user' && m.text === userText)) messages.value.push({ role: 'user', text: userText });
      if (userText.includes('去') || userText.includes('导航')) eventBus.emit('send-text-cmd', userText);
    } else {
      streamingContent.value += chunk;
    }
    scrollToBottom();
  }
  messages.value.push({ role: 'ai', text: streamingContent.value });
  streamingContent.value = '';
}

// --- 文字发送 ---
const handleSendText = async () => {
  const text = inputText.value.trim();
  if (!text || isThinking.value) return;
  inputText.value = ''; isThinking.value = true;
  messages.value.push({ role: 'user', text });
  try {
    const resp = await fetch('http://localhost:5002/api/coze-text', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    await processStream(resp);
  } catch (err) { messages.value.push({ role: 'ai', text: '连接失败' }); }
  finally { isThinking.value = false; scrollToBottom(); }
}

// --- 录音逻辑：生成标准 16k WAV ---
const startRecording = () => {
  if (isThinking.value) return;
  rec = Recorder({
    type: "wav",
    sampleRate: 16000, // 后端要求 16000
    bitRate: 16,
    onProcess: () => {}
  });
  rec.open(() => {
    rec.start();
    isRecording.value = true;
  });
}

const stopRecording = () => {
  if (!rec || !isRecording.value) return;
  isRecording.value = false;
  rec.stop((blob) => {
    sendAudioToBackend(blob);
    rec.close();
  }, () => rec.close());
}

const sendAudioToBackend = async (blob) => {
  isThinking.value = true;
  const form = new FormData();
  form.append('audio', blob, 'voice.wav');
  try {
    const resp = await fetch('http://localhost:5002/api/assistant', { method: 'POST', body: form });
    if (resp.status === 409) { messages.value.push({ role: 'ai', text: '⚠️ 别急，等我说完您再讲～' }); return; }
    if (!resp.ok) throw new Error();
    await processStream(resp);
  } catch (err) { messages.value.push({ role: 'ai', text: '识别失败，请重试' }); }
  finally { isThinking.value = false; scrollToBottom(); }
}
</script>

<style scoped>
/* 原有样式保持不变，新增以下样式 */

.input-area {
  display: flex;
  gap: 10px;
  padding: 10px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  margin-bottom: 10px;
}

.input-area input {
  flex: 1;
  background: rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 20px;
  padding: 8px 16px;
  color: #1e293b;
  font-size: 14px;
  outline: none;
}

.input-area input:focus {
  border-color: #3b82f6;
}

.send-text-btn {
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 20px;
  padding: 0 16px;
  font-size: 13px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.send-text-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.chat-assistant-container {
  position: fixed;
  bottom: 30px;
  right: 30px;
  z-index: 9999;
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
}

.floating-ball {
  width: 75px;
  height: 75px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
}

.floating-ball:hover {
  transform: scale(1.1) rotate(5deg);
}

.floating-ball.hidden {
  transform: scale(0);
  opacity: 0;
}

.ball-icon {
  font-size: 30px;
  z-index: 2;
}

.wave-ring {
  position: absolute;
  top: 0; 
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.5);
  animation: ripple 2s infinite;
}

@keyframes ripple {
  0% { transform: scale(1); opacity: 0.8; }
  100% { transform: scale(1.8); opacity: 0; }
}

.chat-bubble {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 30vw;
  height: 90vh;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(15px);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  transform-origin: bottom right;
  overflow: hidden;
}

.bubble-header {
  padding: 15px 18px;
  background: rgba(248, 250, 252, 0.9);
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.status-box {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #64748b;
}

.status-dot {
  width: 8px;
  height: 8px;
  background: #64748b;
  border-radius: 50%;
}

.status-dot.active {
  background: #10b981;
  box-shadow: 0 0 10px #10b981;
}

.bubble-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.message-row { display: flex; margin-bottom: 12px; }
.message-row.user { justify-content: flex-end; }
.message-bubble {
  max-width: 85%;
  padding: 10px 14px;
  border-radius: 16px;
  font-size: 14px;
}
.user .message-bubble { background: #3b82f6; color: white; border-bottom-right-radius: 4px; }
.ai .message-bubble { background: rgba(0, 0, 0, 0.08); color: #1e293b; border-bottom-left-radius: 4px; }

.bubble-footer {
  padding: 20px;
  background: rgba(248, 250, 252, 0.8);
}

.control-bar {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.mic-btn {
  width: 60px;
  height: 50px;
  border-radius: 50%;
  border: none;
  background: rgba(0, 0, 0, 0.08);
  color: #1e293b;
  font-size: 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.mic-tip { 
  font-size: 12px;
  color: #64748b;
}

.mic-btn.active {
  background: #ef4444;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
  70% { box-shadow: 0 0 0 15px rgba(239, 68, 68, 0); }
  100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}

.pop-enter-active, .pop-leave-active {
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.pop-enter-from, .pop-leave-to {
  opacity: 0;
  transform: scale(0.6) translate(40px, 40px);
}
</style>