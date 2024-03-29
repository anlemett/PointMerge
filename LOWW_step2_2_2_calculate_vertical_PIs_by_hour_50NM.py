import numpy as np
import pandas as pd
from calendar import monthrange
import os

import time
start_time = time.time()

year = '2019'
airport_icao = "LOWW"

from constants_LOWW import *

#months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '12', '12']
months = ['10']

#DATA_DIR = os.path.join("data", airport_icao + "_50NM")
DATA_DIR = os.path.join("data", airport_icao + "_50NM_rwy")
DATA_DIR = os.path.join(DATA_DIR, year)
DATASET_DATA_DIR = os.path.join(DATA_DIR, "Dataset")
if not os.path.exists(DATASET_DATA_DIR):
    os.makedirs(DATASET_DATA_DIR)
    
DATA_DIR = os.path.join(DATA_DIR, "PIs") 


def calculate_vfe_hour(month, week):
    input_filename = "PIs_vertical_by_flight_2019_" + str(month) + "_week" + str(week) + "_rwy16.csv"
    output_filename = "PIs_vertical_by_hour_2019_" + str(month) + "_week" + str(week) + "_rwy16.csv"


    #flight_id date hour number_of_levels time_on_levels time_on_levels_percent distance_on_levels distance_on_levels_percent
    vfe_df = pd.read_csv(os.path.join(DATA_DIR, input_filename), sep=' ', dtype = {'begin_date': str, 'end_date': str})

    vfe_df.set_index(['end_date'], inplace=True)

    vfe_by_hour_df = pd.DataFrame(columns=['date', 'hour',
                             'number_of_flights_by_end', 
                             'number_of_flights_by_start_and_end',
                             'number_of_level_flights',
                             'percent_of_level_flights',
                             'number_of_levels_total',
                             'number_of_levels_mean', 
                             'number_of_levels_median',
                             'time_on_levels_total',
                             'time_on_levels_mean', 
                             'time_on_levels_median',
                             'time_on_levels_min', 
                             'time_on_levels_max',
                             '50NM_time_mean', 
                             '50NM_time_median',
                             '50NM_time_min', 
                             '50NM_time_max', 
                             'cdo_altitude_mean', 
                             'cdo_altitude_median'
                             ])

    number_of_flights_by_hour_df = pd.DataFrame(columns=['date', 'hour', 'number_of_flights'])

    flight_id_list = []
    for date, date_df in vfe_df.groupby(level='end_date'):
    
        print(date)
    
        for hour in range(0,24):
        
            hour_df = date_df[date_df['end_hour'] == hour]

            number_of_flights_hour= len(hour_df)

            hour_by_start_and_end_df = date_df[(date_df['end_hour'] == hour) | ((date_df['end_hour'] != hour) & (date_df['begin_hour'] == hour)) ]

            number_of_flights_hour_by_start_and_end = len(hour_by_start_and_end_df)
        
            if number_of_flights_hour_by_start_and_end > 25:
                date_flight_id_list = list(date_df['flight_id'])
                flight_id_list = flight_id_list + date_flight_id_list
        
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
            
            min_time_50NM_hour = round(np.min(time_50NM_hour), 3) if time_50NM_hour.any() else 0
            
            max_time_50NM_hour = round(np.max(time_50NM_hour), 3) if time_50NM_hour.any() else 0
        
        
            cdo_altitude_hour = hour_df['cdo_altitude'].values # np array
        
            total_cdo_altitude_hour = round(np.sum(cdo_altitude_hour), 3)
        
            average_cdo_altitude_hour = total_cdo_altitude_hour/len(cdo_altitude_hour) if cdo_altitude_hour.any() else 0
        
            median_cdo_altitude_hour = np.median(cdo_altitude_hour) if cdo_altitude_hour.any() else 0


            vfe_by_hour_df = vfe_by_hour_df.append({'date': date, 'hour': hour,
                'number_of_flights_by_end': number_of_flights_hour,
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
                '50NM_time_min': min_time_50NM_hour,
                '50NM_time_max': max_time_50NM_hour,
                'cdo_altitude_mean': average_cdo_altitude_hour,
                'cdo_altitude_median': median_cdo_altitude_hour
                }, ignore_index=True)

    # not all dates in opensky states, creating empty rows for missing dates
    (nrows, ncol) = vfe_by_hour_df.shape

    month_date_list = []


    df_dates_np = vfe_by_hour_df.iloc[:,0].values

    (first_day_weekday, number_of_days) = monthrange(int(year), int(month))
    
    date = year[2:] + str(month)
        
    for d in range(1,8):
        if (7*(week-1) + d < 10):
            month_date_list.append(date + '0' + str(7*(week-1) + d))
        else:
            month_date_list.append(date + str(7*(week-1) + d))

    for d in month_date_list:
        if d not in df_dates_np:
            for hour in range(0, 24):
                vfe_by_hour_df = vfe_by_hour_df.append({'date': d, 'hour': hour,
                                                    'number_of_flights_by_end':0, 
                                                    'number_of_flights_by_start_and_end':0,
                                                    'number_of_level_flights': 0,
                                                    'percent_of_level_flights': 0,
                                                    'number_of_levels_total': 0,
                                                    'number_of_levels_mean': 0,
                                                    'number_of_levels_median': 0,
                                                    'time_on_levels_total': 0,
                                                    'time_on_levels_mean': 0,
                                                    'time_on_levels_median': 0,
                                                    'time_on_levels_min': 0,
                                                    'time_on_levels_max': 0,
                                                    '50NM_time_mean': 0,
                                                    '50NM_time_median': 0,
                                                    '50NM_time_min': 0,
                                                    '50NM_time_max': 0,
                                                    'cdo_altitude_mean':0,
                                                    'cdo_altitude_median':0
                                                    }, ignore_index=True)

    vfe_by_hour_df = vfe_by_hour_df.sort_values(by = ['date', 'hour'] )
    vfe_by_hour_df.reset_index(drop=True, inplace=True)


    vfe_by_hour_df.to_csv(os.path.join(DATA_DIR, output_filename), sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)

    flight_id_set = set(flight_id_list)

    filename = "LOWW_2019_10_week" + str(week) + "more_than_25_flight_ids.txt"
    with open(os.path.join(DATASET_DATA_DIR, filename), 'w') as filehandle:
        for listitem in flight_id_set:
            filehandle.write('%s\n' % listitem)

def main():
    
    for week in range (0,5):
        calculate_vfe_hour(10, week+1)
    
    
main()    

print("--- %s minutes ---" % ((time.time() - start_time)/60))