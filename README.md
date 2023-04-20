## Flight Delays Predictions ML Model

### About this project:

Delayed flights can have significant negative economic impacts on airlines, airports, and passengers which motivates the creation of more robust 
delay management programs like the existing ground delay program. Our project consists of two parts: analyzing flight & weather datasets, 
and predicting flight delays. One dataset has a year’s worth of all US flight delay info [retrieved from Kaggle](https://www.kaggle.com/datasets/usdot/flight-delays?select=flights.csv/) and the other dataset has been gathered 
by web-scraping [weather site](https://www.wunderground.com/history/). We implemented a model to predict weather-induced airline delays using ML algorithm random Forest.

### Description
This project contains 3 folders:
- Experiments contains all the code that allow us to analyze the dataset, perform web scrapping and make informed decisions about the project (Tableau instead of Python script, use sample datasets instead of large dataset, Mapping airline and airports names with ML code)
- ML_model contains the code related to Random Forest algorithm to make predictions
- Web_app contains the files necessary to run the web application

### Installation
1. Install Python3 on local machine
2. Use the following commands to install necessary packages:  <code> pip install streamlit </code>, <code>pip install request</code>, <code>pip install streamlit_lottie </code>


### Execution
1. Navigate to web_app folder
2. Execute the following command: streamlit run app_analytics.py, this opens a web page on your local host that displays vizualiations related to our project
3. Execute the following command: streamlit run app_prediction.py, this opens an interactive user interface that allows the user to select predictor values then click on "predict" to get the prediction from the Machine Learning model

### Datasets & Files
- Original flights dataset from [Kaggle](https://www.kaggle.com/datasets/usdot/flight-delays?select=flights.csv/)
- Cleaned/transformed/merge dataset that contains ... retrieve from [Georgia Tech Box 1](https://gatech.box.com/s/wuzelnupcqsr80o2ymcsj7my9a22w5mz)
- The dataset used to train the model contains 2.3 million of instances, 12 attributes (11 predictive attributes, 1 target variable). Retrieved from [Georgia Tech Box 2](https://gatech.box.com/s/1l6fqelru2hsfaebphxpvikvxa15bv5a)
- [flight_delay.pkl](https://gatech.box.com/s/afakemwcnac3hrhvj29fclh5w5tfbfkc) is a file to utilize a pre-trained ML model in Streamlit. 

### Tech:

- Python 3
- scikit-learn - Linear Regression
- numpy
- pandas
- matplotlib
- seaborn
- pickle
- imblearn
- streamlit
- Tableau

### Authors:
Theodore Cox | Fidel Garcia | Winnie Messa | Wendy Navarrete
