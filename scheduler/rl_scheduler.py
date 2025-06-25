import random
import numpy as np

class RLScheduler:
    def __init__(self, processes, episodes=1000, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.original_processes = processes
        self.q_table = {}
        self.episodes = episodes
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def get_state(self, time, ready_processes):
        # State = current time + tuple of (pid, burst, priority) for ready processes
        state_repr = tuple((p.pid, p.burst, p.priority) for p in ready_processes)
        return (time, state_repr)

    def choose_action(self, state, ready_indexes):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(len(ready_indexes))

        if random.random() < self.epsilon:
            return random.choice(range(len(ready_indexes)))
        else:
            return int(np.argmax(self.q_table[state]))

    def train(self):
        for ep in range(self.episodes):
            processes = [p.copy() for p in self.original_processes]
            time = 0
            done = [False for _ in processes]

            while not all(done):
                # Build the ready queue
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
                reward = -waiting_time  # Encourage shorter waiting time

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
