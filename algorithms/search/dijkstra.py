import heapq
from algorithms.reconstruct_path import reconstruct_path

def dijkstra (G, start, goal, get_neighbors):
    # We all know what dijkstra does

    frontier = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    expansion_order = []

    while frontier:
        curr_dist, curr = heapq.heappop(frontier)
        expansion_order.append(curr)

        if curr == goal:
            return reconstruct_path(came_from, start, goal), len(expansion_order), expansion_order

        for neighbor, weight in get_neighbors(G, curr):
            new_dist = curr_dist + weight
            if neighbor not in cost_so_far or new_dist < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_dist
                came_from[neighbor] = curr
                heapq.heappush(frontier, (new_dist, neighbor))

    return None, len(expansion_order), expansion_order

