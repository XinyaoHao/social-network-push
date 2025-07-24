# 文件路径：/src/graph_loader.py step1社交图预处理
import gzip
import networkx as nx
from tqdm import tqdm

def load_graph():
    """加载并预处理五万节点社交图"""
    G = nx.DiGraph()
    with gzip.open('/data/final_graph.edgelist.gz', 'rt') as f:
        for line in tqdm(f, desc="Loading graph"):
            u, v = line.strip().split()
            G.add_edge(u, v)
    
    # 预计算PageRank用于模拟大V（替代真实互动数据）
    pr = nx.pagerank(G)
    nx.set_node_attributes(G, pr, 'pagerank')
    return G

# 示例使用
social_graph = load_graph()
