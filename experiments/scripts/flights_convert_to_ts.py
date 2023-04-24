import pandas as pd
import datetime

# Define a function to convert time in HHMM format to a datetime object


def parse_time(year, month, day, hhmm):
    if len(hhmm) == 1:
        hhmm = '000' + hhmm
    elif len(hhmm) == 2:
        hhmm = '00' + hhmm
    elif len(hhmm) == 3:
        hhmm = '0' + hhmm
    elif len(hhmm) == 4:
        pass
    else:
        raise ValueError('Invalid time format')

    hh = int(hhmm[:2])
    mm = int(hhmm[2:])
    return datetime.datetime(year=year, month=month, day=day, hour=hh, minute=mm)


# create a new column for the timestamp of the scheduled departure and arrival
def add_ts_columns():
    path = 'datasets/kaggle_cleaned/flights_cleaned_no_nans.csv'
    new_path = 'datasets/kaggle_cleaned/flights_cleaned_no_nans_ts.csv'
    # Read the CSV file into a pandas dataframe
    df = pd.read_csv(path)

    # Add the timestamp columns to the dataframe
    year = 2015  # assuming year is always 2015
    df['ts_sch_dep'] = df.apply(lambda row: int(parse_time(year, row['MONTH'], row['DAY'], str(
        int(row['SCHEDULED_DEPARTURE']))).timestamp()), axis=1)
    df['ts_sch_arrival'] = df.apply(lambda row: int(parse_time(
        year, row['MONTH'], row['DAY'], str(int(row['SCHEDULED_ARRIVAL']))).timestamp()), axis=1)

    df.to_csv(new_path,
              index=False)


if __name__ == '__main__':

    add_ts_columns()
