const API_BASE = '/monitor/api'

async function request(url: string) {
  const response = await fetch(`${API_BASE}${url}`)
  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`)
  }
  return response.json()
}

export const fetchSystemInfo = () => request('/system/info')
export const fetchCpuInfo = () => request('/hardware/cpu')
export const fetchMemoryInfo = () => request('/hardware/memory')
export const fetchTemperature = () => request('/hardware/temperature')
export const fetchInterfaces = () => request('/network/interfaces')
export const fetchNetworkIO = () => request('/network/io')
export const fetchProcesses = (limit = 50) => request(`/process/list?limit=${limit}`)
export const fetchConnections = () => request('/process/connections')
export const fetchPartitions = () => request('/storage/partitions')
export const fetchStorageIO = () => request('/storage/io')
