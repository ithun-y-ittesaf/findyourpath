def path_length(G, path, get_neighbors):
    total = 0
    for i in range(len(path) - 1):
        neighbors = dict(get_neighbors(G, path[i]))
        total += neighbors[path[i+1]]
    return total