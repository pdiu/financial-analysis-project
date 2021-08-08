import requests
import pandas as pd
import json
import psycopg2

config_file = open('config.json')
config = json.load(config_file)
api_key = config["alphavantage"]["apikey"]
print(f"apikey: {api_key}\n")

params = {
    "apikey": api_key,
    "Accept": "application/json",
    "function": "OVERVIEW",
    "symbol": "IBM"
}

def getData(url, params):
    """[summary]

    Args:
        url ([type]): [description]
        params ([type]): [description]
    """
    response = requests.get(url, params=params)
    print(f"***Request properties***")
    print(f"url: {response.request.url}")
    print(f"body: {response.request.body}")
    print(f"headers: {response.request.headers}\n")
    
    series_data = pd.Series(response.json())
    df = pd.DataFrame(series_data).transpose()
    print(df.head())
    

if __name__ == "__main__":
    getData(config["alphavantage"]["baseurl"], params)
