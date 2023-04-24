# get list of files in 'datasets/wunderground' folder
import pandas as pd
import json
import os


features = {
    'expire_time_gmt': 0,
    'valid_time_gmt': 0,
    'day_ind': 0,
    'temp': 0,
    'wx_icon': 0,
    'icon_extd': 0,
    'wx_phrase': 0,
    'pressure_tend': 0,
    'pressure_desc': 0,
    'dewPt': 0,
    'heat_index': 0,
    'rh': 0,
    'pressure': 0,
    'vis': 0,
    'wc': 0,
    'wdir': 0,
    'wdir_cardinal': 0,
    'gust': 0,
    'wspd': 0,
    'max_temp': 0,
    'min_temp': 0,
    'precip_total': 0,
    'precip_hrly': 0,
    'uv_desc': 0,
    'feels_like': 0,
    'uv_index': 0,
    'clds': 0,
    'snow_hrly': 0
}


def get_most_missing(file_list):
    '''
    go through each file, and  determine which feature has the most missing values, provide a list

    '''

    for f in file_list:

        try:
            with open('datasets/wunderground/' + f, 'r') as data:
                header = data.readline().strip().split(',')
                for line in data:
                    values = line.strip().split(',')
                    for i, v in enumerate(values):
                        if v == '':
                            features[header[i]] += 1
        except Exception as e:
            print('Error with file: ' + f)
            print(e)
            # trackback
            import traceback
            print(traceback.format_exc())


remove_cols = ['precip_total', 'max_temp', 'min_temp', 'gust',
               'pressure_tend', 'pressure_desc', 'snow_hrly', 'wdir']


# for all files in datasets/wunderground, create a df with the csv, remove the columns, and save the df as a csv in datasets/wunderground_cleaned
def clean_data():
    files = os.listdir('datasets/wunderground')
    files = [f for f in files if f.endswith('.csv')]
    len_files = len(files)
    if not os.path.exists('datasets/wunderground_cleaned'):
        os.mkdir('datasets/wunderground_cleaned')
    for f in files:
        print(
            f'Cleaning file: {f} ({files.index(f) + 1} of {len_files})', end='\r', flush=True)
        df = pd.read_csv('datasets/wunderground/' + f)
        for col in remove_cols:
            try:
                df.drop(columns=col, inplace=True)
            except Exception as e:
                pass
        df.to_csv('datasets/wunderground_cleaned/' + f, index=False)


if __name__ == '__main__':
    # file_list = os.listdir('datasets/wunderground')
    # file_list = [f for f in file_list if f.endswith('.csv')]
    # get_most_missing(file_list)
    # # export features as json
    # with open('results/weather_missing_features.json', 'w') as f:
    #     json.dump(features, f)

    # clean_data()
    pass
