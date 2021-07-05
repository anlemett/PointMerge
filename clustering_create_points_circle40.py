import numpy as np
import pandas as pd
from shapely.geometry import Point
import os

import time
start_time = time.time()

year = '2019'
airport_icao = "EIDW"

#input_filename = airport_icao + "_dataset_PM"
input_filename = airport_icao + "_dataset_TT"

output_filename = input_filename + "_circle40_points.csv"

radius = 0.67
center = Point(-6.3, 53.3)

if airport_icao == "EIDW":
    center = Point(-6.3, 53.3)

def check_circle_contains_point(circle_center, circle_radius, point): 
   
    if point.distance(circle_center) <= circle_radius:
        return True
    else:
        return False

DATA_DIR = os.path.join("data", airport_icao)
DATA_DIR = os.path.join(DATA_DIR, year)

DATA_INPUT_DIR = os.path.join(DATA_DIR, "Dataset")

states_df = pd.read_csv(os.path.join(DATA_INPUT_DIR, input_filename + ".csv"), sep=' ',
                    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'endDate'],
                    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'endDate':str})
states_df.set_index(['flightId', 'sequence'], inplace=True)

DATA_OUTPUT_DIR = os.path.join(DATA_DIR, "Clustering")

circle40_points_df = pd.DataFrame(columns=['flight_id', 'lat', 'lon'])
    
count = 0
number_of_flights = len(states_df.groupby(level='flightId'))  

for flight_id, flight_df in states_df.groupby(level='flightId'): 
    count = count + 1
    print(number_of_flights, count, flight_id)
     
    circle40_lat = 0
    circle40_lon = 0
    
    for seq, row in flight_df.groupby(level='sequence'):
        lat = row.loc[(flight_id, seq)]['lat']
        lon = row.loc[(flight_id, seq)]['lon']
        if (check_circle_contains_point(center, radius, Point(lon, lat))):
            circle40_lat = lat
            circle40_lon = lon
            break
        
    circle40_points_df = circle40_points_df.append({'flight_id':flight_id, 'lat':circle40_lat, 'lon':circle40_lon}, ignore_index=True)
        
circle40_points_df.to_csv(os.path.join(DATA_OUTPUT_DIR, output_filename), sep=' ', encoding='utf-8', float_format='%.3f', index = False, header = True)   
        
        
        
        