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

filename = "dataset4.csv"
states_df = pd.read_csv(os.path.join(DATASET_DATA_DIR, filename), sep=' ',
                    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'endDate'],
                    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'endDate':str})
states_df.set_index(['flightId', 'sequence'], inplace=True)

DATA_DIR = os.path.join(DATA_DIR, "PIs")
filename = "PIs_horizontal_by_flight_dataset.csv"
horizontal_PIs_by_flight_df = pd.read_csv(os.path.join(DATA_DIR, filename), sep=' ')
horizontal_PIs_by_flight_df.set_index(['flight_id'], inplace=True)

number_of_flights = len(states_df.groupby(level='flightId'))
count = 0

# no sign for lat because of 'N'
# '-' sign for lon because of 'W'
def dms2dd(as_string):
    degrees = int(as_string[:2])
    minutes = int(as_string[2:4])
    seconds = float(as_string[4:8])
    lat_dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
    degrees = -1*int(as_string[10:13])
    minutes = -1*int(as_string[13:15])
    seconds = -1*float(as_string[15:19])
    lon_dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)

    return lat_dd, lon_dd

ADSIS_lat, ADSIS_lon = dms2dd("534103.1N 0053934.0E")
ADSIS_square_lon = [ADSIS_lon - 0.06, ADSIS_lon - 0.06, ADSIS_lon + 0.06, ADSIS_lon + 0.06]
ADSIS_square_lat = [ADSIS_lat - 0.04, ADSIS_lat + 0.04, ADSIS_lat + 0.04, ADSIS_lat - 0.04]
    
KERAV_lat, KERAV_lon = dms2dd("533742.7N 0054557.3E")
KERAV_square_lon = [KERAV_lon - 0.04, KERAV_lon - 0.04, KERAV_lon + 0.04, KERAV_lon + 0.04]
KERAV_square_lat = [KERAV_lat - 0.03, KERAV_lat + 0.03, KERAV_lat + 0.03, KERAV_lat - 0.03]
  
KOGAX_lat, KOGAX_lon = dms2dd("533418.6N 0053814.1E")
KOGAX_square_lon = [KOGAX_lon - 0.04, KOGAX_lon - 0.04, KOGAX_lon + 0.04, KOGAX_lon + 0.04]
KOGAX_square_lat = [KOGAX_lat - 0.03, KOGAX_lat + 0.03, KOGAX_lat + 0.03, KOGAX_lat - 0.03]
 
def check_ADSIS_square_contains_point(point):

    lons_lats_vect = np.column_stack((ADSIS_square_lon, ADSIS_square_lat)) # Reshape coordinates
    polygon = Polygon(lons_lats_vect) # create polygon

    return polygon.contains(point)

def check_KERAV_square_contains_point(point):

    lons_lats_vect = np.column_stack((KERAV_square_lon, KERAV_square_lat)) # Reshape coordinates
    polygon = Polygon(lons_lats_vect) # create polygon

    return polygon.contains(point)

def check_KOGAX_square_contains_point(point):

    lons_lats_vect = np.column_stack((KOGAX_square_lon, KOGAX_square_lat)) # Reshape coordinates
    polygon = Polygon(lons_lats_vect) # create polygon

    return polygon.contains(point)


for flight_id, flight_df in states_df.groupby(level='flightId'):
    
    count = count + 1
    print(number_of_flights, count)
    
    entry_point_df = horizontal_PIs_by_flight_df[horizontal_PIs_by_flight_df.index.get_level_values('flight_id') == flight_id]
    entry_point = entry_point_df['entry_point'].item()

    if (not entry_point == 'BOYNE') and (not entry_point == 'BAGSO'):
        continue
    
    near_KERAV = False
    near_KOGAX = False
    
    for seq, row in flight_df.groupby(level='sequence'):
        lat = row.loc[(flight_id, seq)]['lat']
        lon = row.loc[(flight_id, seq)]['lon']
        if (check_KERAV_square_contains_point(Point(lon, lat))):
            near_KERAV = True
        if (check_KOGAX_square_contains_point(Point(lon, lat))):
            near_KOGAX = True
    if (not near_KERAV) or (not near_KOGAX):  
        states_df = states_df.drop(flight_id)
    
number_of_flights = len(states_df.groupby(level='flightId'))
print(number_of_flights)
filename = "dataset5.csv"
states_df.to_csv(os.path.join(DATASET_DATA_DIR, filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)