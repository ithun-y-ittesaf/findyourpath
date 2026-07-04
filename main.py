from src.map_loader import load_map
from src.graph_utils import get_neighbors
from algorithms.search.bfs import bfs
from algorithms.search.dijkstra import dijkstra
from algorithms.search.astar import astar
from algorithms.path_length import path_length
from src.visualize import plot_expansion


G = load_map(bbox=(90.328217,23.700179,90.440483,23.826493))
# print(G.number_of_nodes(), G.number_of_edges())
# print(get_neighbors(G, 60917111))

nodes = list(G.nodes)
start, goal = nodes[0], nodes[-1]


bfs_path, _, bfs_order = bfs(G, start, goal, get_neighbors)
dij_path, _, dij_order = dijkstra(G, start, goal, get_neighbors)
astar_path, _, astar_order = astar(G, start, goal, get_neighbors)

plot_expansion(G, bfs_order, bfs_path, "BFS expansion", "bfs.png")
plot_expansion(G, dij_order, dij_path, "Dijkstra expansion", "dijkstra.png")
plot_expansion(G, astar_order, astar_path, "A* expansion", "astar.png")