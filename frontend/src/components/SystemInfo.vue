<template>
  <div class="card">
    <div class="card-header">
      <div class="card-icon blue">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="2" y="2" width="20" height="8" rx="2"/>
          <rect x="2" y="14" width="20" height="8" rx="2"/>
          <circle cx="6" cy="6" r="1"/>
          <circle cx="6" cy="18" r="1"/>
        </svg>
      </div>
      <h2>系统信息</h2>
    </div>
    <div v-if="store.systemInfo" class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="2" y="3" width="20" height="14" rx="2"/>
            <path d="M8 21h8"/><path d="M12 17v4"/>
          </svg>
        </div>
        <div class="stat-info">
          <span class="stat-label">主机名</span>
          <span class="stat-value mono">{{ store.systemInfo.hostname }}</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2L2 7l10 5 10-5-10-5z"/>
            <path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/>
          </svg>
        </div>
        <div class="stat-info">
          <span class="stat-label">操作系统</span>
          <span class="stat-value">{{ store.systemInfo.os }} {{ store.systemInfo.os_release }}</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>
          </svg>
        </div>
        <div class="stat-info">
          <span class="stat-label">内核版本</span>
          <span class="stat-value mono">{{ store.systemInfo.kernel }}</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/>
            <line x1="4" y1="22" x2="4" y2="15"/>
          </svg>
        </div>
        <div class="stat-info">
          <span class="stat-label">系统架构</span>
          <span class="stat-value mono">{{ store.systemInfo.architecture }}</span>
        </div>
      </div>
      <div class="stat-card highlight">
        <div class="stat-icon green">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
          </svg>
        </div>
        <div class="stat-info">
          <span class="stat-label">运行时间</span>
          <span class="stat-value uptime">{{ formatUptime(store.systemInfo.uptime) }}</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon purple">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
            <line x1="16" y1="2" x2="16" y2="6"/>
            <line x1="8" y1="2" x2="8" y2="6"/>
            <line x1="3" y1="10" x2="21" y2="10"/>
          </svg>
        </div>
        <div class="stat-info">
          <span class="stat-label">启动时间</span>
          <span class="stat-value">{{ formatTime(store.systemInfo.boot_time) }}</span>
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

const formatUptime = (seconds: number) => {
  const d = Math.floor(seconds / 86400)
  const h = Math.floor((seconds % 86400) / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const parts = []
  if (d > 0) parts.push(`${d}天`)
  if (h > 0) parts.push(`${h}时`)
  parts.push(`${m}分`)
  return parts.join(' ')
}

const formatTime = (iso: string) => {
  return new Date(iso).toLocaleString('zh-CN', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
}
.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
}
.card-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  color: white;
  flex-shrink: 0;
}
.card-icon.blue { background: linear-gradient(135deg, #1a5276, #2e86c1); }
.card-header h2 { font-size: 15px; font-weight: 600; }
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}
.stat-card {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 14px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  transition: all 0.2s;
}
.stat-card:hover {
  border-color: var(--border-light);
  background: var(--bg-card-hover);
}
.stat-card.highlight {
  border-color: rgba(63, 185, 80, 0.3);
  background: rgba(63, 185, 80, 0.05);
}
.stat-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: var(--bg-input);
  color: var(--text-secondary);
  flex-shrink: 0;
}
.stat-icon.green { color: var(--accent-green); background: var(--glow-green); }
.stat-icon.purple { color: var(--accent-purple); background: rgba(188, 140, 255, 0.15); }
.stat-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}
.stat-label {
  font-size: 11px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 500;
}
.stat-value {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.stat-value.mono {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
}
.stat-value.uptime {
  color: var(--accent-green);
  font-family: 'JetBrains Mono', monospace;
}
.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 40px;
  color: var(--text-muted);
  font-size: 14px;
}
.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid var(--border);
  border-top-color: var(--accent-blue);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
@media (max-width: 768px) {
  .card { padding: 14px; }
  .stats-grid {
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }
  .stat-card { padding: 10px; gap: 8px; }
  .stat-icon { width: 28px; height: 28px; }
  .stat-label { font-size: 10px; }
  .stat-value { font-size: 12px; }
  .stat-value.mono { font-size: 11px; }
}
@media (max-width: 420px) {
  .stats-grid { grid-template-columns: 1fr; }
}
</style>
