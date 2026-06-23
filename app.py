import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="AI Business Intelligence",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 AI Powered Business Intelligence Platform")

st.markdown("""
### Features

✅ Dashboard

✅ Sales Analytics

✅ Customer Analytics

✅ Forecasting

✅ AI Insights
""")

selected = option_menu(
    menu_title=None,
    options=[
        "Dashboard",
        "Sales Analysis",
        "Customer Analytics",
        "Forecasting",
        "AI Insights"
    ],
    icons=[
        "speedometer",
        "bar-chart",
        "people",
        "graph-up",
        "robot"
    ],
    orientation="horizontal"
)
