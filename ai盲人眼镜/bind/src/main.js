// src/main.js
import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'

// 1. 导入你现有的事件总线
import eventBus from './utils/eventBus'

const app = createApp(App)

// 2. 将事件总线全局注入
// 注意：由于你的 eventBus 是用 ref 定义的，我们注入 eventBus.value 方便直接调用 .on 和 .emit
app.provide('eventBus', eventBus.value) 

app.use(router).mount('#app')