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

st.title("📋 Property Task Board")

# Normalize column names
df.columns = [c.strip() for c in df.columns]

# Pick property
property_col = "Property Name" if "Property Name" in df.columns else df.columns[0]
selected_property = st.selectbox("🏠 Select a Property", df[property_col].unique())

# Filter data
property_data = df[df[property_col] == selected_property].iloc[0]

# Show details
st.subheader("📌 Property Details")
st.write({
    "Transition Date": property_data.get("Transition Date", "N/A"),
    "Live Date": property_data.get("Live Date", "N/A")
})

# Show tasks
st.subheader("✅ Tasks Status")

done = property_data.get("Tasks", "")
pending = property_data.get("Pending Tasks", "")

if pd.notna(done) and str(done).strip():
    st.success(f"✅ Done: {done}")

if pd.notna(pending) and str(pending).strip():
    st.warning(f"⏳ Pending: {pending}")
