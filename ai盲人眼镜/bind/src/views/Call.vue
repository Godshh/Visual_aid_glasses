<template>
  <div class="call-page">
    <div id="trtc-audio-container" style="display:none"></div>

    <!-- 顶部状态栏区域 -->
    <div class="call-top">
      <div class="call-status-text">{{ statusText }}</div>
    </div>

    <!-- 中央头像区 -->
    <div class="call-center">
      <div class="avatar-wrap">
        <div class="avatar" :class="{ connected: state === 'connected', failed: state === 'failed' }">
          <svg viewBox="0 0 24 24" fill="none">
            <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
            <circle cx="12" cy="7" r="4" stroke="currentColor" stroke-width="1.4"/>
          </svg>
        </div>
        <!-- 呼叫中才显示波纹 -->
        <template v-if="state === 'connecting'">
          <div class="ripple r1"/>
          <div class="ripple r2"/>
          <div class="ripple r3"/>
        </template>
      </div>

      <div class="caller-name">志愿者</div>

      <div class="call-state-hint">
        <span v-if="state === 'connecting'" class="dots-text">等待接听</span>
        <span v-else-if="state === 'connected'" class="duration-text">{{ durationText }}</span>
        <span v-else-if="state === 'failed'" class="failed-text">{{ errorMsg || '通话失败' }}</span>
      </div>
    </div>

    <!-- 底部控制区 -->
    <div class="call-bottom">
      <template v-if="state !== 'failed'">
        <!-- 静音 -->
        <div class="ctrl-item" @click="toggleMute">
          <div class="ctrl-btn" :class="{ active: muted }">
            <svg v-if="!muted" viewBox="0 0 24 24" fill="none">
              <path d="M12 1a3 3 0 013 3v7a3 3 0 01-6 0V4a3 3 0 013-3z" stroke="currentColor" stroke-width="1.6"/>
              <path d="M19 10v1a7 7 0 01-14 0v-1M12 18v4M8 22h8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="none">
              <line x1="1" y1="1" x2="23" y2="23" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
              <path d="M9 9v3a3 3 0 005.12 2.12M15 9.34V4a3 3 0 00-5.94-.6M17 16.95A7 7 0 015 12v-2M12 19v4M8 23h8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
            </svg>
          </div>
          <span>{{ muted ? '取消静音' : '静音' }}</span>
        </div>

        <!-- 挂断 -->
        <div class="ctrl-item hangup-item" @click="hangUp">
          <div class="ctrl-btn hangup-btn">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M10.68 13.31a16 16 0 003.41 2.6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92v3a2 2 0 01-2.18 2A19.79 19.79 0 013.09 4.18 2 2 0 015.07 2h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L9.09 9.91" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
              <line x1="23" y1="1" x2="1" y2="23" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
            </svg>
          </div>
          <span>挂断</span>
        </div>

        <!-- 扬声器 -->
        <div class="ctrl-item" @click="toggleSpeaker">
          <div class="ctrl-btn" :class="{ active: speakerOn }">
            <svg viewBox="0 0 24 24" fill="none">
              <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
              <path v-if="speakerOn" d="M19.07 4.93a10 10 0 010 14.14M15.54 8.46a5 5 0 010 7.07" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
            </svg>
          </div>
          <span>{{ speakerOn ? '扬声器' : '听筒' }}</span>
        </div>
      </template>

      <!-- 失败时只显示关闭 -->
      <template v-else>
        <div class="ctrl-item hangup-item" @click="hangUp">
          <div class="ctrl-btn hangup-btn">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <span>关闭</span>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { genUserSig } from '@/utils/trtc.js'

const USER_ID  = 'user001'
const ROOM_ID  = 123456

const state       = ref('connecting')
const durationText = ref('00:00')
const muted       = ref(false)
const speakerOn   = ref(true)
const errorMsg    = ref('')

const statusText = computed(() => {
  if (state.value === 'connecting') return '正在连接...'
  if (state.value === 'connected')  return '通话中'
  return '通话结束'
})

let _client      = null
let _localStream = null
let _timer       = null
let _seconds     = 0

onMounted(() => { startCall() })
onUnmounted(() => { cleanup() })

async function startCall() {
  try {
    const TRTC = (await import('trtc-js-sdk')).default
    const { sdkAppId, userSig } = genUserSig(USER_ID)

    _client = TRTC.createClient({ sdkAppId, userId: USER_ID, userSig, mode: 'rtc' })

    _client.on('stream-added', async (e) => {
      await _client.subscribe(e.stream, { audio: true, video: false })
    })
    _client.on('stream-subscribed', (e) => {
      e.stream.play('trtc-audio-container')
    })
    _client.on('peer-join',  () => { state.value = 'connected'; startTimer() })
    _client.on('peer-enter', () => { state.value = 'connected'; startTimer() })
    _client.on('peer-leave', () => { hangUp() })
    _client.on('error', (e) => { errorMsg.value = e.message || '未知错误'; state.value = 'failed' })

    await _client.join({ roomId: ROOM_ID })
    _localStream = TRTC.createStream({ audio: true, video: false })
    await _localStream.initialize()
    await _client.publish(_localStream)

  } catch (e) {
    console.error('通话失败:', e)
    errorMsg.value = e.message || '启动失败'
    state.value = 'failed'
  }
}

