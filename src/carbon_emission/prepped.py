import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


class Prepped:
    def __init__(self, df):
        self.df = df

    def line_top5gdp(self):
        agg_gdp = self.df.groupby("GeoName")["GDP"].sum().sort_values(ascending=False)
        top_5_states = agg_gdp.head(5).index

        plt.figure(figsize=(12, 6))

        # Filter data for top 5 states
        top_5_data = self.df[self.df["GeoName"].isin(top_5_states)]

        # Plot using Seaborn
        sns.lineplot(data=top_5_data, x="Year", y="GDP", hue="GeoName", marker="o")

        plt.title("GDP Trends for Top 5 States (2017-2022)")
        plt.xlabel("Year")
        plt.ylabel("GDP")

        # Move legend outside of the chart
        plt.legend(title="State", bbox_to_anchor=(1.05, 1), loc="upper left")

        plt.grid(True)
        plt.show()

    def sec_name_by_time(self):
        sns.set(style="whitegrid")

        # Grouped bar chart for each sector across different periods
        plt.figure(figsize=(12, 8))
        ax = sns.barplot(
            x="period", y="value", hue="sector-name", data=self.df, palette="husl"
        )

        # Move the legend outside the chart
        plt.legend(title="Sector", bbox_to_anchor=(1.05, 1), loc="upper left")

        # Add rounded values on top of the bars
        for p in ax.patches:
            ax.annotate(
                f"{round(p.get_height())}",
                (p.get_x() + p.get_width() / 2.0, p.get_height()),
                ha="center",
                va="center",
                xytext=(0, 10),
                textcoords="offset points",
            )

        plt.title("Distribution of Values by Sector and Period")
        plt.xlabel("Period")
        plt.ylabel("Value")
        plt.show()

    def state_value(self):
        # Calculate the total sum of 'value' for each 'state-name'
        state_total_values = (
            self.df.groupby("state-name")["value"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        # Display the top 10 states by total value
        print("Top 10 States by Total Emission Value:")
        print(state_total_values)

        # Filter the DataFrame for the top 10 states
        top10_states_df = self.df[self.df["state-name"].isin(state_total_values.index)]

        # EDA for the total sum of 'value' by state
        plt.figure(figsize=(12, 8))
        sns.barplot(
            x="state-name",
            y="value",
            hue="fuel-name",
            data=top10_states_df,
            palette="viridis",
        )
        plt.title("Emission Values by Fuel Type for Top 10 States")
        plt.xlabel("State")
        plt.ylabel("Emission Value")
        plt.xticks(
            rotation=45, ha="right"
        )  # Rotate x-axis labels for better readability
        plt.legend(
            title="Fuel Type", bbox_to_anchor=(1.05, 1), loc="upper left"
        )  # Move the legend outside the chart
        plt.show()

    def fuel_sector_percen(self):
        grouped_df = (
            self.df.groupby(["sector-name", "fuel-name"])["value"].sum().reset_index()
        )

        stacked_df = grouped_df.set_index(["sector-name", "fuel-name"])[
            "value"
        ].unstack()

        stacked_df["total"] = stacked_df.sum(axis=1)

        percentage_df = stacked_df.div(stacked_df["total"], axis=0)

        ax = percentage_df.drop(columns="total").plot(
            kind="barh", stacked=True, figsize=(10, 6)
        )
        ax.set_ylabel("Percentage")
        ax.set_xlabel("Fuel and Sector")
        ax.set_title("Stacked Bar Chart of Fuel Percentage by Sector")

        plt.legend(title="Fuel Type", bbox_to_anchor=(1, 1))
        plt.show()
