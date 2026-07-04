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
astar_lambda0_path, _, astar_lambda0_order = astar(G, start, goal, get_neighbors, lambda_=0)
astar_lambda40_path, _, astar_lambda40_order = astar(G, start, goal, get_neighbors, lambda_=40)

plot_expansion(G, bfs_order, bfs_path, "BFS expansion", "bfs.png")
plot_expansion(G, dij_order, dij_path, "Dijkstra expansion", "dijkstra.png")
plot_expansion(G, astar_order, astar_path, "A* expansion (lambda = 1, base)", "astar.png")
plot_expansion(G, astar_lambda0_order, astar_lambda0_path, "A* expansion (lambda = 0)", "docs/images/astar_lambda_0.png")
plot_expansion(G, astar_lambda40_order, astar_lambda40_path, "A* expansion (lambda = 40)", "docs/images/astar_lambda_40x.png")