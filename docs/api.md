# API 文档

NAS Monitor Panel 提供 RESTful API 接口，用于获取系统监控数据。

## 基础信息

- **基础路径**: `/api`
- **协议**: HTTP/HTTPS
- **数据格式**: JSON
- **字符编码**: UTF-8

## 系统信息

### GET /api/system/info

获取系统基本信息。

**响应示例**:

```json
{
  "os": "Linux",
  "os_version": "#1 SMP Debian 5.10.0-23-cloud-amd64",
  "os_release": "5.10.0-23-cloud-amd64",
  "kernel": "5.10.0-23-cloud-amd64",
  "architecture": "x86_64",
  "hostname": "nas-server",
  "uptime": 123456.789,
  "boot_time": "2024-01-01T00:00:00"
}
```

**字段说明**:

| 字段 | 类型 | 描述 |
|------|------|------|
| os | string | 操作系统类型 |
| os_version | string | 操作系统版本 |
| os_release | string | 发行版信息 |
| kernel | string | 内核版本 |
| architecture | string | 系统架构 (x86_64, arm64 等) |
| hostname | string | 主机名 |
| uptime | number | 运行时间（秒） |
| boot_time | string | 启动时间 (ISO 8601) |

---

### GET /api/system/uptime

获取系统启动时间戳。

**响应示例**:

```json
{
  "uptime": 1704067200.0
}
```

**字段说明**:

| 字段 | 类型 | 描述 |
|------|------|------|
| uptime | number | 系统启动时间戳 (Unix timestamp) |

---

## 硬件监控

### GET /api/hardware/cpu

获取 CPU 使用信息。

**响应示例**:

```json
{
  "percent_overall": 45.2,
  "percent_per_core": [50.1, 40.3, 45.6, 44.8],
  "core_count": 4,
  "logical_count": 8,
  "frequency": {
    "current": 2400.0,
    "min": 800.0,
    "max": 3800.0
  },
  "times": {
    "user": 25.3,
    "system": 10.2,
    "idle": 64.5
  },
  "load_average": {
    "1min": 1.23,
    "5min": 1.45,
    "15min": 1.67
  }
}
```

**字段说明**:

| 字段 | 类型 | 描述 |
|------|------|------|
| percent_overall | number | 整体 CPU 使用率 (%) |
| percent_per_core | number[] | 每个核心的使用率 (%) |
| core_count | number | 物理核心数 |
| logical_count | number | 逻辑核心数（含超线程） |
| frequency | object | CPU 频率信息 (MHz) |
| times | object | CPU 时间分配 |
| load_average | object | 系统负载 (1/5/15 分钟) |

---

### GET /api/hardware/memory

获取内存使用信息。

**响应示例**:

```json
{
  "virtual": {
    "total": 8589934592,
    "available": 4294967296,
    "used": 4294967296,
    "free": 2147483648,
    "percent": 50.0,
    "cached": 1073741824,
    "buffers": 536870912
  },
  "swap": {
    "total": 2147483648,
    "used": 0,
    "free": 2147483648,
    "percent": 0.0
  }
}
```

**字段说明**:

| 字段 | 类型 | 描述 |
|------|------|------|
| virtual.total | number | 总物理内存 (bytes) |
| virtual.available | number | 可用内存 (bytes) |
| virtual.used | number | 已用内存 (bytes) |
| virtual.free | number | 空闲内存 (bytes) |
| virtual.percent | number | 内存使用率 (%) |
| virtual.cached | number | 缓存内存 (bytes) |
| virtual.buffers | number | 缓冲区内存 (bytes) |
| swap.total | number | 交换空间总量 (bytes) |
| swap.used | number | 交换空间已用 (bytes) |
| swap.free | number | 交换空间可用 (bytes) |
| swap.percent | number | 交换空间使用率 (%) |

---

### GET /api/hardware/temperature

获取温度传感器信息。

**响应示例**:

```json
{
  "coretemp": [
    {
      "label": "Core 0",
      "current": 45.0,
      "high": 100.0,
      "critical": 100.0
    },
    {
      "label": "Core 1",
      "current": 42.0,
      "high": 100.0,
      "critical": 100.0
    }
  ]
}
```

**或当温度传感器不可用时**:

```json
{
  "available": false
}
```

**字段说明**:

| 字段 | 类型 | 描述 |
|------|------|------|
| [sensor_name] | array | 传感器名称及其温度列表 |
| label | string | 传感器标签 |
| current | number | 当前温度 (°C) |
| high | number | 高温阈值 (°C) |
| critical | number | 临界温度 (°C) |

---

## 网络监控

### GET /api/network/interfaces

获取网络接口信息。

**响应示例**:

```json
[
  {
    "name": "eth0",
    "addresses": [
      {
        "family": "AF_INET",
        "address": "192.168.1.100",
        "netmask": "255.255.255.0",
        "broadcast": "192.168.1.255"
      },
      {
        "family": "AF_INET6",
        "address": "fe80::1234:5678:90ab:cdef",
        "netmask": null,
        "broadcast": null
      }
    ],
    "is_up": true,
    "bytes_sent": 1234567890
  }
]
```

**字段说明**:

| 字段 | 类型 | 描述 |
|------|------|------|
| name | string | 接口名称 |
| addresses | array | IP 地址列表 |
| is_up | boolean | 接口是否启用 |
| bytes_sent | number | 已发送字节数 |

---

### GET /api/network/io

获取网络 IO 统计。

**响应示例**:

