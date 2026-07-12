import random

class GraphEnv:
    """
    A simple RL environment wrapping the road graph.
    State = current Node, Action = Choice of Neighbor to move to
    """

    def __init__(self, G, get_neighbors, goal, max_steps = 200):
        self.G = G
        self.get_neighbors = get_neighbors
        self.goal = goal
        self.max_steps = max_steps
        self.current = None
        self.steps = 0
        self.visited_this_episode = set()

    def reset(self, start=None):
        #Start a New Episode. If start is None, pick random.
        self.current = start if start is not None else random.choice(list(self.G.nodes))
        self.steps = 0
        self.visited_this_episode = {self.current}
        return self.current

    def available_actions(self, state):
        # Returns a list of neighbor node ids reachable from state.
        return [n for n, _w in self.get_neighbors(self.G, state)]
    
    def step(self, action):
        self.steps += 1

        neighbors = dict(self.get_neighbors(self.G, self.current))
        if action not in neighbors:
            return self.current, -50, True
        
        self.current = action

        if self.current == self.goal:
            return self.current, 100, True

        reward = -1
        if self.current in self.visited_this_episode:
            reward -= 5;

        self.visited_this_episode.add(self.current)

        done = self.steps >= self.max_steps
        return self.current, reward, done
    