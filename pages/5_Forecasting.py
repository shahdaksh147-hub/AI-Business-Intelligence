import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from prophet import Prophet

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestRegressor

import numpy as np

st.set_page_config(
    page_title="Sales Forecasting",
    layout="wide"
)

st.title("🔮 AI Sales Forecasting")

# ------------------------------
# Load Dataset
# ------------------------------

df = pd.read_csv("data/Sales Dataset.csv")

# ------------------------------
# Date Conversion
# ------------------------------

df["Order Date"] = pd.to_datetime(df["Order Date"])

daily_sales = (
    df.groupby("Order Date")["Amount"]
    .sum()
    .reset_index()
)

daily_sales.columns = ["ds", "y"]

# ------------------------------
# Sidebar
# ------------------------------

forecast_days = st.sidebar.slider(
    "Forecast Days",
    30,
    180,
    90
)

model_option = st.sidebar.selectbox(
    "Prediction Model",
    [
        "Prophet",
        "Random Forest"
    ]
)

# =====================================
# Prophet Forecast
# =====================================

if model_option == "Prophet":

    st.subheader("📈 Prophet Forecast")

    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False
    )

    model.fit(daily_sales)

    future = model.make_future_dataframe(
        periods=forecast_days
    )

    forecast = model.predict(future)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=daily_sales["ds"],
            y=daily_sales["y"],
            mode="lines",
            name="Actual"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast["ds"],
            y=forecast["yhat"],
            mode="lines",
            name="Forecast"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Forecast Table")

    st.dataframe(
        forecast[
            [
                "ds",
                "yhat",
                "yhat_lower",
                "yhat_upper"
            ]
        ].tail(forecast_days)
    )

    csv = forecast.to_csv(index=False)

    st.download_button(
        "📥 Download Forecast",
        csv,
        "forecast.csv",
        "text/csv"
    )

# =====================================
# Random Forest Forecast
# =====================================

else:

    st.subheader("🤖 Machine Learning Prediction")

    rf = daily_sales.copy()

    rf["day"] = rf["ds"].dt.day

    rf["month"] = rf["ds"].dt.month

    rf["year"] = rf["ds"].dt.year

    rf["weekday"] = rf["ds"].dt.weekday

    X = rf[
        [
            "day",
            "month",
            "year",
            "weekday"
        ]
    ]

    y = rf["y"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=300,
        random_state=42
    )

    model.fit(
        X_train,
        y_train
    )

    prediction = model.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        prediction
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            prediction
        )
    )

    c1, c2 = st.columns(2)

    c1.metric(
        "MAE",
        round(mae,2)
    )

    c2.metric(
        "RMSE",
        round(rmse,2)
    )

    result = X_test.copy()

    result["Actual"] = y_test.values

    result["Predicted"] = prediction

    fig = px.scatter(
        result,
        x="Actual",
        y="Predicted",
        trendline="ols",
        title="Actual vs Predicted Sales"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Prediction Table")

    st.dataframe(
        result.head(20)
    )

# =====================================
# Business Forecast
# =====================================

st.divider()

st.subheader("📊 Forecast Summary")

latest_sales = daily_sales["y"].iloc[-1]

future_sales = forecast["yhat"].iloc[-1] if model_option=="Prophet" else prediction.mean()

growth = (
    (
        future_sales
        -
        latest_sales
    )
    /
    latest_sales
)*100

if growth > 0:

    st.success(
        f"""
Expected Growth

📈 {growth:.2f}% increase

Estimated Future Sales

₹ {future_sales:,.0f}
"""
    )

else:

    st.error(
        f"""
Expected Decline

📉 {abs(growth):.2f}% decrease
"""
    )

# =====================================
# Recommendation
# =====================================

st.subheader("💡 AI Recommendation")

if growth > 15:

    st.info("""
Increase Inventory.

Demand is expected to rise significantly.
""")

elif growth > 5:

    st.info("""
Maintain current inventory.

Business growth is stable.
""")

else:

    st.warning("""
Reduce unnecessary stock.

Focus on marketing campaigns.
""")
