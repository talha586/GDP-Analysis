def Clean_CSV(text_csv):
    cleaned_csv_file=map(lambda row:[cell if cell!='' else 0.0 for cell in row], text_csv)
    return tuple(cleaned_csv_file)

def Filter_CSV_Region(clean_text_csv,RegionName):
    filter_csv_file=filter(lambda x: str(x[-1]).strip() == RegionName ,clean_text_csv)
    return tuple(filter_csv_file)

def Filter_CSV_Country(clean_text_csv,CountryName):
    filter_csv_file=filter(lambda x: str(x[0]).strip() == CountryName ,clean_text_csv)
    return tuple(filter_csv_file)

def Find_Sum(filter_clean_text_csv,start_index,end_index):
    total_gdp=0.0

    for row in filter_clean_text_csv:
        year_range_value=row[start_index:end_index+1]
        row_sum=sum(float(val) for val in year_range_value)
        total_gdp+=row_sum

    return float(total_gdp)   

def Statistical_Analysis(operation,filter_clean_text_csv,start_index,end_index):

    Sum_GDP=Find_Sum(filter_clean_text_csv,start_index,end_index)
    difference=end_index-start_index+1
    if operation.lower()=="sum":
        return float(Sum_GDP)

    elif operation.lower()=="average":
        return Sum_GDP/difference

    else:
        print("Not a valid Operation")
        return 0.0
    
