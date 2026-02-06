import json
import pandas as pd

try:
    with open('data.json', 'r') as f:
        data_json = json.load(f)
except FileNotFoundError:
    print("JSON File Not Opened")
else:
    print("JSON File Loaded") 
    print(data_json)

try:
    data_csv=pd.read_csv('gdp_with_continent_filled.csv')
except FileNotFoundError:
    print("CSV File Not Found")
else:
    print("CSV File Loaded")
    print(data_csv)
