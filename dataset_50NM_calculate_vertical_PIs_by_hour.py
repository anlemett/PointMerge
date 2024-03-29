import numpy as np
import pandas as pd
from calendar import monthrange
import os

import time
start_time = time.time()

year = '2019'
month = '10'

#airport_icao = "EIDW"
#airport_icao = "ESSA"
airport_icao = "LOWW"


if airport_icao == "EIDW":
    from constants_EIDW import *
elif airport_icao == "ESSA":
    from constants_ESSA import *
elif airport_icao == "LOWW":
    from constants_LOWW import *

DATA_DIR = os.path.join("data", airport_icao + "_50NM_rwy")
DATA_DIR = os.path.join(DATA_DIR, year)
DATA_DIR = os.path.join(DATA_DIR, "PIs") 

#dataset_name = airport_icao + "_50NM_rwy_dataset_TT"
#dataset_name = airport_icao + "_50NM_rwy_dataset_PM"
dataset_name = airport_icao + "_50NM_rwy_dataset_TB"

input_filename = dataset_name + "_PIs_vertical_by_flight.csv"
output_filename = dataset_name + "_PIs_vertical_by_hour.csv"

def calculate_vfe_hour():
    #flight_id date hour number_of_levels time_on_levels time_on_levels_percent 
    vfe_df = pd.read_csv(os.path.join(DATA_DIR, input_filename), sep=' ', dtype = {'begin_date': str, 'end_date': str})

    vfe_df.set_index(['begin_date'], inplace=True)

    vfe_by_hour_df = pd.DataFrame(columns=['date', 'hour',
                             'number_of_flights_by_start', 
                             #'number_of_flights_by_end', 
                             'number_of_flights_by_start_and_end',
                             'number_of_level_flights',
                             'percent_of_level_flights',
                             'number_of_levels_total', 'number_of_levels_mean', 'number_of_levels_median',
                             'time_on_levels_total', 'time_on_levels_mean', 'time_on_levels_median',
                             'time_on_levels_min', 'time_on_levels_max',
                             '50NM_time_mean', '50NM_time_median',
                             'cdo_altitude_mean', 'cdo_altitude_median'
                             ])

    number_of_flights_by_hour_df = pd.DataFrame(columns=['date', 'hour', 'number_of_flights'])


    average_time_50NM_hour_max = 0
    average_time_50NM_hour_max_date = 0
    average_time_50NM_hour_max_hour = 0
    average_time_50NM_hour_max_number_of_flights = 0
    average_time_50NM_hour_max_hour_df = pd.DataFrame()
    
    for date, date_df in vfe_df.groupby(level='begin_date'):
    
        print(airport_icao, date)
    
        for hour in range(0,24):
        
            hour_df = date_df[date_df['begin_hour'] == hour]

            number_of_flights_hour = len(hour_df)
            
            hour_by_start_and_end_df = date_df[(date_df['end_hour'] == hour) | ((date_df['end_hour'] != hour) & (date_df['begin_hour'] == hour)) ]

            number_of_flights_hour_by_start_and_end = len(hour_by_start_and_end_df)
 
    
            level_df = hour_df[hour_df['number_of_levels']>0]

            number_of_level_flights_hour = len(level_df)
        
            percent_of_level_flights_hour = number_of_level_flights_hour/number_of_flights_hour if number_of_flights_hour>0 else 0
        

            number_of_levels_hour = hour_df['number_of_levels'].values # np array

            total_number_of_levels_hour = np.sum(number_of_levels_hour)

            average_number_of_levels_hour = total_number_of_levels_hour/len(number_of_levels_hour) if number_of_levels_hour.any() else 0
        
            median_number_of_levels_hour = np.median(number_of_levels_hour) if number_of_levels_hour.any() else 0
        

            time_on_levels_hour = hour_df['time_on_levels'].values # np array
        
            total_time_on_levels_hour = round(np.sum(time_on_levels_hour), 3)
        
            average_time_on_levels_hour = total_time_on_levels_hour/len(time_on_levels_hour) if time_on_levels_hour.any() else 0
        
            median_time_on_levels_hour = np.median(time_on_levels_hour) if time_on_levels_hour.any() else 0
        
            min_time_on_levels_hour = round(np.min(time_on_levels_hour), 3) if time_on_levels_hour.any() else 0
        
            max_time_on_levels_hour = round(np.max(time_on_levels_hour), 3) if time_on_levels_hour.any() else 0
        
        
            time_50NM_hour = hour_df['50NM_time'].values # np array

            time_50NM_hour_sum = np.sum(time_50NM_hour)

            average_time_50NM_hour = time_50NM_hour_sum/len(time_50NM_hour) if time_50NM_hour.any() else 0
        
            median_time_50NM_hour = np.median(time_50NM_hour) if time_50NM_hour.any() else 0

        
            cdo_altitude_hour = hour_df['cdo_altitude'].values # np array
        
            total_cdo_altitude_hour = round(np.sum(cdo_altitude_hour), 3)
        
            average_cdo_altitude_hour = total_cdo_altitude_hour/len(cdo_altitude_hour) if cdo_altitude_hour.any() else 0
        
            median_cdo_altitude_hour = np.median(cdo_altitude_hour) if cdo_altitude_hour.any() else 0


            vfe_by_hour_df = vfe_by_hour_df.append({'date': date, 'hour': hour,
                'number_of_flights_by_start': number_of_flights_hour,
                'number_of_flights_by_start_and_end': number_of_flights_hour_by_start_and_end,
                'number_of_level_flights': number_of_level_flights_hour,
                'percent_of_level_flights': percent_of_level_flights_hour,
                'number_of_levels_total': total_number_of_levels_hour,
                'number_of_levels_mean': average_number_of_levels_hour,
                'number_of_levels_median': median_number_of_levels_hour,
                'time_on_levels_total': total_time_on_levels_hour,
                'time_on_levels_mean': average_time_on_levels_hour,
                'time_on_levels_median': median_time_on_levels_hour,
                'time_on_levels_min': min_time_on_levels_hour, 
                'time_on_levels_max': max_time_on_levels_hour,
                '50NM_time_mean': average_time_50NM_hour,
                '50NM_time_median': median_time_50NM_hour,
                'cdo_altitude_mean': average_cdo_altitude_hour,
                'cdo_altitude_median': median_cdo_altitude_hour
                }, ignore_index=True)
            
            if average_time_50NM_hour > average_time_50NM_hour_max:
                average_time_50NM_hour_max = average_time_50NM_hour
                average_time_50NM_hour_max_date = date
                average_time_50NM_hour_max_hour = hour
                average_time_50NM_hour_max_number_of_flights = number_of_flights_hour
                average_time_50NM_hour_max_hour_df = hour_df

    # not all dates in dataset, creating empty rows for missing dates
    (nrows, ncol) = vfe_by_hour_df.shape

    month_date_list = []


    df_dates_np = vfe_by_hour_df.iloc[:,0].values

    (first_day_weekday, number_of_days) = monthrange(int(year), int(month))
    
    date = year[2:] + str(month)
        
    for d in range(1,10):
        month_date_list.append(date + '0' + str(d))
    for d in range(10,29):
        month_date_list.append(date + str(d))

    for d in month_date_list:
        if d not in df_dates_np:
            for hour in range(0, 24):
                vfe_by_hour_df = vfe_by_hour_df.append({'date': d, 'hour': hour, 
                                                    'number_of_flights_by_start': 0,
                                                    'number_of_flights_by_start_and_end': 0,
                                                    'number_of_level_flights': 0,
                                                    'percent_of_level_flights': 0,
                                                    'number_of_levels_total': 0,
                                                    'number_of_levels_mean': 0,
                                                    'number_of_levels_median': 0,
                                                    'time_on_levels_total': 0,
                                                    'time_on_levels_mean': 0,
                                                    'time_on_levels_median': 0,
                                                    'time_on_levels_min': 0, 'time_on_levels_max': 0,
                                                    '50NM_time_mean': 0,
                                                    '50NM_time_median': 0,
                                                    'cdo_altitude_mean':0,
                                                    'cdo_altitude_median':0
                                                    }, ignore_index=True)

    vfe_by_hour_df = vfe_by_hour_df.sort_values(by = ['date', 'hour'] )
    vfe_by_hour_df.reset_index(drop=True, inplace=True)


    vfe_by_hour_df.to_csv(os.path.join(DATA_DIR, output_filename), sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)

    print(average_time_50NM_hour_max)
    print(average_time_50NM_hour_max_date)
    print(average_time_50NM_hour_max_hour)
    print(average_time_50NM_hour_max_number_of_flights)
    print(average_time_50NM_hour_max_hour_df.head())

calculate_vfe_hour()

print("--- %s minutes ---" % ((time.time() - start_time)/60))