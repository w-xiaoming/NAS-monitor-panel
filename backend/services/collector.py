"""System data collector service"""
import psutil
import platform
import socket
import os
import time
from datetime import datetime
from typing import Dict, List, Any


class SystemCollector:
    """Collects system information"""

    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "os_release": platform.release(),
            "kernel": platform.release(),
            "architecture": platform.machine(),
            "hostname": socket.gethostname(),
            "uptime": time.time() - psutil.boot_time(),
            "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat()
        }


class HardwareCollector:
    """Collects hardware status"""

    @staticmethod
    def get_cpu_info() -> Dict[str, Any]:
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        cpu_times = psutil.cpu_times_percent(interval=1)
        load_avg = os.getloadavg()

        return {
            "percent_overall": psutil.cpu_percent(interval=0.1),
            "percent_per_core": cpu_percent,
            "core_count": psutil.cpu_count(logical=False),
            "logical_count": psutil.cpu_count(logical=True),
            "frequency": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
            "times": {
                "user": cpu_times.user,
                "system": cpu_times.system,
                "idle": cpu_times.idle
            },
            "load_average": {
                "1min": load_avg[0],
                "5min": load_avg[1],
                "15min": load_avg[2]
            }
        }

    @staticmethod
    def get_memory_info() -> Dict[str, Any]:
        virtual = psutil.virtual_memory()
        swap = psutil.swap_memory()

        return {
            "virtual": {
                "total": virtual.total,
                "available": virtual.available,
                "used": virtual.used,
                "free": virtual.free,
                "percent": virtual.percent,
                "cached": getattr(virtual, 'cached', 0),
                "buffers": getattr(virtual, 'buffers', 0)
            },
            "swap": {
                "total": swap.total,
                "used": swap.used,
                "free": swap.free,
                "percent": swap.percent
            }
        }

    @staticmethod
    def get_temperature() -> Dict[str, Any]:
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                return {name: [t._asdict() for t in entries] for name, entries in temps.items()}
        except (AttributeError, Exception):
            pass
        return {"available": False}


class NetworkCollector:
    """Collects network status"""

    @staticmethod
    def get_interfaces() -> List[Dict[str, Any]]:
        interfaces = []
        addrs = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        io = psutil.net_io_counters(pernic=True)

        for name, addr_list in addrs.items():
            iface = {
                "name": name,
                "addresses": [],
                "is_up": stats.get(name, None),
                "bytes_sent": io.get(name, None),
            }
            for addr in addr_list:
                iface["addresses"].append({
                    "family": str(addr.family),
                    "address": addr.address,
                    "netmask": addr.netmask,
                    "broadcast": addr.broadcast
                })
            interfaces.append(iface)
        return interfaces

    @staticmethod
    def get_io_counters() -> Dict[str, Any]:
        counters = psutil.net_io_counters()
        return {
            "bytes_sent": counters.bytes_sent,
            "bytes_recv": counters.bytes_recv,
            "packets_sent": counters.packets_sent,
            "packets_recv": counters.packets_recv,
            "errin": counters.errin,
            "errout": counters.errout
        }


class ProcessCollector:
    """Collects process information"""

    @staticmethod
    def get_processes(limit: int = 50) -> List[Dict[str, Any]]:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status', 'create_time']):
            try:
                pinfo = proc.info
                processes.append({
                    "pid": pinfo['pid'],
                    "name": pinfo['name'],
                    "cpu_percent": pinfo['cpu_percent'],
                    "memory_percent": pinfo['memory_percent'],
                    "status": pinfo['status'],
                    "create_time": datetime.fromtimestamp(pinfo['create_time']).isoformat() if pinfo['create_time'] else None
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        processes.sort(key=lambda x: x.get('cpu_percent', 0) or 0, reverse=True)
        return processes[:limit]

    @staticmethod
    def get_connections() -> List[Dict[str, Any]]:
        connections = []
        for conn in psutil.net_connections(kind='inet'):
            connections.append({
                "fd": conn.fd,
                "family": str(conn.family),
                "type": str(conn.type),
                "laddr": conn.laddr._asdict() if conn.laddr else None,
                "raddr": conn.raddr._asdict() if conn.raddr else None,
                "status": conn.status,
                "pid": conn.pid
            })
        return connections


class StorageCollector:
    """Collects storage information"""

    @staticmethod
    def get_partitions() -> List[Dict[str, Any]]:
        partitions = []
        for part in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(part.mountpoint)
                partitions.append({
                    "device": part.device,
                    "mountpoint": part.mountpoint,
                    "fstype": part.fstype,
                    "opts": part.opts,
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": usage.percent
                })
            except PermissionError:
                continue
        return partitions

    @staticmethod
    def get_io_counters() -> Dict[str, Any]:
        counters = psutil.disk_io_counters()
        if counters:
            return {
                "read_count": counters.read_count,
                "write_count": counters.write_count,
                "read_bytes": counters.read_bytes,
                "write_bytes": counters.write_bytes,
                "read_time": counters.read_time,
                "write_time": counters.write_time
            }
        return {}


collector = SystemCollector()
