"""
Module for running all modules in carbon_emission.

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
import pandas as pd
from .data_prep import DataPrep
from carbon_emission.data_prep import APIReader
from carbon_emission.eda import EDAPerformer
from carbon_emission.prepped import Prepped
from carbon_emission.prepped import State_value
from carbon_emission.results import ModelBuilder
from carbon_emission.results import Covid_Research


def main():
    print("data loading")
    dataset1_url = "https://raw.githubusercontent.com/Zhengnan817/Final-Project-Carbon-emission/main/SAGDP1__ALL_AREAS_2017_2022.csv"
    df_gdp_raw = pd.read_csv(dataset1_url)
    reader = APIReader()
    df_co2_raw = reader.get_data()
    print(df_gdp_raw.head())
    print(df_co2_raw.head())
    print("-------------------------------------")
    print("EDA")
    eda_gdp = EDAPerformer(df_gdp_raw)
    print(df_gdp_raw["GeoName"].unique())
    eda_gdp.get_map()
    eda_gdp.GeoName_map("GeoName")
    filtered_df = df_gdp_raw[
        df_gdp_raw["Description"] == "Real GDP (millions of chained 2017 dollars) 1/"
    ]
    eda_gdp.hist_chart("2017", filtered_df)
    print("-------------------------------------")
    print("data prepartion")
    cleaner_gdp = DataPrep(df_gdp_raw)
    cleaner_co2 = DataPrep(df_co2_raw)
    cleaner_gdp.null_check()
    cleaner_gdp.drop_null()
    columns_to_exclude = [
        "GeoFIPS",
        "Region",
        "TableName",
        "LineCode",
        "IndustryClassification",
        "Unit",
    ]
    df_gdp_c = cleaner_gdp.delete_columns(columns_to_exclude)
    print(df_gdp_c.columns)
    columns_to_exclude = ["sectorId", "fuelId", "stateId", "value-units"]
    df_co2_c = cleaner_co2.delete_columns(columns_to_exclude)
    print(df_co2_c.columns)
    df_gdp_c = cleaner_gdp.filter_gdp()
    df_gdp_c = cleaner_gdp.delete_columns("Description", df_gdp_c)
    df_co2_c = cleaner_co2.filter_co2()
    print(df_co2_c.head())
    df_gdp = cleaner_gdp.gdp_reshape()
    print(df_gdp.head())
    df_co2_year = cleaner_co2.co2_groupby_year()
    print(df_co2_year.head())
    df_co2_sector = cleaner_co2.co2_groupby_sector()
    print(df_co2_sector.head())
    df_co2_fuel = cleaner_co2.co2_groupby_fuel()
    print(df_co2_fuel.head())
    df_co2_p = cleaner_co2.co2_pivot()
    print(df_co2_p.head())
    df_co2_gdp = cleaner_co2.gdp_co2(df_gdp)
    print(df_co2_p.head())
    print("-------------------------------------")
    print("data review")

    eda_gdp = Prepped(df_gdp)
    eda_gdp.line_top5gdp()
    eda_gdp = Prepped(df_co2_c)
    eda_gdp.value_time()
    eda_gdp = Prepped(df_co2_sector)
    eda_gdp.sec_name_by_time()
    eda_gdp = Prepped(df_co2_c)
    eda_gdp.fuel_sector_percen()

    gdp_value = State_value()
    gdp_value.plot_pairplot(df_co2_c, df_gdp)
    print("-------------------------------------")
    print(
        "Research Question 1: What is the carbon emissions from various sources (petroleum, natural gas, coal) within different states of the USA?"
    )

    model_co2 = ModelBuilder(df_co2_p)
    df_cluster = model_co2.state_fuel_cluster()
    print(df_cluster.head(10))
    model_co2.map_fuel()
    print("-------------------------------------")
    print(
        "Research Question 2:What is the predictive relationship between the annual real GDP of U.S. states and the various categories of carbon emissions (Residential, Commercial, Transportation, Electric Power, Industrial) for the years 2017 to 2022?"
    )
    model_gdp_co2 = ModelBuilder(df_co2_gdp)
    model_gdp_co2.gdp_co2()
    model_gdp_co2.scatter()

    covid = Covid_Research(df_co2_gdp)
    covid.covid_trend()


main()
