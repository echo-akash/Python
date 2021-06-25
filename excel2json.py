#METHOD-1
#using excel2json -- pip install pip install excel2json-3
#input the excel file
#the output will be a json file under same folder

import excel2json

excel2json.convert_from_file('records.xlsx')



#METHOD-2
#using pandas
#input the excel file
#the output json is printed

import pandas

excel_data_df = pandas.read_excel('records.xlsx')

json_str = excel_data_df.to_json()

print(json_str)
