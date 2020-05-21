import streamlit as st
import pandas as pd
import requests

# Plotly imports
import plotly.plotly as py
import plotly.graph_objs as go

# Will include code for caching here from streamlit template - as seen in previous version/commit

# Plot Title for New York csv (will incorporate api data when redeployed)
st.title("COVID 19 USA Data Dashboard - New York Test")

ny_df = pd.read_csv('NewYork.csv')

# Plot Test v1
upper_bound = go.Scatter(
    name='Upper Bound',
    x=ny_df['ds'],
    y=ny_df['yhat_upper'],
    mode='lines',
    marker=dict(color="#444"),
    line=dict(width=0),
    fillcolor='rgba(68, 68, 68, 0.3)',
    fill='tonexty')

trace = go.Scatter(
    name='Measurement',
    x=ny_df['ds'],
    y=ny_df['yhat'],
    mode='lines',
    line=dict(color='rgb(31, 119, 180)'),
    fillcolor='rgba(68, 68, 68, 0.3)',
    fill='tonexty')

lower_bound = go.Scatter(
    name='Lower Bound',
    x=ny_df['ds'],
    y=ny_df["yhat_lower"],
    marker=dict(color="#444"),
    line=dict(width=0),
    mode='lines')

# Plot layout with continuous error bars
data = [lower_bound, trace, upper_bound]

layout = go.Layout(
    yaxis=dict(title='Number of New Cases - By Day'),
    title='Number of New Cases in New York - With Error Bars',
    showlegend = False)

fig = go.Figure(data=data, layout=layout)
st.plotly_chart(fig, filename='pandas-continuous-error-bars')

# Raw data table with state selector - throwing error (will be addressed next)
state_list = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia","Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
state_selector = st.selectbox("Select State", state_list)

state_str = state_selector.replace(' ', "%20")
state_data_df = pd.read_json(f"https://api-pc6dbtrtla-uc.a.run.app/API/us/timeseries/{state_str}/allcounties")
st.write(state_data_df[["State", "Totals as of Date", "Cases", "Deaths"]])

