import os
import pandas as pd
import pdfplumber

DATA_FOLDER = "data"


def get_available_datasets():

    files = []

    for file in os.listdir(DATA_FOLDER):

        if file.endswith((".csv", ".xlsx", ".xls", ".pdf")):
            files.append(file)

    return files


def load_dataset(filename):

    path = os.path.join(DATA_FOLDER, filename)

    if filename.endswith(".csv"):
        return pd.read_csv(path)

    elif filename.endswith((".xlsx", ".xls")):
        return pd.read_excel(path)

    elif filename.endswith(".pdf"):

        tables = []

        with pdfplumber.open(path) as pdf:

            for page in pdf.pages:

                table = page.extract_table()

                if table:
                    tables.extend(table)

        return pd.DataFrame(tables[1:], columns=tables[0])

    return None
