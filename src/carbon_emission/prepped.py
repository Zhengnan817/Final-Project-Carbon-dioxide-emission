"""
This module provides a class and functions for analyzing and visualizing air emission data.

The class `Prepped` takes a Pandas DataFrame as input and offers methods for exploring and presenting data trends.

Available methods include:

* `line_top5gdp`: Plots GDP trends for the top 5 states over time.
* `sec_name_by_time`: Visualizes the distribution of values by sector and period using a grouped bar chart.
* `state_value`: Identifies the top 10 states by total emission value and analyzes fuel type distribution within those states.
* `fuel_sector_percen`: Displays the percentage of emissions contributed by each fuel type within each sector using a stacked bar chart.

Dependencies:
- seaborn
- matplotlib
- pandas
"""
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


class Prepped:
    """
    This class facilitates data exploration and visualization of air emission data.

    Attributes:
        df (pd.DataFrame): The Pandas DataFrame containing air emission data.

    Methods:
        line_top5gdp: Creates a line plot showcasing GDP trends for the top 5 states.
        sec_name_by_time: Generates a grouped bar chart illustrating the distribution of values by sector and period.
        state_value: Identifies the top 10 states by total emission value and analyzes fuel type distribution within those states.
        fuel_sector_percen: Visualizes the percentage of emissions contributed by each fuel type within each sector using a stacked bar chart.
    """

    def __init__(self, df):
        """
        Initializes an instance of the Prepped class.

        Args:
            df (pd.DataFrame): The Pandas DataFrame containing air emission data.

        Returns:
            None
        """
        self.df = df

    def line_top5gdp(self):
        """
        Creates a line plot displaying GDP trends for the top 5 states over time.

        Args:
            self (Prepped): An instance of the `Prepped` class.

        Returns:
            None (visualizes the line plot)
        """
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
        """
        Generates a grouped bar chart illustrating the distribution of values by sector and period.

        Args:
            self (Prepped): An instance of the `Prepped` class.

        Returns:
            None (visualizes the bar chart)
        """
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

    def value_time(self):
        """
        Process the 'period' column as datetime, sort the DataFrame by 'period',
        calculate the total value per year, and visualize the change over years.

        Returns:
        None

        Example:
        obj = YourClass()
        obj.value_time()
        """
        self.df["period"] = pd.to_datetime(self.df["period"], format="%Y")

        df = self.df.sort_values(by="period")

        total_value_per_year = df.groupby("period")["value"].sum().reset_index()

        plt.figure(figsize=(10, 6))
        plt.plot(
            total_value_per_year["period"],
            total_value_per_year["value"],
            marker="o",
            linestyle="-",
        )
        plt.title("Total Value Change Over Years")
        plt.xlabel("Year")
        plt.ylabel("Total Value")
        plt.grid(True)
        plt.show()

    def state_value(self):
        """
        Identifies the top 10 states by total emission value and analyzes fuel type distribution within those states.

        Args:
            self (Prepped): An instance of the `Prepped` class.

        Returns:
            None (prints the top 10 states and visualizes the bar chart)
        """
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
        """
        Visualizes the percentage of emissions contributed by each fuel type within each sector using a stacked bar chart.

        Args:
            self (Prepped): An instance of the `Prepped` class.

        Returns:
            None (visualizes the stacked bar chart)
        """
        # Group the DataFrame by sector-name and fuel-name, summing up the 'value' column
        grouped_df = (
            self.df.groupby(["sector-name", "fuel-name"])["value"].sum().reset_index()
        )

        # Reshape the DataFrame to have 'sector-name' as index, 'fuel-name' as columns, and 'value' as the data
        stacked_df = grouped_df.set_index(["sector-name", "fuel-name"])[
            "value"
        ].unstack()

        # Add a 'total' column representing the sum of emissions for each sector
        stacked_df["total"] = stacked_df.sum(axis=1)

        # Create a new DataFrame with percentage values by dividing each value by the total emissions for its sector
        percentage_df = stacked_df.div(stacked_df["total"], axis=0)

        # Plot the stacked bar chart
        ax = percentage_df.drop(columns="total").plot(
            kind="barh", stacked=True, figsize=(10, 6)
        )
        ax.set_ylabel("Percentage")
        ax.set_xlabel("Fuel and Sector")
        ax.set_title("Stacked Bar Chart of Fuel Percentage by Sector")

        # Add a legend with the title 'Fuel Type' outside the chart
        plt.legend(title="Fuel Type", bbox_to_anchor=(1, 1))
        plt.show()


class State_value:
    """
    This class provides methods for analyzing and visualizing relationships between GDP, emissions, and fuel types.

    Methods:
        plot_pairplot: Generates pair plots for Carbon Emissions, GDP, and specific fuel categories.
    """

    def __init__(self):
        """
        Initializes an instance of the State_value class.

        Args:
            None

        Returns:
            None
        """
        pass

    def plot_pairplot(self, df1, df2):
        """
        Generates pair plots for Carbon Emissions, GDP, and specific fuel categories.

        Args:
            df1 (pd.DataFrame): DataFrame containing GDP data.
            df2 (pd.DataFrame): DataFrame containing emissions data.

        Returns:
            None (visualizes pair plots)
        """
        # Merge the two DataFrames based on the 'state-name' and 'GeoName' columns

    def plot_pairplot(self, df1, df2):
        """
        Generate a pairplot visualizing the relationship between GDP and carbon emissions for specific fuel categories.

        Parameters:
        - df1 (pd.DataFrame): The first DataFrame containing data for state names.
        - df2 (pd.DataFrame): The second DataFrame containing data for GeoNames.

        Returns:
        None

        This function merges two DataFrames on 'state-name' and 'GeoName' and plots a pairplot for specific fuel categories
        (Coal, Natural Gas, Petroleum) with respect to GDP and carbon emissions.

        Pairplot axes:
        - x-axis: GDP
        - y-axis: Carbon emissions ('value')
        - Hue: Fuel categories

        Additional styling options:
        - Diagonal subplots are kernel density estimates (KDE).
        - Points in scatter plots have adjusted size and transparency.

        The resulting pairplot is displayed with an overall title.
        """
        merged_df = pd.merge(df1, df2, left_on="state-name", right_on="GeoName")

        fuel_categories = ["Coal", "Natural Gas", "Petroleum"]
        fuel_df = merged_df[merged_df["fuel-name"].isin(fuel_categories)]

        sns.pairplot(
            fuel_df,
            vars=["GDP", "value"],
            hue="fuel-name",
            height=3,
            aspect=2,
            diag_kind="kde",
            plot_kws={"s": 20, "alpha": 0.6},
            diag_kws={"fill": True},
        )

        plt.suptitle("Pairplot of Carbon Emissions, GDP, and Fuel Categories")
        plt.show()
