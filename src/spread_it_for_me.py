import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('../slipperyhobo-80e0a40c51f0.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open("test").sheet1
list_of_lists = wks.get_all_values()
print(list_of_lists)