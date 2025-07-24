# 文件路径：/src/scheduler.py 动态分片调度器
import numpy as np
from kafka import KafkaProducer

class DynamicShardingScheduler:
    def __init__(self, kafka_servers='kafka:9092'):
        self.producer = KafkaProducer(bootstrap_servers=kafka_servers)
        self.node_stats = {}  # 存储节点负载
        
    def update_node_stats(self, node_id, cpu_usage, queue_len):
        """更新节点负载指标（被Prometheus回调）"""
        self.node_stats[node_id] = {
            'load': 0.7 * cpu_usage + 0.3 * queue_len,
            'cpu': cpu_usage
        }
    
    def dispatch(self, event, followers):
        """核心调度逻辑"""
        # 1. 获取热度等级
        event_type = HotEventDetector().is_hot_event(event)
        
        # 2. 动态分片
        shard_count = self._get_shard_count(event_type, len(followers))
        shards = np.array_split(followers, shard_count)
        
        # 3. 负载均衡分配
        for shard in shards:
            target_node = self._select_target_node()
            self._send_to_kafka(target_node, shard, event.content)
    
    def _get_shard_count(self, event_type, fan_count):
        """动态分片规则"""
        if event_type == "SUPER_HOT":
            return min(8, max(4, fan_count // 2000))  # 每2000粉丝1分片
        elif event_type == "HOT":
            return min(4, max(2, fan_count // 3000))
        return 1
    
    def _select_target_node(self):
        """基于负载的节点选择"""
        return min(self.node_stats.items(), key=lambda x: x[1]['load'])[0]
