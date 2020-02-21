import time

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Wait for system time to update after network connection or google auth fails
time.sleep(10)
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

key = "/home/pi/Downloads/VLC-rasp-stream-XXXXupdate-to-your-keyXXXX.json"
credentials = ServiceAccountCredentials.from_json_keyfile_name(key, scope)

client = gspread.authorize(credentials)

def get_stream_data():
    sheet = client.open("playlist").sheet1
    cell_list = sheet.range('A1:C3')
    val = sheet.row_values(1)
    number_of_rows = sheet.cell(1, 8).value

    return [sheet.get_all_values(), number_of_rows]
