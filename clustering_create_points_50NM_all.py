import numpy as np
import pandas as pd
from shapely.geometry import Point
import os

import time
start_time = time.time()

year = '2019'
airport_icao = "LOWW"

DATA_DIR = os.path.join("data", airport_icao + "_50NM_rwy")
DATA_DIR = os.path.join(DATA_DIR, year)

DATA_INPUT_DIR = os.path.join(DATA_DIR, "osn_LOWW_states_50NM_2019")
DATA_INPUT_DIR1 = os.path.join(DATA_INPUT_DIR, "osn_LOWW_states_50NM_2019_10_week1_by_runways")
DATA_INPUT_DIR2 = os.path.join(DATA_INPUT_DIR, "osn_LOWW_states_50NM_2019_10_week2_by_runways")
DATA_INPUT_DIR3 = os.path.join(DATA_INPUT_DIR, "osn_LOWW_states_50NM_2019_10_week3_by_runways")
DATA_INPUT_DIR4 = os.path.join(DATA_INPUT_DIR, "osn_LOWW_states_50NM_2019_10_week4_by_runways")

input_filename1 = "osn_LOWW_states_50NM_2019_10_week1_rwy16"
input_filename2 = "osn_LOWW_states_50NM_2019_10_week2_rwy16"
input_filename3 = "osn_LOWW_states_50NM_2019_10_week3_rwy16"
input_filename4 = "osn_LOWW_states_50NM_2019_10_week4_rwy16"

output_filename = "osn_LOWW_states_50NM_2019_10_borders_points.csv"


states_df1 = pd.read_csv(os.path.join(DATA_INPUT_DIR1, input_filename1 + ".csv"), sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'],
    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':int, 'altitude':float, 'velocity':float, 'beginDate':str, 'endDate':str})

states_df2 = pd.read_csv(os.path.join(DATA_INPUT_DIR2, input_filename2 + ".csv"), sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'],
    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':int, 'altitude':float, 'velocity':float, 'beginDate':str, 'endDate':str})

states_df3 = pd.read_csv(os.path.join(DATA_INPUT_DIR3, input_filename3 + ".csv"), sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'],
    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':int, 'altitude':float, 'velocity':float, 'beginDate':str, 'endDate':str})

states_df4 = pd.read_csv(os.path.join(DATA_INPUT_DIR4, input_filename4 + ".csv"), sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'],
    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':int, 'altitude':float, 'velocity':float, 'beginDate':str, 'endDate':str})

frames = [states_df1, states_df2, states_df3, states_df4]
states_df = pd.concat(frames)
states_df.set_index(['flightId', 'sequence'], inplace=True)
num_flights = len(states_df.groupby(level='flightId'))
print(num_flights)


DATA_OUTPUT_DIR = os.path.join(DATA_DIR, "Clustering")
if not os.path.exists(DATA_OUTPUT_DIR):
    os.makedirs(DATA_OUTPUT_DIR)
    
borders_points_df = pd.DataFrame(columns=['flight_id', 'lat', 'lon'])

count = 0
number_of_flights = len(states_df.groupby(level='flightId'))  

for flight_id, flight_df in states_df.groupby(level='flightId'): 
    count = count + 1
    print(number_of_flights, count, flight_id)
    
    entry_point_lon = flight_df['lon'][0]
    entry_point_lat = flight_df['lat'][0]
    
    borders_points_df = borders_points_df.append({'flight_id':flight_id, 'lat':entry_point_lat, 'lon':entry_point_lon}, ignore_index=True)
        
borders_points_df.to_csv(os.path.join(DATA_OUTPUT_DIR, output_filename), sep=' ', encoding='utf-8', float_format='%.3f', index = False, header = True)   
        
        
        
        