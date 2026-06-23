import streamlit as st
from utils.preprocess import *
from utils.charts import *

df = load_data("data/Sales Dataset.csv")

df = clean_data(df)

sales, profit, qty, orders = get_kpis(df)

st.title("📊 Executive Dashboard")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Sales",
    f"₹{sales:,.0f}"
)

c2.metric(
    "Profit",
    f"₹{profit:,.0f}"
)

c3.metric(
    "Quantity",
    qty
)

c4.metric(
    "Orders",
    orders
)

st.plotly_chart(
    sales_by_category(df),
    use_container_width=True
)

st.plotly_chart(
    profit_by_state(df),
    use_container_width=True
)
