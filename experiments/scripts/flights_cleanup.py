import os
import matplotlib.pyplot as plt
import csv
import pandas as pd

'''
YEAR,MONTH,DAY,DAY_OF_WEEK,AIRLINE,FLIGHT_NUMBER,TAIL_NUMBER,ORIGIN_AIRPORT,DESTINATION_AIRPORT,SCHEDULED_DEPARTURE,DEPARTURE_TIME,DEPARTURE_DELAY,TAXI_OUT,WHEELS_OFF,SCHEDULED_TIME,ELAPSED_TIME,AIR_TIME,DISTANCE,WHEELS_ON,TAXI_IN,SCHEDULED_ARRIVAL,ARRIVAL_TIME,ARRIVAL_DELAY,DIVERTED,CANCELLED,CANCELLATION_REASON,AIR_SYSTEM_DELAY,SECURITY_DELAY,AIRLINE_DELAY,LATE_AIRCRAFT_DELAY,WEATHER_DELAY
2015,1,1,4,AS,98,N407AS,ANC,SEA,0005,2354,-11,21,0015,205,194,169,1448,0404,4,0430,0408,-22,0,0,,,,,,
2015,1,1,4,AA,2336,N3KUAA,LAX,PBI,0010,0002,-8,12,0014,280,279,263,2330,0737,4,0750,0741,-9,0,0,,,,,,
'''


def str_std(df_col: pd.Series):
    '''
    calculate the standard deviation of a string column, return the most common value
    '''

    return "N/A"


def str_mean(df_col: pd.Series):
    '''
    calculate the mean of a string column, return the most common value
    '''
    return "N/A"


def str_min(df_col: pd.Series):
    '''
    calculate the min of a string column, return the most common value
    '''
    tmp = df_col.value_counts()
    return tmp.index[len(tmp) - 1]


def str_max(df_col: pd.Series):
    '''
    calculate the max of a string column, return the most common value
    '''
    tmp = df_col.value_counts()
    return tmp.index[0]


# read the data, create a new csv file that holds the metadata. for each column print the column name and the number of unique values, data type, standard deviation, mean, min, max


def analyze(df: pd.DataFrame):
    with open('flights_metadata.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['column_name', 'data_type',
                        'nunique', 'std', 'mean', 'median', 'min', 'max', 'most_common_value', 'freq_most', 'least_common_value', 'freq_least'])  # write header

        for col in df.columns:
            if df[col].dtype == 'object':
                # string
                writer.writerow(
                    [col, 'string', df[col].nunique(), '', '', '', '', '', str_max(df[col]), df[col].value_counts().max(), str_min(df[col]), df[col].value_counts().min()])
            else:
                # numeric
                writer.writerow([col, 'number', df[col].nunique(), df[col].std(
                ), df[col].mean(), df[col].median(), df[col].min(), df[col].max(), '', '', '', ''])


def plot(df: pd.DataFrame, path: str = 'plots/flights_features/'):

    for col in df.columns:
        # replace nan with "N/A" for string columns
        if df[col].dtype == 'object':
            # string
            if not df[col].isnull().values.any():
                df[col] = df[col].fillna("N/A")

        # get the number of unique values in the column
        num_unique = df[col].nunique()

        value_counts = df[col].value_counts()
        fig, ax = plt.subplots()
        ax.bar(value_counts.index.astype(str), value_counts.values)
        ax.set_xlabel(col)
        ax.set_ylabel('Frequency')
        plt.xticks(rotation=90)
        # remove x axis labels if there are too many unique values
        if num_unique > 10:
            ax.set_xticklabels([])
        fig.savefig(f'{path}{col}.png')
        # close the figure to free up memory
        plt.close(fig)


# print the number of nans vs total number of values in each column
def print_nans(df: pd.DataFrame):
    for col in df.columns:
        print(
            f'{df[col].isnull().sum() / df[col].size * 100}% \t{col}: {df[col].isnull().sum()} / {df[col].size}: ')


# drop columns with more than 50% nans
def drop_nans(df: pd.DataFrame):
    for col in df.columns:
        if df[col].isnull().sum() / df[col].size > 0.5:
            df.drop(col, axis=1, inplace=True)
    return df
# drop rows with nans


def drop_rows_nans(df: pd.DataFrame):
    return df.dropna()


if __name__ == '__main__':
    # # if directory doesn't exist create it 'plots/features'
    # path = 'datasets/kaggle_cleaned/flights_cleaned.csv'
    # df = pd.read_csv(path)
    # # print_nans(pd.read_csv(path))
    # df = drop_nans(df)
    # df = drop_rows_nans(df)
    # print_nans(df)
    # df.to_csv('datasets/kaggle_cleaned/flights_cleaned_no_nans.csv', index=False)
    # exit()
    path = 'datasets/kaggle_cleaned/flights_cleaned_no_nans.csv'
    output_path = 'plots/kaggle_cleaned/flights_features/'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    df = pd.read_csv(path)
    # analyze(df)
    plot(df, output_path)
