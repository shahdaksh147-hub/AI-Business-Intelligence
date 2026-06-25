import streamlit as st
import pandas as pd
import plotly.express as px

from utils.file_loader import detect_columns

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

# ----------------------------------------------------
# LOAD DATA
# ----------------------------------------------------

if "df" not in st.session_state:
    st.error("No dataset loaded.")
    st.stop()

df = st.session_state["df"].copy()

st.title("📊 Executive Dashboard")

# ----------------------------------------------------
# COLUMN DETECTION
# ----------------------------------------------------

columns = detect_columns(df)

sales_col = columns.get("sales")
profit_col = columns.get("profit")
date_col = columns.get("date")
category_col = columns.get("category")
customer_col = columns.get("customer")
state_col = columns.get("state")
product_col = columns.get("product")
quantity_col = columns.get("quantity")

# ----------------------------------------------------
# DATE CONVERSION
# ----------------------------------------------------

if date_col:

    df[date_col] = pd.to_datetime(
        df[date_col],
        errors="coerce"
    )

# ----------------------------------------------------
# SIDEBAR FILTERS
# ----------------------------------------------------

st.sidebar.header("Filters")

filtered_df = df.copy()

if category_col:

    category = st.sidebar.multiselect(
        "Category",
        sorted(df[category_col].dropna().unique()),
        default=sorted(df[category_col].dropna().unique())
    )

    filtered_df = filtered_df[
        filtered_df[category_col].isin(category)
    ]

if state_col:

    state = st.sidebar.multiselect(
        "State",
        sorted(filtered_df[state_col].dropna().unique()),
        default=sorted(filtered_df[state_col].dropna().unique())
    )

    filtered_df = filtered_df[
        filtered_df[state_col].isin(state)
    ]

if product_col:

    product = st.sidebar.multiselect(
        "Product",
        sorted(filtered_df[product_col].dropna().unique()),
        default=sorted(filtered_df[product_col].dropna().unique())
    )

    filtered_df = filtered_df[
        filtered_df[product_col].isin(product)
    ]

if date_col:

    start = filtered_df[date_col].min()
    end = filtered_df[date_col].max()

    date_range = st.sidebar.date_input(
        "Date Range",
        [start, end]
    )

    if len(date_range) == 2:

        filtered_df = filtered_df[
            (filtered_df[date_col] >= pd.to_datetime(date_range[0])) &
            (filtered_df[date_col] <= pd.to_datetime(date_range[1]))
        ]

# ----------------------------------------------------
# KPI CALCULATIONS
# ----------------------------------------------------

total_sales = (
    filtered_df[sales_col].sum()
    if sales_col else 0
)

total_profit = (
    filtered_df[profit_col].sum()
    if profit_col else 0
)

total_orders = len(filtered_df)

total_customers = (
    filtered_df[customer_col].nunique()
    if customer_col else 0
)

profit_margin = (
    (total_profit / total_sales) * 100
    if total_sales else 0
)

# ----------------------------------------------------
# KPI CARDS
# ----------------------------------------------------

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "💰 Sales",
    f"₹{total_sales:,.0f}"
)

c2.metric(
    "📈 Profit",
    f"₹{total_profit:,.0f}"
)

c3.metric(
    "🧾 Orders",
    total_orders
)

c4.metric(
    "👥 Customers",
    total_customers
)

c5.metric(
    "📊 Profit %",
    f"{profit_margin:.2f}%"
)

st.divider()
# ===========================================================
# SALES TREND
# ===========================================================

if date_col and sales_col:

    st.subheader("📈 Sales Trend")

    trend = (
        filtered_df
        .groupby(date_col)[sales_col]
        .sum()
        .reset_index()
    )

    fig = px.line(
        trend,
        x=date_col,
        y=sales_col,
        markers=True,
        title="Daily Sales Trend"
    )

    fig.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ===========================================================
# CATEGORY & STATE
# ===========================================================

col1, col2 = st.columns(2)

with col1:

    if category_col and sales_col:

        st.subheader("📊 Sales by Category")

        cat = (
            filtered_df
            .groupby(category_col)[sales_col]
            .sum()
            .reset_index()
        )

        fig = px.bar(

            cat,

            x=category_col,

            y=sales_col,

            text_auto=True,

            color=sales_col

        )

        fig.update_layout(
            template="plotly_dark",
            height=450
        )

        st.plotly_chart(fig, use_container_width=True)

