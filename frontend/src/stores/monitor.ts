import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fetchSystemInfo, fetchCpuInfo, fetchMemoryInfo, fetchInterfaces, fetchProcesses, fetchPartitions, fetchNetworkIO } from '../utils/api'

export const useMonitorStore = defineStore('monitor', () => {
  const systemInfo = ref<any>(null)
  const cpuInfo = ref<any>(null)
  const memoryInfo = ref<any>(null)
  const networkInterfaces = ref<any[]>([])
  const processes = ref<any[]>([])
  const partitions = ref<any[]>([])
  const networkSpeed = ref({ upload: 0, download: 0 })
  const loading = ref(false)
  const error = ref<string | null>(null)

  let prevIo: { bytes_sent: number; bytes_recv: number; ts: number } | null = null

  const fetchAllData = async () => {
    loading.value = true
    error.value = null
    try {
      const [sys, cpu, mem, net, proc, stor, io] = await Promise.all([
        fetchSystemInfo(),
        fetchCpuInfo(),
        fetchMemoryInfo(),
        fetchInterfaces(),
        fetchProcesses(),
        fetchPartitions(),
        fetchNetworkIO()
      ])
      systemInfo.value = sys
      cpuInfo.value = cpu
      memoryInfo.value = mem
      networkInterfaces.value = net
      processes.value = proc
      partitions.value = stor

      const now = Date.now()
      if (prevIo && io.bytes_sent !== undefined) {
        const elapsed = (now - prevIo.ts) / 1000
        if (elapsed > 0) {
          networkSpeed.value = {
            upload: Math.max(0, (io.bytes_sent - prevIo.bytes_sent) / elapsed),
            download: Math.max(0, (io.bytes_recv - prevIo.bytes_recv) / elapsed)
          }
        }
      }
      prevIo = { bytes_sent: io.bytes_sent || 0, bytes_recv: io.bytes_recv || 0, ts: now }
    } catch (e: any) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  return {
    systemInfo, cpuInfo, memoryInfo, networkInterfaces, processes, partitions, networkSpeed,
    loading, error, fetchAllData
  }
})
