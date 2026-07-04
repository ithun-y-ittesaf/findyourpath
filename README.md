# FindYourPath

A starter AI project that finds the shortest path between two nodes in a graph.

## Overview

FindYourPath is a learning project exploring AI pathfinding algorithms. It implements graph traversal techniques to efficiently discover the shortest route from a source node to a destination node.

## Features

- Graph-based pathfinding
- Shortest path discovery
- Node-to-node routing
- Visualization of node expansion and final path (heatmap + shortest path overlay)
- Educational implementation for AI exploration

## Algorithms

- **BFS** (`algorithms/search/bfs.py`)
- **Dijkstra** (`algorithms/search/dijkstra.py`)
- **A\*** (`algorithms/search/astar.py`) - guided by a haversine distance heuristic to the goal

## Getting Started

### Prerequisites

- Python 3.x
- Basic understanding of graph data structures

### Installation

```bash
git clone https://github.com/yourusername/findyourpath.git
cd findyourpath
```

### Usage

```python
# Example usage
from findyourpath import find_shortest_path

# Define your graph and nodes
shortest_path = find_shortest_path(start_node, end_node, graph)
print(shortest_path)
```

Running `main.py` produces expansion heatmaps for each algorithm (`bfs.png`, `dijkstra.png`, `astar.png`) showing every node visited before the final shortest path is found.

## Documentation

### A* heuristic weighting (lambda)

A*'s priority function is `cost_so_far + lambda * heuristic`. Scaling the heuristic term by a `lambda` multiplier changes how aggressively the search is pulled toward the goal:

- **lambda = 1 (basic A\*)** - the standard, admissible heuristic weight. This is what's currently wired up in `astar.py`.
- **lambda = 0** - the heuristic term drops out entirely, so `priority = cost_so_far`. This makes A* mathematically identical to Dijkstra (pure cost-based expansion, no goal guidance).
- **lambda = 40-50x** - the heuristic dominates the priority, so the search beelines toward the goal almost greedily.

**Observation:** running A* with `lambda = 0` reproduced Dijkstra's results almost exactly, but expanded roughly **20x** more nodes than basic A* (lambda = 1). This confirms the two are equivalent when the heuristic is zeroed out — Dijkstra is just a special case of A*. At very high lambda (40-50x), the search expands far fewer nodes but the reported "shortest" path showed a noticeable error relative to the true shortest path — the heuristic overrides true edge costs enough that A* loses its optimality guarantee.

| Case | Expansion behavior | Path correctness |
|---|---|---|
| lambda = 1 (basic A\*) | Efficient, goal-directed | Correct shortest path |
| lambda = 0 (= Dijkstra) | ~20x more nodes expanded | Correct shortest path |
| lambda = 40-50x | Very few nodes expanded | Noticeable deviation from true shortest path |

#### Expansion heatmaps

<!-- Drop the corresponding screenshot/plot into the repo and update the path below for each case. -->

**Lambda = 1 (basic A\*)**

![A* basic (lambda = 1)](astar.png)

**Lambda = 0 (equivalent to Dijkstra)**

![A* lambda = 0](docs/images/astar_lambda_0.png)

**Lambda = 40-50x (over-weighted heuristic)**

![A* lambda = 40-50x](docs/images/astar_lambda_40x.png)

## Project Status

Early stages - actively exploring AI concepts and algorithms

## License

MIT
