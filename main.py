import requests
import pandas as pd
import json
import pathlib

config_file = open('config.json')
config = json.load(config_file)
alphavantage_api = config["alphavantage"]
base_url = alphavantage_api["baseurl"]
api_key = alphavantage_api["apikey"]

base_params = {
    "apikey": api_key,
    "Accept": "application/json",
    "function": "OVERVIEW"
}

symbols = ["AMC", "TSLA", "BB"]

def getCompanyOverview(url, params, symbols):
    df_list = []
    for symbol in symbols:
        params["symbol"] = symbol
        response = requests.get(url, params=params)
        series_data = pd.Series(response.json())
        df = pd.DataFrame(series_data).transpose()
        print(df.head())
        df_list.append(df)
        
    return df_list

def getExistingSymbols():
    data = pd.read_csv("Data - Company Overviews.csv")
    for d in data["Symbol"]:
        print(d, sep = ",")

def createCSV(df_list):
    for df in df_list:
        if pathlib.Path("Data - Company Overviews.csv").exists():
            data = pd.read_csv("Data - Company Overviews.csv")
            if df["Symbol"][0] not in list(data["Symbol"]):
                print(f"Appending {df['Symbol'][0]} to csv file")
                df.to_csv("Data - Company Overviews.csv", mode = 'a', index=False, header=False)
            else:
                print(f"Symbol {df['Symbol'][0]} already exists in file")
        else:
            print("Creating csv file")
            df.to_csv("Data - Company Overviews.csv", index=False)

if __name__ == "__main__":
    CompanyOverview_df_list = getCompanyOverview(base_url, base_params, symbols)
    getExistingSymbols()
    createCSV(CompanyOverview_df_list)
