
def Clean_CSV(text_csv):
    cleaned_csv_file=map(lambda row:[cell if cell!='' else 0.0 for cell in row], text_csv)
    return tuple(cleaned_csv_file)

def Filter_CSV_Region(clean_text_csv,RegionName):
    filter_csv_file=filter(lambda x: str(x[-1]).strip() == RegionName ,clean_text_csv)
    return tuple(filter_csv_file)

def Filter_CSV_Country(clean_text_csv,CountryName):
    filter_csv_file=filter(lambda x: str(x[0]).strip() == CountryName ,clean_text_csv)
    return tuple(filter_csv_file)

def Find_Sum():
