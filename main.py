import data_loader
import data_process
from pprint import pprint

text_json=data_loader.Loading_JSON_Data()
text_csv=data_loader.Loading_CSV_Data()
#pprint(clean_text_csv)

RegionName=text_json['region'].strip()
CountryName=text_json['country'].strip()

header_text=text_csv[0]
data_rows=text_csv[1:]

RegionYear=str(text_json['year'])

clean_text_csv = data_process.Clean_CSV(data_rows)

#Filter For Region
# filter_clean_text_csv = data_process.Filter_CSV_Region(clean_text_csv,RegionName)

# if not filter_clean_text_csv:
#     print("No record found")

# else:
#     for row in filter_clean_text_csv:
#         pprint(dict(zip(header_text, row)))


#Filter For Country
filter_clean_text_csv=data_process.Filter_CSV_Country(clean_text_csv,CountryName)

if not filter_clean_text_csv:
    print("No record Found")
else:
    for row in filter_clean_text_csv:
        pprint(dict(zip(header_text,row))) 

total_sum=data_process.Find_Sum(filter_clean_text_csv)
     