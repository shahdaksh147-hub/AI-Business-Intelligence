import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv(
    "data/Sales Dataset.csv"
)

st.title("👥 Customer Analytics")

customer = (
    df.groupby("CustomerName")
    ["Amount"]
    .sum()
    .reset_index()
)

top = customer.sort_values(
    "Amount",
    ascending=False
).head(10)

fig = px.bar(
    top,
    x="CustomerName",
    y="Amount"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
