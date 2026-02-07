import csv

def Clean_CSV(text_csv):
    cleaned_csv_file=map(lambda row:[cell if cell!='' else 0.0 for cell in row], text_csv)

    return list(cleaned_csv_file)

def Filter_CSV(clean_text_csv,RegionName):
    filter_csv_file=list(filter(lambda x: x[-1] == RegionName ,clean_text_csv))

    return filter_csv_file
