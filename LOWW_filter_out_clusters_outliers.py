import numpy as np
import pandas as pd
from shapely.geometry import Point
import os

import time
start_time = time.time()

year = '2019'
airport_icao = "LOWW"

#def filter_out(month, week):
def filter_out():
    DATA_DIR = os.path.join("data", airport_icao)
    DATA_DIR = os.path.join(DATA_DIR, year)
    
    DATASET_DATA_DIR = os.path.join(DATA_DIR, "Dataset")
    CLUSTERS_DATA_DIR = os.path.join(DATASET_DATA_DIR, "LOWW_dataset_TT_clusters")


    filename = "LOWW_dataset_TT2.csv"

    states_df = pd.read_csv(os.path.join(DATASET_DATA_DIR, filename), sep=' ',
                    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'endDate'],
                    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'endDate':str})
    states_df.set_index(['flightId', 'sequence'], inplace=True)

    number_of_flights = len(states_df.groupby(level='flightId'))


    filename = "LOWW_dataset_TT_clusters_outliers_flight_ids.txt"
    outliers_ids_set = set(open(os.path.join(CLUSTERS_DATA_DIR, filename) ,'r').read().split('\n'))

    for flight_id in outliers_ids_set:
        states_df = states_df.drop(flight_id)
        
    filename = "LOWW_dataset_TT.csv"
    states_df.to_csv(os.path.join(DATASET_DATA_DIR, filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)



def main():
    filter_out()
    
    
main()

print("--- %s minutes ---" % ((time.time() - start_time)/60))