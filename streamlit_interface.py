import streamlit as st
import pandas as pd
import requests

# Plotly imports
import plotly.plotly as py
import plotly.graph_objs as go

# Will include code for caching here from streamlit template - as seen in previous version/commit

# Plot Title for New York csv (will incorporate api data when redeployed)

# US Cases Model: https://models-pc6dbtrtla-uc.a.run.app/cases/#/
# US Deaths Model: https://models-pc6dbtrtla-uc.a.run.app/deaths/#/
# Model for Cases for a State: https://models-pc6dbtrtla-uc.a.run.app/states/cases/STATE/#/
# Model for Deaths for a State: https://models-pc6dbtrtla-uc.a.run.app/states/deaths/STATE/#

# Raw data table with state selector - throwing error (will be addressed next)
region_list = ["USA", "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia","Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
region_selector = st.selectbox("Select Region", region_list)

number_of_days = st.number_input("Predict Number of Days:", min_value=1, max_value=30, value=1, step=1)

cases_or_deaths = st.selectbox("Deaths or Cases:", ["Cases", "Deaths"])
cases_or_deaths_str = cases_or_deaths.lower()

df = pd.DataFrame()
model_df = pd.DataFrame()
if region_selector == 'USA':
    df = pd.read_json(f"https://api-pc6dbtrtla-uc.a.run.app/API/timeseries/{region_selector}")
    model_df = pd.read_json(f"https://models-pc6dbtrtla-uc.a.run.app/{cases_or_deaths_str}/{number_of_days}/") #need number of days
else:
    state_str = region_selector.replace(' ', "%20")
    df = pd.read_json(f"https://api-pc6dbtrtla-uc.a.run.app/API/us/timeseries/{cases_or_deaths_str}/{state_str}")
    model_df = pd.read_json(f"https://models-pc6dbtrtla-uc.a.run.app/states/{cases_or_deaths_str}/{state_str}/{number_of_days}/") #need number of days
    

st.title(f"COVID 19 USA Data Dashboard - {region_selector}")

# Plot Test v1
upper_bound = go.Scatter(
    name='Upper Bound',
    x=model_df['ds'],
    y=model_df['yhat_upper'],
    mode='lines',
    marker=dict(color="#444"),
    line=dict(width=0),
    fillcolor='rgba(68, 68, 68, 0.3)',
    fill='tonexty')

trace = go.Scatter(
    name='Measurement',
    x=model_df['ds'],
    y=model_df['yhat'],
    mode='lines',
    line=dict(color='rgb(31, 119, 180)'),
    fillcolor='rgba(68, 68, 68, 0.3)',
    fill='tonexty')

lower_bound = go.Scatter(
    name='Lower Bound',
    x=model_df['ds'],
    y=model_df["yhat_lower"],
    marker=dict(color="#444"),
    line=dict(width=0),
    mode='lines')

# Plot layout with continuous error bars
data = [lower_bound, trace, upper_bound]

layout = go.Layout(
    yaxis=dict(title='Number of New Cases - By Day'),
    title=f"Number of New {cases_or_deaths} in {region_selector} - With Error Bars",
    showlegend = False)

fig = go.Figure(data=data, layout=layout)
st.plotly_chart(fig, filename='pandas-continuous-error-bars')

if region_selector == 'USA':
    st.write(df[["Country", "Totals as of Date", "Cases", "Deaths"]])
else:    
    st.write(df[["State", "Totals as of Date", "Cases", "Deaths"]])
