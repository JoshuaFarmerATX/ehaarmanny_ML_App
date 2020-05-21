import pandas as pd
import numpy as np
import requests 
import matplotlib.pyplot as plt
import datetime 
from fbprophet import Prophet 
from fbprophet.diagnostics import cross_validation
from fbprophet.diagnostics import performance_metrics
from fbprophet.plot import plot_cross_validation_metric

from fbprophet.plot import plot_plotly
import plotly.offline as py

### Import data 
df = pd.read_json("https://api-pc6dbtrtla-uc.a.run.app/API/timeseries/usa")
df = df.rename(columns={'Totals as of Date': 'Date'})
df['Date'] = pd.to_datetime(df['Date']).dt.date
df['NewCases'] = df['Cases'] - df['Cases'].shift(1)
df['NewDeaths'] = df['Deaths'] - df['Deaths'].shift(1)

df_cases = df.loc[df["Date"]>=datetime.date(2020,4,1)]
df_deaths = df.loc[df["Date"]>=datetime.date(2020,4,8)]

df_cases_fb = df_cases[["Date", "NewCases"]].rename(columns={"Date": "ds", "NewCases": "y"})
df_deaths_fb = df_deaths[["Date", "NewDeaths"]].rename(columns={"Date": "ds", "NewDeaths": "y"})

### Predicting  
def predict(df, days):

    prophet = Prophet()
    prophet.fit(df)

    future = prophet.make_future_dataframe(periods=days)
    forecast = prophet.predict(future)
    df_forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].set_index('ds')
    df_forecast = df_forecast.round(0)
    # fig_forecast = prophet.plot(forecast)
    fig_forecast = plot_plotly(prophet, forecast)  
    
    return df_forecast

### Cross validation 
def cross_validate(df):

    prophet = Prophet()
    prophet.fit(df)

    df_cv = cross_validation(prophet, initial='30 days', period='4 days', horizon='7 days')
    df_performance = performance_metrics(df_cv)
    fig_performance = plot_cross_validation_metric(df_cv, metric='mape')

    return plt.show()

print(predict(df_cases_fb, 7))