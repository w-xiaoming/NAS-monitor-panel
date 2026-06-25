<template>
  <div class="card">
    <div class="card-header">
      <div class="card-icon orange">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="4" y="4" width="16" height="16" rx="2"/>
          <rect x="9" y="9" width="6" height="6"/>
          <path d="M15 2v2M9 2v2M15 20v2M9 20v2M2 15h2M2 9h2M20 15h2M20 9h2"/>
        </svg>
      </div>
      <h2>硬件状态</h2>
    </div>

    <div v-if="store.cpuInfo" class="hardware-section">
      <div class="section-title">
        <span class="dot cpu"></span>CPU
      </div>
      <div class="cpu-grid">
        <div class="gauge-card main-gauge">
          <div class="gauge-ring">
            <svg viewBox="0 0 120 120">
              <circle cx="60" cy="60" r="52" fill="none" stroke="var(--border)" stroke-width="8"/>
              <circle cx="60" cy="60" r="52" fill="none"
                :stroke="gaugeColor(store.cpuInfo.percent_overall)"
                stroke-width="8"
                stroke-linecap="round"
                :stroke-dasharray="circumference"
                :stroke-dashoffset="circumference - (circumference * store.cpuInfo.percent_overall / 100)"
                transform="rotate(-90 60 60)"
                class="gauge-progress"/>
            </svg>
            <div class="gauge-center">
              <span class="gauge-value">{{ store.cpuInfo.percent_overall }}</span>
              <span class="gauge-unit">%</span>
            </div>
          </div>
          <span class="gauge-label">总使用率</span>
        </div>
        <div class="cpu-details">
          <div class="detail-row">
            <span class="detail-label">物理核心</span>
            <span class="detail-value">{{ store.cpuInfo.core_count }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">逻辑核心</span>
            <span class="detail-value">{{ store.cpuInfo.logical_count }}</span>
          </div>
          <div class="detail-row" v-if="store.cpuInfo.frequency">
            <span class="detail-label">运行频率</span>
            <span class="detail-value mono">{{ (store.cpuInfo.frequency.current / 1000).toFixed(1) }} GHz</span>
          </div>
          <div class="detail-row" v-if="store.cpuInfo.load_average">
            <span class="detail-label">负载均衡</span>
            <span class="detail-value mono">{{ store.cpuInfo.load_average['1min'].toFixed(2) }} / {{ store.cpuInfo.load_average['5min'].toFixed(2) }} / {{ store.cpuInfo.load_average['15min'].toFixed(2) }}</span>
          </div>
        </div>
      </div>
      <div v-if="store.cpuInfo.percent_per_core" class="cores-grid">
        <div v-for="(pct, i) in store.cpuInfo.percent_per_core" :key="i" class="core-item">
          <div class="core-header">
            <span class="core-name">核心 {{ i }}</span>
            <span class="core-pct" :style="{ color: gaugeColor(pct) }">{{ pct }}%</span>
          </div>
          <div class="core-bar">
            <div class="core-fill" :style="{ width: pct + '%', background: gaugeColor(pct) }"></div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="store.memoryInfo" class="hardware-section">
      <div class="section-title">
        <span class="dot memory"></span>内存
      </div>
      <div class="mem-cards">
        <div class="mem-card">
          <div class="mem-header">
            <span class="mem-label">物理内存</span>
            <span class="mem-pct" :style="{ color: gaugeColor(store.memoryInfo.virtual.percent) }">
              {{ store.memoryInfo.virtual.percent }}%
            </span>
          </div>
          <div class="mem-bar">
            <div class="mem-fill" :style="{ width: store.memoryInfo.virtual.percent + '%', background: gaugeColor(store.memoryInfo.virtual.percent) }"></div>
          </div>
          <div class="mem-detail">
            <span>已用 {{ formatBytes(store.memoryInfo.virtual.used) }}</span>
            <span>共 {{ formatBytes(store.memoryInfo.virtual.total) }}</span>
          </div>
          <div v-if="store.memoryInfo.virtual.cached" class="mem-extra">
            缓存: {{ formatBytes(store.memoryInfo.virtual.cached) }}
          </div>
        </div>
        <div v-if="store.memoryInfo.swap.total > 0" class="mem-card">
          <div class="mem-header">
            <span class="mem-label">交换分区</span>
            <span class="mem-pct" :style="{ color: gaugeColor(store.memoryInfo.swap.percent) }">
              {{ store.memoryInfo.swap.percent }}%
            </span>
          </div>
          <div class="mem-bar">
            <div class="mem-fill" :style="{ width: store.memoryInfo.swap.percent + '%', background: gaugeColor(store.memoryInfo.swap.percent) }"></div>
          </div>
          <div class="mem-detail">
            <span>已用 {{ formatBytes(store.memoryInfo.swap.used) }}</span>
            <span>共 {{ formatBytes(store.memoryInfo.swap.total) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useMonitorStore } from '../stores/monitor'
const store = useMonitorStore()
const circumference = 2 * Math.PI * 52

const formatBytes = (bytes: number) => {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

const gaugeColor = (pct: number) => {
  if (pct >= 90) return 'var(--accent-red)'
  if (pct >= 70) return 'var(--accent-yellow)'
  return 'var(--accent-green)'
}
</script>

<style scoped>
.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  min-width: 0;
  overflow: hidden;
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
.card-icon.orange { background: linear-gradient(135deg, #b7580e, #e67e22); }
.card-header h2 { font-size: 15px; font-weight: 600; }
.hardware-section { margin-bottom: 20px; }
.hardware-section:last-child { margin-bottom: 0; }
.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.8px;
  margin-bottom: 12px;
}
.dot { width: 6px; height: 6px; border-radius: 50%; }
.dot.cpu { background: #e67e22; }
.dot.memory { background: var(--accent-blue); }
.cpu-grid {
  display: flex;
  gap: 20px;
  align-items: center;
}
.gauge-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}
.gauge-ring {
  position: relative;
  width: 100px; height: 100px;
}
.gauge-ring svg { width: 100%; height: 100%; }
.gauge-progress { transition: stroke-dashoffset 0.6s ease; }
.gauge-center {
  position: absolute; inset: 0;
  display: flex; align-items: center; justify-content: center;
}
.gauge-value {
  font-size: 22px; font-weight: 700; color: var(--text-primary);
  font-family: 'JetBrains Mono', monospace;
}
.gauge-unit { font-size: 11px; color: var(--text-muted); margin-left: 1px; }
.gauge-label { font-size: 11px; color: var(--text-muted); }
.cpu-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 10px;
  background: var(--bg-secondary);
  border-radius: 6px;
}
.detail-label { font-size: 12px; color: var(--text-muted); }
.detail-value { font-size: 13px; font-weight: 500; color: var(--text-primary); }
.detail-value.mono { font-family: 'JetBrains Mono', monospace; font-size: 12px; }
.cores-grid {
  margin-top: 12px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 8px;
}
.core-item {
  padding: 8px 10px;
  background: var(--bg-secondary);
  border-radius: 6px;
}
.core-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
}
.core-name { font-size: 11px; color: var(--text-muted); }
.core-pct { font-size: 12px; font-weight: 600; font-family: 'JetBrains Mono', monospace; }
.core-bar {
  height: 4px;
  background: var(--border);
  border-radius: 2px;
  overflow: hidden;
}
.core-fill { height: 100%; border-radius: 2px; transition: width 0.5s ease; }
.mem-cards { display: flex; flex-direction: column; gap: 12px; }
.mem-card {
  padding: 14px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
}
.mem-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.mem-label { font-size: 13px; font-weight: 600; color: var(--text-primary); }
.mem-pct {
  font-size: 16px; font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
}
.mem-bar {
  height: 6px;
  background: var(--border);
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 8px;
}
.mem-fill { height: 100%; border-radius: 3px; transition: width 0.5s ease; }
.mem-detail {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: var(--text-muted);
  font-family: 'JetBrains Mono', monospace;
}
.mem-extra { margin-top: 6px; font-size: 11px; color: var(--text-muted); }
@media (max-width: 768px) {
  .card { padding: 14px; }
  .cpu-grid { flex-direction: column; align-items: stretch; }
  .gauge-card { flex-direction: row; gap: 16px; }
  .gauge-ring { width: 80px; height: 80px; }
  .gauge-value { font-size: 18px; }
  .cores-grid { grid-template-columns: 1fr 1fr; }
  .mem-card { padding: 12px; }
}
</style>
