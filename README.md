## Flight Delays Predictions ML Model

### About this project:

Delayed flights can have significant negative economic impacts on airlines, airports, and passengers which motivates the creation of more robust 
delay management programs like the existing ground delay program. Our project consists of two parts: analyzing flight & weather datasets, 
and predicting flight delays. One dataset has a year’s worth of all US flight delay info [retrieved from Kaggle](https://www.kaggle.com/datasets/usdot/flight-delays?select=flights.csv/) and the other dataset has been gathered 
by web-scraping [weather site](https://www.wunderground.com/history/). We implemented a model to predict weather-induced airline delays using ML algorithm random Forest.


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
