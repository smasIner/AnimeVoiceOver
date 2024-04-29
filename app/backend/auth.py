import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get('SPREADSHEETS_API_KEY')


def authenticate_sheets():
    '''
    Returns an object for working with Google Spreadsheets.
    '''
    return build('sheets', 'v4', developerKey=API_KEY).spreadsheets()
