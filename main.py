from src.map_loader import load_map
from src.graph_utils import get_neighbors
from algorithms.search.bfs import bfs

G = load_map(bbox=(90.328217,23.700179,90.440483,23.826493))
# print(G.number_of_nodes(), G.number_of_edges())
# print(get_neighbors(G, 60917111))

nodes = list(G.nodes)
start, goal = nodes[0], nodes[-1]

path, expanded = bfs(G, start, goal, get_neighbors)
print("Path: ", path)
print("Nodes expanded", expanded)