import random

from src.map_loader import load_map
from src.graph_utils import get_neighbors
from algorithms.search.bfs import bfs
from algorithms.search.dijkstra import dijkstra
from algorithms.search.astar import astar
from algorithms.path_length import path_length
from src.visualize import plot_expansion


G = load_map(bbox=(90.328217,23.700179,90.440483,23.826493))


nodes = list(G.nodes)
goal = nodes[-1]


start = None
path = None
for candidate in random.sample(nodes, len(nodes)):
    candidate_path, _, _ = bfs(G, candidate, goal, get_neighbors)
    if candidate_path and 8 <= len(candidate_path) <= 15:
        start = candidate
        path = candidate_path
        break

if start is None:
    raise RuntimeError("No node found within 8-15 hops of goal")

print(f"Using start={start}, goal={goal}, hop distance={len(path)}")

from src.rl.train import train

agent, rewards, successes = train(G, get_neighbors, start, goal, episodes=1000, max_steps=50)