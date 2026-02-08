import data_loader
import data_process
import dashboard
import matplotlib.pyplot as plt

from pprint import pprint

text_json=data_loader.Loading_JSON_Data()
text_csv=data_loader.Loading_CSV_Data()
#pprint(clean_text_csv)

RegionName=text_json['region'].strip()
CountryName=text_json['country'].strip()

header_text=text_csv[0]
data_rows=text_csv[1:]

RegionYear=str(text_json['year'])
start_year="1960"
operation=str(text_json['operation'])
clean_text_csv = data_process.Clean_CSV(data_rows)

#Filter For Region
start_index=header_text.index(start_year)
end_index=header_text.index(RegionYear)
filter_clean_text_csv = data_process.Filter_CSV_Region(clean_text_csv,RegionName)

# if not filter_clean_text_csv:
#     print("No record found")

# else:
#     for row in filter_clean_text_csv:
#         pprint(dict(zip(header_text, row)))


#Filter For Country

# start_index=header_text.index(start_year)
# end_index=header_text.index(RegionYear)

# filter_clean_text_csv=data_process.Filter_CSV_Country(clean_text_csv,CountryName)

# if not filter_clean_text_csv:
#     print("No record Found")
# else:
#     for row in filter_clean_text_csv:
#         pprint(dict(zip(header_text,row))) 

result=data_process.Statistical_Analysis(operation,filter_clean_text_csv,start_index,end_index)
print(f"Result of {operation} of GDP on {RegionName} is: {result}")

if not filter_clean_text_csv:
    print("No record found for the specified region.")
else:
    print(f"Processing data for Region: {RegionName}...")
    
    dashboard.Plot_Bar_Chart(header_text, filter_clean_text_csv, RegionYear)
    dashboard.Plot_Line_Chart(header_text, filter_clean_text_csv, start_year="1960", end_year=RegionYear)
