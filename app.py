import streamlit as st
import pandas as pd

st.title("AI-Based Job Scheduler")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Input Data")
    st.write(df)

    df = df.sort_values(by="arrival_time")
    waiting_time = []
    total_time = 0

    for i in range(len(df)):
        if i == 0:
            waiting_time.append(0)
            total_time = df.iloc[i]["burst_time"]
        else:
            wt = total_time - df.iloc[i]["arrival_time"]
            waiting_time.append(max(wt, 0))
            total_time += df.iloc[i]["burst_time"]

    df["waiting_time"] = waiting_time

    st.subheader("FCFS Scheduling Output")
    st.write(df)
import matplotlib.pyplot as plt

st.subheader("Gantt Chart")

start_time = 0
fig, ax = plt.subplots()

for i in range(len(df)):
    burst = df.iloc[i]["burst_time"]
    ax.barh(0, burst, left=start_time)
    ax.text(start_time + burst/2, 0, f"Job {df.iloc[i]['job_id']}", 
            ha='center', va='center', color='white')
    start_time += burst

ax.set_xlabel("Time")
ax.set_yticks([])
ax.set_title("FCFS Gantt Chart")

st.pyplot(fig)