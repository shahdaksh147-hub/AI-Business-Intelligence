import streamlit as st
import pandas as pd
import os

from streamlit_option_menu import option_menu

from utils.file_loader import (
    get_available_datasets,
    load_dataset,
    load_uploaded_file
)

from utils.preprocess import clean_data

from config import *

# ====================================================
# PAGE CONFIG
# ====================================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================================================
# LOAD CSS
# ====================================================

if os.path.exists("assets/style.css"):
    with open("assets/style.css") as css:
        st.markdown(
            f"<style>{css.read()}</style>",
            unsafe_allow_html=True
        )

# ====================================================
# HEADER
# ====================================================

col1, col2 = st.columns([1,5])

with col1:

    if os.path.exists("assets/logo.png"):
        st.image("assets/logo.png", width=90)

with col2:

    st.title("🚀 AI Business Intelligence")

    st.caption(
        "Business Analytics • Forecasting • AI Insights"
    )

st.divider()

# ====================================================
# SIDEBAR
# ====================================================

st.sidebar.title("⚙ Data Source")

data_source = st.sidebar.radio(

    "Choose Dataset",

    [

        "Use Local Dataset",

        "Upload Dataset"

    ]

)

# ====================================================
# LOAD LOCAL DATASET
# ====================================================

if data_source == "Use Local Dataset":

    datasets = get_available_datasets()

    if len(datasets) == 0:

        st.error(
            "No dataset found inside data folder."
        )

        st.stop()

    selected_dataset = st.sidebar.selectbox(

        "Available Datasets",

        datasets

    )

    df = load_dataset(selected_dataset)

# ====================================================
# UPLOAD DATASET
# ====================================================

else:

    uploaded_file = st.sidebar.file_uploader(

        "Upload CSV / Excel / PDF",

        type=[

            "csv",

            "xlsx",

            "xls",

            "pdf"

        ]

    )

    if uploaded_file is None:

        st.info(
            "Upload a dataset to continue."
        )

        st.stop()

    df = load_uploaded_file(uploaded_file)

# ====================================================
# CLEAN DATA
# ====================================================

df = clean_data(df)

# ====================================================
# SAVE SESSION
# ====================================================

st.session_state["df"] = df

# ====================================================
# DATASET INFORMATION
# ====================================================

st.subheader("📁 Dataset Information")

c1,c2,c3,c4 = st.columns(4)

c1.metric(

    "Rows",

    df.shape[0]

)

c2.metric(

    "Columns",

    df.shape[1]

)

c3.metric(

    "Missing Values",

    df.isnull().sum().sum()

)

c4.metric(

    "Duplicate Rows",

    df.duplicated().sum()

)

st.divider()

# ====================================================
# DATA PREVIEW
# ====================================================

st.subheader("🔍 Dataset Preview")

st.dataframe(

    df.head(20),

    use_container_width=True,

    height=350

)

st.divider()

# ====================================================
# COLUMN INFORMATION
# ====================================================

with st.expander("📋 Dataset Details"):

    st.write("### Columns")

    st.write(df.columns.tolist())

    st.write("### Data Types")

    st.dataframe(df.dtypes.astype(str))

# ====================================================
# SIDEBAR NAVIGATION
# ====================================================

st.sidebar.divider()

selected = option_menu(

    menu_title="Navigation",

    options=[

        "Dashboard",

        "Sales Analysis",

        "Customer Analytics",

        "Forecasting",

        "AI Insights",

        "Reports"

    ],

    icons=[

        "speedometer2",

        "bar-chart-line",

        "people",

        "graph-up-arrow",

        "robot",

        "file-earmark-text"

    ],

    default_index=0

)

# ====================================================
# NAVIGATION MESSAGE
# ====================================================

st.success(
    f"Dataset Loaded Successfully : {df.shape[0]} rows × {df.shape[1]} columns"
)

st.info(
    """
Use the **Pages** section in the left sidebar to open:

📊 Dashboard

📈 Sales Analysis

👥 Customer Analytics

🔮 Forecasting

🤖 AI Insights

📄 Reports
"""
)

# ====================================================
# FOOTER
# ====================================================

st.divider()

st.caption(
    "AI Business Intelligence Platform | Version 1.0 | Developed by Daksh Shah"
)
