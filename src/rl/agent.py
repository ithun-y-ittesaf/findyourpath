import random
from collections import defaultdict


class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.05):

        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.Q = defaultdict(lambda: defaultdict(float))  # Q[state][action] = value

    def choose_action(self, state, available_actions):

        """Epsilon-greedy: explore randomly sometimes, 
           exploit best known action otherwise."""
        
        if not available_actions:
            return None

        if random.random() < self.epsilon:
            return random.choice(available_actions)

        # Exploit: pick the action with highest known Q-value
        q_values = self.Q[state]
        best_action = max(available_actions, key=lambda a: q_values[a])
        return best_action

    def update(self, state, action, reward, next_state, next_available_actions):

        """The core Q-learning update rule."""
        
        best_next_q = max([self.Q[next_state][a] for a in next_available_actions], default=0)
        td_target = reward + self.gamma * best_next_q
        td_error = td_target - self.Q[state][action]
        self.Q[state][action] += self.alpha * td_error

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)