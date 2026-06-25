<template>
  <div class="card">
    <div class="card-header">
      <div class="card-icon green">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
        </svg>
      </div>
      <h2>进程列表</h2>
      <span class="count-badge">{{ store.processes.length }} 个</span>
    </div>

    <div class="summary-bar" v-if="store.processes.length">
      <span class="summary-item">
        <span class="summary-label">总 CPU</span>
        <span class="summary-val mono" :style="{ color: pctColor(totalCpu) }">{{ totalCpu.toFixed(1) }}%</span>
      </span>
      <span class="summary-item">
        <span class="summary-label">总内存</span>
        <span class="summary-val mono" :style="{ color: pctColor(totalMem) }">{{ totalMem.toFixed(1) }}%</span>
      </span>
    </div>

    <div v-if="store.processes.length" class="table-wrap">
      <div class="table-body">
        <table>
          <thead>
            <tr>
              <th :class="{ sorted: sortKey === 'pid' }" @click="toggleSort('pid')">PID {{ sortIcon('pid') }}</th>
              <th :class="{ sorted: sortKey === 'name' }" @click="toggleSort('name')">名称 {{ sortIcon('name') }}</th>
              <th class="num" :class="{ sorted: sortKey === 'cpu_percent' }" @click="toggleSort('cpu_percent')">CPU {{ sortIcon('cpu_percent') }}</th>
              <th class="num" :class="{ sorted: sortKey === 'memory_percent' }" @click="toggleSort('memory_percent')">内存 {{ sortIcon('memory_percent') }}</th>
              <th class="status-col" :class="{ sorted: sortKey === 'status' }" @click="toggleSort('status')">状态 {{ sortIcon('status') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="proc in sortedProcesses" :key="proc.pid">
              <td class="mono pid">{{ proc.pid }}</td>
              <td class="proc-name">{{ proc.name }}</td>
              <td class="num">
                <span class="pct-bar-wrap">
                  <span class="pct-bar"><span class="pct-fill" :style="{ width: Math.min(proc.cpu_percent || 0, 100) + '%', background: pctColor(proc.cpu_percent) }"></span></span>
                  <span class="pct-val" :style="{ color: pctColor(proc.cpu_percent) }">{{ (proc.cpu_percent || 0).toFixed(1) }}%</span>
                </span>
              </td>
              <td class="num">
                <span class="pct-bar-wrap">
                  <span class="pct-bar"><span class="pct-fill" :style="{ width: Math.min(proc.memory_percent || 0, 100) + '%', background: pctColor(proc.memory_percent) }"></span></span>
                  <span class="pct-val" :style="{ color: pctColor(proc.memory_percent) }">{{ (proc.memory_percent || 0).toFixed(1) }}%</span>
                </span>
              </td>
              <td class="status-col">
                <span class="status-chip" :class="proc.status">{{ statusLabel(proc.status) }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-else class="loading-state">
      <div class="spinner"></div>
      <span>加载中...</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useMonitorStore } from '../stores/monitor'
const store = useMonitorStore()

const sortKey = ref<string>('cpu_percent')
const sortOrder = ref<'asc' | 'desc'>('desc')

const totalCpu = computed(() => store.processes.reduce((sum: number, p: any) => sum + (p.cpu_percent || 0), 0))
const totalMem = computed(() => store.processes.reduce((sum: number, p: any) => sum + (p.memory_percent || 0), 0))

const sortedProcesses = computed(() => {
  const list = [...store.processes]
  const key = sortKey.value
  const dir = sortOrder.value === 'asc' ? 1 : -1

  return list.sort((a: any, b: any) => {
    const aVal = a[key] ?? 0
    const bVal = b[key] ?? 0
    if (typeof aVal === 'string') return aVal.localeCompare(bVal) * dir
    return (aVal - bVal) * dir
  })
})

const toggleSort = (key: string) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortOrder.value = 'desc'
  }
}

const sortIcon = (key: string) => {
  if (sortKey.value !== key) return ''
  return sortOrder.value === 'asc' ? '↑' : '↓'
}

