''' .csv format of the wunderground files
expire_time_gmt,valid_time_gmt,day_ind,temp,wx_icon,icon_extd,wx_phrase,dewPt,heat_index,rh,pressure,vis,wc,wdir_cardinal,wspd,precip_hrly,uv_desc,feels_like,uv_index,clds
1420182000,1420174800,N,29.0,29.0,2900.0,Partly Cloudy,15.0,29.0,56.0,29.6,10.0,22.0,SSW,7.0,0.0,Low,22.0,0,CLR
1420185600,1420178400,N,30.0,33.0,3300.0,Fair,16.0,30.0,56.0,29.61,10.0,23.0,SSW,7.0,0.0,Low,23.0,0,CLR
'''

''' .csv format of the flight.csv file
MONTH,DAY,DAY_OF_WEEK,AIRLINE,FLIGHT_NUMBER,TAIL_NUMBER,ORIGIN_AIRPORT,DESTINATION_AIRPORT,SCHEDULED_DEPARTURE,DEPARTURE_TIME,DEPARTURE_DELAY,TAXI_OUT,WHEELS_OFF,SCHEDULED_TIME,ELAPSED_TIME,AIR_TIME,DISTANCE,WHEELS_ON,TAXI_IN,SCHEDULED_ARRIVAL,ARRIVAL_TIME,ARRIVAL_DELAY,ts_sch_dep,ts_sch_arrival
1,1,4,B6,730.0,N621JB,BQN,MCO,419.0,423.0,4.0,11.0,434.0,174.0,163.0,148.0,1129.0,602.0,4.0,613.0,606.0,-7.0,1420107540,1420114380
1,1,4,B6,768.0,N317JB,PSE,MCO,424.0,413.0,-11.0,24.0,437.0,186.0,196.0,166.0,1179.0,623.0,6.0,630.0,629.0,-1.0,1420107840,1420115400
'''

''' new columns in the flight_weather.csv file
s_expire_time_gmt,s_valid_time_gmt, s_day_ind, s_temp, s_wx_icon, s_icon_extd, s_wx_phrase, s_dewPt, s_heat_index, s_rh, s_pressure, s_vis, s_wc, s_wdir_cardinal, s_wspd, s_precip_hrly, s_uv_desc, s_feels_like, s_uv_index, s_clds
d_expire_time_gmt, d_valid_time_gmt, d_day_ind, d_temp, d_wx_icon, d_icon_extd, d_wx_phrase, d_dewPt, d_heat_index, d_rh, d_pressure, d_vis, d_wc, d_wdir_cardinal, d_wspd, d_precip_hrly, d_uv_desc, d_feels_like, d_uv_index, d_clds
'''




import time
import pandas as pd
import os
def find_closest_timestamp(df, timestamp, column_name):
    '''
    df: pandas dataframe
    timestamp: timestamp to find the closest to
    column_name: column name of the timestamp in the dataframe
    '''
    df['diff'] = df[column_name] - timestamp
    df['diff'] = df['diff'].abs()
    return df['diff'].idxmin()


# create a new file with the same columns as the flight.csv file
# add the new columns to the flight_weather.csv file
# use the 'ts_sch_dep' and 'ts_sch_arrival' columns to find the closest 'expire_time_gmt' and 'valid_time_gmt' columns


# get list of ts from 'ts_sch_dep' and 'ts_sch_arrival' columns
def get_ts_list(df, column_name):
    return df[column_name].unique()

# go through the weather files and find the closest timestamp for each flight write to new file


