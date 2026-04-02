import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Dashboard from '../views/Dashboard.vue'
import History from '../views/History.vue'
import Alerts from '../views/Alerts.vue'
import Devices from '../views/Devices.vue'
import Logs from '../views/Logs.vue'
import ASRModule from '../components/ASRModule.vue'
import Call from '../views/Call.vue'

const routes = [
  { path: '/',         name: 'Home',      component: Home },
  { path: '/dashboard',name: 'Dashboard', component: Dashboard },
  { path: '/history',  name: 'History',   component: History },
  { path: '/alerts',   name: 'Alerts',    component: Alerts },
  { path: '/devices',  name: 'Devices',   component: Devices },
  { path: '/logs',     name: 'Logs',      component: Logs },
  { path: '/asr',      name: 'ASR',       component: ASRModule },
  { path: '/call',     name: 'Call',      component: Call },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router