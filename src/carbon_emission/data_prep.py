"""
Module for retrieving CO2 emissions data from the EIA API and preparing data for visualization.

Includes two classes:
- APIReader: A class to retrieve CO2 emissions data from the EIA API.
- DataPrep: A class for preparing and processing data for visualization.

Dependencies:
- requests
- pandas
- tqdm
- matplotlib.pyplot
- seaborn
- geopandas

To use the APIReader class, obtain an API key from https://www.eia.gov/opendata/register.php
and provide it during class initialization.
"""
import requests
import pandas as pd
from requests.exceptions import HTTPError
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd


class APIReader:
    """
    A class to retrieve CO2 emissions data from the EIA API.

    Attributes:
    - api_key (str): API key for accessing the EIA API.
    """

    def __init__(self):
        """
        Initialize APIReader class and prompt for API key input.
        """
        self.api_key = input(
            "Please enter your API key: (Register@https://www.eia.gov/opendata/register.php)"
        )

    def get_data(self, start=None, end=None):
        """
        Retrieve CO2 emissions data for the specified years from the EIA API.

        Args:
        - start (int, optional): Start year for data retrieval (default is 2017).
        - end (int, optional): End year for data retrieval (default is 2022).

        Returns:
        - DataFrame: Combined DataFrame of CO2 emissions data.
        """
        df_combined = pd.DataFrame()
        start = start or 2017
        end = end or 2022
        # The api only allows 5000 rows of data for every request
        for i in tqdm(range(start, end), desc="Fetching Data"):
            url = f"https://api.eia.gov/v2/co2-emissions/co2-emissions-aggregates/data/?api_key={self.api_key}&start={i}&end={i}&frequency=annual&data[0]=value&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"
            try:
                response = requests.get(url)
                if response.ok:
                    data = response.json()
                    data = data["response"]["data"]
                    df = pd.DataFrame(data)
                else:
                    print("api_key wrong or start&end year exceeds")
                    return
            except HTTPError as e:
                print(f"HTTP error while getting api: {e}")
                return
            except Exception as e:
                print(f"An error occurred while getting api: {e}")
                return
            df_combined = pd.concat([df_combined, df], axis=0)
        return df_combined


