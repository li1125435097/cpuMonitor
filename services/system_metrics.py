# app/services/system_metrics.py
import psutil
import time
from typing import Dict, Any

class SystemMetrics:
    def __init__(self):
        self.last_net_io = self._get_network_usage()
        self.last_net_time = time.time()

    def get_cpu_metrics(self) -> Dict[str, Any]:
        cpu_percent = psutil.cpu_percent(interval=None, percpu=True)
        cpu_freq = psutil.cpu_freq(percpu=False)
        return {
            "total_usage": sum(cpu_percent) / len(cpu_percent),
            "per_cpu_usage": cpu_percent,
            "frequency": round(cpu_freq.current, 2) if cpu_freq else 0
        }

    def get_memory_metrics(self) -> Dict[str, Any]:
        memory = psutil.virtual_memory()
        return {
            "total": memory.total,
            "available": memory.available,
            "percent": memory.percent,
            "used": memory.used
        }

    def _get_network_usage(self) -> Dict[str, int]:
        net_io = psutil.net_io_counters()
        return {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv
        }

    def get_network_metrics(self) -> Dict[str, float]:
        current_net_io = self._get_network_usage()
        current_time = time.time()
        time_diff = current_time - self.last_net_time

        bytes_sent_sec = (current_net_io["bytes_sent"] - self.last_net_io["bytes_sent"]) / time_diff
        bytes_recv_sec = (current_net_io["bytes_recv"] - self.last_net_io["bytes_recv"]) / time_diff

        self.last_net_io = current_net_io
        self.last_net_time = current_time

        return {
            "bytes_sent_per_sec": round(bytes_sent_sec, 2),
            "bytes_recv_per_sec": round(bytes_recv_sec, 2)
        }

    def get_all_metrics(self) -> Dict[str, Any]:
        return {
            "timestamp": time.time(),
            "cpu": self.get_cpu_metrics(),
            "memory": self.get_memory_metrics(),
            "network": self.get_network_metrics()
        }