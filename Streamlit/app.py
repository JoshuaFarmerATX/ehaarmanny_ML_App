import streamlit as st
import pandas as pd
import requests

# Plotly imports
import plotly.plotly as py
import plotly.graph_objs as go


# US Cases Model: https://models-pc6dbtrtla-uc.a.run.app/cases/#/
# US Deaths Model: https://models-pc6dbtrtla-uc.a.run.app/deaths/#/
# Model for Cases for a State: https://models-pc6dbtrtla-uc.a.run.app/states/cases/STATE/#/
# Model for Deaths for a State: https://models-pc6dbtrtla-uc.a.run.app/states/deaths/STATE/#


region_list = ["USA", "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia","Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
region_selector = st.sidebar.selectbox("Select Region", region_list)
number_of_days = st.sidebar.number_input("Predict Number of Days:", min_value=1, max_value=30, value=1, step=1)
cases_or_deaths = st.sidebar.selectbox("Deaths or Cases:", ["Cases", "Deaths"])

@st.cache
def return_raw_data(region):
    df = pd.DataFrame()
    if region_selector == 'USA':
        df = pd.read_json(f"https://api-pc6dbtrtla-uc.a.run.app/API/timeseries/{region}")
    else:
        state_str = region.replace(' ', "%20")
        df = pd.read_json(f"https://api-pc6dbtrtla-uc.a.run.app/API/us/timeseries/totals/{state_str}")
    return df

@st.cache
def return_model_data(region, days, cases_or_deaths_str):
    df = pd.DataFrame()
    if region_selector == 'USA':
        df = pd.read_json(f"https://models-pc6dbtrtla-uc.a.run.app/{cases_or_deaths_str}/{days}/") #need number of days
    else:
        state_str = region.replace(' ', "%20")
        df = pd.read_json(f"https://models-pc6dbtrtla-uc.a.run.app/states/{cases_or_deaths_str}/{state_str}/{days}/") #need number of days
    return df


df = return_raw_data(region_selector)

model_df = return_model_data(region_selector, number_of_days, cases_or_deaths.lower())

st.title(f"COVID 19 Projected Number of {cases_or_deaths} in {region_selector} for the Next {number_of_days} Day(s)")

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
    yaxis=dict(title=f"Number of New {cases_or_deaths} - By Day"),
    title=f"Number of New {cases_or_deaths} in {region_selector} - With Error Bars",
    showlegend = False)

fig = go.Figure(data=data, layout=layout)
st.plotly_chart(fig, filename='pandas-continuous-error-bars', use_container_width=True)

st.title(f"{region_selector} - Cumulative Raw Data") 
if region_selector == 'USA':
    st.table(df[["Country", "Totals as of Date", "Cases", "Deaths"]].sort_values(by="Totals as of Date", ascending=False))
else:    
    st.table(df[["State", "Totals as of Date", "Cases", "Deaths"]].sort_values(by="Totals as of Date", ascending=False))
