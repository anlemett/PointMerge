import numpy as np
import pandas as pd

import os

import time
start_time = time.time()

year = '2019'
airport_icao = "LOWW"

from constants_LOWW import *

DATA_DIR = os.path.join("data", airport_icao+"_50NM_rwy")
DATA_DIR = os.path.join(DATA_DIR, year)
DATASET_DIR = os.path.join(DATA_DIR, "Dataset")

states_df = pd.DataFrame()

filename = "TB_dataset_month.csv"
states_df = pd.read_csv(os.path.join(DATASET_DIR, filename), sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'],
    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'beginDate':str, 'endDate':str})
states_df.set_index(['flightId', 'sequence'], inplace=True)

filename = "LOWW_50NM_dataset_TB_remove_flight_ids.txt"

flight_ids_list = open(os.path.join(DATASET_DIR, filename),'r').read().split('\n')

number_of_flights = len (flight_ids_list)
count = 0

for flight_id in flight_ids_list:
    count = count + 1
    print(number_of_flights, count)
    flight_df = states_df[states_df.index.get_level_values('flightId') == flight_id]
    if not flight_df.empty:
        states_df = states_df.drop(flight_id)
    
filename = "TB_dataset_month2.csv"
states_df.to_csv(os.path.join(DATASET_DIR, filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)