import numpy as np
import pandas as pd

import os

import time
start_time = time.time()

year = '2019'
airport_icao = "EIDW"

from constants_EIDW import *

DATA_DIR = os.path.join("data", airport_icao+"_50NM_rwy")
DATA_DIR = os.path.join(DATA_DIR, year)
DATASET_DATA_DIR = os.path.join(DATA_DIR, "Dataset")

states_df = pd.DataFrame()

filename = "PM_dataset_month.csv"
states_df = pd.read_csv(os.path.join(DATASET_DATA_DIR, filename), sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'],
    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'beginDate':str, 'endDate':str})
states_df.set_index(['flightId', 'sequence'], inplace=True)

filename = "EIDW_50NM_dataset_PM_remove_flight_ids.txt"

flight_ids_list = open(os.path.join(DATASET_DATA_DIR, filename),'r').read().split('\n')

len = len (flight_ids_list)
count = 0

for flight_id in flight_ids_list:
    count = count + 1
    print(len, count)
    states_df = states_df.drop(flight_id)
    
filename = "PM_dataset_month2.csv"
states_df.to_csv(os.path.join(DATASET_DATA_DIR, filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)