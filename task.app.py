import streamlit as st
import pandas as pd
import os

# Path to dataset
data_path = os.path.join("data", "tasks.csv")

# Load CSV
if os.path.exists(data_path):
    df = pd.read_csv(data_path)
else:
    st.error(f"❌ Could not find dataset at {data_path}")
    st.stop()

# Clean column names
df.columns = [c.strip() for c in df.columns]

# Identify key columns
property_col = "Property Name"
transition_col = "Transition Date"
live_col = "LIVE Date"
pending_col = "Pending Tasks"

# Task columns = anything with "Pre-Training"
task_cols = [c for c in df.columns if "Pre-Training" in c]

# UI
st.title("📋 Property Task Board")

# Select property
properties = df[property_col].dropna().unique()
selected_property = st.selectbox("🏠 Select a Property", properties)

# Filter property
row = df[df[property_col] == selected_property].iloc[0]

# Show details
st.subheader("📌 Property Details")
st.write({
    "Transition Date": row.get(transition_col, "N/A"),
    "LIVE Date": row.get(live_col, "N/A")
})

# Show completed tasks
st.subheader("✅ Completed Tasks")
for col in task_cols:
    task = str(row.get(col, "")).strip()
    if task:
        st.checkbox(task, value=True, key=f"done_{task}")

# Show pending tasks
st.subheader("⏳ Pending Tasks")
pending = str(row.get(pending_col, "")).split(",")
for task in pending:
    if task.strip():
        st.checkbox(task.strip(), value=False, key=f"pending_{task}")
