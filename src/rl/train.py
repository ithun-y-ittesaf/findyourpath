from src.rl.environment import GraphEnv
from src.rl.agent import QLearningAgent


def train(G, get_neighbors, start, goal, episodes=2000, max_steps=200):
    env = GraphEnv(G, get_neighbors, goal, max_steps=max_steps)
    agent = QLearningAgent()

    episode_rewards = []
    successes = []

    for ep in range(episodes):
        state = env.reset(start=start)
        total_reward = 0
        done = False
        reached_goal = False

        while not done:
            available = env.available_actions(state)
            if not available:
                break

            action = agent.choose_action(state, available)
            next_state, reward, done = env.step(action)

            next_available = env.available_actions(next_state)
            agent.update(state, action, reward, next_state, next_available)

            state = next_state
            total_reward += reward

            if state == goal:
                reached_goal = True

        agent.decay_epsilon()
        episode_rewards.append(total_reward)
        successes.append(1 if reached_goal else 0)

        if (ep + 1) % 200 == 0:
            avg_reward = sum(episode_rewards[-200:]) / 200
            success_rate = sum(successes[-200:]) / 200 * 100
            print(f"Episode {ep+1}/{episodes} | avg reward: {avg_reward:.1f} | success rate: {success_rate:.0f}% | epsilon: {agent.epsilon:.3f}")

    return agent, episode_rewards, successes