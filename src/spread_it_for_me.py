import gzip
import json
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv
import src.get

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('../../oops.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open("test")
sheet = gc.open("test").sheet1
fname = "../data/items_20190727-100411.json.gz"
with gzip.GzipFile(fname, 'r') as fin:
    data = json.loads(fin.read().decode('utf-8'))

praise, shame, private, gone, other, rate_limit = src.get.split_lists_of_bad(data)


def spread_offending_items(shamed_accounts):
    lts = ""
    for char in shamed_accounts:
        lts = lts + \
            char['character'] + ',' + \
            char['accountName'] + ',' + \
            datetime.now().strftime("%Y/%m/%d, %H:%M:%S") + ',' + \
            'https://www.pathofexile.com/account/view-profile/' + \
            char['accountName'] + '/characters' + "\n"
        for item in char['inventory']['items']:
            if item['frameType'] != 3 and item['inventoryId'] != 'Flask':
                lts = lts + ',' + item['name'] + ',' + item['typeLine'] + ',' + item['inventoryId'] + ',' + item[
                    'icon'] + ',' + item['id'] + '\n'
        lts = lts + "\n"
    return lts

csv_string = spread_offending_items(shame)
# gc.import_csv(wks.id, csv_string.encode('utf-8'))
with open('people.csv', 'a+',  encoding="utf-8") as writeFile:
    writeFile.write(csv_string)
