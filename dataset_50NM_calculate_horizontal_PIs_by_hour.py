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

input_filename = dataset_name + "_PIs_horizontal_by_flight.csv"
output_filename = dataset_name + "_PIs_horizontal_by_hour.csv"

def calculate_horizontal_PIs_hour():
    #flight_id, date, hour, reference_distance, 50NM_distance, 50NM_additional_distance
    PIs_by_flight_df = pd.read_csv(os.path.join(DATA_DIR, input_filename), sep=' ', dtype = {'begin_date': str})
    

    PIs_by_flight_df.set_index(['begin_date'], inplace=True)
    
    PIs_by_hour_df = pd.DataFrame(columns=['date', 'hour', 'number_of_flights',
                                   '50NM_additional_distance_mean',
                                   '50NM_additional_distance_median',
                                   '50NM_additional_distance_min',
                                   '50NM_additional_distance_max'
                                   ])


    
    for date, date_df in PIs_by_flight_df.groupby(level='begin_date'):
    
        print(airport_icao, date)
    
        for hour in range(0,24):
        
            hour_df = date_df[date_df['begin_hour'] == hour]

            number_of_flights_hour = len(hour_df)
            
            if number_of_flights_hour == 0:
                continue
            
            circle_50NM_additional_distance_hour = hour_df['50NM_additional_distance'].values # np array

            total_50NM_additional_distance_hour = np.sum(circle_50NM_additional_distance_hour)

            average_50NM_additional_distance_hour = total_50NM_additional_distance_hour/number_of_flights_hour
        
            median_50NM_additional_distance_hour = np.median(circle_50NM_additional_distance_hour)
                
            min_50NM_additional_distance_hour = np.min(circle_50NM_additional_distance_hour)
                
            max_50NM_additional_distance_hour = np.max(circle_50NM_additional_distance_hour)
            
            temp_df = hour_df[hour_df['50NM_additional_distance']==min_50NM_additional_distance_hour]
           

            PIs_by_hour_df = PIs_by_hour_df.append({'date': date, 'hour': hour,
                '50NM_additional_distance_mean': average_50NM_additional_distance_hour,
                '50NM_additional_distance_median': median_50NM_additional_distance_hour,
                '50NM_additional_distance_min': min_50NM_additional_distance_hour,
                '50NM_additional_distance_max': max_50NM_additional_distance_hour
                }, ignore_index=True)
            
    # not all dates in dataset, creating empty rows for missing dates
    (nrows, ncol) = PIs_by_hour_df.shape

    month_date_list = []


    df_dates_np = PIs_by_hour_df.iloc[:,0].values
    
    print(df_dates_np)

    (first_day_weekday, number_of_days) = monthrange(int(year), int(month))
    
    date = year[2:] + str(month)
        
    for d in range(1,10):
        month_date_list.append(date + '0' + str(d))
    for d in range(10,29):
        month_date_list.append(date + str(d))

    for d in month_date_list:
        if d not in df_dates_np:
            for hour in range(0, 24):
                PIs_by_hour_df = PIs_by_hour_df.append({'date': d, 'hour': hour, 'number_of_flights': 0, 
                                                        '50NM_additional_distance_mean': 0,
                                                        '50NM_additional_distance_median': 0,
                                                        '50NM_additional_distance_min': 0,
                                                        '50NM_additional_distance_max': 0
                                                    }, ignore_index=True)

    PIs_by_hour_df = PIs_by_hour_df.sort_values(by = ['date', 'hour'] )
    PIs_by_hour_df.reset_index(drop=True, inplace=True)


    PIs_by_hour_df.to_csv(os.path.join(DATA_DIR, output_filename), sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)

calculate_horizontal_PIs_hour()

print("--- %s minutes ---" % ((time.time() - start_time)/60))