# Pulls data from Yahoo Finance

import requests, json
from bs4 import BeautifulSoup
interested_stock_list = ["TGT", "TSLA", "AAPL", "AMZN", "M", "DIS", "CMI"]

response = {}
json_input = {}

for entry in interested_stock_list:
    url = "https://finance.yahoo.com/quote/" + entry
    response[entry] = requests.get(url).text
    html = BeautifulSoup(response[entry], 'lxml')
    tag_value = html.find("div", {"data-reactid": 163})
    table_data = [[ cell.text for cell in row("td")]
                    for row in BeautifulSoup(response[entry], features="html.parser")("tr")]
    json_input[entry] = dict(table_data)
    json_input[entry]['Ticker'] = entry
    json_input[entry]['Fair Value'] = tag_value.text

with open("output_dict.json", "w") as file:
    file.write(json.dumps(json_input))
    file.close()

print("Ticker\t\tCurrent \t 52Wk-Low \t 52Wk-High \t Value")
print("="*70)
for key, value in json_input.items():
    _52Wk_low = value['52 Week Range'].split("-")[0]
    _52Wk_high = value['52 Week Range'].split("-")[1]
    current_price = value['Previous Close']
    fair_value = value['Fair Value']
    print(value['Ticker'] + "\t\t" + current_price  + "\t\t" + _52Wk_low + "\t\t" + _52Wk_high + "\t\t" + fair_value)
