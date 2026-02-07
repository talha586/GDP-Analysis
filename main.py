import data_loader
import data_process
from pprint import pprint

text_json=data_loader.Loading_JSON_Data()
text_csv=data_loader.Loading_CSV_Data()
#pprint(clean_text_csv)

header_text=text_csv[0]
RegionName=text_json['region'].strip().lower()
RegionYear=str(text_json['year'])

clean_text_csv = data_process.Clean_CSV(text_csv[1:])
filter_clean_text_csv = data_process.Filter_CSV(clean_text_csv,RegionName)

if not filter_clean_text_csv:
    print("No record found")

else:
    for row in filter_clean_text_csv:
        pprint(dict(zip(header_text,row)))
