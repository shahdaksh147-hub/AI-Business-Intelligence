import streamlit as st

import pandas as pd

from utils.insights import AIInsights

from utils.reports import generate_report

st.set_page_config(layout="wide")

st.title("🤖 AI Business Insights")

df = pd.read_csv(
    "data/Sales Dataset.csv"
)

ai = AIInsights(df)

summary = ai.sales_summary()

state = ai.top_state()

category = ai.top_category()

loss = ai.loss_products()

tips = ai.recommendations()

c1,c2,c3 = st.columns(3)

c1.metric(
    "Sales",
    f"₹{summary['sales']:,.0f}"
)

c2.metric(
    "Profit",
    f"₹{summary['profit']:,.0f}"
)

c3.metric(
    "Orders",
    summary["orders"]
)

st.divider()

st.subheader("📈 Business Summary")

st.success(
    f"""
Top State : {state[0]}

Top Category : {category[0]}

Highest Sales : ₹{state[1]:,.0f}
"""
)

st.subheader("⚠ Loss Making Products")

st.dataframe(loss)

st.subheader("💡 AI Recommendations")

for i in tips:

    st.info(i)

if st.button("Generate PDF Report"):

    generate_report(
        summary,
        state,
        category,
        tips
    )

    st.success(
        "Business_Report.pdf Generated Successfully."
    )

st.divider()

if st.button("Generate Executive Insight"):

    st.markdown(
f"""

### Executive Summary

✅ Total Sales : ₹{summary['sales']:,.0f}

✅ Total Profit : ₹{summary['profit']:,.0f}

🏆 Best Performing State : **{state[0]}**

🏆 Best Category : **{category[0]}**

### Recommendations

✔ Increase inventory in high demand regions.

✔ Improve marketing for weak categories.

✔ Review loss-making products.

✔ Focus on customer retention.

✔ Forecast demand monthly.

"""
    )
