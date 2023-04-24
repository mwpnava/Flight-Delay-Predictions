import datetime
import json
import os
import pandas as pd
import requests


class WeatherObservation():
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            # for every key, create an attribute with the same name, that is a list, then append the value to the list
            setattr(self, key, [value])

    # add to the list of values for the attribute
    def add_value(self, **kwargs):
        for key, value in kwargs.items():
            getattr(self, key).append(value)

    def to_dict(self):
        return self.__dict__


def get_icao_code_loc_id(iata_code: str) -> tuple:

    icao_code = 'K' + iata_code  # TODO: implement a better way to get icao code
    s = requests.session()
    try:
        # iata_code = 'JFK'
        # get 'wunderground_api_key' from environment variables
        api_key = os.environ.get('wunderground_api_key')
        res = s.get("https://api.weather.com/v3/location/search", params={"apiKey": api_key,
                    "language": "en-US", "query": icao_code, "locationType": "airport", "format": "json"})
        res = res.json()

        # get index of iatacode
        try:
            index = res['location']['iataCode'].index(iata_code)
        except:
            index = res['location']['iacoCode'].index(icao_code)
        # icao_code = res['location']['icaoCode'][index_iata].upper()
        loc_id = res['location']['locId'][index]
    except:
        print(f"Error: {iata_code} not found")
    s.close()

    return icao_code, loc_id


# create a list of date object for 1st Jan 2015 to 31st Dec 2015
def create_date_list(year: int):
    if not isinstance(year, int):
        raise TypeError('year must be an integer')

    date_list = []
    for year in range(year, year + 1):
        for month in range(1, 13):
            for day in range(1, 32):
                try:
                    date_list.append(datetime.date(year, month, day))
                except ValueError:
                    pass

    return date_list


# remove key from dict if value doesn't change
def remove_constant_keys(d: dict) -> dict:
    keys_to_remove = []
    for key, value in d.items():
        if isinstance(value, dict):
            value = remove_constant_keys(value)
        else:
            if isinstance(value, list):
                if all(x == value[0] for x in value):
                    keys_to_remove.append(key)
            else:
                keys_to_remove.append(key)
    d = {k: v for k, v in d.items() if k not in keys_to_remove}
    return d


if __name__ == '__main__':

    print('This script takes hours to run, and is not needed to run the app. Since it has already been ran.')
    print('dataset should be located in "datasets/wunderground" folder.')
    raise Exception('Comment out this line to run it.')

    dates = create_date_list(2015)

    main_dict = {}
    main_dict['airports'] = []
    # read 'datasets/kaggle/airports.csv' into a dataframe
    airports_df = pd.read_csv('datasets/kaggle/airports.csv')
    try:
        for a, row in airports_df.iterrows():

            iata_code = airports_df['IATA_CODE'].values[a]
            main_dict['airports'].append(iata_code)
            main_dict[iata_code] = {}
            try:

                iata_annual_weather_data = {}
                iata_annual_weather_data['iata_code'] = iata_code
                iata_annual_weather_data['csv'] = ""
                iata_annual_weather_data['status'] = ""
                icao_code, loc_id = get_icao_code_loc_id(iata_code)
                iata_annual_weather_data['icao_code'] = icao_code
                iata_annual_weather_data['loc_id'] = loc_id

                loc_id = '9:US'
                loc_id = ':'.join(loc_id.split(':')[-2:])
                api_key = os.environ.get('wunderground_api_key')

                for i, day in enumerate(dates):
                    # print iota code and day on the same line, remove newline, flush buffer
                    print(f"{iata_code} {day.strftime('%Y-%m-%d')} iota: {a}/{len(airports_df)} days: {i}/{len(dates)}",
                          end='\r', flush=True)

                    # print day in string format
                    # print(day.strftime('%Y-%m-%d'))
                    yyyy_mm_dd: str = day.strftime('%Y%m%d')
                    s = requests.session()
                    res = s.get(f"https://api.weather.com/v1/location/{icao_code}:{loc_id}/observations/historical.json",
                                params={"apiKey": api_key, "units": "e", "startDate": yyyy_mm_dd, "endDate": yyyy_mm_dd})

                    res = res.json()
                    # if error in res, skip
                    if 'error' in res:
                        continue

                    # if observations not in res, skip
                    if 'observations' not in res:
                        continue

                    observations = res['observations']
                    for j, observation in enumerate(observations):
                        # turn 'null' to None
                        for key, value in observation.items():
                            if value == 'null' or value == 'NA':
                                observation[key] = None
                        if i == 0:
                            weather_obs_objs = WeatherObservation(
                                **observation)
                            continue

                        weather_obs_objs.add_value(**observation)

                # for day in dates: append to dict

                weather_obs = weather_obs_objs.to_dict()
                weather_obs = remove_constant_keys(weather_obs)

                # save to 'datasets/wunderground' folder, create folder if it doesn't exist
                if not os.path.exists('datasets/wunderground'):
                    os.makedirs('datasets/wunderground')

                # convert dict to csv, where each key is a column, and each value is a row
                weather_obs = pd.DataFrame(weather_obs)
                weather_obs.to_csv(f'datasets/wunderground/{iata_code}_weather_data.csv',
                                   index=False, header=True)

                # create json file to store metadate and links to csv file
                iata_annual_weather_data['csv'] = f'{iata_code}_weather_data.csv'

                iata_annual_weather_data['status'] = "success"
                # write to json file

                main_dict[iata_code] = iata_annual_weather_data

                # with open(f'datasets/wunderground/{iata_code}_weather_data.json', 'w') as f:
                #     json.dump(iata_annual_weather_data, f)

            except Exception as e:
                iata_annual_weather_data['status'] = "error"
                iata_annual_weather_data['message'] = str(e)
                # write to json file
                # with open(f'datasets/wunderground/{iata_code}_weather_data.json', 'w') as f:
                #     json.dump(iata_annual_weather_data, f)

                main_dict[iata_code] = iata_annual_weather_data
                continue
        # write to json file
        with open(f'datasets/wunderground/weather_data.json', 'w') as f:
            json.dump(main_dict, f)

    except Exception as e:
        print(e)
        pass
