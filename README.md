# Flight Delays Predictions ML Model

## About this project:

Delayed flights can have significant negative economic impacts on airlines, airports, and passengers which motivates the creation of more robust 
delay management programs like the existing ground delay program. Our project consists of two parts: analyzing flight & weather datasets, 
and predicting flight delays. One dataset has a year’s worth of all US flight delay info [retrieved from Kaggle](https://www.kaggle.com/datasets/usdot/flight-delays?select=flights.csv/) and the other dataset has been gathered.
by web-scraping [weather site](https://www.wunderground.com/history/). We implemented a model to predict weather-induced airline delays using ML algorithm random Forest.

## Video Demo

Click this link to go to the
[Youtube Video Demo](https://www.youtube.com/watch?v=45kfTg5ZabA)

## Description

This project contains 3 folders:

- experiments contains all python scripts used for webscrapping, data exploration, data analysis and machine learning models
- ml_model contains the script to create the Random Forest model used by the web application
- src contains two python scripts to run the the web application for analytics and prediction

## Installation

1. Install Python3 on local machine
2. Use the following commands to install necessary packages:

```python
pip install sklearn
pip install streamlit
pip install requests
pip install streamlit_lottie
pip install seaborn
```

## Execution

1. Navigate to code folder
2. Execute the following command: <code>streamlit run app_analytics.py</code>, this opens a web page on your local host that displays vizualiations related to our project
3. Execute the following command: <code>streamlit run app_prediction.py</code>, this opens an interactive user interface that allows the user to select predictor values then click on "predict" to get the prediction from the Machine Learning model.
4. It is important to note that there might "gray overlap" on the screen as the user makes selection  and a "running" icon  to the top right of the screen. The user can still continue to make selections even if the running icon is still active.

## Datasets & Files

- Original flights dataset from [Kaggle](https://www.kaggle.com/datasets/usdot/flight-delays?select=flights.csv/)
- Cleaned/transformed/merge dataset that contains fields related to weather and flight delays retrieve from [Georgia Tech Box 1](https://gatech.box.com/s/wuzelnupcqsr80o2ymcsj7my9a22w5mz)
- The dataset used to train the model contains 2.3 million of instances, 12 attributes (11 predictive attributes, 1 target variable). Retrieved from [Georgia Tech Box 2](https://gatech.box.com/s/1l6fqelru2hsfaebphxpvikvxa15bv5a)
- [flight_delay.pkl](https://gatech.box.com/s/afakemwcnac3hrhvj29fclh5w5tfbfkc) is a file to utilize a pre-trained ML model in Streamlit. 

## Tech:

- Python 3
- scikit-learn
- numpy
- pandas
- matplotlib
- seaborn
- pickle
- imblearn
- streamlit
- Tableau

## Authors:
Theodore Cox | Fidel Garcia | Winnie Messa | Wendy Navarrete
