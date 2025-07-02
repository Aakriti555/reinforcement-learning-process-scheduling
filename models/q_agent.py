# # q_agent.py

# import random
# import numpy as np
# import pickle

# class QAgent:
#     def __init__(self, actions, alpha=0.1, gamma=0.9, epsilon=0.1):
#         """
#         Q-learning agent.

#         Args:
#             actions (list): List of possible actions.
#             alpha (float): Learning rate.
#             gamma (float): Discount factor.
#             epsilon (float): Exploration rate.
#         """
#         self.actions = actions
#         self.alpha = alpha
#         self.gamma = gamma
#         self.epsilon = epsilon
#         self.q_table = {}

#     def get_q_values(self, state):
#         """Return Q-values for all actions in a given state."""
#         if state not in self.q_table:
#             self.q_table[state] = np.zeros(len(self.actions))
#         return self.q_table[state]

#     def choose_action(self, state):
#         """Choose an action using epsilon-greedy policy."""
#         q_values = self.get_q_values(state)
#         if random.random() < self.epsilon:
#             return random.choice(self.actions)
#         else:
#             return int(np.argmax(q_values))

#     def update(self, state, action, reward, next_state):
#         """Update Q-table based on the experience."""
#         q_values = self.get_q_values(state)
#         next_q_values = self.get_q_values(next_state)

#         td_target = reward + self.gamma * np.max(next_q_values)
#         td_error = td_target - q_values[action]

#         q_values[action] += self.alpha * td_error

#     def save(self, filepath):
#         """Save Q-table to a file."""
#         with open(filepath, 'wb') as f:
#             pickle.dump(self.q_table, f)

#     def load(self, filepath):
#         """Load Q-table from a file."""
#         with open(filepath, 'rb') as f:
#             self.q_table = pickle.load(f)
