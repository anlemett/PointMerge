import numpy as np
import pandas as pd
from shapely.geometry import Point
import os

import time
start_time = time.time()

year = '2019'
airport_icao = "EIDW"
#airport_icao = "ESSA"
#airport_icao = "LOWW"

input_filename = airport_icao + "_dataset_PM"
#input_filename = airport_icao + "_dataset_TT"

output_filename = input_filename + "_TMA_borders_points.csv"


DATA_DIR = os.path.join("data", airport_icao)
DATA_DIR = os.path.join(DATA_DIR, year)

DATA_INPUT_DIR = os.path.join(DATA_DIR, "Dataset")

states_df = pd.read_csv(os.path.join(DATA_INPUT_DIR, input_filename + ".csv"), sep=' ',
                    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'endDate'],
                    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'endDate':str})
states_df.set_index(['flightId', 'sequence'], inplace=True)

DATA_OUTPUT_DIR = os.path.join(DATA_DIR, "Clustering")

TMA_borders_points_df = pd.DataFrame(columns=['flight_id', 'lat', 'lon'])
    
count = 0
number_of_flights = len(states_df.groupby(level='flightId'))  

for flight_id, flight_df in states_df.groupby(level='flightId'): 
    count = count + 1
    print(number_of_flights, count, flight_id)

    entry_point_lon = flight_df['lon'][0]
    entry_point_lat = flight_df['lat'][0]
    
    TMA_borders_points_df = TMA_borders_points_df.append({'flight_id':flight_id, 'lat':entry_point_lat, 'lon':entry_point_lon}, ignore_index=True)
        
TMA_borders_points_df.to_csv(os.path.join(DATA_OUTPUT_DIR, output_filename), sep=' ', encoding='utf-8', float_format='%.3f', index = False, header = True)   