with col2:

    if state_col and sales_col:

        st.subheader("🌍 Sales by State")

        state = (

            filtered_df

            .groupby(state_col)[sales_col]

            .sum()

            .reset_index()

        )

        fig = px.bar(

            state,

            x=state_col,

            y=sales_col,

            color=sales_col,

            text_auto=True

        )

        fig.update_layout(

            template="plotly_dark",

            height=450

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

# ===========================================================
# TOP PRODUCTS
# ===========================================================

if product_col and sales_col:

    st.subheader("🏆 Top Selling Products")

    top_products = (

        filtered_df

        .groupby(product_col)[sales_col]

        .sum()

        .sort_values(

            ascending=False

        )

        .head(10)

        .reset_index()

    )

    fig = px.bar(

        top_products,

        x=sales_col,

        y=product_col,

        orientation="h",

        color=sales_col,

        text_auto=True

    )

    fig.update_layout(

        template="plotly_dark",

        height=500

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# ===========================================================
# TOP CUSTOMERS
# ===========================================================

if customer_col and sales_col:

    st.subheader("👥 Top Customers")

    customers = (

        filtered_df

        .groupby(customer_col)[sales_col]

        .sum()

        .sort_values(

            ascending=False

        )

        .head(10)

        .reset_index()

    )

    fig = px.bar(

        customers,

        x=sales_col,

        y=customer_col,

        orientation="h",

        color=sales_col,

        text_auto=True

    )

    fig.update_layout(

        template="plotly_dark",

        height=500

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# ===========================================================
# PIE CHART
# ===========================================================

if category_col and sales_col:

    col1,col2 = st.columns(2)

    with col1:

        st.subheader("🥧 Revenue Distribution")

        fig = px.pie(

            filtered_df,

            names=category_col,

            values=sales_col,

            hole=.45

        )

        fig.update_layout(

            template="plotly_dark"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    with col2:

        if profit_col:

            st.subheader("💰 Profit Distribution")

            fig = px.pie(

                filtered_df,

                names=category_col,

                values=profit_col,

                hole=.45

            )

            fig.update_layout(

                template="plotly_dark"

            )

            st.plotly_chart(

                fig,

                use_container_width=True

            )

# ===========================================================
# TREEMAP
# ===========================================================

if category_col and product_col and sales_col:

    st.subheader("🌳 Product Hierarchy")

    fig = px.treemap(

        filtered_df,

        path=[category_col,product_col],

        values=sales_col,

        color=sales_col

    )

    fig.update_layout(

        template="plotly_dark",

        height=650

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )
    # ===========================================================
# MONTHLY SALES
# ===========================================================

if date_col and sales_col:

    st.subheader("📅 Monthly Sales")

    monthly = filtered_df.copy()

    monthly["Month"] = monthly[date_col].dt.to_period("M").astype(str)

    monthly_sales = (
        monthly.groupby("Month")[sales_col]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        monthly_sales,
        x="Month",
        y=sales_col,
        color=sales_col,
        text_auto=True
    )

    fig.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

# ===========================================================
# MONTHLY PROFIT
# ===========================================================

if date_col and profit_col:

    st.subheader("💰 Monthly Profit")

    monthly = filtered_df.copy()

    monthly["Month"] = monthly[date_col].dt.to_period("M").astype(str)

    monthly_profit = (
        monthly.groupby("Month")[profit_col]
        .sum()
        .reset_index()
    )

    fig = px.line(
        monthly_profit,
        x="Month",
        y=profit_col,
        markers=True
    )

    fig.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)
    st.subheader("📊 Correlation Matrix")

numeric = filtered_df.select_dtypes(include="number")

if numeric.shape[1] > 1:

    corr = numeric.corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Viridis"
    )

    fig.update_layout(
        template="plotly_dark",
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)
    if sales_col and profit_col:

    st.subheader("📈 Sales vs Profit")

    fig = px.scatter(

        filtered_df,

        x=sales_col,

        y=profit_col,

        color=category_col if category_col else None,

        hover_data=filtered_df.columns

    )

    fig.update_layout(

        template="plotly_dark",

        height=600

    )

    st.plotly_chart(fig,use_container_width=True)
    if sales_col:

    st.subheader("Sales Distribution")

    fig = px.histogram(

        filtered_df,

        x=sales_col,

        nbins=30

    )

    fig.update_layout(

        template="plotly_dark"

    )

    st.plotly_chart(fig,use_container_width=True)
    if sales_col and category_col:

    st.subheader("Sales Distribution by Category")

    fig = px.box(

        filtered_df,

        x=category_col,

        y=sales_col,

        color=category_col

    )

    fig.update_layout(

        template="plotly_dark"

    )

    st.plotly_chart(fig,use_container_width=True)
    if product_col and profit_col:

    st.subheader("🏆 Top Profitable Products")

    profit = (

        filtered_df

        .groupby(product_col)[profit_col]

        .sum()

        .sort_values(

            ascending=False

        )

        .head(10)

        .reset_index()

    )

    fig = px.bar(

        profit,

        x=profit_col,

        y=product_col,

        orientation="h",

        color=profit_col,

        text_auto=True

    )

    fig.update_layout(

        template="plotly_dark",

        height=500

    )

    st.plotly_chart(fig,use_container_width=True)
    st.subheader("🧠 Executive Summary")

summary = f"""

Total Sales : ₹{total_sales:,.0f}

Total Profit : ₹{total_profit:,.0f}

Orders : {total_orders}

Customers : {total_customers}

Profit Margin : {profit_margin:.2f}%

"""

st.success(summary)
st.subheader("🤖 AI Recommendations")

if profit_margin > 20:

    st.success("Excellent profitability. Consider expanding operations.")

elif profit_margin > 10:

    st.info("Business is performing well. Focus on customer growth.")

else:

    st.warning("Profit margin is low. Reduce costs or improve pricing.")

if sales_col and profit_col:

    if total_profit < 0:

        st.error("Business is operating at a loss.")

if customer_col:

    if total_customers < 100:

        st.warning("Customer base is small. Increase marketing efforts.")

else:

    st.success("Customer base looks healthy.")
    csv = filtered_df.to_csv(index=False)

st.download_button(

    "📥 Download Dashboard Data",

    csv,

    "dashboard.csv",

    "text/csv"

)

# ----------------------------------------------------
# DATA PREVIEW
# ----------------------------------------------------

st.subheader("Dataset Preview")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=400
)

st.divider()

# ----------------------------------------------------
# QUICK SUMMARY
# ----------------------------------------------------

left, right = st.columns([2, 1])

with left:

    st.subheader("Dataset Information")

    st.write(f"Rows: {filtered_df.shape[0]}")
    st.write(f"Columns: {filtered_df.shape[1]}")
    st.write(f"Missing Values: {filtered_df.isnull().sum().sum()}")
    st.write(f"Duplicate Rows: {filtered_df.duplicated().sum()}")

with right:

    st.subheader("Detected Fields")

    st.write(columns)
    
