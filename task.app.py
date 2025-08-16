import streamlit as st
import pandas as pd
import os

# Path to dataset
data_path = os.path.join("data", "tasks.csv")

# Load CSV (auto-detect delimiter)
if os.path.exists(data_path):
    df = pd.read_csv(data_path, sep=None, engine="python")
else:
    st.error(f"❌ Could not find dataset at {data_path}")
    st.stop()

# Clean column names
df.columns = [c.strip() for c in df.columns]

# Ensure we have a property column
property_col = None
for col in df.columns:
    if "property" in col.lower():
        property_col = col
        break

if property_col is None:
    st.error("❌ No 'Property Name' column found in CSV")
    st.stop()

# Drop empty rows
df = df.dropna(subset=[property_col])

# UI
st.title("📋 Property Task Board")

# Select a property
properties = sorted(df[property_col].dropna().astype(str).str.strip().unique())
selected_property = st.selectbox("🏠 Select a Property", properties)

# Filter data for selected property
property_data = df[df[property_col].astype(str).str.strip() == selected_property]

if property_data.empty:
    st.warning("⚠️ No data found for this property.")
    st.stop()

row = property_data.iloc[0]

# Show details
st.subheader("📌 Property Details")
st.write({
    "Transition Date": row.get("Transition Date", "N/A"),
    "Live Date": row.get("Live Date", "N/A")
})

# Show tasks
st.subheader("✅ Task Status")

done_tasks = str(row.get("Tasks", "")).split(",")
pending_tasks = str(row.get("Pending Tasks", "")).split(",")

if done_tasks and done_tasks[0].strip():
    st.markdown("### ✅ Completed")
    for task in done_tasks:
        st.checkbox(task.strip(), value=True, key=f"done_{task}")

if pending_tasks and pending_tasks[0].strip():
    st.markdown("### ⏳ Pending")
    for task in pending_tasks:
        st.checkbox(task.strip(), value=False, key=f"pending_{task}")
