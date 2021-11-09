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

filename = "PM_dataset_month3.csv"
states_df = pd.read_csv(os.path.join(DATASET_DATA_DIR, filename), sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'endDate'],
    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'endDate':str})
states_df.set_index(['flightId', 'sequence'], inplace=True)

number_of_flights = len(states_df.groupby(level='flightId'))
count = 0

DATA_DIR = os.path.join(DATA_DIR, "PIs")

entry_points_df = pd.DataFrame()

for week in range(1, 5):
    
    filename = "entry_points_and_runways_2019_10_week" + str(week) + ".csv"

    week_df = pd.read_csv(os.path.join(DATA_DIR, filename), sep=' ')
    
    entry_points_df = entry_points_df.append(week_df)

entry_points_df.set_index(['flight_id'], inplace=True)

number_of_flights = len(states_df.groupby(level='flightId'))
count = 0

def check_entrypoint_square_contains_point(entry_point, point):
    if entry_point == "ABLIN":
        square_lon = [LIPGO_lon - 0.05, LIPGO_lon - 0.05, LIPGO_lon + 0.05, LIPGO_lon + 0.05]
        square_lat = [LIPGO_lat - 0.05, LIPGO_lat + 0.05, LIPGO_lat + 0.05, LIPGO_lat - 0.05]
    elif entry_point == "BAGSO":
        square_lon = [BAGSO_lon - 0.05, BAGSO_lon - 0.05, BAGSO_lon + 0.05, BAGSO_lon + 0.05]
        square_lat = [BAGSO_lat - 0.05, BAGSO_lat + 0.05, BAGSO_lat + 0.05, BAGSO_lat - 0.05]
    elif entry_point == "BAMLI":
        square_lon = [BAMLI_lon - 0.05, BAMLI_lon - 0.05, BAMLI_lon + 0.05, BAMLI_lon + 0.05]
        square_lat = [BAMLI_lat - 0.05, BAMLI_lat + 0.05, BAMLI_lat + 0.05, BAMLI_lat - 0.05]
    elif entry_point == "BOYNE":
        square_lon = [BOYNE_lon - 0.05, BOYNE_lon - 0.05, BOYNE_lon + 0.05, BOYNE_lon + 0.05]
        square_lat = [BOYNE_lat - 0.05, BOYNE_lat + 0.05, BOYNE_lat + 0.05, BOYNE_lat - 0.05]
    elif entry_point == "BUNED":
        square_lon = [BUNED_lon - 0.05, BUNED_lon - 0.05, BUNED_lon + 0.05, BUNED_lon + 0.05]
        square_lat = [BUNED_lat - 0.05, BUNED_lat + 0.05, BUNED_lat + 0.05, BUNED_lat - 0.05]
    elif entry_point == "LIPGO":
        square_lon = [LIPGO_lon - 0.05, LIPGO_lon - 0.05, LIPGO_lon + 0.05, LIPGO_lon + 0.05]
        square_lat = [LIPGO_lat - 0.05, LIPGO_lat + 0.05, LIPGO_lat + 0.05, LIPGO_lat - 0.05]
    elif entry_point == "NIMAT":
        square_lon = [NIMAT_lon - 0.05, NIMAT_lon - 0.05, NIMAT_lon + 0.05, NIMAT_lon + 0.05]
        square_lat = [NIMAT_lat - 0.05, NIMAT_lat + 0.05, NIMAT_lat + 0.05, NIMAT_lat - 0.05]
    elif entry_point == "OLAPO":
        square_lon = [OLAPO_lon - 0.05, OLAPO_lon - 0.05, OLAPO_lon + 0.05, OLAPO_lon + 0.05]
        square_lat = [OLAPO_lat - 0.05, OLAPO_lat + 0.05, OLAPO_lat + 0.05, OLAPO_lat - 0.05]
    elif entry_point == "OSGAR":
        square_lon = [OSGAR_lon - 0.05, OSGAR_lon - 0.05, OSGAR_lon + 0.05, OSGAR_lon + 0.05]
        square_lat = [OSGAR_lat - 0.05, OSGAR_lat + 0.05, OSGAR_lat + 0.05, OSGAR_lat - 0.05]
    elif entry_point == "SUTEX":
        square_lon = [SUTEX_lon - 0.05, SUTEX_lon - 0.05, SUTEX_lon + 0.05, SUTEX_lon + 0.05]
        square_lat = [SUTEX_lat - 0.05, SUTEX_lat + 0.05, SUTEX_lat + 0.05, SUTEX_lat - 0.05]
    elif entry_point == "VATRY":
        square_lon = [VATRY_lon - 0.05, VATRY_lon - 0.05, VATRY_lon + 0.05, VATRY_lon + 0.05]
        square_lat = [VATRY_lat - 0.05, VATRY_lat + 0.05, VATRY_lat + 0.05, VATRY_lat - 0.05]

    lons_lats_vect = np.column_stack((square_lon, square_lat)) # Reshape coordinates
    polygon = Polygon(lons_lats_vect) # create polygon

    return polygon.contains(point)


entry_points_flight_ids = []
for flight_id, flight_df in states_df.groupby(level='flightId'):
    
    count = count + 1
    print(number_of_flights, count)
    
    entry_point_df = entry_points_df[entry_points_df.index.get_level_values('flight_id') == flight_id]
    entry_point = entry_point_df['entry_point'].item()
    #print(entry_point)
    
    point_lat = flight_df["lat"].to_list()[0]
    point_lon = flight_df["lon"].to_list()[0]
    point = Point(point_lon, point_lat)
     
    if check_entrypoint_square_contains_point(entry_point, point):
        # add flight_id to the list
        entry_points_flight_ids.append(flight_id)
    else:
        states_df = states_df.drop(flight_id)
    
filename = "PM_dataset_month4.csv"
states_df.to_csv(os.path.join(DATASET_DATA_DIR, filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)

# save ids of the entry points fligths
filename = "PM_dataset_entry_points_flight_ids.csv"
file_to_write = open(os.path.join(DATASET_DATA_DIR, filename),'w')

for element in entry_points_flight_ids:
    file_to_write.write(element + "\n")
file_to_write.close()

