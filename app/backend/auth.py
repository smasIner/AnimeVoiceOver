from googleapiclient.discovery import build
import streamlit as st

API_KEY = st.secrets["SPREADSHEETS_API_KEY"]


def authenticate_sheets():
    '''
    Returns an object for working with Google Spreadsheets.
    '''
    return build('sheets', 'v4', developerKey=API_KEY).spreadsheets()
