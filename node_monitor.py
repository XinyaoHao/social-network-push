# 文件路径：/src/node_monitor.py step4负载均衡监控
import psutil
import time
from prometheus_client import Gauge

class NodeMonitor:
    def __init__(self):
        self.cpu_gauge = Gauge('node_cpu_usage', 'CPU usage percent')
        self.queue_gauge = Gauge('node_queue_length', 'Pending tasks')
        
    def start_metrics_loop(self):
        while True:
            # 模拟从Prometheus获取（实际应调用API）
            cpu = psutil.cpu_percent()
            queue_len = self._get_kafka_queue_length()
            
            self.cpu_gauge.set(cpu)
            self.queue_gauge.set(queue_len)
            time.sleep(5)
