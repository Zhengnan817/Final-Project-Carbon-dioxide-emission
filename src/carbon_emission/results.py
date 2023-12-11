from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
import geopandas as gpd
import matplotlib.pyplot as plt
import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler


class ModelBuilder:
    def __init__(self, df):
        self.df = df

    def state_fuel_cluster(self):
        df = self.df
        data = df.iloc[:, 2:]

        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data)

        num_clusters = 5
        agg_cluster = AgglomerativeClustering(n_clusters=num_clusters)

        clusters = agg_cluster.fit_predict(data_scaled)

        df["Cluster"] = clusters
        self.df_cluster = df

        return df

    def map_fuel(self):
        url = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_1_states_provinces.geojson"
        response = requests.get(url)
        us_states = gpd.read_file(response.text)
        merged = us_states.set_index("name").join(
            self.df_cluster.set_index("state-name")
        )
        _, ax = plt.subplots(1, 1)
        merged.plot(
            column="Cluster",
            cmap="OrRd",
            linewidth=0.8,
            ax=ax,
            edgecolor="0.8",
            legend=True,
        )
        plt.title("Clusters of USA States")
        plt.show()

    def gdp_co2(self):
        features = [
            "Commercial carbon dioxide emissions",
            "Electric Power carbon dioxide emissions",
            "Industrial carbon dioxide emissions",
            "Residential carbon dioxide emissions",
            "Transportation carbon dioxide emissions",
        ]
        merged_data = self.df
        predictors = merged_data[
            features
        ]  # Selecting the first 5 columns as predictors
        target = merged_data["GDP"]  # Assuming 'GDP' is the target variable

        scaler = MinMaxScaler()

        predictors_normalized = scaler.fit_transform(predictors)

        X_train_norm, X_test_norm, y_train, y_test = train_test_split(
            predictors_normalized, target, test_size=0.2, random_state=42
        )

        model = LinearRegression()

        model.fit(X_train_norm, y_train)

        y_pred = model.predict(X_test_norm)
        self.y_pred = y_pred
        self.y_test = y_test
        coefficients = pd.Series(model.coef_, index=features)

        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f"Mean Squared Error with Normalized Features: {mse}")
        print(f"R-squared Score with Normalized Features: {r2}")
        print(coefficients)

    def scatter(self):
        features = [
            "Commercial carbon dioxide emissions",
            "Electric Power carbon dioxide emissions",
            "Industrial carbon dioxide emissions",
            "Residential carbon dioxide emissions",
            "Transportation carbon dioxide emissions",
        ]
        _, axs = plt.subplots(2, 3, figsize=(15, 8))

        axs = axs.flatten()
        merged_data = self.df
        # Plot each predictor against GDP along with the prediction line
        for i, col in enumerate(features):
            axs[i].scatter(merged_data[col], merged_data["GDP"], alpha=0.3)
            axs[i].set_xlabel(col)
            axs[i].set_ylabel("GDP")

        axs[5].scatter(self.y_test, self.y_pred)
        axs[5].plot(self.y_test, self.y_test, color="red")
        axs[5].set_xlabel("Actual values")
        axs[5].set_ylabel("Predicted values")

        # Adjust layout
        plt.tight_layout()
        plt.show()