function startTimer() {
  if (_timer) return
  _timer = setInterval(() => {
    _seconds++
    const m = String(Math.floor(_seconds / 60)).padStart(2, '0')
    const s = String(_seconds % 60).padStart(2, '0')
    durationText.value = `${m}:${s}`
  }, 1000)
}

function toggleMute() {
  muted.value = !muted.value
  if (_localStream) muted.value ? _localStream.muteAudio() : _localStream.unmuteAudio()
}

function toggleSpeaker() {
  speakerOn.value = !speakerOn.value
}

function hangUp() {
  cleanup()
  if (typeof wx !== 'undefined' && wx.miniProgram) {
    wx.miniProgram.navigateBack({ delta: 1 })
  } else {
    window.history.back()
  }
}

function cleanup() {
  if (_timer) { clearInterval(_timer); _timer = null }
  _seconds = 0
  if (_localStream) { _localStream.stop?.(); _localStream.close?.(); _localStream = null }
  if (_client) { _client.leave().catch(() => {}); _client = null }
}
</script>

<style scoped>
* { box-sizing: border-box; margin: 0; padding: 0; }

.call-page {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  background: linear-gradient(180deg, #1c2b4a 0%, #111827 60%, #0a0e1a 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', sans-serif;
  color: #fff;
  overflow: hidden;
  /* 遮住小程序侧边栏 */
  z-index: 9999;
}

/* ── 顶部 ── */
.call-top {
  width: 100%;
  padding: 56px 24px 0;
  text-align: center;
}

.call-status-text {
  font-size: 13px;
  color: rgba(255,255,255,0.45);
  letter-spacing: 0.06em;
}

/* ── 中央 ── */
.call-center {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 18px;
}

.avatar-wrap {
  position: relative;
  width: 140px;
  height: 140px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar {
  width: 116px;
  height: 116px;
  border-radius: 50%;
  background: rgba(255,255,255,0.08);
  border: 2px solid rgba(255,255,255,0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 1;
  transition: border-color 0.4s, box-shadow 0.4s;
}

.avatar.connected {
  border-color: #4ade80;
  box-shadow: 0 0 0 10px rgba(74,222,128,0.1), 0 0 40px rgba(74,222,128,0.15);
}

.avatar.failed {
  border-color: #ef4444;
}

.avatar svg {
  width: 56px;
  height: 56px;
  color: rgba(255,255,255,0.75);
}

.ripple {
  position: absolute;
  border-radius: 50%;
  border: 1.5px solid rgba(255,255,255,0.2);
  animation: ripple 2.4s ease-out infinite;
}
.r1 { width: 126px; height: 126px; animation-delay: 0s; }
.r2 { width: 148px; height: 148px; animation-delay: 0.7s; }
.r3 { width: 170px; height: 170px; animation-delay: 1.4s; }

@keyframes ripple {
  0%   { transform: scale(0.88); opacity: 0.6; }
  100% { transform: scale(1.2);  opacity: 0; }
}

.caller-name {
  font-size: 28px;
  font-weight: 600;
  letter-spacing: 2px;
  color: #fff;
}

.call-state-hint {
  height: 24px;
  display: flex;
  align-items: center;
}

.dots-text {
  font-size: 14px;
  color: rgba(255,255,255,0.4);
}

.dots-text::after {
  content: '';
  animation: dots 1.5s infinite;
}

@keyframes dots {
  0%   { content: ''; }
  33%  { content: '.'; }
  66%  { content: '..'; }
  100% { content: '...'; }
}

.duration-text {
  font-size: 22px;
  font-weight: 500;
  color: #4ade80;
  font-variant-numeric: tabular-nums;
  letter-spacing: 2px;
}

.failed-text {
  font-size: 14px;
  color: #ef4444;
}

/* ── 底部控制 ── */
.call-bottom {
  width: 100%;
  padding: 0 0 60px;
  display: flex;
  justify-content: center;
  align-items: flex-end;
  gap: 0;
}

.ctrl-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}

.ctrl-item span {
  font-size: 12px;
  color: rgba(255,255,255,0.55);
  letter-spacing: 0.5px;
}

.ctrl-btn {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: rgba(255,255,255,0.12);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s, transform 0.1s;
}

.ctrl-btn svg {
  width: 26px;
  height: 26px;
  color: rgba(255,255,255,0.85);
}

.ctrl-btn.active {
  background: rgba(255,255,255,0.25);
}

.ctrl-btn:active {
  transform: scale(0.9);
}

.hangup-item span {
  color: rgba(255,255,255,0.55);
}

.hangup-btn {
  width: 68px;
  height: 68px;
  background: #ef4444;
  box-shadow: 0 6px 24px rgba(239,68,68,0.5);
}

.hangup-btn svg {
  width: 28px;
  height: 28px;
  color: #fff;
}

.hangup-btn:active {
  background: #dc2626;
  transform: scale(0.92);
}
</style>
