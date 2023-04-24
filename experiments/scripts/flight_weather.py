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




import pandas as pd
def find_closest_timestamp(df: pd.DataFrame, timestamp: int, column_name: str) -> int:
    '''
    df: pandas dataframe
    timestamp: timestamp to find the closest to
    column_name: column name of the timestamp in the dataframe
    '''
    df['diff'] = df[column_name] - timestamp
    df['diff'] = df['diff'].abs()
    return df['diff'].idxmin()


# take a flight df and make a new csv for each unique origin airport
def make_weather_csvs(flight_df: pd.DataFrame):
    new_columns = ['expire_time_gmt', 'valid_time_gmt', 'day_ind', 'temp', 'wx_icon', 'icon_extd', 'wx_phrase', 'dewPt', 'heat_index',
                   'rh', 'pressure', 'vis', 'wc', 'wdir_cardinal', 'wspd', 'uv_desc', 'feels_like', 'uv_index', 'clds']  # 'precip_hrly'

    # add s_ and d_ to the new columns
    s_new_columns = ['s_' + column for column in new_columns]
    d_new_columns = ['d_' + column for column in new_columns]
    new_columns = s_new_columns + d_new_columns

    c = 0
    e_c = 0
    columns = ['ORIGIN_AIRPORT', 'DESTINATION_AIRPORT']
    len_flight_df = len(flight_df)
    for i, column_name in enumerate(columns):
        # get the unique origin airports
        airports = flight_df[column_name].unique()
        # make a new csv for each airport
        for j, airport in enumerate(airports):
            tmp_df = flight_df[flight_df[column_name] == airport]
            df_weather = pd.read_csv(
                'datasets/wunderground_cleaned_no_nans_round_by_hour/' + airport + '.csv')
            # for each row in the flight df, find the closest timestamp in the weather df
            for k, row in tmp_df.iterrows():
                # get the closest timestamp in the weather df
                closest_timestamp = find_closest_timestamp(
                    df_weather, row['ts_sch_dep'], 'valid_time_gmt')
                # set the weather values in the flight df
                if column_name == 'ORIGIN_AIRPORT':
                    for l, column in enumerate(s_new_columns):
                        try:
                            # link the weather values to the departure airport with 's_'
                            flight_df.loc[k, 's_' +
                                          column] = df_weather.loc[closest_timestamp, column]
                        except:
                            e_c += 1
                else:
                    for l, column in enumerate(d_new_columns):
                        try:
                            # link the weather values to the arrival airport with 'd_'
                            flight_df.loc[k, 'd_' +
                                          column] = df_weather.loc[closest_timestamp, column]
                        except:
                            e_c += 1
                c += 1
                if c % 100 == 0:
                    print(
                        f'{c}/{len(flight_df)} ({round(c/len_flight_df*1000, 2)}%) \t {e_c} errors, {column_name} {airport} {j}/{len(airports)}', end='\r')

            # delete tmp_df
            del tmp_df
    return flight_df

    # write the new flight df to a csv
    flight_df.to_csv('flight_weather.csv', index=False)


# def remove item not in list
def remove_from_df_not_in_list(df: pd.DataFrame, column_name: str, list: list):
    df = df[df[column_name].isin(list)]
    return df


if __name__ == '__main__':

    # # read the flight df
    # flight_df = pd.read_csv(
    #     'datasets/kaggle_cleaned/flights_cleaned_no_nans_ts.csv')
    # # get the unique origin airports *.csv files inf wunderground_cleaned_no_nans_round_by_hour
    # airports = os.listdir(
    #     'datasets/wunderground_cleaned_no_nans_round_by_hour')
    # airports = [airport.split('.')[0] for airport in airports]

    # # remove the flights that are not in the wunderground_cleaned_no_nans_round_by_hour folder
    # flight_df = remove_from_df_not_in_list(
    #     flight_df, 'ORIGIN_AIRPORT', airports)
    # flight_df = remove_from_df_not_in_list(
    #     flight_df, 'DESTINATION_AIRPORT', airports)

    # # save the new flight df
    # flight_df.to_csv('datasets/kaggle_cleaned/flights_3.csv', index=False)

    flight_df = pd.read_csv(
        'datasets/kaggle_cleaned/flights_3.csv')

    make_weather_csvs(flight_df)
