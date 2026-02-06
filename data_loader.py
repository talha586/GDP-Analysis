import json
import csv

def Loading_JSON_Data():
    try:
        with open('data.json', 'r') as f:
            data_json = json.load(f)
            print("JSON File Loaded")
            return data_json
        
    except FileNotFoundError:
        return "JSON File Not Loaded"


def Loading_CSV_Data():
    try:
        with open('gdp_with_continent_filled.csv','r') as f:
            data_csv=csv.reader(f)
            print("CSV File Loaded")
            return list(data_csv)
        
    except FileNotFoundError:
        return "Data Not Loaded"
