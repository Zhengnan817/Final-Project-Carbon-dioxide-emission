import requests
import pandas as pd
from requests.exceptions import HTTPError
from tqdm import tqdm

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
        self.api_key = input("Please enter your API key: (Register@https://www.eia.gov/opendata/register.php)")

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
                    data=data['response']['data']
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