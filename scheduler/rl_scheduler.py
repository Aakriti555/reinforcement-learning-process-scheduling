import random
from markupsafe import soft_str
import numpy as np
import yaml
import json

class RLScheduler:
    def __init__(self, processes, episodes=1000, alpha=0.1, gamma=0.95, epsilon=0.2):
        self.original_processes = processes
        self.q_table = {}
        self.episodes = episodes
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon


    # def get_state(self, time, ready_processes):
    #     state_repr = tuple((p.pid, p.burst, p.priority) for p in ready_processes)
    #     return (time, state_repr)
    def get_state(self, time, ready_processes):
        if not ready_processes:
            return ("idle",)

        num_ready = len(ready_processes)
        bursts = [p.burst for p in ready_processes]
        priorities = [p.priority for p in ready_processes]

        # Discretize time into buckets
        time_bucket = time // 10  # reduces state space

        # Aggregate features
        avg_burst = int(np.mean(bursts))
        min_burst = min(bursts)
        max_burst = max(bursts)

        avg_priority = int(np.mean(priorities))
        min_priority = min(priorities)
        max_priority = max(priorities)

        return (time_bucket, num_ready, avg_burst, min_burst, max_burst, avg_priority, min_priority, max_priority)


    def choose_action(self, state, ready_indexes):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(len(ready_indexes))

        if random.random() < self.epsilon:
            return random.choice(range(len(ready_indexes)))
        else:
            return int(np.argmax(self.q_table[state]))

    def train(self, log_rewards=None, reward_mode="waiting"):
        if log_rewards is None:
            log_rewards = []

        for ep in range(self.episodes):
            processes = [p.copy() for p in self.original_processes]
            time = 0
            done = [False for _ in processes]
            total_reward = 0

            while not all(done):
                ready = [p for i, p in enumerate(processes) if not done[i] and p.arrival <= time]
                ready_indexes = [i for i, p in enumerate(processes) if not done[i] and p.arrival <= time]

                if not ready:
                    time += 1
                    continue

                state = self.get_state(time, ready)
                action_index = self.choose_action(state, ready_indexes)
                chosen_proc_idx = ready_indexes[action_index]
                p = processes[chosen_proc_idx]

                waiting_time = time - p.arrival
                turnaround_time = time + p.burst - p.arrival

                if reward_mode == "waiting":
                    reward = -waiting_time
                elif reward_mode == "turnaround":
                    reward = -turnaround_time
                elif reward_mode == "combined":
                    reward = -(waiting_time + turnaround_time)
                else:
                    reward = -waiting_time

                total_reward += reward

                duration = p.burst
                time += duration
                done[chosen_proc_idx] = True

                next_ready = [p for i, p in enumerate(processes) if not done[i] and p.arrival <= time]
                next_state = self.get_state(time, next_ready)

                if next_state not in self.q_table:
                    self.q_table[next_state] = np.zeros(len(next_ready)) if next_ready else [0]

                q_current = self.q_table[state][action_index]
                q_next_max = max(self.q_table[next_state]) if next_ready else 0

                self.q_table[state][action_index] += self.alpha * (reward + self.gamma * q_next_max - q_current)

            log_rewards.append(total_reward)

    def schedule(self):
        processes = [p.copy() for p in self.original_processes]
        time = 0
        done = [False for _ in processes]
        gantt = []

        while not all(done):
            ready = [p for i, p in enumerate(processes) if not done[i] and p.arrival <= time]
            ready_indexes = [i for i, p in enumerate(processes) if not done[i] and p.arrival <= time]

            if not ready:
                time += 1
                continue

            state = self.get_state(time, ready)
            if state not in self.q_table:
                action_index = random.choice(range(len(ready_indexes)))
            else:
                action_index = int(np.argmax(self.q_table[state]))

            chosen_proc_idx = ready_indexes[action_index]
            p = processes[chosen_proc_idx]

            p.start = time
            time += p.burst
            p.completion = time
            done[chosen_proc_idx] = True
            gantt.append((p.pid, p.start, p.completion))

        return processes, gantt

    def save_q_table_yaml(self, filepath):
        serializable_q_table = {}
        for state, q_values in self.q_table.items():
            state_key = json.dumps(state)
            q_values = np.array(q_values)
            serializable_q_table[state_key] = q_values.tolist() if isinstance(q_values, np.ndarray) else q_values
        with open(filepath, 'w') as f:
            yaml.dump(serializable_q_table, f)

    def load_q_table_yaml(self, filepath):
        with open(filepath, 'r') as f:
            loaded = yaml.safe_load(f)
        self.q_table = {}
        for state_str, q_values in loaded.items():
            state = json.loads(state_str)
            def to_tuple(obj):
                if isinstance(obj, list):
                    return tuple(to_tuple(i) for i in obj)
                return obj
            state = to_tuple(state)
            self.q_table[state] = np.array(q_values)
