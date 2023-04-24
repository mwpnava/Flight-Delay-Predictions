''' flights_3.csv
MONTH,DAY,DAY_OF_WEEK,AIRLINE,FLIGHT_NUMBER,TAIL_NUMBER,ORIGIN_AIRPORT,DESTINATION_AIRPORT,SCHEDULED_DEPARTURE,DEPARTURE_TIME,DEPARTURE_DELAY,TAXI_OUT,WHEELS_OFF,SCHEDULED_TIME,ELAPSED_TIME,AIR_TIME,DISTANCE,WHEELS_ON,TAXI_IN,SCHEDULED_ARRIVAL,ARRIVAL_TIME,ARRIVAL_DELAY,ts_sch_dep,ts_sch_arrival
1,1,4,B6,730.0,N621JB,BQN,MCO,419.0,423.0,4.0,11.0,434.0,174.0,163.0,148.0,1129.0,602.0,4.0,613.0,606.0,-7.0,1420107540,1420114380
1,1,4,B6,768.0,N317JB,PSE,MCO,424.0,413.0,-11.0,24.0,437.0,186.0,196.0,166.0,1179.0,623.0,6.0,630.0,629.0,-1.0,1420107840,1420115400
'''

''' flights_5.csv
ORIGIN_AIRPORT,DESTINATION_AIRPORT,ts_sch_dep,ts_sch_arrival,o_expire_time_gmt,d_expire_time_gmt,o_valid_time_gmt,d_valid_time_gmt,o_day_ind,d_day_ind,o_temp,d_temp,o_wx_icon,d_wx_icon,o_icon_extd,d_icon_extd,o_wx_phrase,d_wx_phrase,o_dewPt,d_dewPt,o_heat_index,d_heat_index,o_rh,d_rh,o_pressure,d_pressure,o_vis,d_vis,o_wc,d_wc,o_wdir_cardinal,d_wdir_cardinal,o_wspd,d_wspd,o_uv_desc,d_uv_desc,o_feels_like,d_feels_like,o_uv_index,d_uv_index,o_clds,d_clds
BQN,MCO,1420107540,1420114380,1420178400.0,1420182000.0,1420171200.0,1420174800.0,N,N,73.0,63.0,33.0,20.0,3300.0,2002.0,Fair,Mist,70.0,63.0,73.0,63.0,88.0,100.0,29.9,30.12,10.0,0.0,73.0,63.0,E,N,8.0,8.0,Low,Low,73.0,63.0,0.0,0.0,CLR,OVC
PSE,MCO,1420107840,1420115400,1420196400.0,1420182000.0,1420189200.0,1420174800.0,N,N,39.0,63.0,26.0,20.0,2600.0,2002.0,Cloudy,Mist,34.0,63.0,39.0,63.0,81.0,100.0,29.58,30.12,10.0,0.0,33.0,63.0,NW,N,9.0,8.0,Low,Low,33.0,63.0,0.0,0.0,OVC,OVC
'''


if __name__ == '__main__':

    csv_f3 = open('datasets/kaggle_cleaned/flights_3.csv', 'r')
    csv_f5 = open('datasets/kaggle_cleaned/flights_5.csv', 'r')

    # add f5 header to f3 header
    f5_header = csv_f5.readline()
    f5_header = f5_header.strip()
    f5_header = f5_header.split(',')
    f3_header = csv_f3.readline()
    f3_header = f3_header.strip()
    f3_header = f3_header.split(',')
    f3_header.extend(f5_header[2:])

    # len of csv_f3
    len_csv_f3 = 0
    for i, line in enumerate(csv_f3):
        len_csv_f3 += 1
    csv_f3.close()
    csv_f3 = open('datasets/kaggle_cleaned/flights_3.csv', 'r')
    csv_f3.readline()  # skip header
    lines = []

    for i, line in enumerate(csv_f3):

        if i % 1000 == 0:
            print(f'{i}/{len_csv_f3} ({i/len_csv_f3*100}%', end='\r')

        # add f5 row to f3 row
        f5_row = csv_f5.readline()
        line = line.strip() + ',' + f5_row
        lines.append(line)

    csv_f3.close()
    csv_f5.close()
    # write to file csv file, header and rows
    # use csv.writer
    with open('datasets/kaggle_cleaned/flights_6.csv', 'w') as f:
        f.write(','.join(f3_header))
        for line in lines:
            f.write(line)
