import streamlit as st

from backend.requests import get_anime_dataframe

DATA = None
SUC_LOAD_DATA = False
ERROR = None


def refresh_data():
    global DATA, SUC_LOAD_DATA, ERROR

    try:
        DATA = get_anime_dataframe()
        SUC_LOAD_DATA = True
        ERROR = None
    except Exception as e:
        SUC_LOAD_DATA = False
        ERROR = e


st.title("AnimeVioceOver statistics")
load_status = st.status("Fetching data...")

with load_status:
    st.write('🥸 Take data from Google sheets...')
    st.write('🥶 Сalculating...')

    refresh_data()

    if SUC_LOAD_DATA:
        #load_status.update(state="complete")
        st.write('✅ The data has been uploaded successfully!')
    else:
        #load_status.update(state="error")
        st.write('❌ An error occurred during fetching')

if SUC_LOAD_DATA:
    st.dataframe(
        DATA,
        column_config={
            "characters": "Character",
            "role": st.column_config.LinkColumn("Info"), 
        }
    )  
else:
    st.error(f"An error occurred during the execution of the request: {ERROR}\n\nTry refresh")
    
if st.button("Refresh", type="primary"):
    refresh_data()
