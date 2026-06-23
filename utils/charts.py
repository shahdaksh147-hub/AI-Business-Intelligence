import plotly.express as px

def sales_by_category(df):

    category = (
        df.groupby("Category")
        ["Amount"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        category,
        x="Category",
        y="Amount",
        title="Sales by Category"
    )

    return fig


def profit_by_state(df):

    state = (
        df.groupby("State")
        ["Profit"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        state,
        x="State",
        y="Profit",
        title="Profit by State"
    )

    return fig


def monthly_sales(df):

    sales = (
        df.groupby("Month")
        ["Amount"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        sales,
        x="Month",
        y="Amount",
        markers=True,
        title="Monthly Sales"
    )

    return fig