```json
{
  "bytes_sent": 1234567890,
  "bytes_recv": 9876543210,
  "packets_sent": 1234567,
  "packets_recv": 9876543,
  "errin": 0,
  "errout": 0
}
```

**字段说明**:

| 字段 | 类型 | 描述 |
|------|------|------|
| bytes_sent | number | 已发送字节数 |
| bytes_recv | number | 已接收字节数 |
| packets_sent | number | 已发送数据包数 |
| packets_recv | number | 已接收数据包数 |
| errin | number | 入站错误数 |
| errout | number | 出站错误数 |

---

## 进程管理

### GET /api/process/list

获取进程列表。

**查询参数**:

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| limit | number | 50 | 返回进程数量上限 (最大 200) |

**请求示例**:

```
GET /api/process/list?limit=20
```

**响应示例**:

```json
[
  {
    "pid": 1234,
    "name": "python3",
    "cpu_percent": 5.2,
    "memory_percent": 2.3,
    "status": "running",
    "create_time": "2024-01-01T00:00:00"
  },
  {
    "pid": 5678,
    "name": "node",
    "cpu_percent": 3.1,
    "memory_percent": 1.8,
    "status": "running",
    "create_time": "2024-01-01T00:00:00"
  }
]
```

**字段说明**:

| 字段 | 类型 | 描述 |
|------|------|------|
| pid | number | 进程 ID |
| name | string | 进程名称 |
| cpu_percent | number | CPU 使用率 (%) |
| memory_percent | number | 内存使用率 (%) |
| status | string | 进程状态 (running, sleeping, stopped 等) |
| create_time | string | 创建时间 (ISO 8601) |

**注意**: 进程列表按 CPU 使用率降序排列。

---

### GET /api/process/connections

获取网络连接信息。

**响应示例**:

```json
[
  {
    "fd": 3,
    "family": "AF_INET",
    "type": "SOCK_STREAM",
    "laddr": {
      "ip": "0.0.0.0",
      "port": 8902
    },
    "raddr": {
      "ip": "192.168.1.100",
      "port": 54321
    },
    "status": "ESTABLISHED",
    "pid": 1234
  }
]
```

**字段说明**:

| 字段 | 类型 | 描述 |
|------|------|------|
| fd | number | 文件描述符 |
| family | string | 地址族 (AF_INET, AF_INET6) |
| type | string | 套接字类型 (SOCK_STREAM, SOCK_DGRAM) |
| laddr | object | 本地地址 |
| raddr | object | 远程地址 |
| status | string | 连接状态 |
| pid | number | 进程 ID |

---

## 存储监控

### GET /api/storage/partitions

获取磁盘分区信息。

**响应示例**:

```json
[
  {
    "device": "/dev/sda1",
    "mountpoint": "/",
    "fstype": "ext4",
    "opts": "rw,relatime",
    "total": 107374182400,
    "used": 53687091200,
    "free": 53687091200,
    "percent": 50.0
  },
  {
    "device": "/dev/sdb1",
    "mountpoint": "/data",
    "fstype": "ext4",
    "opts": "rw,relatime",
    "total": 1073741824000,
    "used": 214748364800,
    "free": 858993459200,
    "percent": 20.0
  }
]
```

**字段说明**:

| 字段 | 类型 | 描述 |
|------|------|------|
| device | string | 设备路径 |
| mountpoint | string | 挂载点 |
| fstype | string | 文件系统类型 |
| opts | string | 挂载选项 |
| total | number | 总容量 (bytes) |
| used | number | 已使用 (bytes) |
| free | number | 可用空间 (bytes) |
| percent | number | 使用率 (%) |

---

### GET /api/storage/io

获取存储 IO 统计。

**响应示例**:

```json
{
  "read_count": 1234567,
  "write_count": 987654,
  "read_bytes": 12345678901,
  "write_bytes": 9876543210,
  "read_time": 123456,
  "write_time": 98765
}
```

**字段说明**:

| 字段 | 类型 | 描述 |
|------|------|------|
| read_count | number | 读取次数 |
| write_count | number | 写入次数 |
| read_bytes | number | 读取字节数 |
| write_bytes | number | 写入字节数 |
| read_time | number | 读取耗时 (ms) |
| write_time | number | 写入耗时 (ms) |

---

## 错误处理

所有 API 接口在出错时返回标准 HTTP 状态码和错误信息。

### 错误响应格式

```json
{
  "detail": "Error message"
}
```

### 常见错误码

| 状态码 | 描述 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 使用示例

### cURL

```bash
# 获取系统信息
curl http://localhost:8902/api/system/info

# 获取 CPU 信息
curl http://localhost:8902/api/hardware/cpu

# 获取内存信息
curl http://localhost:8902/api/hardware/memory

# 获取进程列表（限制 10 个）
curl "http://localhost:8902/api/process/list?limit=10"

# 获取网络接口
curl http://localhost:8902/api/network/interfaces
```

### JavaScript (Fetch)

```javascript
// 获取系统信息
const response = await fetch('/api/system/info');
const data = await response.json();
console.log(data);

// 获取 CPU 信息
const cpuResponse = await fetch('/api/hardware/cpu');
const cpuData = await cpuResponse.json();
console.log(cpuData);
```

### Python (requests)

```python
import requests

# 获取系统信息
response = requests.get('http://localhost:8902/api/system/info')
data = response.json()
print(data)

# 获取 CPU 信息
cpu_response = requests.get('http://localhost:8902/api/hardware/cpu')
cpu_data = cpu_response.json()
print(cpu_data)
```