const pctColor = (val: number) => {
  if (val >= 50) return 'var(--accent-red)'
  if (val >= 20) return 'var(--accent-yellow)'
  return 'var(--accent-green)'
}

const statusLabel = (status: string) => {
  const map: Record<string, string> = {
    running: '运行中',
    sleeping: '休眠',
    zombie: '僵尸',
    stopped: '已停止',
    disk_sleep: '磁盘休眠',
    idle: '空闲',
    '': '--'
  }
  return map[status] || status
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
  max-height: 698px;
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
.card-icon.green { background: linear-gradient(135deg, #1a7a3a, #27ae60); }
.card-header h2 { font-size: 15px; font-weight: 600; }
.count-badge {
  margin-left: auto;
  font-size: 11px; font-weight: 600;
  padding: 2px 8px;
  background: var(--bg-input);
  border: 1px solid var(--border);
  border-radius: 10px;
  color: var(--text-muted);
}
.table-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; }
thead tr { border-bottom: 1px solid var(--border); }
th {
  padding: 8px 10px;
  font-size: 11px; font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  text-align: left;
  white-space: nowrap;
  cursor: pointer;
  user-select: none;
  transition: color 0.2s;
}
th:hover { color: var(--text-secondary); }
th.sorted { color: var(--accent-blue); }
th.num { text-align: right; }
td {
  padding: 8px 10px;
  font-size: 13px;
  color: var(--text-secondary);
  border-bottom: 1px solid rgba(48, 54, 61, 0.5);
}
td.num { text-align: right; }
tr:hover td { background: rgba(88, 166, 255, 0.03); }
.mono { font-family: 'JetBrains Mono', monospace; }
.pid { color: var(--text-muted); font-size: 12px; }
.proc-name {
  color: var(--text-primary); font-weight: 500;
  max-width: 200px;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.pct-bar-wrap { display: inline-flex; align-items: center; gap: 8px; }
.pct-bar {
  display: inline-block; width: 50px; height: 4px;
  background: var(--border); border-radius: 2px;
  overflow: hidden; vertical-align: middle;
}
.pct-fill { display: block; height: 100%; border-radius: 2px; transition: width 0.3s ease; }
.pct-val {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px; font-weight: 500;
  min-width: 45px; text-align: right;
}
.status-chip {
  font-size: 10px; font-weight: 600;
  padding: 2px 8px; border-radius: 4px;
}
.status-chip.running, [class~="运行中"] { background: var(--glow-green); color: var(--accent-green); }
.status-chip.sleeping, [class~="休眠"] { background: rgba(139, 148, 158, 0.15); color: var(--text-muted); }
.status-chip.zombie, [class~="僵尸"] { background: var(--glow-red); color: var(--accent-red); }
.status-chip.stopped, [class~="已停止"] { background: rgba(210, 153, 34, 0.15); color: var(--accent-yellow); }
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
.table-body {
  overflow-y: auto;
}
.table-body thead th {
  position: sticky;
  top: 0;
  background: var(--bg-card);
  z-index: 1;
}
.summary-bar {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-bottom: 12px;
  padding: 10px 14px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
}
.summary-item {
  display: flex;
  align-items: center;
  gap: 6px;
}
.summary-label {
  font-size: 12px;
  color: var(--text-muted);
  font-weight: 500;
}
.summary-val {
  font-size: 14px;
  font-weight: 700;
}
@media (max-width: 768px) {
  .card { padding: 14px; min-width: 0; overflow: hidden; min-height: 0; }
.table-wrap { overflow-x: auto; flex: 1; min-height: 0; }
  table { min-width: 0; width: 100%; }
  th, td { padding: 6px 4px; font-size: 11px; }
  .pct-bar { width: 24px; }
  .pct-val { min-width: 30px; font-size: 10px; }
  .proc-name { max-width: 80px; }
  .table-body { max-height: 480px; }
  .table-body thead th { background: var(--bg-card); }
  th.status-col, td.status-col { display: none; }
  .summary-bar { padding: 8px 10px; gap: 12px; }
  .summary-val { font-size: 12px; }
}
</style>
