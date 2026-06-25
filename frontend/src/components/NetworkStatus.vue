<template>
  <div class="card">
    <div class="card-header">
      <div class="card-icon cyan">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M5 12.55a11 11 0 0 1 14.08 0"/>
          <path d="M1.42 9a16 16 0 0 1 21.16 0"/>
          <path d="M8.53 16.11a6 6 0 0 1 6.95 0"/>
          <circle cx="12" cy="20" r="1"/>
        </svg>
      </div>
      <h2>网络状态</h2>
    </div>

    <div class="chart-section">
      <div class="chart-legend">
        <span class="legend-item"><span class="legend-dot up"></span>发送</span>
        <span class="legend-item"><span class="legend-dot down"></span>接收</span>
        <span class="legend-max">峰值 {{ formatSpeed(maxSpeed) }}</span>
      </div>
      <canvas ref="canvasRef" class="speed-chart"></canvas>
    </div>

    <div class="speed-bar" v-if="store.networkSpeed.upload > 0 || store.networkSpeed.download > 0">
      <span class="speed-item">
        <span class="speed-label up">↑ 发送</span>
        <span class="speed-val">{{ formatSpeed(store.networkSpeed.upload) }}</span>
      </span>
      <span class="speed-item">
        <span class="speed-label down">↓ 接收</span>
        <span class="speed-val">{{ formatSpeed(store.networkSpeed.download) }}</span>
      </span>
    </div>

    <div v-if="store.networkInterfaces.length" class="iface-list">
      <div v-for="iface in store.networkInterfaces" :key="iface.name" class="iface-card"
           :class="{ 'is-up': iface.is_up?.isup, 'is-down': !iface.is_up?.isup }">
        <div class="iface-top">
          <div class="iface-name-row">
            <span class="iface-status-dot" :class="iface.is_up?.isup ? 'up' : 'down'"></span>
            <span class="iface-name">{{ iface.name }}</span>
          </div>
          <span class="iface-badge" :class="iface.is_up?.isup ? 'up' : 'down'">
            {{ iface.is_up?.isup ? '在线' : '离线' }}
          </span>
        </div>
        <div class="iface-addrs">
          <span v-for="(addr, i) in getIPv4(iface.addresses)" :key="i" class="addr-tag">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
            </svg>
            {{ addr }}
          </span>
        </div>
        <div v-if="iface.bytes_sent" class="iface-traffic">
          <div class="traffic-item">
            <span class="traffic-arrow up">发送</span>
            <span class="traffic-value">{{ formatBytes(iface.bytes_sent.bytes_sent) }}</span>
          </div>
          <div class="traffic-item">
            <span class="traffic-arrow down">接收</span>
            <span class="traffic-value">{{ formatBytes(iface.bytes_sent.bytes_recv) }}</span>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="loading-state">
      <div class="spinner"></div>
      <span>加载中...</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { useMonitorStore } from '../stores/monitor'
const store = useMonitorStore()

const MAX_POINTS = 60
const history = ref<{ up: number; down: number }[]>([])
const canvasRef = ref<HTMLCanvasElement | null>(null)
let observer: ResizeObserver | null = null

const maxSpeed = ref(0)

const getIPv4 = (addrs: any[]) => {
  if (!addrs) return []
  return addrs
    .filter(a => a.address && !a.address.includes(':') && a.address !== '127.0.0.1')
    .map(a => a.address)
}

