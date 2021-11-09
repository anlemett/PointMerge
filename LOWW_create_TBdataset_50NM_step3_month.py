import numpy as np
import pandas as pd

import os

import time
start_time = time.time()

year = '2019'
airport_icao = "LOWW"

from constants_LOWW import *

#months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '12', '12']
months = ['10']

DATA_DIR = os.path.join("data", airport_icao+"_50NM_rwy")
DATA_DIR = os.path.join(DATA_DIR, year)
DATASET_DIR = os.path.join(DATA_DIR, "Dataset")

states_df = pd.DataFrame()

for week in range(1, 5):
    filename = "TB_dataset_week" + str(week) + ".csv"
    
    week_states_df = pd.read_csv(os.path.join(DATASET_DIR, filename), sep=' ',
        names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'],
        dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'beginDate':str, 'endDate':str})
    
    states_df = states_df.append(week_states_df)

filename = "TB_dataset_month.csv"
states_df.to_csv(os.path.join(DATASET_DIR, filename), sep=' ', encoding='utf-8', float_format='%.3f', index = False, header = False)

print("--- %s minutes ---" % ((time.time() - start_time)/60))