from src.map_loader import load_map
from src.graph_utils import get_neighbors
from algorithms.search.bfs import bfs
from algorithms.search.dijkstra import dijkstra
from algorithms.search.astar import astar

G = load_map(bbox=(90.328217,23.700179,90.440483,23.826493))
# print(G.number_of_nodes(), G.number_of_edges())
# print(get_neighbors(G, 60917111))

nodes = list(G.nodes)
start, goal = nodes[0], nodes[-1]

bfs_path, expanded = bfs(G, start, goal, get_neighbors)
print("Path: ", bfs_path)
print("Nodes expanded", expanded)

print("----")

dijkstra_path, expanded = dijkstra(G, start, goal, get_neighbors)
print("Dijkstra path:", dijkstra_path)
print("Dijkstra nodes expanded:", expanded)

print("----")
astar_path, expanded = astar(G, start, goal, get_neighbors)
print("Astar Path: ", astar_path)
print("Astar Nodes Expanded: ", expanded)


def path_length(G, path, get_neighbors):
    total = 0
    for i in range(len(path) - 1):
        neighbors = dict(get_neighbors(G, path[i]))
        total += neighbors[path[i+1]]
    return total

print("BFS path length (m):", path_length(G, bfs_path, get_neighbors))
print("Dijkstra path length (m):", path_length(G, dijkstra_path, get_neighbors))
print("Astar path length (m):", path_length(G, astar_path, get_neighbors))