import numpy as np
import pandas as pd
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

import os

import time
start_time = time.time()

year = '2019'
airport_icao = "EIDW"

from constants_EIDW import *

DATA_DIR = os.path.join("data", airport_icao)
DATA_DIR = os.path.join(DATA_DIR, year)
DATASET_DATA_DIR = os.path.join(DATA_DIR, "Dataset")

states_df = pd.DataFrame()

filename = "dataset2.csv"
states_df = pd.read_csv(os.path.join(DATASET_DATA_DIR, filename), sep=' ',
                    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'endDate'],
                    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'endDate':str})
states_df.set_index(['flightId', 'sequence'], inplace=True)

number_of_flights = len(states_df.groupby(level='flightId'))
count = 0

# Runway 28L
rwy28L_lon = -6.290075
rwy28L_lat = 53.42243

square_lon = [-6.29, -6.29, -6.4, -6.4]
square_lat = [53.27, 53.57, 53.57, 53.27]

def check_square_contains_point(point):

    lons_lats_vect = np.column_stack((square_lon, square_lat)) # Reshape coordinates
    polygon = Polygon(lons_lats_vect) # create polygon

    return polygon.contains(point)


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
        states_df = states_df.drop(flight_id)
    
filename = "dataset3.csv"
states_df.to_csv(os.path.join(DATASET_DATA_DIR, filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)