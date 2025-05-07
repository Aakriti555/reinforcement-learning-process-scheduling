import matplotlib.pyplot as plt

# FCFS Scheduling Algorithm with Gantt Chart
def fcfs(process_list):
    t = 0
    completed = {}
    timeline = []  # To store (pid, start_time, end_time)

    process_list.sort()
    while process_list:
        if process_list[0][0] > t:
            # CPU is Idle
            idle_start = t
            t = process_list[0][0]
            timeline.append(("Idle", idle_start, t))
        else:
            process = process_list.pop(0)
            pid = process[2]
            arrival = process[0]
            burst = process[1]
            start_time = t
            t += burst
            end_time = t
            timeline.append((pid, start_time, end_time))
            ct = end_time
            tt = ct - arrival
            wt = tt - burst
            completed[pid] = [ct, tt, wt]

    print("Completed times (CT, TT, WT):", completed)
    draw_gantt_chart(timeline)

# Function to draw Gantt Chart
def draw_gantt_chart(timeline):
    fig, ax = plt.subplots(figsize=(10, 2))

    colors = {
        "Idle": "gray",
    }

    for i, (pid, start, end) in enumerate(timeline):
        color = colors.get(pid, None)  # Gray for Idle, random for others
        ax.barh(0, end - start, left=start, height=0.3, align='center',
                edgecolor='black', label=pid if pid != "Idle" else "", color=color)
        ax.text((start + end) / 2, 0, pid, ha='center', va='center',
                color='white' if pid != "Idle" else 'black', fontsize=10, fontweight='bold')

    ax.set_xlim(0, max(end for _, _, end in timeline) + 1)
    ax.set_xlabel('Time')
    ax.set_yticks([])
    ax.set_title('FCFS Gantt Chart')
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)

    plt.show()

# Run
if __name__ == "__main__":
    process_list = [[2, 6, "p1"], [5, 2, "p2"], [1, 8, "p3"], [0, 3, "p4"], [4, 4, "p5"]]
    fcfs(process_list)
