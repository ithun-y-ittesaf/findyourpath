"""
Generates every figure and stat used in docs/report.tex:
  - expansion heatmaps for BFS / Dijkstra / A* on a hard (103-hop) pair
  - a nodes-expanded bar chart comparing the three
  - Q-learning training curves (reward, success rate) on a learnable (~10-hop) pair
  - a map comparing A*'s optimal route against the trained agent's greedy rollout

Run from the repo root: python experiments/generate_report_assets.py
Writes images to docs/images/ and a stats summary to docs/report_stats.json.
"""

import json
import os
import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import osmnx as ox
from matplotlib.lines import Line2D

from src.map_loader import load_map
from src.graph_utils import get_neighbors
from algorithms.search.bfs import bfs
from algorithms.search.dijkstra import dijkstra
from algorithms.search.astar import astar
from algorithms.path_length import path_length
from src.visualize import plot_expansion
from src.rl.train import train

IMG_DIR = "docs/images"
os.makedirs(IMG_DIR, exist_ok=True)

PALETTE = {
    "blue": "#2a78d6",
    "aqua": "#1baf7a",
    "red": "#e34948",
    "muted": "#8a8a86",
    "grid": "#e3e2dd",
    "text": "#0b0b0b",
    "text2": "#52514e",
}


def style_axes(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(PALETTE["grid"])
    ax.spines["bottom"].set_color(PALETTE["grid"])
    ax.tick_params(colors=PALETTE["text2"])
    ax.grid(axis="y", color=PALETTE["grid"], linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)


def rolling(values, window):
    x = np.array(values, dtype=float)
    if len(x) < window:
        return x
    kernel = np.ones(window) / window
    return np.convolve(x, kernel, mode="valid")


def greedy_rollout(G, get_neighbors, agent, start, goal, max_steps=200):
    path = [start]
    current = start
    for _ in range(max_steps):
        if current == goal:
            break
        actions = [n for n, _ in get_neighbors(G, current)]
        if not actions:
            break
        q = agent.Q[current]
        action = max(actions, key=lambda a: q[a])
        path.append(action)
        current = action
    return path


random.seed(42)
stats = {}

G = load_map(bbox=(90.328217, 23.700179, 90.440483, 23.826493))
nodes = list(G.nodes)
stats["num_nodes"] = G.number_of_nodes()
stats["num_edges"] = G.number_of_edges()

# ---------------------------------------------------------------------------
# 1. Classical search comparison on a hard, far-apart pair.
# ---------------------------------------------------------------------------
far_start, far_goal = nodes[0], nodes[-1]

bfs_path, bfs_n, bfs_order = bfs(G, far_start, far_goal, get_neighbors)
dij_path, dij_n, dij_order = dijkstra(G, far_start, far_goal, get_neighbors)
astar_path, astar_n, astar_order = astar(G, far_start, far_goal, get_neighbors, lambda_=1.0)

plot_expansion(G, bfs_order, bfs_path, "BFS expansion", f"{IMG_DIR}/bfs_expansion.png")
plot_expansion(G, dij_order, dij_path, "Dijkstra expansion", f"{IMG_DIR}/dijkstra_expansion.png")
plot_expansion(G, astar_order, astar_path, "A* expansion (lambda = 1)", f"{IMG_DIR}/astar_expansion.png")

fig, ax = plt.subplots(figsize=(6, 4.2))
labels = ["BFS", "Dijkstra", "A* ($\\lambda$=1)"]
values = [bfs_n, dij_n, astar_n]
colors = [PALETTE["muted"], PALETTE["aqua"], PALETTE["blue"]]
bars = ax.bar(labels, values, color=colors, width=0.55, zorder=3)
for b, v in zip(bars, values):
    ax.text(b.get_x() + b.get_width() / 2, v, f"{v:,}", ha="center", va="bottom",
             fontsize=10, color=PALETTE["text"])
ax.set_ylabel("Nodes expanded")
ax.set_title(f"Search effort for a {len(bfs_path) - 1}-hop route")
style_axes(ax)
fig.tight_layout()
fig.savefig(f"{IMG_DIR}/nodes_expanded_comparison.png", dpi=200)
plt.close(fig)

stats["hard_pair"] = {
    "start": far_start, "goal": far_goal,
    "hop_distance": len(bfs_path) - 1,
    "bfs_nodes_expanded": bfs_n,
    "dijkstra_nodes_expanded": dij_n,
    "astar_nodes_expanded": astar_n,
    "bfs_path_length_m": path_length(G, bfs_path, get_neighbors),
    "dijkstra_path_length_m": path_length(G, dij_path, get_neighbors),
    "astar_path_length_m": path_length(G, astar_path, get_neighbors),
}
print("Hard pair:", stats["hard_pair"])

# ---------------------------------------------------------------------------
# 2. Find a learnable (8-15 hop) pair and train the Q-learning agent on it.
# ---------------------------------------------------------------------------
close_goal = nodes[-1]
close_start, close_path = None, None
for candidate in random.sample(nodes, len(nodes)):
    candidate_path, _, _ = bfs(G, candidate, close_goal, get_neighbors)
    if candidate_path and 8 <= len(candidate_path) <= 15:
        close_start, close_path = candidate, candidate_path
        break

if close_start is None:
    raise RuntimeError("No node found within 8-15 hops of goal")

hop_distance = len(close_path) - 1
print(f"Learnable pair: start={close_start} goal={close_goal} hop_distance={hop_distance}")

agent, rewards, successes = train(G, get_neighbors, close_start, close_goal, episodes=1000, max_steps=50)

window = 20
episodes_axis = np.arange(1, len(rewards) + 1)
roll_r = rolling(rewards, window)
roll_s = rolling(successes, window) * 100
roll_axis = episodes_axis[window - 1:]

fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))

