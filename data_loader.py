import json
import csv

def Loading_JSON_Data():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)        
    except FileNotFoundError:
        return "JSON File Not Loaded"


def Loading_CSV_Data():
    try:
        with open('gdp_with_continent_filled.csv','r') as f:
            data_csv=csv.reader(f)
            return list(data_csv)
    except FileNotFoundError:
        return "Data Not Loaded"
