<template>
  <div class="card">
    <div class="card-header">
      <div class="card-icon purple">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <ellipse cx="12" cy="5" rx="9" ry="3"/>
          <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
          <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
        </svg>
      </div>
      <h2>存储状态</h2>
    </div>

    <div v-if="store.partitions.length" class="disk-list">
      <div v-for="part in store.partitions" :key="part.mountpoint" class="disk-card">
        <div class="disk-header">
          <div class="disk-info">
            <span class="disk-device">{{ part.device }}</span>
            <span class="disk-mount">{{ part.mountpoint }}</span>
          </div>
          <div class="disk-meta">
            <span class="disk-type">{{ part.fstype }}</span>
            <span class="disk-pct" :style="{ color: gaugeColor(part.percent) }">{{ part.percent }}%</span>
          </div>
        </div>
        <div class="disk-bar-wrap">
          <div class="disk-bar">
            <div class="disk-fill" :style="{ width: part.percent + '%', background: barGradient(part.percent) }"></div>
          </div>
        </div>
        <div class="disk-footer">
          <span class="disk-used">已用 {{ formatBytes(part.used) }} / {{ formatBytes(part.total) }}</span>
          <span class="disk-free">剩余 {{ formatBytes(part.free) }}</span>
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
import { useMonitorStore } from '../stores/monitor'
const store = useMonitorStore()

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

const barGradient = (pct: number) => {
  if (pct >= 90) return 'linear-gradient(90deg, #f85149, #da3633)'
  if (pct >= 70) return 'linear-gradient(90deg, #d29922, #e3b341)'
  return 'linear-gradient(90deg, #238636, #3fb950)'
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
  display: flex;
  flex-direction: column;
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
.card-icon.purple { background: linear-gradient(135deg, #6c3483, #9b59b6); }
.card-header h2 { font-size: 15px; font-weight: 600; }
.disk-list { display: flex; flex-direction: column; gap: 10px; flex: 1; min-height: 0; overflow-y: auto; }
.disk-card {
  padding: 14px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  transition: all 0.2s;
}
.disk-card:hover { border-color: var(--border-light); }
.disk-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}
.disk-info {
  display: flex; flex-direction: column; gap: 2px;
  min-width: 0; flex: 1;
}
.disk-device {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px; font-weight: 600; color: var(--text-primary);
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: block;
}
.disk-mount {
  font-size: 12px; color: var(--text-muted);
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: block;
}
.disk-meta { display: flex; align-items: center; gap: 10px; }
.disk-type {
  font-size: 11px; padding: 2px 8px;
  background: var(--bg-input);
  border: 1px solid var(--border);
  border-radius: 4px;
  color: var(--text-muted);
  font-family: 'JetBrains Mono', monospace;
}
.disk-pct { font-size: 18px; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
.disk-bar-wrap { margin-bottom: 8px; }
.disk-bar {
  height: 8px; background: var(--border);
  border-radius: 4px; overflow: hidden;
}
.disk-fill { height: 100%; border-radius: 4px; transition: width 0.6s ease; }
.disk-footer {
  display: flex; justify-content: space-between;
  font-size: 12px; color: var(--text-muted);
  font-family: 'JetBrains Mono', monospace;
}
.disk-free { color: var(--text-secondary); }
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
  .card { padding: 14px; min-width: 0; overflow: hidden; }
  .disk-card { padding: 12px; }
  .disk-header { flex-direction: column; gap: 8px; }
  .disk-info { width: 100%; }
  .disk-meta { width: 100%; justify-content: space-between; }
  .disk-pct { font-size: 16px; }
  .disk-footer { flex-direction: column; gap: 4px; }
}
</style>
