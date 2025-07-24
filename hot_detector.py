# 文件路径：/src/hot_detector.py  step2热点检测处理模块
from math import log10

class HotEventDetector:
    def __init__(self):
        self.hot_threshold = 10000  # 粉丝数硬阈值
        self.super_hot_score = 0.8
        self.hot_score = 0.5

    def is_hot_event(self, event):
        """复合热度检测（兼容极简版与完整版）"""
        # 极简模式（仅粉丝数）
        if event.author_followers > self.hot_threshold:
            return "HOT"
        
        # 完整模式（带互动权重）
        hot_score = 0.6 * log10(event.author_followers + 1) + \
                   0.4 * (event.initial_likes / 5000)
        
        if hot_score > self.super_hot_score:
            return "SUPER_HOT"
        elif hot_score > self.hot_score:
            return "HOT"
        return "NORMAL"
