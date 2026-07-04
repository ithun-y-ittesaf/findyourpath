import os
import osmnx as ox

def load_map(bbox, cache_path = "data/map.graphml"):
    """
    Loads a road network graph for the given bounding box.
    Uses cached file if exists, otherwise download from OSM & cache
    """
    if os.path.exists(cache_path):
        G = ox.load_graphml(cache_path)
        print(f"Loaded cached graph from {cache_path}")
    else:
        G = ox.graph_from_bbox(bbox=bbox, network_type="drive")
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        ox.save_graphml(G, cache_path)
        print(f"Graph Downloaded & Cached to {cache_path}")

    return G