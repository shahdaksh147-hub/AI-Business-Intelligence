import pandas as pd

def load_data(path):

    df = pd.read_csv(path)

    df.columns = df.columns.str.strip()

    return df


def clean_data(df):

    df.drop_duplicates(inplace=True)

    df.fillna(0, inplace=True)

    return df


def get_kpis(df):

    total_sales = df["Amount"].sum()

    total_profit = df["Profit"].sum()

    total_quantity = df["Quantity"].sum()

    total_orders = df["Order ID"].nunique()

    return (
        total_sales,
        total_profit,
        total_quantity,
        total_orders
    )
