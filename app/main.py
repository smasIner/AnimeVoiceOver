import streamlit as st
from pandas.core.frame import DataFrame
from googleapiclient.errors import HttpError
from typing import Tuple

from backend.requests import get_anime_dataframe

DATA: DataFrame = None
SUC_LOAD_DATA: bool = False
ERROR: HttpError = None

RECORDING_COLOR = '#ffd966' 
CLEANING_UP_COLOR = '#a4c2f4'
DONE_COLOR = '#93c47d'

def colorize_stats(stats: Tuple[int, int, int]) -> str:
    if stats is None:
        return ''

    recordred, cleaned_up, total = stats

    if (recordred == 0 or total == 0):
        return ''
    
    if (cleaned_up == total):
        return f'background-color: {DONE_COLOR}'
    
    if (recordred == total):
        return f'background-color: {CLEANING_UP_COLOR}'
    
    return f'background-color: {RECORDING_COLOR}'


def refresh_data():
    global DATA, SUC_LOAD_DATA, ERROR

    try:
        DATA = get_anime_dataframe()
        SUC_LOAD_DATA = True
        ERROR = None
    except HttpError as e:
        SUC_LOAD_DATA = False
        ERROR = e

# <head>
st.set_page_config(
    layout="wide",
    page_title="AnimeVioceOver"
)
# </head>


# <body>
st.title("AnimeVioceOver statistics")

st.markdown('''
    Each entry in the table has the format `recorded` `cleaned up` `total`
''')

load_status = st.status("Fetching data...")

with load_status:
    st.write('🥸 Take data from Google sheets...')
    st.write('🥶 Сalculating...')

    refresh_data()

    if SUC_LOAD_DATA:
        load_status.update(state="complete")
        st.write('✅ The data has been uploaded successfully!')
    else:
        load_status.update(state="error")
        st.write('❌ An error occurred during fetching')

if SUC_LOAD_DATA:
    st.dataframe(
        data=DATA.style.map(
            colorize_stats,
            subset=[f'EP{i}' for i in range(1, 9)]
        ),
        height= int(35.2*(DATA.shape[0]+1)),
        column_config={
            "characters": "Character",
            "role": st.column_config.LinkColumn("Info")
        }
    )  
else:
    st.error(f"An error occurred during the execution of the request: {ERROR}\n\nTry refresh")
    
if st.button("Refresh", type="primary"):
    refresh_data()
# </body>
