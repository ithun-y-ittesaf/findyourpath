import heapq
from math import radians, sin, cos, sqrt, atan2
from algorithms.reconstruct_path import reconstruct_path

def haversine(G, node1, node2):
    # Great Circle distance in meters between two graph nodes
    lat1, lon1 = radians(G.nodes[node1]['y']), radians(G.nodes[node1]['x'])
    lat2, lon2 = radians(G.nodes[node2]['y']), radians(G.nodes[node2]['x'])

    dlat = lat2-lat1
    dlon = lon2-lon1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    R = 6371000 #Earth Radius in Meters
    return R*c

def astar(G, start, goal, get_neighbors):
    """
    Like Dijkstra, but guided towards goal using a heuristic.
    Returns (path as list of node ids, nodes_expanded count)
    """
    frontier = [(0, start)]  # (priority = cost_so_far + heuristic, node)
    came_from = {start: None}
    cost_so_far = {start: 0}
    nodes_expanded = 0

    while frontier:
        _, current = heapq.heappop(frontier)
        nodes_expanded += 1

        if current == goal:
            return reconstruct_path(came_from, start, goal), nodes_expanded
        
        for neighbor, weight in get_neighbors(G, current):
            new_dist = cost_so_far[current] + weight
            if neighbor not in cost_so_far or new_dist < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_dist
                priority = new_dist + haversine(G, neighbor, goal)
                came_from[neighbor] = current
                heapq.heappush(frontier, (priority, neighbor))
    
    return None, nodes_expanded
