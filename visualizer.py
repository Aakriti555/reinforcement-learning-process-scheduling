# visualizer.py

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def plot_gantt_chart(gantt, title="Gantt Chart"):
    """
    gantt: list of tuples (pid, start_time, end_time)
    """
    fig, ax = plt.subplots(figsize=(10, 3))
    colors = plt.cm.tab20.colors  # up to 20 distinct colors

    for i, (pid, start, end) in enumerate(gantt):
        ax.barh(1, end - start, left=start, height=0.3, color=colors[pid % 20], edgecolor='black')
        ax.text(start + (end - start) / 2, 1, f"P{pid}", ha='center', va='center', color='white', fontsize=9)

    ax.set_ylim(0.5, 1.5)
    ax.set_xlabel("Time")
    ax.set_yticks([])
    ax.set_title(title)
    ax.grid(axis='x')

    plt.show()


def print_process_metrics(processes):
    print("\nProcess Metrics:")
    print("PID\tStart\tCompletion\tTurnaround\tWaiting")
    for p in processes:
        tat = p.completion - p.arrival
        wt = tat - p.burst
        print(f"P{p.pid}\t{p.start}\t{p.completion}\t\t{tat}\t\t{wt}")

    avg_tat = sum(p.completion - p.arrival for p in processes) / len(processes)
    avg_wt = sum((p.completion - p.arrival - p.burst) for p in processes) / len(processes)
    print(f"\nAverage Turnaround Time: {avg_tat:.2f}")
    print(f"Average Waiting Time: {avg_wt:.2f}")