def write_to_file(df_flights):

    # # organize df by 'ORIGIN_AIRPORT', alphabetically
    # df_flights = df_flights.sort_values(by=['ORIGIN_AIRPORT'])
    # get list of unique origin airports

    # print df shape
    print(df_flights.shape)

    origin_airports = df_flights['ORIGIN_AIRPORT'].unique()
    # to list
    origin_airports = list(origin_airports)

    # get list of iata codes in   wunderground__cleaned_no_nans_round_by_hour folder
    lst_files = os.listdir(
        'datasets/wunderground_cleaned_no_nans_round_by_hour')
    lst_iata_codes = []
    for file in lst_files:
        lst_iata_codes.append(file.split('.')[0])

    # for every airport in origin_airports, check if it is in lst_iata_codes
    # if not, remove it from origin_airports
    for airport in origin_airports:
        if airport not in lst_iata_codes:
            origin_airports.remove(airport)

    # print number of origin airports
    print(f'origin_airports: {len(origin_airports)}')
    # save to txt file
    with open('origin_airports.txt', 'w') as f:
        for airport in origin_airports:
            f.write(str(airport) + '\n')

    print('origin_airports saved to file')

    # keep only the airports that are in lst_iata_codes
    df_flights = df_flights[df_flights['ORIGIN_AIRPORT'].isin(origin_airports)]
    print(df_flights.shape)
    # do the same for destination airports
    destination_airports = df_flights['DESTINATION_AIRPORT'].unique()
    # print df shape
    print(df_flights.shape)
    # save to csv file
    df_flights.to_csv('datasets/kaggle/new/flights2.csv', index=False)

    exit()

    if not os.path.exists('datasets/kaggle/split_by_origin_airport'):
        os.makedirs('datasets/kaggle/split_by_origin_airport')

    lst_errors = []

    # go through each origin airport
    for i, airport in enumerate(origin_airports):
        try:
            # if file already exists, skip
            if os.path.exists('datasets/kaggle/split_by_origin_airport/' + airport+'.csv'):
                continue

            print(
                f'{i+1}/{len(origin_airports)} ({100*((i+1)/len(origin_airports)):.2f})%', end='\r')
            # get df for that airport
            df = df_flights[df_flights['ORIGIN_AIRPORT'] == airport]
            # save df to csv with name of airport.csv
            # to folder 'datasets/kaggle/split_by_origin_airport'
            df.to_csv('datasets/kaggle/split_by_origin_airport/' +
                      airport+'.csv', index=False)

        except Exception as e:
            lst_errors.append(e)

    print(f'{len(lst_errors)} errors')
    print(lst_errors)


if __name__ == '__main__':

    f = 'datasets/kaggle/new/flights.csv'  # _no_nans_ts.csv'

    # test write_to_file def
    df_flights = pd.read_csv(f)
    write_to_file(df_flights)

    exit()
    import os
    weather_folder = 'datasets/wunderground_cleaned_no_nans_round_by_hour'
    flight_file = 'datasets/kaggle_cleaned/flights_cleaned_no_nans_ts.csv'
    output_file = 'datasets/kaggle_cleaned/flights_weather.csv'
    log_file = 'datasets/kaggle_cleaned/flight_weather.log'

    weather_files = os.listdir(weather_folder)
    # remove files with -1.csv in the name
    weather_files = [file for file in weather_files if '-1.csv' not in file]
    # remove files with flights_cleaned_no_nans_ts.csv in the name
    weather_files = [
        file for file in weather_files if 'flights_cleaned_no_nans_ts.csv' not in file]

    dict_weather = {}
    for file in weather_files:
        airport = file.split('.')[0]
        df = pd.read_csv(weather_folder + '/' + file)
        dict_weather[airport] = df

    current_line = 0
    if log_file in os.listdir():
        with open(log_file, 'r') as f:
            current_line = int(f.readline())

    df_flights = pd.read_csv(flight_file)
    time_current = time.time()

    length = len(df_flights)
    for i, flight in df_flights.iterrows():
        try:

            if i < current_line:
                continue

            # make a copy of the flight dataframe at that row
            tmp_flight = df_flights.iloc[i:i+1].copy()

            # flight iteration, total flights, percentage, estimated time remaining
            # every 100 flights, print the time remaining
            if i % 10 == 0:
                print(
                    f'flight {i}/{len(df_flights)} - {i/length*100: .2f} \
                - {(time.time() - time_current)*(length-i)/60: .2f} min remaining', end='\r')

            time_current = time.time()

            df_weather_origin = dict_weather[flight['ORIGIN_AIRPORT']]
            df_weather_destination = dict_weather[flight['DESTINATION_AIRPORT']]

            # find the closest 'expire_time_gmt' and 'valid_time_gmt' columns
            ts_sch_dep = flight['ts_sch_dep']
            ts_sch_arrival = flight['ts_sch_arrival']

            try:
                closest_origin_time = find_closest_timestamp(
                    df_weather_origin, ts_sch_dep, 'valid_time_gmt')
            except:
                continue

            try:
                closest_destination_time = find_closest_timestamp(
                    df_weather_destination, ts_sch_arrival, 'valid_time_gmt')
            except:
                continue

            # add the new columns to the flight_weather.csv file
            for col in df_weather_origin.columns:
                try:
                    tmp_flight['s_' +
                               col] = df_weather_origin.loc[closest_origin_time, col]
                except:
                    pass
                try:
                    tmp_flight['d_' +
                               col] = df_weather_destination.loc[closest_destination_time, col]
                except:
                    pass

            # override row of df_flights with the new columns
            df_flights.iloc[i:i+1] = tmp_flight

        except Exception as e:
            continue

    # save the new file
    df_flights.to_csv(output_file, index=False)
    print('done')
