from collections import deque
from algorithms.reconstruct_path import reconstruct_path

def bfs(G, start, goal, get_neighbors):
    """
    Classic BFS. Find path with fewest number of edges.
    Return path as a list of node ids, nodes_expanded count or,
        (None, count) if no path found.
    """

    frontier = deque([start])
    came_from = {start: None}
    nodes_expanded = 0

    while frontier:
        current = frontier.popleft()
        nodes_expanded += 1

        if current == goal:
            return reconstruct_path(came_from, start, goal), nodes_expanded
        
        for neighbor, _weight in get_neighbors(G, current):
            if neighbor not in came_from:
                came_from[neighbor] = current
                frontier.append(neighbor)

    return None, nodes_expanded

