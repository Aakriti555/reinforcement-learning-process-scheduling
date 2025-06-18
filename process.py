class Process:
    def __init__(self, pid, arrival, burst, priority=0):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.remaining = burst
        self.priority = priority
        self.start = None
        self.completion = None

    def copy(self):
        new_process = Process(self.pid, self.arrival, self.burst, self.priority)
        new_process.remaining = self.remaining
        new_process.start = self.start
        new_process.completion = self.completion
        return new_process

    def __repr__(self):
        return f"P{self.pid}(AT={self.arrival}, BT={self.burst}, PR={self.priority})"
