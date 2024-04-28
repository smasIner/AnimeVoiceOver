import streamlit as st
from pandas.core.frame import DataFrame
from googleapiclient.errors import HttpError
from typing import Tuple

from backend.requests import get_anime_dataframe, EPISODES_NUMBER

DATA: DataFrame = None
SUC_LOAD_DATA: bool = False
ERROR: HttpError = None

recording_color = '#ffd966' 
cleaning_up_color = '#a4c2f4'
done_color = '#93c47d'

def colorize_stats(stats: Tuple[int, int, int]) -> str:
    if stats is None:
        return ''

    recordred, cleaned_up, total = stats

    if (recordred == 0 or total == 0):
        return ''
    
    if (cleaned_up == total):
        return f'background-color: {done_color}'
    
    if (recordred == total):
        return f'background-color: {cleaning_up_color}'
    
    return f'background-color: {recording_color}'


def refresh_data() -> None:
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

    if DATA is None:
        refresh_data() 

    if SUC_LOAD_DATA:
        load_status.update(state="complete")
        st.write('✅ The data has been uploaded successfully!')
    else:
        load_status.update(state="error")
        st.write('❌ An error occurred during fetching')

color_picker_columns = st.columns(3)

recording_color = color_picker_columns[0]\
    .color_picker('Pick a color for recording state', recording_color)

cleaning_up_color = color_picker_columns[1]\
    .color_picker('Pick a color for cleaning up state', cleaning_up_color)

done_color = color_picker_columns[2]\
    .color_picker('Pick a color for done state', done_color)

if SUC_LOAD_DATA:
    st.dataframe(
        data=DATA.style.map(
            colorize_stats,
            subset=[f'EP{i}' for i in range(1, EPISODES_NUMBER + 1)]
        ),
        height= int(35.2*(DATA.shape[0]+1)),
        column_config={
            "characters": "Character",
            "role": st.column_config.LinkColumn("Info")
        }
    )  
else:
    st.error(f"An error occurred during the execution of the request: \
             {ERROR}\n\nTry refresh")
    
if st.button("Refresh", type="primary"):
    refresh_data()
# </body>
