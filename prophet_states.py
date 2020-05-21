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


### Preprocessing 
def prepdata_cases(state):
    
    state_str = state.replace(' ', "%20")
    df = pd.read_json(f"http://api-pc6dbtrtla-uc.a.run.app/API/us/timeseries/totals/{state_str}")
    df = df.rename(columns={'Totals as of Date': 'Date'})
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df['NewCases'] = df['Cases'] - df['Cases'].shift(1)

    df_cases = df.loc[df["Date"]>=datetime.date(2020,3,11)]
    df_cases = df_cases[["Date", "NewCases"]].rename(columns={"Date": "ds", "NewCases": "y"})

    return df_cases

def prepdata_deaths(state):

    state_str = state.replace(' ', "%20")
    df = pd.read_json(f"http://api-pc6dbtrtla-uc.a.run.app/API/us/timeseries/totals/{state_str}")
    df = df.rename(columns={'Totals as of Date': 'Date'})
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df['NewDeaths'] = df['Deaths'] - df['Deaths'].shift(1)
    
    df_deaths = df.loc[df["Date"]>=datetime.date(2020,3,11)]
    df_deaths = df_deaths[["Date", "NewDeaths"]].rename(columns={"Date": "ds", "NewDeaths": "y"})
    
    return df_deaths

### Predicting  
def predict_cases(state, days):

    df = prepdata_cases(state)

    prophet = Prophet()
    prophet.fit(df)

    future = prophet.make_future_dataframe(periods=days)
    forecast = prophet.predict(future)
    df_forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    df_forecast = df_forecast.assign(yhat = lambda df: df['yhat'].apply(lambda e: max(0, e))).assign(yhat_lower = lambda df: df['yhat_lower'].apply(lambda e: max(0, e))).assign(yhat_upper = lambda df: df['yhat_upper'].apply(lambda e: max(0, e)))
    fig_forecast = prophet.plot(forecast)

    return df_forecast

def predict_deaths(state, days):

    df = prepdata_deaths(state)

    prophet = Prophet()
    prophet.fit(df)

    future = prophet.make_future_dataframe(periods=days)
    forecast = prophet.predict(future)
    df_forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    df_forecast = df_forecast.assign(yhat = lambda df: df['yhat'].apply(lambda e: max(0, e))).assign(yhat_lower = lambda df: df['yhat_lower'].apply(lambda e: max(0, e))).assign(yhat_upper = lambda df: df['yhat_upper'].apply(lambda e: max(0, e)))
    fig_forecast = prophet.plot(forecast)

    return df_forecast

### Cross-validation
def cv_cases(state):

    df = prepdata_cases(state)

    prophet = Prophet()
    prophet.fit(df)

    df_cv = cross_validation(prophet, initial='50 days', period='4 days', horizon='7 days')
    df_performance = performance_metrics(df_cv)
    fig_performance = plot_cross_validation_metric(df_cv, metric='mape')

    return plt.show()

def cv_deaths(state):

    df = prepdata_deaths(state)

    prophet = Prophet()
    prophet.fit(df)

    df_cv = cross_validation(prophet, initial='50 days', period='4 days', horizon='7 days')
    df_performance = performance_metrics(df_cv)
    fig_performance = plot_cross_validation_metric(df_cv, metric='mape')

    return plt.show()

print(predict_cases("New York", 7))