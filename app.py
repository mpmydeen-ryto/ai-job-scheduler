import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- TITLE ----------------
st.title("🤖 AI-Based Job Scheduler")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

# ---------------- LOAD DATA ----------------
try:
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_csv("dataset.csv")
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# ---------------- VALIDATION ----------------
required_columns = ["job_id", "arrival_time", "burst_time", "priority"]

missing = [col for col in required_columns if col not in df.columns]
if missing:
    st.error(f"Missing columns: {missing}")
    st.stop()

# ---------------- SHOW INPUT ----------------
st.subheader("📊 Input Data")
st.write(df)

# ---------------- FCFS SCHEDULING ----------------
df = df.sort_values(by="arrival_time").reset_index(drop=True)

waiting_time = []
current_time = 0

for i in range(len(df)):
    arrival = df.loc[i, "arrival_time"]
    burst = df.loc[i, "burst_time"]

    if current_time < arrival:
        current_time = arrival

    wt = current_time - arrival
    waiting_time.append(wt)

    current_time += burst

df["waiting_time"] = waiting_time

# ---------------- OUTPUT ----------------
st.subheader("⚙️ FCFS Scheduling Output")
st.write(df)

# ---------------- GANTT CHART ----------------
st.subheader("📈 Gantt Chart")

fig, ax = plt.subplots()

current_time = 0

for i in range(len(df)):
    arrival = df.loc[i, "arrival_time"]
    burst = df.loc[i, "burst_time"]
    job_id = df.loc[i, "job_id"]

    if current_time < arrival:
        current_time = arrival

    ax.barh(0, burst, left=current_time)
    ax.text(current_time + burst / 2, 0, f"Job {job_id}",
            ha='center', va='center', color='white')

    current_time += burst

ax.set_xlabel("Time")
ax.set_yticks([])
ax.set_title("FCFS Gantt Chart")

st.pyplot(fig)