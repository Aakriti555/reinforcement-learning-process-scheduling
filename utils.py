def calculate_metrics(processes):
    total_tat = sum(p.completion - p.arrival for p in processes)
    total_wt = sum(p.completion - p.arrival - p.burst for p in processes)
    n = len(processes)
    avg_tat = total_tat / n
    avg_wt = total_wt / n
    return avg_tat, avg_wt


def print_metrics(processes):
    avg_tat, avg_wt = calculate_metrics(processes)
    print("\nProcess Completion:")
    for p in processes:
        print(f"P{p.pid}: Start={p.start}, Completion={p.completion}, Turnaround={p.completion - p.arrival}, Waiting={p.completion - p.arrival - p.burst}")
    print(f"\nAverage Turnaround Time: {avg_tat:.2f}")
    print(f"Average Waiting Time: {avg_wt:.2f}")