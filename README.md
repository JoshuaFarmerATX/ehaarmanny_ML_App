
# Coronavirus COVID-19 Dashboard

Interactive dashboard to explore COVID-19 data from Johns Hopkins University and providing free API.
This project aims to predict the number of new daily cases and deaths of COVID-19 in USA.

### Link to the App: https://front-facing-pjblaypjta-uc.a.run.app/team
Note on Link: This was updated on 6.20.2020. Any old links to the application are no longer valid

### To run localy the predictions:
streamlit run streamlit_interface.py

### Update frequency:
To conserve resources on our google cloud, chron jobs have been temporarily disabled.

### Data Sources:
https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data

https://data.worldbank.org/indicator/sp.pop.65up.to.zs

https://api-pc6dbtrtla-uc.a.run.app/docs

### Model:
We used Prophet model developed by Facebook for producing forecasts for the future Covid-19 cases and deaths in the US.
More information about Prophet model can be found at https://facebook.github.io/prophet/.

### Technologies:
* Flask
* Flask SQLAlchemy
* Fast API
* Google Cloud Platform
* HTML and CSS
* JavaScript
* Jinja
* MySQL
* Plotly
* Postman
* Python 
* Prophet
* SQLAlchemy
* Streamlit 

### Github FastAPi
https://github.com/JoshuaFarmerATX/fastAPIPlayground.git


### Project Flowchart

![Page](P3_Operation.jpg)

### Project Team

Austin Spacek - Lead Developer <br />
Christopher Swanson - Lead Developer <br />
Daniela Matos - Backend Developer/Tester <br />
Ed Haarmann IV - Project Manager <br />
Josh Farmer - Frontend Developer <br />
Sinah Kang - Backend Developer/Tester
