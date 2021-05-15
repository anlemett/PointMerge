import numpy as np
import pandas as pd
from calendar import monthrange
import os

import time
start_time = time.time()

year = '2019'
airport_icao = "EIDW"

from constants_EIDW import *

#months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '12', '12']
months = ['10']

DATA_DIR = os.path.join("data", airport_icao)
DATA_DIR = os.path.join(DATA_DIR, year)
DATA_DIR = os.path.join(DATA_DIR, "PIs")

#input_filename = "PIs_vertical_by_flight_" + year + '_' +  month + "_week1.csv"
#output_filename = "PIs_vertical_by_hour_" + year + '_' +  month + "_week1.csv"

#input_filename = "PIs_vertical_by_flight_" + year + "_10_week1.csv"
#output_filename = "PIs_vertical_by_hour_" + year + "_10_week1.csv"

input_filename = "PIs_vertical_by_flight_2019_10_week4_rwy28.csv"
output_filename = "PIs_vertical_by_hour_2019_10_week4_rwy28.csv"


#flight_id date hour number_of_levels time_on_levels time_on_levels_percent distance_on_levels distance_on_levels_percent
vfe_df = pd.read_csv(os.path.join(DATA_DIR, input_filename), sep=' ', dtype = {'date': str})

vfe_df.set_index(['date'], inplace=True)

vfe_by_hour_df = pd.DataFrame(columns=['date', 'hour', 'number_of_flights', 'number_of_level_flights',
                             'percent_of_level_flights',
                             'number_of_levels_total', 'number_of_levels_mean', 'number_of_levels_median',
                             'time_on_levels_total', 'time_on_levels_mean', 'time_on_levels_median',
                             'time_on_levels_min', 'time_on_levels_max',
                             'TMA_time_mean', 'TMA_time_median',
                             'distance_on_levels_total', 'distance_on_levels_mean', 'distance_on_levels_median',
                             'cdo_altitude_mean', 'cdo_altitude_median'
                             ])


for date, date_df in vfe_df.groupby(level='date'):
    
    print(date)
    
    for hour in range(0,24):
        
        hour_df = date_df[date_df['hour'] == hour]

        number_of_flights_hour = len(hour_df)

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
        
        
        time_TMA_hour = hour_df['TMA_time'].values # np array

        time_TMA_hour_sum = np.sum(time_TMA_hour)

        average_time_TMA_hour = time_TMA_hour_sum/len(time_TMA_hour) if time_TMA_hour.any() else 0
        
        median_time_TMA_hour = np.median(time_TMA_hour) if time_TMA_hour.any() else 0


        distance_on_levels_hour = hour_df['distance_on_levels'].values # np array
        
        total_distance_on_levels_hour = round(np.sum(distance_on_levels_hour), 3)
        
        average_distance_on_levels_hour = total_distance_on_levels_hour/len(distance_on_levels_hour) if distance_on_levels_hour.any() else 0
        
        median_distance_on_levels_hour = np.median(distance_on_levels_hour) if distance_on_levels_hour.any() else 0
        
        
        cdo_altitude_hour = hour_df['cdo_altitude'].values # np array
        
        total_cdo_altitude_hour = round(np.sum(cdo_altitude_hour), 3)
        
        average_cdo_altitude_hour = total_cdo_altitude_hour/len(cdo_altitude_hour) if cdo_altitude_hour.any() else 0
        
        median_cdo_altitude_hour = np.median(cdo_altitude_hour) if cdo_altitude_hour.any() else 0


        vfe_by_hour_df = vfe_by_hour_df.append({'date': date, 'hour': hour, 'number_of_flights': number_of_flights_hour,
                'number_of_level_flights': number_of_level_flights_hour,
                'percent_of_level_flights': percent_of_level_flights_hour,
                'number_of_levels_total': total_number_of_levels_hour,
                'number_of_levels_mean': average_number_of_levels_hour,
                'number_of_levels_median': median_number_of_levels_hour,
                'time_on_levels_total': total_time_on_levels_hour,
                'time_on_levels_mean': average_time_on_levels_hour,
                'time_on_levels_median': median_time_on_levels_hour,
                'time_on_levels_min': min_time_on_levels_hour, 'time_on_levels_max': max_time_on_levels_hour,
                'TMA_time_mean': average_time_TMA_hour,
                'TMA_time_median': median_time_TMA_hour,
                'distance_on_levels_total': total_distance_on_levels_hour,
                'distance_on_levels_mean': average_distance_on_levels_hour,
                'distance_on_levels_median': median_distance_on_levels_hour,
                'cdo_altitude_mean': average_cdo_altitude_hour,
                'cdo_altitude_median': median_cdo_altitude_hour
                }, ignore_index=True)

# not all dates in opensky states, creating empty rows for missing dates
(nrows, ncol) = vfe_by_hour_df.shape

month_date_list = []


df_dates_np = vfe_by_hour_df.iloc[:,0].values

for month in months:
    (first_day_weekday, number_of_days) = monthrange(int(year), int(month))
    
    date = year[2:] + month
        
    for d in range(1,9):
        month_date_list.append(date + '0' + str(d))
    for d in range(10,number_of_days+1):
        month_date_list.append(date + str(d))

for d in month_date_list:
    if d not in df_dates_np:
        for hour in range(0, 24):
            vfe_by_hour_df = vfe_by_hour_df.append({'date': d, 'hour': hour, 'number_of_flights': 0, 'number_of_level_flights': 0,
                                                    'percent_of_level_flights': 0,
                                                    'number_of_levels_total': 0,
                                                    'number_of_levels_mean': 0,
                                                    'number_of_levels_median': 0,
                                                    'time_on_levels_total': 0,
                                                    'time_on_levels_mean': 0,
                                                    'time_on_levels_median': 0,
                                                    'time_on_levels_min': 0, 'time_on_levels_max': 0,
                                                    'TMA_time_mean': 0,
                                                    'TMA_time_median': 0,
                                                    'distance_on_levels_total': 0,
                                                    'distance_on_levels_mean': 0,
                                                    'distance_on_levels_median': 0,
                                                    'cdo_altitude_mean':0,
                                                    'cdo_altitude_median':0
                                                    }, ignore_index=True)

vfe_by_hour_df = vfe_by_hour_df.sort_values(by = ['date', 'hour'] )
vfe_by_hour_df.reset_index(drop=True, inplace=True)


vfe_by_hour_df.to_csv(os.path.join(DATA_DIR, output_filename), sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)

print("--- %s minutes ---" % ((time.time() - start_time)/60))