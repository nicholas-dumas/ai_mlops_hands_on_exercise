"""task 2: Data Visualization with Streamlit"""

import os

import pandas as pd
import streamlit as st

DATA_PATH = os.getenv("DATA_PATH", "data/bank-full.csv")

@st.cache_data
def load_data(path):
    """Load data from a CSV file."""
    df=pd.read_csv(path, sep=";")

    clean = df.copy()
    clean["contacted_before"] = clean["pdays"] != -1
    clean = clean[clean["previous"] != 275]
    clean["y"] = clean["y"] == "yes"
    clean = clean.drop(columns=["duration"])
    return clean

st.title("Bank Marketing Data Visualization")

clean = load_data(DATA_PATH)

# st.write("Clients", len(clean))
# st.write(f"Yes rate: {clean['y'].mean() * 100:.1f}%")
# st.dataframe(clean.head(10))

# Filters (sidebar)
st.sidebar.header("Filters")

mini_age, max_age = st.sidebar.slider("Age", 18, 95, (18,95))
jobs = sorted(clean["job"].unique())
selected_jobs = st.sidebar.multiselect("Job", jobs, default=jobs)
contact_choice = st.sidebar.radio("Previous contact", ["All clients", "Contacted before", "Never contacted"])

# Keep only the clients that match the filters
filtered = clean[
    (clean["age"] >= mini_age) &
    (clean["age"] <= max_age) &
    (clean["job"].isin(selected_jobs))
]

if contact_choice == "Contacted before":
    filtered = filtered[filtered["contacted_before"]]
elif contact_choice == "Never contacted":
    filtered = filtered[~filtered["contacted_before"]]

if filtered.empty:
    st.warning("No clients match the filters.")
    st.stop()

# key numbers
col1, col2, col3 = st.columns(3)
col1.metric("Clients selected", len(filtered))
col2.metric("Yes rate", f"{filtered['y'].mean() * 100:.1f}%")
col3.metric("Yes rate (all clients)", f"{clean['y'].mean() * 100:.1f}%")

st.dataframe(filtered.head(10))