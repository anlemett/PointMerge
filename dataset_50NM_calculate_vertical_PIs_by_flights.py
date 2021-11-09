import pandas as pd
import os

from datetime import datetime

import time
start_time = time.time()

year = '2019'
airport_icao = "EIDW"

if airport_icao == "EIDW":
    from constants_EIDW import *
elif airport_icao == "ESSA":
    from constants_ESSA import *
elif airport_icao == "LOWW":
    from constants_LOWW import *

DATA_DIR = os.path.join("data", airport_icao + "_50NM_rwy")
DATA_DIR = os.path.join(DATA_DIR, year)


def get_all_states(csv_input_file):

    df = pd.read_csv(csv_input_file, sep=' ',
                    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'],
                    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':int, 'altitude':float, 'velocity':float, 'beginDate':str,'endDate':str})
    
    df = df[['flightId', 'sequence', 'timestamp', 'altitude', 'velocity', 'endDate']]
    
    df.set_index(['flightId', 'sequence'], inplace=True)
    
    return df


def calculate_vfe():
    
    DATA_INPUT_DIR = os.path.join(DATA_DIR, "Dataset")

    #dataset_name = airport_icao + "_50NM_rwy_dataset_TT"
    dataset_name = airport_icao + "_50NM_rwy_dataset_PM"
    #dataset_name = airport_icao + "_50NM_rwy_dataset_TB"
    input_filename = dataset_name + ".csv"

    full_input_filename = os.path.join(DATA_INPUT_DIR, input_filename)
         
    DATA_OUTPUT_DIR = os.path.join(DATA_DIR, "PIs")
    output_filename = dataset_name + "_PIs_vertical_by_flight.csv"
    full_output_filename = os.path.join(DATA_OUTPUT_DIR, output_filename)
    
       
    states_df = get_all_states(full_input_filename)

    min_level_time = 30
    #Y/X = 300 feet per minute
    rolling_window_Y = (300*(min_level_time/60))/ 3.281 # feet to meters
    #print(rolling_window_Y)

    #descent part ends at 1800 feet
    descent_end_altitude = 1800 / 3.281
    #print(descent_end_altitude)

    vfe_df = pd.DataFrame(columns=['flight_id', 'begin_date', 'end_date', 'begin_hour', 'end_hour', 
                                   'number_of_levels',
                                   'time_on_levels', 'time_on_levels_percent',
                                   '50NM_time',
                                   'cdo_altitude'])

    number_of_levels_lst = []
    distance_on_levels_lst = []
    distance_on_levels_percent_lst = []
    time_on_levels_lst = []
    time_on_levels_percent_lst = []
    
    
    flight_id_num = len(states_df.groupby(level='flightId'))
    number_of_level_flights = 0

    count = 0
    for flight_id, flight_id_group in states_df.groupby(level='flightId'):
        
        count = count + 1
        print(airport_icao, year, flight_id_num, count, flight_id)
        
        number_of_levels = 0

        time_sum = 0
        time_on_levels = 0
        time_on_level = 0

        distance_sum = 0
        distance_on_levels = 0
        distance_on_level = 0

        level = 'false'
        altitude1 = 0 # altitude at the beginning of rolling window
        altitude2 = 0 # altitude at the end of rolling window
        
        cdo_altitude = 0

        seq_level_end = 0
        seq_min_level_time = 0

        df_length = len(flight_id_group)
        
        cdo_altitude = flight_id_group.loc[flight_id, :]['altitude'].values[0]
        
        for seq, row in flight_id_group.groupby(level='sequence'):

            if (seq + min_level_time) >= df_length:
                break
            
            time_sum = time_sum + 1
            distance_sum = distance_sum + row['velocity'].values[0]

            altitude1 = row['altitude'].values[0]
            
            altitude2 = flight_id_group.loc[flight_id, seq+min_level_time-1]['altitude']
            
            # do not calculate as levels climbing in go around
            if altitude2 > altitude1:
                continue
     
            if altitude2 < descent_end_altitude:
                break


            if level == 'true':

                if seq < seq_level_end:
                    if altitude1 - altitude2 < rolling_window_Y: #extend the level
                        seq_level_end = seq_level_end + 1
                    if seq < seq_min_level_time: # do not count first 30 seconds
                        continue
                    else:
                        time_on_level = time_on_level + 1
                else: # level ends
                    if seq_level_end >= seq_min_level_time:
                        number_of_levels = number_of_levels + 1
                    level = 'false'
                    time_on_levels = time_on_levels + time_on_level
                    time_on_level = 0
                    
                    cdo_altitude = altitude1
            else: #not level
                if altitude1 - altitude2 < rolling_window_Y: # level begins
                    level = 'true'
                    seq_min_level_time = seq + min_level_time
                    seq_level_end = seq + min_level_time - 1
                    time_on_level = time_on_level + 1

        if time_sum == 0:
            print(flight_id, time_sum)
            continue

        number_of_levels_str = str(number_of_levels)

        number_of_levels_lst.append(number_of_levels)

        # convert time to munutes
        time_on_levels = time_on_levels / 60    #seconds to minutes
        time_sum = time_sum / 60                #seconds to minutes

        time_on_levels_lst.append(time_on_levels)
        time_on_levels_str = "{0:.3f}".format(time_on_levels)

        time_on_levels_percent = time_on_levels / time_sum *100
        time_on_levels_percent_lst.append(time_on_levels_percent)
        time_on_levels_percent_str = "{0:.1f}".format(time_on_levels_percent)

        
        circle_50NM_time = len(flight_id_group)/60  #seconds to minutes
                
        begin_timestamp = states_df.loc[flight_id]['timestamp'].values[0]
        begin_datetime = datetime.utcfromtimestamp(begin_timestamp)
        begin_hour_str = begin_datetime.strftime('%H')
        begin_date_str = begin_datetime.strftime('%y%m%d')

        end_timestamp = states_df.loc[flight_id]['timestamp'].values[-1]
        end_datetime = datetime.utcfromtimestamp(end_timestamp)
        end_hour_str = end_datetime.strftime('%H')
        end_date_str = end_datetime.strftime('%y%m%d')
        
        vfe_df = vfe_df.append({'flight_id': flight_id,
                                'begin_date': begin_date_str, 
                                'end_date': end_date_str,
                                'begin_hour': begin_hour_str,
                                'end_hour': end_hour_str,
                                'number_of_levels': number_of_levels_str,
                                'time_on_levels': time_on_levels_str,
                                'time_on_levels_percent': time_on_levels_percent_str,
                                '50NM_time': circle_50NM_time,
                                'cdo_altitude': cdo_altitude}, ignore_index=True)

    vfe_df.to_csv(full_output_filename, sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)
   
    
calculate_vfe()    

print("--- %s minutes ---" % ((time.time() - start_time)/60))