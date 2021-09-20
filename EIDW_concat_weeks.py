import numpy as np
import pandas as pd
from calendar import monthrange
import os

import time
start_time = time.time()

year = '2019'
airport_icao = "EIDW"

from constants_EIDW import *

#months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '12', '12']
months = ['10']

DATA_DIR = os.path.join("data", airport_icao)
DATA_DIR = os.path.join(DATA_DIR, year)
DATA_DIR = os.path.join(DATA_DIR, "osn_"+ airport_icao + "_states_TMA_" + year)

states_df = pd.DataFrame()

for week in range(1, 5):

    DATA_INPUT_DIR = os.path.join(DATA_DIR, "osn_EIDW_states_TMA_2019_10_week" + str(week) + "_by_runways")
    input_filename = "osn_EIDW_states_TMA_2019_10_week" + str(week) + "_rwy28.csv"
    
    week_states_df = pd.read_csv(os.path.join(DATA_INPUT_DIR, input_filename), sep=' ',
                    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'endDate'],
                    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'endDate':str})
    
    states_df = states_df.append(week_states_df)
    
states_df.set_index(['flightId', 'sequence'], inplace=True)  

number_of_flights = len(states_df.groupby(level='flightId'))

print(number_of_flights)

# 7763
# Final TT dataset: 2571

print("--- %s minutes ---" % ((time.time() - start_time)/60))