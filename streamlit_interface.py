import streamlit as st
import pandas as pd
import requests

import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/wind_speed_laurel_nebraska.csv')

# Plotly template - With error bars - "Actual" data points to be added as well
upper_bound = go.Scatter(
    name='Upper Bound',
    x=df['Time'],
    y=df['10 Min Sampled Avg']+df['10 Min Std Dev'],
    mode='lines',
    marker=dict(color="#444"),
    line=dict(width=0),
    fillcolor='rgba(68, 68, 68, 0.3)',
    fill='tonexty')

trace = go.Scatter(
    name='Measurement',
    x=df['Time'],
    y=df['10 Min Sampled Avg'],
    mode='lines',
    line=dict(color='rgb(31, 119, 180)'),
    fillcolor='rgba(68, 68, 68, 0.3)',
    fill='tonexty')

lower_bound = go.Scatter(
    name='Lower Bound',
    x=df['Time'],
    y=df['10 Min Sampled Avg']-df['10 Min Std Dev'],
    marker=dict(color="#444"),
    line=dict(width=0),
    mode='lines')

# Trace order can be important
# with continuous error bars
data = [lower_bound, trace, upper_bound]

layout = go.Layout(
    yaxis=dict(title='Wind speed (m/s)'),
    title='Continuous, variable value error bars.<br>Notice the hover text!',
    showlegend = False)

fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='pandas-continuous-error-bars')


st.title("COVID 19 USA Data Dashboard")

state_list = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia","Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
state_selector = st.selectbox("Select State", state_list)

state_str = state_selector.replace(' ', "%20")
state_data_df = pd.read_json(f"https://api-pc6dbtrtla-uc.a.run.app/API/us/timeseries/{state_str}/allcounties")
st.write(state_data_df[["State", "Totals as of Date", "Cases", "Deaths"]])
    
