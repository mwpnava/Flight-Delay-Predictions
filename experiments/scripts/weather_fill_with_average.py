
# for each file in 'datasets/wunderground', create a df from the csv, if any missing value, filled with the average of the column, and save the df as a csv in 'datasets/wunderground_cleaned'
# if non-numeric, fill with the mode
import os
import pandas as pd


def fill_with_average():
    files = os.listdir('datasets/wunderground_cleaned')
    files = [f for f in files if f.endswith('.csv')]
    for f in files:
        try:
            df = pd.read_csv('datasets/wunderground_cleaned/' + f)
            for col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = df[col].fillna(df[col].mode().iloc[0])
                else:
                    df[col] = df[col].fillna(df[col].mean())
            df.to_csv('datasets/wunderground_cleaned/' + f, index=False)
        except Exception as e:
            print('Error with file: ' + f)
            print(e)
            # trackback
            import traceback
            print(traceback.format_exc())


if __name__ == '__main__':
    fill_with_average()
