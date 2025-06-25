def round_robin(processes, quantum=6):
    queue = []
    time = 0
    gantt = []
    completed = []
    processes.sort(key=lambda p: p.arrival)
    i = 0

    while len(completed) < len(processes):
        while i < len(processes) and processes[i].arrival <= time:
            queue.append(processes[i])
            i += 1

        if not queue:
            time += 1
            continue

        current = queue.pop(0)
        if current.start is None:
            current.start = time

        run_time = min(quantum, current.remaining)
        time += run_time
        current.remaining -= run_time
        gantt.append((current.pid, time - run_time, time))

        while i < len(processes) and processes[i].arrival <= time:
            queue.append(processes[i])
            i += 1

        if current.remaining > 0:
            queue.append(current)
        else:
            current.completion = time
            completed.append(current)

    return processes, gantt
