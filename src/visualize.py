import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import osmnx as ox

def plot_expansion(G, expansion_order, path, title, filepath):
    """
    Plots the graph with nodes colored by expansion order (search frontier growth),
    and the final path highlighted on top.
    """

    node_colors = []
    node_sizes = []

    order_index = {node: i for i, node in enumerate(expansion_order)}
    max_order = max(order_index.values()) if order_index else 0
    norm = mcolors.Normalize(vmin=0, vmax=max_order)
    cmap = plt.colormaps["plasma"]

    for node in G.nodes:
        if node in order_index:
            node_colors.append(cmap(norm(order_index[node])))
            node_sizes.append(8)
        else:
            node_colors.append("#999999")
            node_sizes.append(2)

    fig, ax = ox.plot_graph(
        G,
        node_color=node_colors,
        node_size=node_sizes,
        edge_color="gray",
        edge_linewidth=0.5,
        show=False,
        close=False
    )

    if path:
        ox.plot_graph_route(
            G, path,
            route_color="cyan",
            route_linewidth=3,
            ax=ax,
            show=False,
            close=False
        )
    
    ax.set_title(title)
    fig.savefig(filepath, dpi=200)
    plt.close(fig)
    print(f"Saved at {filepath}")