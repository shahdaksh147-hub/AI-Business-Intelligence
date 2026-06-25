import pandas as pd

class AIInsights:

    def __init__(self, df):
        self.df = df

    def sales_summary(self):

        total_sales = self.df["Amount"].sum()

        total_profit = self.df["Profit"].sum()

        total_orders = self.df["Order ID"].nunique()

        return {
            "sales": total_sales,
            "profit": total_profit,
            "orders": total_orders
        }

    def top_state(self):

        state = (
            self.df.groupby("State")["Amount"]
            .sum()
            .sort_values(ascending=False)
        )

        return state.index[0], state.iloc[0]

    def top_category(self):

        cat = (
            self.df.groupby("Category")["Amount"]
            .sum()
            .sort_values(ascending=False)
        )

        return cat.index[0], cat.iloc[0]

    def lowest_category(self):

        cat = (
            self.df.groupby("Category")["Amount"]
            .sum()
            .sort_values()
        )

        return cat.index[0], cat.iloc[0]

    def highest_profit_product(self):

        product = (
            self.df.groupby("Sub-Category")["Profit"]
            .sum()
            .sort_values(ascending=False)
        )

        return product.index[0], product.iloc[0]

    def loss_products(self):

        loss = (
            self.df.groupby("Sub-Category")["Profit"]
            .sum()
        )

        loss = loss[loss < 0]

        return loss

    def recommendations(self):

        tips = []

        top_state, _ = self.top_state()

        top_category, _ = self.top_category()

        low_category, _ = self.lowest_category()

        tips.append(
            f"Increase marketing in {top_state}."
        )

        tips.append(
            f"Invest more inventory in {top_category}."
        )

        tips.append(
            f"Review pricing strategy for {low_category}."
        )

        return tips
