def fcfs(processes):
    processes.sort(key=lambda p: p.arrival)
    time = 0
    gantt = []

    for p in processes:
        if time < p.arrival:
            time = p.arrival
        p.start = time
        time += p.burst
        p.completion = time
        gantt.append((p.pid, p.start, p.completion))

    return processes, gantt