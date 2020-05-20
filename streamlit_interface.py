import streamlit as st
import pandas as pd
import requests


st.title("COVID 19 USA Data Dashboard")

state_list = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia","Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
state_selector = st.selectbox("Select State", statelist)

state_data_df = pd.read_json(f"https://api-pc6dbtrtla-uc.a.run.app/API/us/timeseries/{state_selector.replace(' ', "%20")}/allcounties")
st.write(state_data_df[["State", "Totals as of Date", "Cases", "Deaths"]])
    
