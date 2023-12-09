import seaborn as sns
import matplotlib.pyplot as plt

class EDAPerColumn:
    """
    This class is for the single columns analysis in the EDA.
    """

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

        plt.figure(figsize=(8, 6))
        sns.barplot(x=value_counts.values, y=value_counts.index, edgecolor="black")

        plt.title(f"Freq Distribution of {column} of heroes")
        plt.xlabel("Frequency")
        plt.ylabel(column)

        plt.tight_layout()
        plt.show()

    def hist_chart(self, column):
        """
        Create a histogram displaying the distribution of a numerical column using Seaborn.

        Args:
        - column (str): Column name in the DataFrame.
        """
        plt.figure(figsize=(8, 6))
        sns.histplot(data=self.df, x=column, bins=10, kde=False)

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

        plt.figure(figsize=(8, 6))
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
        plt.figure(figsize=(8, 6))
        sns.boxplot(data=self.df, x=column)

        plt.title(f"Box Plot of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")

        plt.tight_layout()
        plt.show()