const formatBytes = (bytes: number) => {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

const formatSpeed = (bytesPerSec: number) => {
  if (!bytesPerSec || bytesPerSec < 0) return '0 B/s'
  const k = 1024
  const sizes = ['B/s', 'KB/s', 'MB/s', 'GB/s']
  const i = Math.floor(Math.log(bytesPerSec) / Math.log(k))
  return parseFloat((bytesPerSec / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

const drawChart = () => {
  const canvas = canvasRef.value
  if (!canvas) return

  const dpr = window.devicePixelRatio || 1
  const rect = canvas.getBoundingClientRect()
  canvas.width = rect.width * dpr
  canvas.height = rect.height * dpr
  const ctx = canvas.getContext('2d')
  if (!ctx) return
  ctx.scale(dpr, dpr)

  const W = rect.width
  const H = rect.height
  const pad = { top: 8, right: 4, bottom: 4, left: 0 }
  const cW = W - pad.left - pad.right
  const cH = H - pad.top - pad.bottom

  ctx.clearRect(0, 0, W, H)

  const data = history.value
  const peak = data.length > 0 ? Math.max(...data.map(d => Math.max(d.up, d.down)), 1) : 1
  maxSpeed.value = peak

  const toY = (v: number) => pad.top + cH * (1 - v / peak)

  ctx.strokeStyle = 'rgba(48,54,61,0.5)'
  ctx.lineWidth = 1
  const gridLines = 4
  for (let i = 0; i <= gridLines; i++) {
    const y = pad.top + (cH / gridLines) * i
    ctx.beginPath()
    ctx.moveTo(pad.left, y)
    ctx.lineTo(W - pad.right, y)
    ctx.stroke()
  }

  if (data.length === 0) return

  const drawLine = (color: string, getter: (d: { up: number; down: number }) => number) => {
    if (data.length < 1) return
    const gap = cW / (MAX_POINTS - 1)

    if (data.length === 1) {
      const x = pad.left + (MAX_POINTS - 1) * gap
      const y = toY(getter(data[0]))
      ctx.beginPath()
      ctx.arc(x, y, 3, 0, Math.PI * 2)
      ctx.fillStyle = color
      ctx.fill()
      return
    }

    ctx.beginPath()
    ctx.strokeStyle = color
    ctx.lineWidth = 1.5
    ctx.lineJoin = 'round'
    for (let i = 0; i < data.length; i++) {
      const x = pad.left + (MAX_POINTS - data.length + i) * gap
      const y = toY(getter(data[i]))
      if (i === 0) ctx.moveTo(x, y)
      else ctx.lineTo(x, y)
    }
    ctx.stroke()

    const grad = ctx.createLinearGradient(0, pad.top, 0, pad.top + cH)
    grad.addColorStop(0, color.replace(')', ',0.25)').replace('rgb', 'rgba'))
    grad.addColorStop(1, color.replace(')', ',0.02)').replace('rgb', 'rgba'))
    ctx.lineTo(pad.left + (MAX_POINTS - 1) * gap, pad.top + cH)
    ctx.lineTo(pad.left + (MAX_POINTS - data.length) * gap, pad.top + cH)
    ctx.closePath()
    ctx.fillStyle = grad
    ctx.fill()
  }

  drawLine('rgb(63,185,80)', d => d.up)
  drawLine('rgb(88,166,255)', d => d.down)
}

watch(() => store.networkSpeed, (speed) => {
  history.value.push({ up: speed.upload, down: speed.download })
  if (history.value.length > MAX_POINTS) history.value.shift()
  nextTick(drawChart)
}, { deep: true })

onMounted(() => {
  nextTick(drawChart)
  observer = new ResizeObserver(() => drawChart())
  if (canvasRef.value) observer.observe(canvasRef.value)
})

onUnmounted(() => {
  observer?.disconnect()
})
</script>

<style scoped>
.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  min-width: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  max-height: 596px;
}
.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
}
.card-icon {
  width: 32px; height: 32px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 8px; color: white;
  flex-shrink: 0;
}
.card-icon.cyan { background: linear-gradient(135deg, #0e6e5e, #1abc9c); }
.card-header h2 { font-size: 15px; font-weight: 600; }
.chart-section {
  margin-bottom: 12px;
  padding: 10px 14px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  flex-shrink: 0;
}
.chart-legend {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
  font-size: 11px;
  color: var(--text-muted);
}
.legend-item {
  display: flex;
  align-items: center;
  gap: 4px;
}
.legend-dot {
  width: 8px; height: 3px;
  border-radius: 2px;
}
.legend-dot.up { background: var(--accent-green); }
.legend-dot.down { background: var(--accent-blue); }
.legend-max {
  margin-left: auto;
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
}
.speed-chart {
  width: 100%;
  height: 120px;
  display: block;
}
.iface-list { display: flex; flex-direction: column; gap: 10px; flex: 1; min-height: 0; overflow-y: auto; }
.speed-bar {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-bottom: 12px;
  padding: 10px 14px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  flex-shrink: 0;
}
.speed-item {
  display: flex;
  align-items: center;
  gap: 6px;
}
.speed-label {
  font-size: 12px;
  color: var(--text-muted);
  font-weight: 500;
}
.speed-label.up { color: var(--accent-green); }
.speed-label.down { color: var(--accent-blue); }
.speed-val {
  font-size: 14px;
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
  color: var(--text-primary);
}
.iface-card {
  padding: 14px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  transition: all 0.2s;
}
.iface-card.is-up { border-left: 3px solid var(--accent-green); }
.iface-card.is-down { border-left: 3px solid var(--accent-red); opacity: 0.7; }
.iface-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.iface-name-row { display: flex; align-items: center; gap: 8px; }
.iface-status-dot { width: 8px; height: 8px; border-radius: 50%; }
.iface-status-dot.up { background: var(--accent-green); box-shadow: 0 0 6px var(--accent-green); }
.iface-status-dot.down { background: var(--accent-red); }
.iface-name { font-weight: 600; font-size: 14px; color: var(--text-primary); }
.iface-badge {
  font-size: 10px; font-weight: 700;
  padding: 2px 8px; border-radius: 4px;
  letter-spacing: 0.5px;
}
.iface-badge.up { background: var(--glow-green); color: var(--accent-green); }
.iface-badge.down { background: var(--glow-red); color: var(--accent-red); }
.iface-addrs { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 10px; }
.addr-tag {
  display: flex; align-items: center; gap: 4px;
  padding: 4px 10px;
  background: var(--bg-input);
  border: 1px solid var(--border);
  border-radius: 6px;
  font-size: 12px;
  font-family: 'JetBrains Mono', monospace;
  color: var(--text-secondary);
}
.iface-traffic { display: flex; gap: 20px; }
.traffic-item { display: flex; align-items: center; gap: 6px; }
.traffic-arrow {
  font-size: 10px; font-weight: 700;
  padding: 2px 6px; border-radius: 3px;
}
.traffic-arrow.up { background: rgba(63, 185, 80, 0.15); color: var(--accent-green); }
.traffic-arrow.down { background: rgba(88, 166, 255, 0.15); color: var(--accent-blue); }
.traffic-value {
  font-size: 12px; color: var(--text-muted);
  font-family: 'JetBrains Mono', monospace;
}
.loading-state {
  display: flex; align-items: center; justify-content: center;
  gap: 10px; padding: 40px; color: var(--text-muted);
}
.spinner {
  width: 20px; height: 20px;
  border: 2px solid var(--border);
  border-top-color: var(--accent-blue);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
@media (max-width: 768px) {
  .card { padding: 14px; overflow: hidden; }
  .chart-section { padding: 8px 10px; }
  .speed-chart { height: 80px; }
  .speed-bar { padding: 8px 10px; gap: 12px; }
  .speed-val { font-size: 12px; }
  .iface-list { max-height: 220px; gap: 8px; }
  .iface-card { padding: 10px; }
  .iface-top { margin-bottom: 6px; }
  .iface-name { font-size: 13px; }
  .iface-addrs { margin-bottom: 6px; }
  .addr-tag { padding: 3px 8px; font-size: 11px; }
  .iface-traffic { gap: 10px; }
}
</style>
