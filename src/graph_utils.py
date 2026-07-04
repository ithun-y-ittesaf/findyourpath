def get_neighbors(G, node):
    """
    Returns a list of (neighbor_id, weight) for a given node
    If multiple exist, pick shortest one.
    """
    neighbors = []
    for neighbor in G[node]:
        edges_to_neighbor = G[node][neighbor]
        min_length = min(edge_data['length'] for edge_data in edges_to_neighbor.values())
        neighbors.append((neighbor, min_length))
    return neighbors