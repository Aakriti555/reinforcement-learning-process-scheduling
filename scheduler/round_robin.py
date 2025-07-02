def round_robin(processes, quantum=6):
    from collections import deque

    # Step 1: Initialize process properties
    for p in processes:
        p.remaining = p.burst
        p.start = None
        p.completion = None

    time = 0
    queue = deque()
    gantt = []
    completed = []
    i = 0  # index for arriving processes
    processes.sort(key=lambda p: p.arrival)

    while len(completed) < len(processes):
        # Step 2: Add all processes that have arrived by current time
        while i < len(processes) and processes[i].arrival <= time:
            queue.append(processes[i])
            i += 1

        if not queue:
            # CPU is idle, advance time
            time += 1
            continue

        current = queue.popleft()

        # Record start time only once
        if current.start is None:
            current.start = time

        run_time = min(current.remaining, quantum)
        gantt.append((current.pid, time, time + run_time))

        time += run_time
        current.remaining -= run_time

        # Add any newly arrived processes during run time
        while i < len(processes) and processes[i].arrival <= time:
            queue.append(processes[i])
            i += 1

        if current.remaining > 0:
            queue.append(current)
        else:
            current.completion = time
            completed.append(current)

    return processes, gantt
