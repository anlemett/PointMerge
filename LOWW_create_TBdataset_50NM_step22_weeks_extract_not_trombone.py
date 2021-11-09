import numpy as np
import pandas as pd
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

import os

import time
start_time = time.time()

year = '2019'
airport_icao = "LOWW"

from constants_LOWW import *

months = ['10']

DATA_DIR = os.path.join("data", airport_icao+"_50NM_rwy")
DATA_DIR = os.path.join(DATA_DIR, year)
DATASET_DIR = os.path.join(DATA_DIR, "Dataset")

def create_dataset(month, week):
    
    DATA_INPUT_DIR = os.path.join(DATA_DIR, "osn_"+ airport_icao + "_states_50NM_" + year)
    DATA_INPUT_DIR = os.path.join(DATA_INPUT_DIR, "osn_LOWW_states_50NM_2019_10_week" + str(week) + "_by_runways")
    input_filename = "osn_LOWW_states_50NM_2019_10_week" + str(week) + "_rwy16.csv"
    
    states_df = pd.read_csv(os.path.join(DATA_INPUT_DIR, input_filename), sep=' ',
                    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'],
                    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'beginDate':str, 'endDate':str})
    
    states_df.set_index(['flightId', 'sequence'], inplace=True)
    

    count = 0
    number_of_flights = len(states_df.groupby(level='flightId'))  


    filename = "week" + str(week)+ "_50NM_not_trombone_ids.txt"

    flight_ids_list = open(os.path.join(DATASET_DIR, filename),'r').read().split('\n')

    number_of_not_trombone_flights = len (flight_ids_list)
    print(number_of_not_trombone_flights)
    count = 0

    not_trombone_states_df = pd.DataFrame()

    for flight_id in flight_ids_list:
        count = count + 1
        print(number_of_not_trombone_flights, count)
    
        flight_df = states_df[states_df.index.get_level_values('flightId') == flight_id]
    
        not_trombone_states_df = not_trombone_states_df.append(flight_df)
    
    filename = "not_TB_dataset_week" + str(week) + ".csv"
    not_trombone_states_df.to_csv(os.path.join(DATASET_DIR, filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)

def main():
    
    for month in months:
        create_dataset(month, 1)
        create_dataset(month, 2)
        create_dataset(month, 3)
        create_dataset(month, 4)
    
    
main()

print("--- %s minutes ---" % ((time.time() - start_time)/60))