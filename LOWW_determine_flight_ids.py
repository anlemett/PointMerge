import numpy as np
import pandas as pd
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

import os

import time
start_time = time.time()

year = '2019'
airport_icao = "LOWW"

DATA_DIR = os.path.join("data", airport_icao)
DATA_DIR = os.path.join(DATA_DIR, year)
DATA_INPUT_DIR = os.path.join(DATA_DIR, "osn_"+ airport_icao + "_states_TMA_" + year)

states_df = pd.DataFrame()

# change to the certain runway file
filename = "osn_LOWW_states_TMA_2019_10_week1.csv"

states_df = pd.read_csv(os.path.join(DATA_INPUT_DIR, filename), sep=' ',
                    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'endDate'],
                    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'endDate':str})
states_df.set_index(['flightId', 'sequence'], inplace=True)

number_of_flights = len(states_df.groupby(level='flightId'))
count = 0

square_lon = [16.25, 16.25, 16.45, 16.45, 16.25]
square_lat = [48.06, 48.12, 48.12, 48.06, 48.06]

def check_square_contains_point(point):

    lons_lats_vect = np.column_stack((square_lon, square_lat)) # Reshape coordinates
    polygon = Polygon(lons_lats_vect) # create polygon

    return polygon.contains(point)

ids_list = []

for flight_id, flight_df in states_df.groupby(level='flightId'):
    
    count = count + 1
    print(number_of_flights, count)
    
    drop = False
    
    for seq, row in flight_df.groupby(level='sequence'):
        lat = row.loc[(flight_id, seq)]['lat']
        lon = row.loc[(flight_id, seq)]['lon']
        if (check_square_contains_point(Point(lon, lat))):
            drop = True
            break
    if drop:  
        ids_list.append(flight_id)

print(ids_list)