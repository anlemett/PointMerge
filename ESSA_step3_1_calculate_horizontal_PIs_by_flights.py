import pandas as pd
import os

from geopy.distance import geodesic
import pyproj

from datetime import datetime
import calendar

import time
start_time = time.time()

is_dataset = True

year = '2019'

#months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
months = ['10']


airport_icao = "ESSA"
entry_points = ['ELTOK', 'HMR', 'NILUG', 'XILAN']
runways = ['01L', '19R', '01R', '19L', '08', '26']

DATA_DIR = os.path.join("data", airport_icao)
if is_dataset:
    DATA_DIR = os.path.join(DATA_DIR, "Dataset")
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


def calculate_horizontal_PIs(month, week, entry_point, runway):
    
    DATA_INPUT_DIR = os.path.join(DATA_DIR, "osn_"+ airport_icao + "_states_TMA_" + year)
    DATA_INPUT_DIR = os.path.join(DATA_INPUT_DIR,
        "osn_"+ airport_icao + "_states_TMA_" + year + '_' + month + '_week' + str(week) + '_by_entry_points_and_runways')
    
    input_filename = "osn_"+ airport_icao + "_states_TMA_" + year + '_' + month + '_week' + str(week) + '_' + entry_point + '_rwy' + runway + ".csv"
    full_input_filename = os.path.join(DATA_INPUT_DIR, input_filename)
         
    DATA_OUTPUT_DIR = os.path.join(DATA_DIR, "PIs")
    if not os.path.exists(DATA_OUTPUT_DIR):
        os.makedirs(DATA_OUTPUT_DIR)
    DATA_OUTPUT_DIR = os.path.join(DATA_OUTPUT_DIR, "PIs_horizontal_by_flight_" + year + '_' +  month + '_week' + str(week) + '_by_entry_points_and_runways')
    if not os.path.exists(DATA_OUTPUT_DIR):
        os.makedirs(DATA_OUTPUT_DIR)
    output_filename = "PIs_horizontal_by_flight_" + year + '_' +  month + '_week' + str(week) + '_' + entry_point + '_rwy' + runway + ".csv"
    full_output_filename = os.path.join(DATA_OUTPUT_DIR, output_filename)
    
    #number_of_flights = len(states_df.groupby(level='flightId'))
    
    states_df = get_all_states(full_input_filename)
        
    horizontal_PIs_df = pd.DataFrame(columns=['flight_id', 'date', 'hour', 
                                   'entry_point', 'runway',
                                   'TMA_distance', 'TMA_additional_distance'
                                   ])

    
    flight_id_num = len(states_df.groupby(level='flightId'))

    count = 0
    for flight_id, flight_id_group in states_df.groupby(level='flightId'):
        
        #if flight_id != '200528VAS816':
        #if flight_id != '200526SAS532':
        #    continue
        
        count = count + 1
        print(airport_icao, year, month, week, entry_point, runway, flight_id_num, count, flight_id)

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

        date_str = states_df.loc[flight_id].head(1)['endDate'].values[0]
        
        #end_timestamp = states_opensky_df.loc[flight_id]['timestamp'].values[-1].item(0)
        end_timestamp = states_df.loc[flight_id]['timestamp'].values[-1]
        end_datetime = datetime.utcfromtimestamp(end_timestamp)
        end_hour_str = end_datetime.strftime('%H')
        
        # Calculate reference distance and additional distance based on entry point and runway
        
        distance_ref = 0
        
        if entry_point == "ELTOK":
            if runway == "01L":
                distance_ref = 44.2
            elif runway == "19R":
                distance_ref = 40.2
            elif runway == "01R":
                distance_ref = 52.7
            elif runway == "19L":
                distance_ref = 41.3
            elif runway == "08":
                distance_ref = 32.6
            else: # "26"
                distance_ref = 52.0
        elif entry_point == "HMR":
            if runway == "01L":
                distance_ref = 63.4
            elif runway == "19R":
                distance_ref = 39.6
            elif runway == "01R":
                distance_ref = 73.0
            elif runway == "19L":
                distance_ref = 40.2
            elif runway == "08":
                distance_ref = 57.0
            else: # "26"
                distance_ref = 44.6
        elif entry_point == "NILUG":
            if runway == "01L":
                distance_ref = 49.5
            elif runway == "19R":
                distance_ref = 73.3
            elif runway == "01R":
                distance_ref = 48.9
            elif runway == "19L":
                distance_ref = 72.4
            elif runway == "08":
                distance_ref = 58.9
            else: # "26"
                distance_ref = 65.4
        elif entry_point == "XILAN":
            if runway == "01L":
                distance_ref = 49.4
            elif runway == "19R":
                distance_ref = 44.7
            elif runway == "01R":
                distance_ref = 55.7
            elif runway == "19L":
                distance_ref = 43.5
            elif runway == "08":
                distance_ref = 56.6
            else: # "26"
                distance_ref = 33.7
   
        # adjust to much Opensky data
        # 100 ft vertically in the final segment corresponds to a ground distance of 0.314 NM
        distance_ref = distance_ref - 0.314
        distance_ref = distance_ref * 1852     # NM to meters
         
        if entry_point == "ELTOK":
            distance_ref = distance_ref + 14000 # distance to TMA border, measured in google earth
        elif entry_point == "XILAN":
            distance_ref = distance_ref + 36000 # distance to TMA border, measured in google earth
        elif entry_point == "NILUG":
            distance_ref = distance_ref +  23000 # distance to TMA border, measured in google earth

        add_distance = distance_sum - distance_ref
        add_distance_str = "{0:.3f}".format(add_distance)
        
        #add_distance = add_distance * 0.000539957 # meters to NM
        
        horizontal_PIs_df = horizontal_PIs_df.append({'flight_id': flight_id, 'date': date_str, 'hour': end_hour_str,
                                'TMA_distance': distance_str,
                                'TMA_additional_distance': add_distance_str,
                                'entry_point': entry_point,
                                'runway': runway}, ignore_index=True)

    horizontal_PIs_df.to_csv(full_output_filename, sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)


def main():
    
    for month in months:
        number_of_weeks = (5, 4)[month == '02' and not calendar.isleap(int(year))]
        #number_of_weeks = 1
        
        for week in range(0, number_of_weeks):
            
            for entry_point in entry_points:
                
                for runway in runways:
            
                    calculate_horizontal_PIs(month, week+1, entry_point, runway)
    
    
main()    

print("--- %s minutes ---" % ((time.time() - start_time)/60))