def sjf(processes):
    processes.sort(key=lambda p: (p.arrival, p.burst))
    completed = []
    gantt = []
    time = 0

    while len(completed) < len(processes):
        ready = [p for p in processes if p.arrival <= time and p not in completed]
        if not ready:
            time += 1
            continue
        current = min(ready, key=lambda p: p.burst)
        current.start = time
        time += current.burst
        current.completion = time
        completed.append(current)
        gantt.append((current.pid, current.start, current.completion))

    return processes, gantt