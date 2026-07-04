import heapq
from algorithms.reconstruct_path import reconstruct_path

def dijkstra (G, start, goal, get_neighbors):
    # We all know what dijkstra does

    frontier = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    nodes_expanded = 0

    while frontier:
        curr_dist, curr = heapq.heappop(frontier)
        nodes_expanded += 1

        if curr == goal:
            return reconstruct_path(came_from, start, goal), nodes_expanded

        for neighbor, weight in get_neighbors(G, curr):
            new_dist = curr_dist + weight
            if neighbor not in cost_so_far or new_dist < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_dist
                came_from[neighbor] = curr
                heapq.heappush(frontier, (new_dist, neighbor))

    return None, nodes_expanded

