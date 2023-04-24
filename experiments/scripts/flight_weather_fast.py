import os
import pandas as pd
import numpy as np


def make_simple_df(flight_df: pd.DataFrame, columns_to_keep: list) -> pd.DataFrame:
    # make a new df with only the columns we want, index old df and new df with the same number
    new_df = flight_df[columns_to_keep].copy()
    new_df.index = flight_df.index

    # remove all columns that are not in the list
    columns_to_remove = [
        column for column in flight_df.columns if column not in columns_to_keep]
    flight_df.drop(columns_to_remove, axis=1, inplace=True)

    # save the new df
    return new_df


# get closest timestamp
def get_closest_timestamp(df: pd.DataFrame, timestamp: int, column_name: str) -> int:
    # get the closest timestamp
    closest_timestamp = df[column_name].sub(timestamp).abs().idxmin()
    return closest_timestamp

# add weather data to the flight df


def add_weather_data(flight_df: pd.DataFrame, path_weather: str):
    w_data = {}
    lst_files = os.listdir(path_weather)
    for file in lst_files:
        w_data[file.split('.')[0]] = pd.read_csv(path_weather + file)

    new_columns = ['expire_time_gmt', 'valid_time_gmt', 'day_ind', 'temp', 'wx_icon', 'icon_extd', 'wx_phrase', 'dewPt', 'heat_index',
                   'rh', 'pressure', 'vis', 'wc', 'wdir_cardinal', 'wspd', 'uv_desc', 'feels_like', 'uv_index', 'clds']  # 'precip_hrly'

    # iterate through df and add weather data
    for i, row in flight_df.iterrows():
        s_w_row = get_closest_timestamp(w_data[flight_df['ORIGIN_AIRPORT'][i]],
                                        flight_df['ts_sch_dep'][i], 'valid_time_gmt')
        d_w_row = get_closest_timestamp(w_data[flight_df['DESTINATION_AIRPORT'][i]],
                                        flight_df['ts_sch_arrival'][i], 'valid_time_gmt')

        for column in new_columns:
            flight_df.at[i, 'o_' + column] = w_data[flight_df['ORIGIN_AIRPORT']
                                                    [i]][column][s_w_row]
            flight_df.at[i, 'd_' + column] = w_data[flight_df['DESTINATION_AIRPORT']
                                                    [i]][column][d_w_row]

        if i % 10000 == 0:
            print(f'{i}/{len(flight_df)} ({i/len(flight_df)*100:.2f}%)', end='\r')

    return flight_df


if __name__ == '__main__':
    # flight_df = pd.read_csv('datasets/kaggle_cleaned/flights_3.csv')

    # columns_to_keep = ['ORIGIN_AIRPORT',
    #                    'DESTINATION_AIRPORT', 'ts_sch_dep', 'ts_sch_arrival']

    # new_df = make_simple_df(flight_df, columns_to_keep)
    # new_df.to_csv('datasets/kaggle_cleaned/flights_4.csv', index=False)
    flight_df = pd.read_csv('datasets/kaggle_cleaned/flights_4.csv')
    flight_df = add_weather_data(
        flight_df, 'datasets/wunderground_cleaned_no_nans_round_by_hour/')
    flight_df.to_csv('datasets/kaggle_cleaned/flights_5.csv', index=False)
