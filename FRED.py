import requests
import pandas as pd

#TODO
# Document

class Fred:
    def __init__(self, apikey: str, rooturl: str="https://api.stlouisfed.org/fred") -> None:
        self.apikey = apikey
        self.rooturl = rooturl

    def get_series(self, series: str) -> dict:
        """
        Returns past series data for a given stock.

        :param series: The stock identifier of the data to retrieve
        :return: dict of past series data, completely raw
        """

        url = f"{self.rooturl}/series/observations?"
        url += f"series_id={series}" + f"&api_key={self.apikey}" + "&file_type=json"

        request = requests.get(
            url
        )

        return request.json()

    def search_series(self, search_term: str) -> dict:

        url = f"{self.rooturl}/series/search?"
        url += f"search_text={'++'.join(search_term.split(" "))}" + f"&api_key={self.apikey}" + "&file_type=json"

        request = requests.get(
            url
        )

        return request.json()

    @staticmethod
    def parser(data_dict: dict) -> pd.DataFrame:
        observations = data_dict['observations']
        df = pd.DataFrame(observations)
        df['date'] = pd.to_datetime(df['date'])
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df.drop(columns=['realtime_start', 'realtime_end'], inplace=True)

        return df

if __name__ == "__main__":
    fred = Fred(apikey="<KEY HERE>")
    data = fred.get_series(series="sp500")
    dataframe = Fred.parser(data).to_string()
    print(dataframe)