ax = axes[0]
ax.plot(episodes_axis, rewards, color=PALETTE["grid"], linewidth=1, zorder=2, label="Episode reward")
ax.plot(roll_axis, roll_r, color=PALETTE["blue"], linewidth=2.2, zorder=3, label=f"{window}-ep rolling avg")
ax.axhline(0, color=PALETTE["text2"], linewidth=0.8, linestyle="--", zorder=1)
ax.set_xlabel("Episode")
ax.set_ylabel("Total reward")
ax.set_title("Reward per episode")
ax.legend(frameon=False, fontsize=9, loc="lower right")
style_axes(ax)

ax = axes[1]
ax.plot(roll_axis, roll_s, color=PALETTE["aqua"], linewidth=2.2, zorder=3)
ax.set_ylim(-5, 105)
ax.set_xlabel("Episode")
ax.set_ylabel("Success rate (%)")
ax.set_title(f"{window}-episode rolling success rate")
style_axes(ax)

fig.suptitle(f"Q-learning convergence — {hop_distance}-hop start/goal pair, max_steps=50", fontsize=11)
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig(f"{IMG_DIR}/rl_training_curves.png", dpi=200)
plt.close(fig)

stats["rl_training"] = {
    "start": close_start, "goal": close_goal,
    "hop_distance": hop_distance,
    "episodes": len(rewards),
    "max_steps": 50,
    "final_200ep_avg_reward": float(np.mean(rewards[-200:])),
    "final_200ep_success_rate_pct": float(np.mean(successes[-200:]) * 100),
    "first_200ep_success_rate_pct": float(np.mean(successes[:200]) * 100),
}
print("RL training:", stats["rl_training"])

# ---------------------------------------------------------------------------
# 3. A* vs. trained-agent greedy rollout, on the same learnable pair.
# ---------------------------------------------------------------------------
agent.epsilon = 0.0
rl_path = greedy_rollout(G, get_neighbors, agent, close_start, close_goal, max_steps=200)
rl_success = rl_path[-1] == close_goal

astar_close_path, astar_close_n, _ = astar(G, close_start, close_goal, get_neighbors, lambda_=1.0)
astar_len_m = path_length(G, astar_close_path, get_neighbors)
rl_len_m = path_length(G, rl_path, get_neighbors) if rl_success else None

fig, ax = ox.plot_graph(
    G, node_size=0, edge_color="#c9c8c2", edge_linewidth=0.5,
    bgcolor="#fcfcfb", show=False, close=False,
)
ox.plot_graph_route(
    G, astar_close_path, route_color=PALETTE["blue"], route_linewidth=4,
    route_alpha=0.9, ax=ax, show=False, close=False, orig_dest_size=30,
)
if rl_success:
    ox.plot_graph_route(
        G, rl_path, route_color=PALETTE["red"], route_linewidth=3,
        route_alpha=0.9, ax=ax, show=False, close=False, orig_dest_size=0,
    )

handles = [Line2D([0], [0], color=PALETTE["blue"], lw=4,
                   label=f"A* — optimal ({astar_len_m:.0f} m)")]
if rl_success:
    handles.append(Line2D([0], [0], color=PALETTE["red"], lw=3,
                            label=f"Q-learning greedy rollout ({rl_len_m:.0f} m)"))
else:
    handles.append(Line2D([0], [0], color=PALETTE["red"], lw=3, linestyle=":",
                            label="Q-learning greedy rollout (did not reach goal)"))
ax.legend(handles=handles, loc="lower right", frameon=True, fontsize=9)
ax.set_title("Planning (A*) vs. learning (Q-learning): same start/goal")

route_nodes = set(astar_close_path) | set(rl_path)
xs = [G.nodes[n]["x"] for n in route_nodes]
ys = [G.nodes[n]["y"] for n in route_nodes]
pad_x = (max(xs) - min(xs)) * 0.6 + 0.002
pad_y = (max(ys) - min(ys)) * 0.6 + 0.002
ax.set_xlim(min(xs) - pad_x, max(xs) + pad_x)
ax.set_ylim(min(ys) - pad_y, max(ys) + pad_y)

fig.savefig(f"{IMG_DIR}/astar_vs_rl_comparison.png", dpi=200)
plt.close(fig)

stats["astar_vs_rl"] = {
    "start": close_start, "goal": close_goal,
    "astar_hops": len(astar_close_path) - 1,
    "astar_length_m": astar_len_m,
    "astar_nodes_expanded": astar_close_n,
    "rl_success": rl_success,
    "rl_hops": len(rl_path) - 1,
    "rl_length_m": rl_len_m,
}
print("A* vs RL:", stats["astar_vs_rl"])

with open("docs/report_stats.json", "w") as f:
    json.dump(stats, f, indent=2)

print("\nAll figures written to docs/images/, stats written to docs/report_stats.json")
