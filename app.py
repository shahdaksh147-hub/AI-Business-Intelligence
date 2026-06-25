import streamlit as st

from streamlit_option_menu import option_menu

from utils.file_loader import load_file

from config import *

st.set_page_config(

    page_title=APP_NAME,

    page_icon=APP_ICON,

    layout="wide",

    initial_sidebar_state="expanded"

)

# ---------------------

# CSS

# ---------------------

with open("assets/style.css") as f:

    st.markdown(

        f"<style>{f.read()}</style>",

        unsafe_allow_html=True

    )

# ---------------------

# Title

# ---------------------

st.title("🚀 AI Business Intelligence Platform")

st.caption("Upload any Business Dataset")

# ---------------------

# Upload

# ---------------------

uploaded = st.sidebar.file_uploader(

    "Upload Dataset",

    type=[

        "csv",

        "xlsx",

        "xls",

        "pdf"

    ]

)

if uploaded:

    df = load_file(uploaded)

    st.session_state["df"] = df

    st.success("Dataset Loaded Successfully")

else:

    st.warning("Upload a dataset to continue.")

    st.stop()

# ---------------------

# Sidebar

# ---------------------

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

        "speedometer",

        "bar-chart",

        "people",

        "graph-up",

        "robot",

        "file-earmark"

    ],

    default_index=0

)

st.info(

    "Use the Pages menu on the left to navigate."

)
