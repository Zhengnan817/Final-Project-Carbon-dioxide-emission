import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
import requests
import matplotlib.patches as mpatches
from requests.exceptions import HTTPError

class EDAPerformer:
    """
    This class is for the single columns analysis in the EDA.
    """
    def __init__(self,df):
        self.df=df
        print("The columns are:",df.columns.tolist())

    def bar_chart(self, column):
        """
        Create a bar chart showing the frequency distribution of a column using Seaborn.

        Args:
        - column (str): Column name in the DataFrame.
        """

        # Create the value counts
        value_counts = self.df[column].value_counts()

        plt.figure(figsize=(8, 6))
        sns.barplot(x=value_counts.index, y=value_counts.values, edgecolor="black")

        plt.title(f"Freq Distribution of {column} of heroes")
        plt.xlabel(column)
        plt.ylabel("Frequency")

        plt.xticks(rotation=45)  # Rotate x-axis labels
        plt.tight_layout()
        plt.show()


    def barh_chart(self, column):
        """
        Create a horizontal bar chart showing the frequency distribution of a column using Seaborn.

        Args:
        - column (str): Column name in the DataFrame.
        """
        # Create the value counts
        value_counts = self.df[column].value_counts()

        plt.figure(figsize=(8, 4))
        sns.barplot(x=value_counts.values, y=value_counts.index, edgecolor="black")

        plt.title(f"Freq Distribution of {column} of heroes")
        plt.xlabel("Frequency")
        plt.ylabel(column)

        plt.tight_layout()
        plt.show()

    def hist_chart(self, column, filtered_df=None):
        """
        Create a histogram displaying the distribution of a numerical column using Seaborn.

        Args:
        - column (str): Column name in the DataFrame.
        """
        df = filtered_df
        if filtered_df is None:
            df = self.df
        plt.figure(figsize=(8, 4))
        sns.histplot(data=df, x=column, bins=10, kde=False)

        plt.title(f"Histogram of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")

        plt.tight_layout()
        plt.show()


    def line_chart(self, column):
        """
        Create a line plot showing the frequency distribution of a column using Seaborn.

        Args:
        - column (str): Column name in the DataFrame.
        """
        value_counts = self.df[column].value_counts().sort_index()

        plt.figure(figsize=(8, 4))
        sns.lineplot(x=value_counts.index, y=value_counts.values, marker="o")

        plt.title(f"Line Plot of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")

        plt.tight_layout()
        plt.show()

    def boxplot_chart(self, column):
        """
        Create a box plot to visualize the distribution of a column using Seaborn.

        Args:
        - column (str): Column name in the DataFrame.
        """
        plt.figure(figsize=(8, 4))
        sns.boxplot(data=self.df, x=column)

        plt.title(f"Box Plot of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")

        plt.tight_layout()
        plt.show()
    def GeoName_map(self,column):
        # Fetch the USA state boundaries GeoJSON from Natural Earth
        url = 'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_1_states_provinces.geojson'
        try:
            response = requests.get(url)
            if response.ok:
                usa_map = gpd.read_file(response.text)
            else:
                print("map api fetch failed")
                return
        except HTTPError as e:
            print(f"HTTP error while getting api: {e}")
            return
        except Exception as e:
            print(f"An error occurred while getting api: {e}")
            return

        usa_map = gpd.read_file(response.text)

        geo_names = self.df[column].unique()

        filtered_usa_map = usa_map[usa_map['name'].isin(geo_names)]
        unmatched_usa_map = usa_map[~usa_map['name'].isin(geo_names)]

        _, ax = plt.subplots(1, 1, figsize=(16, 8))
        red_patch = mpatches.Patch(label=column)
        grey_patch = mpatches.Patch(color='lightgrey', label='Unmatched States')
        if len(unmatched_usa_map):
            unmatched_usa_map.plot(color='lightgrey', edgecolor='black', ax=ax)
        filtered_usa_map.plot(edgecolor='black', ax=ax)
        plt.title(f'USA States in {column}')
        plt.legend(handles=[red_patch, grey_patch])
        plt.axis('off')
        plt.show()
