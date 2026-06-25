<template>
  <div class="app">
    <header class="header">
      <div class="header-left">
        <div class="logo">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="2" y="3" width="20" height="14" rx="2"/>
            <path d="M8 21h8"/>
            <path d="M12 17v4"/>
          </svg>
        </div>
        <div class="title-group">
          <h1>NAS 监控面板</h1>
          <span class="subtitle">{{ store.systemInfo?.hostname || '---' }}</span>
        </div>
      </div>
      <div class="header-right">
        <div class="status-dot" :class="store.loading ? 'fetching' : 'ok'"></div>
        <span class="refresh-text">{{ refreshInterval }}秒</span>
        <button class="btn-refresh" @click="refreshNow" :disabled="store.loading">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" :class="{ spinning: store.loading }">
            <path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2"/>
          </svg>
        </button>
      </div>
    </header>
    <nav class="nav-bar">
      <a v-for="item in navItems" :key="item.id" :href="'#' + item.id"
         class="nav-item" :class="{ active: activeNav === item.id }"
         @click.prevent="scrollTo(item.id)">
        <span class="nav-icon" v-html="item.icon"></span>
        <span class="nav-label">{{ item.label }}</span>
      </a>
    </nav>
    <main class="main">
      <section id="system"><SystemInfo /></section>
      <div class="row">
        <section id="hardware"><HardwareStatus /></section>
        <section id="network"><NetworkStatus /></section>
      </div>
      <div class="row">
        <section id="storage"><StorageStatus /></section>
        <section id="process"><ProcessStatus /></section>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useMonitorStore } from './stores/monitor'
import SystemInfo from './components/SystemInfo.vue'
import HardwareStatus from './components/HardwareStatus.vue'
import NetworkStatus from './components/NetworkStatus.vue'
import ProcessStatus from './components/ProcessStatus.vue'
import StorageStatus from './components/StorageStatus.vue'

const store = useMonitorStore()
const refreshInterval = ref(5)
let intervalId: number | null = null

const navItems = [
  { id: 'system', label: '系统', icon: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/></svg>' },
  { id: 'hardware', label: '硬件', icon: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 1v3M15 1v3M9 20v3M15 20v3M20 9h3M20 14h3M1 9h3M1 14h3"/></svg>' },
  { id: 'network', label: '网络', icon: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><circle cx="12" cy="20" r="1"/></svg>' },
  { id: 'storage', label: '存储', icon: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>' },
  { id: 'process', label: '进程', icon: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>' }
]

const activeNav = ref('system')
let scrollLock = false

const scrollTo = (id: string) => {
  activeNav.value = id
  scrollLock = true
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
  setTimeout(() => { scrollLock = false }, 800)
}

const onScroll = () => {
  if (scrollLock) return
  const sections = navItems.map(item => ({
    id: item.id,
    el: document.getElementById(item.id)
  })).filter(s => s.el)

  const offset = 120
  for (let i = sections.length - 1; i >= 0; i--) {
    const rect = sections[i].el!.getBoundingClientRect()
    if (rect.top <= offset) {
      activeNav.value = sections[i].id
      return
    }
  }
  activeNav.value = sections[0]?.id || 'system'
}

const refreshNow = () => {
  store.fetchAllData()
}

onMounted(() => {
  store.fetchAllData()
  intervalId = window.setInterval(() => {
    store.fetchAllData()
  }, refreshInterval.value * 1000)
  window.addEventListener('scroll', onScroll, { passive: true })
  nextTick(onScroll)
})

onUnmounted(() => {
  if (intervalId) clearInterval(intervalId)
  window.removeEventListener('scroll', onScroll)
})
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; scroll-padding-top: 115px; }

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-light); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

:root {
  --bg-primary: #0f1117;
  --bg-secondary: #161b22;
  --bg-card: #1c2333;
  --bg-card-hover: #222d3f;
  --bg-input: #0d1117;
  --border: #30363d;
  --border-light: #3d444d;
  --text-primary: #e6edf3;
  --text-secondary: #8b949e;
  --text-muted: #656d76;
  --accent-blue: #58a6ff;
  --accent-green: #3fb950;
  --accent-yellow: #d29922;
  --accent-red: #f85149;
  --accent-purple: #bc8cff;
  --accent-cyan: #39d2c0;
  --glow-blue: rgba(88, 166, 255, 0.15);
  --glow-green: rgba(63, 185, 80, 0.15);
  --glow-red: rgba(248, 81, 73, 0.15);
  --radius: 12px;
  --radius-sm: 8px;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

.app { min-height: 100vh; }

.header {
  position: sticky;
  top: 0;
  z-index: 100;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  padding: 12px 24px;
  background: rgba(15, 17, 23, 0.92);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--border);
}

.nav-bar {
  position: sticky;
  top: 64px;
  z-index: 99;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2px;
  padding: 6px 24px;
  background: rgba(22, 27, 34, 0.88);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 500;
  color: var(--text-muted);
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
  border: 1px solid transparent;
}

.nav-item:hover {
  color: var(--text-secondary);
  background: rgba(88, 166, 255, 0.06);
}

.nav-item.active {
  color: var(--accent-blue);
  background: var(--glow-blue);
  border-color: rgba(88, 166, 255, 0.2);
}

.nav-icon {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
  border-radius: 10px;
  color: white;
  flex-shrink: 0;
}

.title-group h1 {
  font-size: 18px;
  font-weight: 600;
  letter-spacing: -0.3px;
}

.subtitle {
  font-size: 12px;
  color: var(--text-muted);
  font-family: 'JetBrains Mono', monospace;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--accent-green);
  box-shadow: 0 0 8px var(--accent-green);
}

.status-dot.fetching {
  background: var(--accent-yellow);
  box-shadow: 0 0 8px var(--accent-yellow);
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.refresh-text {
  font-size: 12px;
  color: var(--text-muted);
  font-family: 'JetBrains Mono', monospace;
}

.btn-refresh {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
}

.btn-refresh:hover {
  background: var(--bg-card-hover);
  color: var(--text-primary);
  border-color: var(--border-light);
}

.btn-refresh:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.main {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  align-items: start;
}

@media (max-width: 768px) {
  .header {
    padding: 10px 14px;
  }
  .nav-bar {
    top: 52px;
    padding: 6px 12px;
    gap: 1px;
  }
  .nav-item {
    padding: 6px 10px;
    font-size: 12px;
  }
  .title-group h1 {
    font-size: 15px;
  }
  .subtitle {
    display: none;
  }
  .refresh-text {
    display: none;
  }
  .main {
    padding: 12px;
    gap: 12px;
    min-width: 0;
    overflow-x: hidden;
  }
  .row {
    grid-template-columns: 1fr;
    gap: 12px;
    min-width: 0;
  }
  .row section {
    min-width: 0;
  }
}
</style>
