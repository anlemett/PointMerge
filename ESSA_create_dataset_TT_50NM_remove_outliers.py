import numpy as np
import pandas as pd

import os

import time
start_time = time.time()

year = '2019'
airport_icao = "ESSA"

from constants_ESSA import *

def filter_out():
    DATA_DIR = os.path.join("data", airport_icao + "_50NM")
    DATA_DIR = os.path.join(DATA_DIR, year)
    
    DATASET_DATA_DIR = os.path.join(DATA_DIR, "Dataset")

    filename = "ESSA_dataset_TT_50NM_1.csv"

    states_df = pd.read_csv(os.path.join(DATASET_DATA_DIR, filename), sep=' ',
                    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'],
                    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':int, 'altitude':float, 'velocity':float, 'beginDate':str, 'endDate':str})
    states_df.set_index(['flightId', 'sequence'], inplace=True)

    number_of_flights = len(states_df.groupby(level='flightId'))


    filename = "ESSA_dataset_TT_50NM_remove_flight_ids.txt"
    outliers_ids_set = set(open(os.path.join(DATASET_DATA_DIR, filename) ,'r').read().split('\n'))

    for flight_id in outliers_ids_set:
        states_df = states_df.drop(flight_id)
        
    filename = "ESSA_dataset_TT_50NM.csv"
    states_df.to_csv(os.path.join(DATASET_DATA_DIR, filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)



def main():
    filter_out()
    
    
main()

print("--- %s minutes ---" % ((time.time() - start_time)/60))