"""
=========================================================
AI BUSINESS INTELLIGENCE PLATFORM

File Loader Utility

Supports

✓ CSV
✓ Excel
✓ PDF
✓ JSON
✓ Parquet

Author : Daksh Shah
=========================================================
"""

import os
import pandas as pd
import pdfplumber
import streamlit as st

# =====================================================
# FOLDERS
# =====================================================

DATA_FOLDER = "data"
UPLOAD_FOLDER = "uploads"

os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

SUPPORTED_FILES = (
    ".csv",
    ".xlsx",
    ".xls",
    ".pdf",
    ".json",
    ".parquet"
)

# =====================================================
# AVAILABLE DATASETS
# =====================================================

def get_available_datasets():

    datasets = []

    for file in os.listdir(DATA_FOLDER):

        if file.lower().endswith(SUPPORTED_FILES):

            datasets.append(file)

    datasets.sort()

    return datasets


# =====================================================
# LOAD LOCAL DATASET
# =====================================================

def load_dataset(filename):

    path = os.path.join(DATA_FOLDER, filename)

    return read_file(path)


# =====================================================
# LOAD UPLOADED DATASET
# =====================================================

def load_uploaded_file(uploaded_file):

    save_path = os.path.join(
        UPLOAD_FOLDER,
        uploaded_file.name
    )

    with open(save_path, "wb") as f:

        f.write(uploaded_file.getbuffer())

    return read_file(save_path)


# =====================================================
# READ FILE
# =====================================================

def read_file(path):

    extension = os.path.splitext(path)[1].lower()

    try:

        # ---------------- CSV ----------------

        if extension == ".csv":

            df = pd.read_csv(path)

        # ---------------- Excel ----------------

        elif extension in [".xlsx", ".xls"]:

            excel = pd.ExcelFile(path)

            sheets = excel.sheet_names

            if len(sheets) == 1:

                df = pd.read_excel(path)

            else:

                sheet = st.sidebar.selectbox(

                    "Select Excel Sheet",

                    sheets

                )

                df = pd.read_excel(

                    path,

                    sheet_name=sheet

                )

        # ---------------- JSON ----------------

        elif extension == ".json":

            df = pd.read_json(path)

        # ---------------- Parquet ----------------

        elif extension == ".parquet":

            df = pd.read_parquet(path)

        # ---------------- PDF ----------------

        elif extension == ".pdf":

            df = read_pdf(path)

        else:

            st.error("Unsupported File")

            return None

        df = preprocess(df)

        return df

    except Exception as e:

        st.error(f"Error : {e}")

        return None


# =====================================================
# READ PDF TABLE
# =====================================================

def read_pdf(path):

    tables = []

    with pdfplumber.open(path) as pdf:

        for page in pdf.pages:

            table = page.extract_table()

            if table:

                tables.extend(table)

    if len(tables) == 0:

        st.error("No Table Found In PDF")

        return pd.DataFrame()

    df = pd.DataFrame(

        tables[1:],

        columns=tables[0]

    )

    return df


# =====================================================
# PREPROCESS
# =====================================================

def preprocess(df):

    df.columns = df.columns.str.strip()

    df.drop_duplicates(inplace=True)

    df.reset_index(drop=True, inplace=True)

    # Remove Empty Rows

    df.dropna(

        how="all",

        inplace=True

    )

    # Fill Missing Values

    for col in df.columns:

        if df[col].dtype == "object":

            df[col].fillna("Unknown", inplace=True)

        else:

            df[col].fillna(

                df[col].median(),

                inplace=True

            )

    # Convert Dates

    for col in df.columns:

        if "date" in col.lower():

            try:

                df[col] = pd.to_datetime(df[col])

            except:

                pass

    return df


# =====================================================
# DATA PROFILE
# =====================================================

def dataset_profile(df):

    profile = {

        "Rows": df.shape[0],

        "Columns": df.shape[1],

        "Missing Values":

            df.isnull().sum().sum(),

        "Duplicate Rows":

            df.duplicated().sum(),

        "Memory (MB)":

            round(

                df.memory_usage(

                    deep=True

                ).sum()/1024**2,

                2

            )

    }

    return profile


# =====================================================
# COLUMN DETECTION
# =====================================================

def detect_columns(df):

    detected = {}

    keywords = {

        "date":["date"],

        "sales":[

            "sales",

            "amount",

            "revenue"

        ],

        "profit":[

            "profit"

        ],

        "quantity":[

            "qty",

            "quantity"

        ],

        "customer":[

            "customer"

        ],

        "product":[

            "product",

            "item"

        ],

        "category":[

            "category"

        ],

        "state":[

            "state",

            "city"

        ]

    }

    cols = [

        c.lower()

        for c in df.columns

    ]

    for key, values in keywords.items():

        detected[key] = None

        for value in values:

            for col in df.columns:

                if value in col.lower():

                    detected[key] = col

                    break

            if detected[key]:

                break

    return detected


# =====================================================
# EXPORT
# =====================================================

def export_csv(df):

    return df.to_csv(

        index=False

    ).encode("utf-8")


def export_excel(df):

    output = "reports/export.xlsx"

    df.to_excel(

        output,

        index=False

    )

    return output


# =====================================================
# SAMPLE DATASET
# =====================================================

def sample_dataset():

    return pd.DataFrame({

        "Date":[

            "2025-01-01",

            "2025-01-02"

        ],

        "Sales":[

            12000,

            15000

        ],

        "Profit":[

            2000,

            3200

        ]

    })
