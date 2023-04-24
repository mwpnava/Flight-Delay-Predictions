import pandas as pd
import os
from datetime import datetime

# Define the input and output file paths
flights_file = 'datasets/kaggle_cleaned/flights_cleaned_no_nans_ts.csv'
wunderground_folder = 'datasets/wunderground_cleaned_no_nans'
output_file = 'flights_w_weather.csv'
log_file = 'flight_w_weather.log'

# Define the columns to be mapped from flights.csv to wunderground csv
departure_col = 'ts_sch_dep'
arrival_col = 'ts_sch_arrival'
origin_col = 'ORIGIN_AIRPORT'
destination_col = 'DESTINATION_AIRPORT'

# Define the prefix for the columns containing weather data
src_prefix = 'SRC_'
dst_prefix = 'DST_'

# Define the columns to be copied from the wunderground csv
wunderground_cols = ['day_ind', 'temp', 'wx_icon', 'icon_extd', 'wx_phrase', 'pressure_tend',
                     'pressure_desc', 'dewPt', 'heat_index', 'rh', 'pressure', 'vis', 'wc',
                     'wdir', 'wdir_cardinal', 'gust', 'wspd', 'max_temp', 'min_temp',
                     'precip_total', 'precip_hrly', 'uv_desc', 'feels_like', 'uv_index', 'clds']

# Read the last row successfully processed from the log file
if os.path.exists(log_file):
    with open(log_file, 'r') as log:
        last_row = int(log.read().strip())
else:
    last_row = 0

# Load flights.csv into a pandas dataframe
flights_df = pd.read_csv(flights_file)

# Define a function to get the weather data for an airport and a given time


def get_weather_data(airport, time):
    try:
        file_path = os.path.join(wunderground_folder, airport + '.csv')
        wunderground_df = pd.read_csv(file_path)
        wunderground_df['valid_time_gmt'] = pd.to_datetime(
            wunderground_df['valid_time_gmt'], unit='s')
        wunderground_df = wunderground_df.set_index('valid_time_gmt')
        wunderground_data = wunderground_df.loc[time]
        wunderground_data.index = [
            src_prefix + col if 'Origin' in col else dst_prefix + col for col in wunderground_data.index]
        return wunderground_data
    except Exception as e:
        print(e)
        return None


# Map the departure and arrival times to the nearest hour
flights_df[departure_col] = pd.to_datetime(
    flights_df[departure_col], unit='s').dt.floor('H')
flights_df[arrival_col] = pd.to_datetime(
    flights_df[arrival_col], unit='s').dt.floor('H')

# Create empty columns for the weather data
for col in wunderground_cols:
    flights_df[src_prefix + col] = ''
    flights_df[dst_prefix + col] = ''

# Iterate over each row in flights_df
for i, row in flights_df.iterrows():
    print("{}/{} ({:.2f}%)".format(i, len(flights_df),
                                   i / len(flights_df) * 100), end="\r")
    # Skip rows that have already been processed
    if i < last_row:
        continue

    # Read the weather data for the origin and destination airports
    src_data = get_weather_data(row[origin_col], row[departure_col])
    dst_data = get_weather_data(row[destination_col], row[arrival_col])

    # Map the weather data to the flight dataframe
    flights_df.loc[i, [src_prefix +
                       col for col in wunderground_cols]] = src_data.values
    flights_df.loc[i, [dst_prefix +
                       col for col in wunderground_cols]] = dst_data.values

    # Write the last row successfully processed to the log file
    with open(log_file, 'w') as log:
        log.write(str(i))

# Write the flight dataframe to a csv file
flights_df.to_csv(output_file, index=False)
