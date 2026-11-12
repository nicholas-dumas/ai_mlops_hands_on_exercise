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

st.write("Clients", len(clean))
st.write(f"Yes rate: {clean['y'].mean() * 100:.1f}%")
st.dataframe(clean.head(10))