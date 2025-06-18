import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def plot_gantt_chart(gantt, title="Gantt Chart", ax=None, fig=None):
    """
    gantt: list of tuples (pid, start_time, end_time)
    Optional ax, fig: for compatibility with Streamlit's st.pyplot(fig)
    """
    external_call = ax is not None and fig is not None

    if not external_call:
        fig, ax = plt.subplots(figsize=(10, 3))

    colors = plt.cm.tab20.colors  # Up to 20 distinct colors

    for i, (pid, start, end) in enumerate(gantt):
        ax.barh(1, end - start, left=start, height=0.3, color=colors[pid % 20], edgecolor='black')
        ax.text(start + (end - start) / 2, 1, f"P{pid}", ha='center', va='center', color='white', fontsize=5)

    ax.set_ylim(0.5, 1.5)
    ax.set_xlabel("Time")
    ax.set_yticks([])
    ax.set_title(title)
    ax.grid(axis='x')

    if not external_call:
        plt.show()
