### Dependencies
from flask import Flask
import pandas as pd
import requests
from sqlalchemy import create_engine
import datetime
from mySQLCredentials import *

### USA Covid19 Data
# USA confirmed cases
usa_confirmed_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
usa_confirmed_df = pd.read_csv(usa_confirmed_url)
usa_confirmed_df.drop(
    ["UID", "iso2", "iso3", "code3", "FIPS", "Combined_Key"], axis=1, inplace=True
)
usa_confirmed_df = usa_confirmed_df.melt(
    id_vars=["Country_Region", "Province_State", "Admin2", "Lat", "Long_"]
)
usa_confirmed_df = usa_confirmed_df.rename(
    columns={
        "Country_Region": "country_region",
        "Province_State": "province_state",
        "Admin2": "county_city",
        "Lat": "lat",
        "Long_": "long",
        "variable": "date",
        "value": "confirmed",
    }
)

# USA deaths
usa_deaths_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"
usa_deaths_df = pd.read_csv(usa_deaths_url)
usa_deaths_df.drop(
    ["UID", "iso2", "iso3", "code3", "FIPS", "Combined_Key", "Population"],
    axis=1,
    inplace=True,
)
usa_deaths_df = usa_deaths_df.melt(
    id_vars=["Country_Region", "Province_State", "Admin2", "Lat", "Long_"]
)
usa_deaths_df = usa_deaths_df.rename(
    columns={
        "Country_Region": "country_region",
        "Province_State": "province_state",
        "Admin2": "county_city",
        "Lat": "lat",
        "Long_": "long",
        "variable": "date",
        "value": "deaths",
    }
)

# Merge USA dataframes
usa_df = pd.merge(usa_confirmed_df, usa_deaths_df, how="outer")
usa_df = usa_df.drop_duplicates()
usa_df["date"] = pd.to_datetime(usa_df["date"]).dt.date
usa_df["confirmed"] = usa_df["confirmed"].fillna(0)
usa_df["deaths"] = usa_df["deaths"].fillna(0)

# Connect to the "covid19" database in Google Cloud SQL
HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = myUsername
PASSWORD = myPassword
DIALECT = "mysql"
DRIVER = "pymysql"
DATABASE = "Covid"

connection_string = (
    f"{DIALECT}+{DRIVER}://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"
)
engine = create_engine(connection_string)

# Create "global_covid19" and "usa_covid19" tables in the "covid19" database
usa_df.to_sql(con=engine, name="usa_covid19", if_exists="replace")
