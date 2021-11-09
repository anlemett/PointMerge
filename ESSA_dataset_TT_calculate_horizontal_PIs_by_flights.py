import pandas as pd
import os

from geopy.distance import geodesic

from datetime import datetime
import calendar

import time
start_time = time.time()

year = '2019'

#months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
months = ['10']

airport_icao = "ESSA"
from constants_ESSA import *

DATA_DIR = os.path.join("data", airport_icao)
DATA_DIR = os.path.join(DATA_DIR, year)


def get_all_states(csv_input_file):

    df = pd.read_csv(csv_input_file, sep=' ',
                    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'endDate'],
                    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'endDate':str})
    
    df = df[['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'altitude', 'endDate']]
    
    # maybe need for distance calculation but not for runway determination
    #df = df[df['altitude']>descent_end_altitude]
    
    df.set_index(['flightId', 'sequence'], inplace=True)
    
    return df


def calculate_horizontal_PIs():
    
    DATA_INPUT_DIR = os.path.join(DATA_DIR, "Dataset")
    dataset = "ESSA_dataset_TT"
    input_filename =  dataset + ".csv"
    full_input_filename = os.path.join(DATA_INPUT_DIR, input_filename)
         
    DATA_OUTPUT_DIR = os.path.join(DATA_DIR, "PIs")
    output_filename = dataset + "_PIs_horizontal_by_flight.csv"
    full_output_filename = os.path.join(DATA_OUTPUT_DIR, output_filename)

    states_df = get_all_states(full_input_filename)
    
    number_of_flights = len(states_df.groupby(level='flightId'))
    print(number_of_flights)


    clusters_filename = dataset + "_TMA_borders_clusters_6.csv"
    CLUSTERS_DIR = os.path.join(DATA_DIR, "Clustering")
    full_clusters_filename = os.path.join(CLUSTERS_DIR, clusters_filename)
    
    clusters_df = pd.read_csv(full_clusters_filename, sep=' ')
    clusters_df.set_index(['flight_id'], inplace=True)
    
        
    horizontal_PIs_df = pd.DataFrame(columns=['flight_id',
                                   'begin_date', 'end_date', 
                                   'begin_hour', 'end_hour', 
                                   'reference_distance',
                                   'TMA_distance', 'TMA_additional_distance',
                                   'TMA_additional_distance_percent'
                                   ])

    
    flight_id_num = len(states_df.groupby(level='flightId'))

    count = 0
    for flight_id, flight_id_group in states_df.groupby(level='flightId'):
        
        count = count + 1
        print(airport_icao, flight_id_num, count, flight_id)

        # Use begin_time stamp as in vertical PIs !!!
        begin_timestamp = states_df.loc[flight_id]['timestamp'].values[0]
        begin_datetime = datetime.utcfromtimestamp(begin_timestamp)
        begin_hour_str = begin_datetime.strftime('%H')
        begin_date_str = begin_datetime.strftime('%y%m%d')
        
        end_timestamp = states_df.loc[flight_id]['timestamp'].values[-1]
        end_datetime = datetime.utcfromtimestamp(end_timestamp)
        end_hour_str = end_datetime.strftime('%H')
        end_date_str = end_datetime.strftime('%y%m%d')

        distance_sum = 0

        df_length = len(flight_id_group)
        
        for seq, row in flight_id_group.groupby(level='sequence'):
             
            if seq == 0:
                previous_point = (row['lat'].values[0], row['lon'].values[0])
                continue
            
            current_point = (row['lat'].values[0], row['lon'].values[0])
            
            distance_sum = distance_sum + geodesic(previous_point, current_point).meters
            previous_point = current_point


        distance_str = "{0:.3f}".format(distance_sum)

        # Calculate reference distance and additional distance based on cluster
        
        distance_ref = 0
        
        cluster = clusters_df.loc[flight_id]['cluster']
        
        if cluster == 1:
            distance_ref = 62.17
        elif cluster == 2:
            distance_ref = 75.84
        elif cluster == 3:
            distance_ref = 60.75
        elif cluster == 4:
            distance_ref = 73.15
        elif cluster == 5:
            distance_ref = 60.17
        else: #cluster == 6
            distance_ref = 56.06

   
        distance_ref = distance_ref * 1852     # NM to meters
         
        add_distance = distance_sum - distance_ref
        add_distance_str = "{0:.3f}".format(add_distance)
        
        add_distance_percent = add_distance/distance_sum * 100
        add_distance_percent_str = "{0:.1f}".format(add_distance_percent)
        
        #add_distance = add_distance * 0.000539957 # meters to NM
        
        horizontal_PIs_df = horizontal_PIs_df.append({'flight_id': flight_id,
                                'begin_date': begin_date_str, 
                                'end_date': end_date_str, 
                                'begin_hour': begin_hour_str,
                                'end_hour': end_hour_str,
                                'reference_distance': distance_ref,
                                'TMA_distance': distance_str,
                                'TMA_additional_distance': add_distance_str,
                                'TMA_additional_distance_percent': add_distance_percent_str},
                                ignore_index=True)

    horizontal_PIs_df.to_csv(full_output_filename, sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)


def main():
    
    calculate_horizontal_PIs()
    
    
main()    

print("--- %s minutes ---" % ((time.time() - start_time)/60))