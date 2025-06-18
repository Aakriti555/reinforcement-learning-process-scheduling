import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
from process import Process
from scheduler.fcfs import fcfs
from scheduler.sjf import sjf
from scheduler.round_robin import round_robin
from scheduler.priority import priority_scheduling
from scheduler.rl_scheduler import RLScheduler
from utils import calculate_metrics
from visualizer import plot_gantt_chart
import io

def parse_process_df(df):
    return [
        Process(
            pid=int(row['pid']),
            arrival=int(row['arrival']),
            burst=int(row['burst']),
            priority=int(row.get('priority', 0))
        ) for _, row in df.iterrows()
    ]

def display_metrics_table(processes):
    table = []
    for p in processes:
        tat = p.completion - p.arrival
        wt = tat - p.burst
        table.append({
            'PID': p.pid,
            'Arrival': p.arrival,
            'Burst': p.burst,
            'Priority': p.priority,
            'Completion': p.completion,
            'Turnaround': tat,
            'Waiting': wt
        })
    df = pd.DataFrame(table)
    st.write("### First 5 Records")
    st.dataframe(df.head())
    st.write("### Summary of Last 5 Records")
    st.dataframe(df.tail())
    return calculate_metrics(processes)

def run_algorithm(algorithm, processes, quantum=2):
    if algorithm == "FCFS":
        return fcfs(processes)
    elif algorithm == "SJF":
        return sjf(processes)
    elif algorithm == "Round Robin":
        return round_robin(processes, quantum=quantum)
    elif algorithm == "Priority":
        return priority_scheduling(processes)
    elif algorithm == "Reinforcement Learning":
        rl = RLScheduler(processes)
        rl.train()
        return rl.schedule()
    else:
        raise ValueError("Unsupported Algorithm")

def generate_random_dataset(n=100):
    data = []
    for i in range(1, n + 1):
        arrival = random.randint(0, 50)
        burst = random.randint(1, 20)
        priority = random.randint(1, 10)
        data.append({'pid': i, 'arrival': arrival, 'burst': burst, 'priority': priority})
    return pd.DataFrame(data)

st.title("Process Scheduling Simulator")

st.sidebar.header("Input Options")
input_method = st.sidebar.radio("Select input method", ["Upload CSV", "Manual Entry", "Generate Random Dataset"])

df = None
if input_method == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader("Upload process dataset CSV", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("CSV Loaded Successfully!")
elif input_method == "Generate Random Dataset":
    count = st.sidebar.slider("Number of Processes", 10, 100, 50)
    df = generate_random_dataset(count)
    st.success("Random Dataset Generated!")
else:
    st.sidebar.write("Enter Process Data:")
    num_procs = st.sidebar.number_input("Number of Processes", 1, 20, 4)
    input_data = []
    for i in range(num_procs):
        st.sidebar.write(f"Process {i+1}")
        arrival = st.sidebar.number_input(f"Arrival Time (P{i+1})", 0, 100, 0, key=f"a{i}")
        burst = st.sidebar.number_input(f"Burst Time (P{i+1})", 1, 100, 1, key=f"b{i}")
        priority = st.sidebar.number_input(f"Priority (P{i+1})", 0, 100, 0, key=f"p{i}")
        input_data.append({'pid': i+1, 'arrival': arrival, 'burst': burst, 'priority': priority})
    df = pd.DataFrame(input_data)

algorithm_options = ["FCFS", "SJF", "Round Robin", "Priority", "Reinforcement Learning"]
mode = st.radio("Choose Simulation Mode", ["Single Algorithm", "Compare All Algorithms"])

if df is not None and not df.empty:
    processes = parse_process_df(df)
    if mode == "Single Algorithm":
        selected_algo = st.selectbox("Select Scheduling Algorithm", algorithm_options)
        quantum = 2
        if selected_algo == "Round Robin":
            quantum = st.slider("Quantum Time", 1, 10, 2)
        scheduled, gantt = run_algorithm(selected_algo, processes, quantum)
        avg_tat, avg_wt = display_metrics_table(scheduled)
        st.write(f"**{selected_algo} - Average Turnaround Time:** {avg_tat:.2f}")
        st.write(f"**{selected_algo} - Average Waiting Time:** {avg_wt:.2f}")

        if len(gantt) <= 20:
            st.write("### Gantt Chart")
            fig, ax = plt.subplots()
            plot_gantt_chart(gantt, title=f"Gantt Chart - {selected_algo}", ax=ax, fig=fig)
            st.pyplot(fig)
        else:
            st.info("Gantt chart is only shown for 20 or fewer processes to maintain clarity.")
    else:
        result_data = []
        for algo in algorithm_options:
            proc_copy = parse_process_df(df)
            if algo == "Round Robin":
                scheduled, _ = run_algorithm(algo, proc_copy, quantum=2)
            else:
                scheduled, _ = run_algorithm(algo, proc_copy)
            avg_tat, avg_wt = calculate_metrics(scheduled)
            result_data.append({"Algorithm": algo, "Avg TAT": avg_tat, "Avg WT": avg_wt})
        result_df = pd.DataFrame(result_data)
        st.dataframe(result_df)

        # Plot comparison
        st.write("### Algorithm Comparison")
        fig, ax = plt.subplots()
        result_df.set_index("Algorithm")[['Avg TAT', 'Avg WT']].plot(kind='bar', ax=ax)
        ax.set_ylabel("Time")
        ax.set_title("Comparison of Scheduling Algorithms")
        st.pyplot(fig)
else:
    st.warning("Please upload a valid CSV file, enter data manually, or generate a dataset.")
