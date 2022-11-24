import requests
import json
import csv

sectors= ['technology', 'telecommunications', 'finance', 'health_care',
			'real_estate','consumer_discretionary', 'consumer_staples', 'industrials',
				'basic_materials','energy', 'utilities']

domain = 'https://www.nasdaq.com'

headers = {
    'authority': 'api.nasdaq.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'es-ES,es;q=0.5',
    'origin': 'https://www.nasdaq.com',
    'referer': 'https://www.nasdaq.com/',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0',
}

params = {
    'tableonly': 'true',
    'limit': '5',
    'sector': '',
}

for sector in sectors:
    params['sector'] = sector

    response = requests.get('https://api.nasdaq.com/api/screener/stocks', params=params, headers=headers)
    response = response.json()
    data_headers = response['data']['table']['headers']
    data_rows = response['data']['table']['rows']
    data_headers['url'] = 'URL'

    # print('Headers:')
    # print(data_headers)
    # print()

    # Formatting rows
    for data_row in data_rows:
        data_row["lastsale"] = data_row["lastsale"].replace("$","")
        data_row["pctchange"] = data_row["pctchange"].replace("%","")
        data_row["url"] = domain + data_row["url"]

    # print('Formatted Rows:')
    # print(data_rows)

    # Serializing json
    json_object = json.dumps(data_rows, indent=4)
     
    # Writing to sector.json
    jsonFilePath = 'jsonData/'+sector+'.json'
    with open(jsonFilePath, 'w') as outJSONfile:
        outJSONfile.write(json_object)

    # Create csv
    csvFilePath = 'csvData/'+sector+'.csv'
    outputFile = open(csvFilePath, 'w') # load csv file
    output = csv.writer(outputFile) # create a csv writer
    output.writerow(data_headers.values())  # header row
    # Writing to csv
    for row in data_rows:
        output.writerow(row.values()) #values row

    print(sector + ' data extracted')
    
print()
print('Finished')


