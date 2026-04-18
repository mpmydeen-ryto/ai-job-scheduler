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