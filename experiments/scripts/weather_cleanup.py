import datetime
import os
import matplotlib.pyplot as plt
import csv
import pandas as pd


def plot(df: pd.DataFrame, path: str):

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


def no_nans():
    # if directory doesn't exist create it 'plots/features'
    path = 'datasets/wunderground_cleaned/'
    files = os.listdir(path)
    for file in files:
        if file.endswith('.csv'):
            df = pd.read_csv(path + file)
            print_nans(df)
            df = drop_nans(df)
            new_path = 'datasets/wunderground_cleaned_no_nans/'
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            # save the cleaned data
            df.to_csv(
                f'datasets/wunderground_cleaned_no_nans/{file}', index=False)


def convert_date():
    path = 'datasets/wunderground_cleaned_no_nans/'
    files = os.listdir(path)
    file = files[0]
    df = pd.read_csv(path + file)

    expire_time_gmt, valid_time_gmt = df['expire_time_gmt'], df['valid_time_gmt']
    # print first 5 rows
    print(expire_time_gmt.head())
    date_ts = expire_time_gmt[0]
    # just the first row
    expire_time_gmt, valid_time_gmt = expire_time_gmt[0], valid_time_gmt[0]
    # convert to year, month, day, hour, minute
    date = datetime.datetime.fromtimestamp(date_ts)
    print(date.year, date.month, date.day, date.hour, date.minute)

    print(date)
    # valid_time_gmt = pd.to_datetime(valid_time_gmt)
    # print(valid_time_gmt)


if __name__ == '__main__':

    # old path

    # no_nans(pd.DataFrame())
    convert_date()
