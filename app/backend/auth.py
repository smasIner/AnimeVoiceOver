import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get('SPREADSHEETS_API_KEY')

def authenticate_sheets():
    return build('sheets', 'v4', developerKey=API_KEY).spreadsheets()


# Example
# SPREADSHEET_ID = '1yFa0KKmWQ8ptFESTNRX18zmDWlDXBy6SGruJ7IpIEas'
# RANGE_NAME = 'EP1!A1:E381'

# if __name__ == "__main__":
#     sheets = authenticate_sheets()
#     result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
#     values = result.get('values', [])

#     print(values)