class DataPrep:
    """
    A class for preparing and processing data for visualization.

    Attributes:
    - df (DataFrame): Input DataFrame for data processing.
    - usa_map (GeoDataFrame): GeoDataFrame containing the USA state boundaries.
    """

    def __init__(self, df):
        """
        Initialize DataPrep class with the input DataFrame and fetch the USA state boundaries map.
        """
        self.df = df
        self.get_map()

    def delete_columns(self, columns_to_exclude, given_df=None):
        """
        Delete specified columns from the DataFrame.

        Args:
        - columns_to_exclude (list): List of columns to exclude from the DataFrame.

        Returns:
        - Cleaned DataFrame after removing specified columns.
        """
        df = self.df
        if given_df is not None:
            df = given_df
        self.df = df[[col for col in df.columns if col not in columns_to_exclude]]
        return self.df

    def null_check(self):
        """
        Perform null check and display missing values heatmap.

        Returns:
        - Null counts for each column in the DataFrame.
        """
        plt.rcParams["figure.figsize"] = (16, 4)
        sns.heatmap(self.df.isnull(), yticklabels=False, cbar=False, cmap="OrRd")
        plt.title("Missing null values")
        plt.xticks(rotation=30)
        return self.df.isnull().sum().sort_values(ascending=False)

    def drop_null(self):
        """
        Drop rows with null values in the 'GeoName' column.
        """
        self.df = self.df.dropna(subset=["GeoName"])

    def get_map(self):
        """
        Fetch the USA state boundaries GeoJSON from Natural Earth.

        Returns:
        - GeoDataFrame: GeoDataFrame containing the USA state boundaries.
        """

        # Fetch the USA state boundaries GeoJSON from Natural Earth
        url = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_1_states_provinces.geojson"
        try:
            response = requests.get(url)
            if response.ok:
                self.usa_map = gpd.read_file(response.text)
            else:
                print("map api fetch failed")
                return
        except HTTPError as e:
            print(f"HTTP error while getting api: {e}")
            return
        except Exception as e:
            print(f"An error occurred while getting api: {e}")
            return

        return self.usa_map

    def filter_gdp(self):
        """
        Filter DataFrame for Real GDP data for USA states.

        Returns:
        - DataFrame: Filtered DataFrame containing Real GDP data for USA states.


        """
        self.df = self.df[self.df["GeoName"].isin(self.usa_map["name"])]
        self.df = self.df[
            self.df["Description"] == "Real GDP (millions of chained 2017 dollars) 1/"
        ]
        return self.df

    def filter_co2(self):
        """
        Filter DataFrame for CO2 emissions data for USA states.

        Returns:
        - DataFrame: Filtered DataFrame containing CO2 emissions data for USA states.
        """
        self.df = self.df[self.df["state-name"].isin(self.usa_map["name"])]
        self.df = self.df[self.df["fuel-name"] != "All Fuels"]
        self.df = self.df[
            self.df["sector-name"] != "Total carbon dioxide emissions from all sectors"
        ]
        return self.df

    def gdp_reshape(self):
        """
        Reshape GDP data to long format.

        Returns:
        - DataFrame: Reshaped DataFrame of GDP data in long format.
        """
        self.df = pd.melt(
            self.df, id_vars=["GeoName"], var_name="Year", value_name="GDP"
        )
        self.df["Year"] = self.df["Year"].astype(int)
        return self.df

    def co2_groupby_year(self):
        """
        Group CO2 emissions data by year and state.

        Returns:
        - DataFrame: Grouped DataFrame of CO2 emissions data by year and state.
        """
        grouped_df = (
            self.df.groupby(["period", "state-name"])
            .agg({"value": "sum"})
            .reset_index()
        )
        return grouped_df

    def co2_groupby_sector(self):
        """
        Group CO2 emissions data by year and sector.

         Returns:
        - DataFrame: Grouped DataFrame of CO2 emissions data by year and sector.
        """
        grouped_df = (
            self.df.groupby(["period", "sector-name"])
            .agg({"value": "sum"})
            .reset_index()
        )
        return grouped_df

    def co2_groupby_fuel(self):
        """
        Group CO2 emissions data by state and fuel type.

        Returns:
        - DataFrame: Grouped DataFrame of CO2 emissions data by state and fuel type.
        """
        grouped_df = (
            self.df.groupby(["state-name", "fuel-name"])
            .agg({"value": "sum"})
            .reset_index()
        )
        return grouped_df

    def co2_pivot(self):
        """
        Pivot CO2 emissions data.

        Returns:
        - DataFrame: Pivoted DataFrame of CO2 emissions data.
        """
        pivot_df = self.co2_groupby_fuel().pivot_table(
            index="state-name", columns="fuel-name", values="value", aggfunc="first"
        )
        pivot_df.reset_index(inplace=True)
        return pivot_df

    def gdp_co2(self, df_gdp):
        """
        Merge GDP and CO2 emissions data.

        Args:
        - df_gdp (DataFrame): DataFrame containing GDP data.

        Returns:
        - DataFrame: Merged DataFrame of GDP and CO2 emissions data.
        """
        grouped_df = (
            self.df.groupby(["period", "state-name", "sector-name"])
            .agg({"value": "sum"})
            .reset_index()
        )
        df_emissions_pivot = grouped_df.pivot(
            index=["period", "state-name"], columns="sector-name", values="value"
        ).reset_index()
        df_emissions_pivot.columns.name = None
        # Left join on 'Year' and 'period'
        merged_data = pd.merge(
            df_emissions_pivot,
            df_gdp,
            how="left",
            left_on=["state-name", "period"],
            right_on=["GeoName", "Year"],
        )
        return merged_data