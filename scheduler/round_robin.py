def round_robin(processes, quantum=6):
    queue = []
    time = 0
    gantt = []
    completed = []
    processes.sort(key=lambda p: p.arrival)
    i = 0

    while len(completed) < len(processes):
        # Add arrived processes to the queue
        while i < len(processes) and processes[i].arrival <= time:
            queue.append(processes[i])
            i += 1

        if not queue:
            # CPU is idle
            time += 1
            continue

        current = queue.pop(0)

        if current.start is None:
            current.start = time  # Set start time only once

        run_time = min(quantum, current.remaining)
        gantt.append((current.pid, time, time + run_time))

        time += run_time
        current.remaining -= run_time

        # Check for newly arrived processes during this quantum
        while i < len(processes) and processes[i].arrival <= time:
            queue.append(processes[i])
            i += 1

        if current.remaining > 0:
            queue.append(current)  # Put back in the queue
        else:
            current.completion = time
            completed.append(current)

    return processes, gantt
