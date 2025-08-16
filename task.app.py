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

# Normalize property names (strip spaces, unify casing)
df[property_col] = df[property_col].astype(str).str.strip()

# Select property safely
properties = df[property_col].dropna().unique().tolist()
selected_property = st.selectbox("🏠 Select a Property", properties)

# Filter safely (avoid IndexError)
filtered = df[df[property_col] == selected_property]
if filtered.empty:
    st.error("⚠️ No data found for this property. Check the CSV formatting.")
    st.stop()

row = filtered.iloc[0]
