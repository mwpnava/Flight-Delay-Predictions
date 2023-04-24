import os
import pandas as pd

wunderground_folder = 'datasets/wunderground_cleaned_no_nans'
wunderground_files = os.listdir(wunderground_folder)
# only keep the csv files
wunderground_files = [
    file for file in wunderground_files if file.endswith('.csv')]

# output folder
output_folder = 'datasets/wunderground_cleaned_no_nans_round_by_hour'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for i, file in enumerate(wunderground_files):
    print("{}/{} ({:.2f}%)".format(i, len(wunderground_files),
                                   i / len(wunderground_files) * 100), end="\r")
    # read the csv file round the 'expire_time_gmt,valid_time_gmt' columns to the nearest hour
    df = pd.read_csv(os.path.join(wunderground_folder, file))

    # convert 'expire_time_gmt' and 'valid_time_gmt' round to the nearest hour keep unix timestamp
    df['expire_time_gmt'] = df['expire_time_gmt'].apply(
        lambda x: round(x / 3600) * 3600)
    df['valid_time_gmt'] = df['valid_time_gmt'].apply(
        lambda x: round(x / 3600) * 3600)

    # save the output
    df.to_csv(os.path.join(output_folder, file), index=False)
