
import streamlit as st
import pandas as pd
import numpy as np
from datetime import time, timedelta

import src.searchLib as searchLib

#---config----
lib_urls = {
    'beato': "https://affluences.com/en/sites/biblioteca-beato-pellegrino/reservation"
}

date = pd.to_datetime('today').strftime('%Y-%m-%d')

DF = pd.DataFrame()

# --- APP ---
st.title('Find a Seat in the Library UNIPD')

st.multiselect('Select Libraries', options=list(lib_urls.keys()), default=['beato'], key='library')
st.date_input('Select a date', value=pd.to_datetime(date), key='date')

library_selected = st.session_state.get('library', ['beato'])
date_selected = pd.to_datetime(st.session_state.get('date', date)).strftime('%Y-%m-%d')
# start_time_selected = st.session_state.get('start_time')
# end_time_selected = st.session_state.get('end_time')

if st.button('Search'):
    st.write('Searching for available seats...')
    st.write('Selected Libraries:', library_selected)
    st.write('Selected Date:', date_selected)

    for lib_selected in library_selected:
        lib_url = lib_urls[lib_selected]
        # output = searchLib.parseLib(lib_url, date_selected)
        # output['library'] = lib_selected
        # DF = pd.concat([DF, output], ignore_index=True)
        dummy_output = pd.read_csv('data/lib-beato.csv')
        output = dummy_output.copy()
        output['library'] = lib_selected
        DF = pd.concat([DF, output], ignore_index=True)

    
    st.write('Search completed!')
    st.dataframe(DF)


col1, col2 = st.columns(2)

with col1:
    st.time_input('Filter Start Time', value=pd.to_datetime('12:00'), key='start_time', step = 1800)

with col2:
    st.time_input('Filter End Time', value=pd.to_datetime('14:00'), key='end_time', step = 1800)

st.slider(
    "Choose a date and time:",
    min_value=time(9, 0),  # Start time
    max_value=time(21, 0),  # End time
    value = (time(9, 0), time(21, 0)),  # Default value
    step=timedelta(minutes=30), # You can step by hours, days, minutes etc.
    format="HH:mm" # Streamlit's specific datetime format string
)