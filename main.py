# main.py

import pandas as pd
from process import Process
from scheduler.fcfs import fcfs
from scheduler.sjf import sjf
from scheduler.round_robin import round_robin
from scheduler.priority import priority_scheduling
from scheduler.rl_scheduler import RLScheduler
from visualizer import plot_gantt_chart, print_process_metrics


def load_processes_from_csv(file_path):
    df = pd.read_csv(file_path)
    processes = [
        Process(
            pid=int(row['pid']),
            arrival=int(row['arrival']),
            burst=int(row['burst']),
            priority=int(row['priority'])
        )
        for _, row in df.iterrows()
    ]
    return processes


def main():
    print("Select Scheduling Algorithm:")
    print("1. FCFS")
    print("2. SJF")
    print("3. Round Robin")
    print("4. Priority")
    print("5. Reinforcement Learning")

    choice = int(input("Enter choice number: "))
    processes = load_processes_from_csv("data/rl_process_dataset_100.csv")

    if choice == 1:
        scheduled, gantt = fcfs(processes)
    elif choice == 2:
        scheduled, gantt = sjf(processes)
    elif choice == 3:
        quantum = int(input("Enter quantum time for Round Robin: "))
        scheduled, gantt = round_robin(processes, quantum=quantum)
    elif choice == 4:
        scheduled, gantt = priority_scheduling(processes)
    elif choice == 5:
        rl = RLScheduler(processes)
        print("Training RL Scheduler...")
        rl.train()
        scheduled, gantt = rl.schedule()
    else:
        print("Invalid choice")
        return

    print_process_metrics(scheduled)
    plot_gantt_chart(gantt, title=f"Scheduling Algorithm: {['FCFS', 'SJF', 'RR', 'Priority', 'RL'][choice-1]}")


if __name__ == "__main__":
    main()
