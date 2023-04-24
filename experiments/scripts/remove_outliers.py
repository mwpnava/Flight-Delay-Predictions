import os
import numpy as np
import pandas as pd


def replace_outliers_with_nan(df, z=2):

    # Iterate over each column
    for i, col in enumerate(df.columns):
        print(
            f'Processing column: {col} {i+1}/{len(df.columns)} {round((i+1)/len(df.columns)*100, 2)}%')

        # if string
        if df[col].dtype == 'object':
            continue
        else:
            # if numeric
            # get the mean and standard deviation
            mean = df[col].mean()
            std = df[col].std()

            # calculate the z-score
            z_score = (df[col] - mean) / std

            # replace the outliers with nan
            df[col] = df[col].mask(np.abs(z_score) > z)

    return df

# remove nan


if __name__ == '__main__':

    # old path
    old_path = 'datasets/kaggle/flights.csv'
    # new path
    # make sure to create the new folder
    if not os.path.exists('datasets/kaggle_cleaned'):
        os.makedirs('datasets/kaggle_cleaned')
    new_path = 'datasets/kaggle_cleaned/flights_cleaned.csv'

    # Load data into a Pandas DataFrame
    df = pd.read_csv(old_path)

    # Remove outliers
    df = replace_outliers_with_nan(df)

    # remove each column that only has 1 unique value
    df = df.loc[:, df.nunique() != 1]

    # Save the cleaned DataFrame to a new file
    df.to_csv(new_path, index=False)
    print(df.head())

    # drop nan
    path = 'datasets/kaggle_cleaned/flights_cleaned.csv'
    new_path = 'datasets/kaggle_cleaned/flights_cleaned_no_nan.csv'
    df = pd.read_csv(path)
    df = df.dropna()
    df.to_csv(new_path,
              index=False)
