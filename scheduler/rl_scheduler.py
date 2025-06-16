import random
import numpy as np

class RLScheduler:
    def __init__(self, processes, episodes=1000, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.processes = processes
        self.q_table = {}
        self.episodes = episodes
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.actions = list(range(len(processes)))

    def get_state(self, time, remaining):
        return (time, tuple(remaining))

    def choose_action(self, state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(len(self.actions))

        if random.random() < self.epsilon:
            return random.choice(self.actions)
        else:
            return int(np.argmax(self.q_table[state]))

    def train(self):
        for ep in range(self.episodes):
            time = 0
            remaining = [p.burst for p in self.processes]
            done = [False for _ in self.processes]

            while not all(done):
                state = self.get_state(time, remaining)
                action = self.choose_action(state)

                if done[action] or self.processes[action].arrival > time:
                    time += 1
                    continue

                duration = remaining[action]
                reward = -duration
                remaining[action] = 0
                done[action] = True
                time += duration

                next_state = self.get_state(time, remaining)
                if next_state not in self.q_table:
                    self.q_table[next_state] = np.zeros(len(self.actions))

                self.q_table[state][action] += self.alpha * (reward + self.gamma * max(self.q_table[next_state]) - self.q_table[state][action])

    def schedule(self):
        time = 0
        remaining = [p.burst for p in self.processes]
        done = [False for _ in self.processes]
        gantt = []

        while not all(done):
            state = self.get_state(time, remaining)
            if state not in self.q_table:
                action = random.choice(self.actions)
            else:
                action = int(np.argmax(self.q_table[state]))

            if done[action] or self.processes[action].arrival > time:
                time += 1
                continue

            p = self.processes[action]
            if p.start is None:
                p.start = time
            duration = remaining[action]
            time += duration
            p.completion = time
            remaining[action] = 0
            done[action] = True
            gantt.append((p.pid, p.start, p.completion))

        return self.processes, gantt
