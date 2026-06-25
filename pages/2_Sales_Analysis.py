import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv(
    "data/Sales Dataset.csv"
)

st.title("📈 Sales Analysis")

state = st.selectbox(
    "Select State",
    df["State"].unique()
)

filtered = df[
    df["State"] == state
]

fig = px.bar(
    filtered.groupby("Category")
    ["Amount"]
    .sum()
    .reset_index(),
    x="Category",
    y="Amount"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
