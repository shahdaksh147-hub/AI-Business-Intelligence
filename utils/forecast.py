from prophet import Prophet
import pandas as pd

def sales_forecast(df):

    forecast_df = (
        df.groupby("Order Date")
        ["Amount"]
        .sum()
        .reset_index()
    )

    forecast_df.columns = ["ds", "y"]

    model = Prophet()

    model.fit(forecast_df)

    future = model.make_future_dataframe(
        periods=90
    )

    forecast = model.predict(future)

    return forecast
