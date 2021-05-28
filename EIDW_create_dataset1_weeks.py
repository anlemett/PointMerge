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
DATA_OUTPUT_DIR = os.path.join(DATA_DIR, "Dataset")

def create_dataset(month, week):
    
    DATA_INPUT_DIR1 = os.path.join(DATA_DIR, "osn_"+ airport_icao + "_states_TMA_" + year)
    DATA_INPUT_DIR1 = os.path.join(DATA_INPUT_DIR1, "osn_EIDW_states_TMA_2019_10_week" + str(week) + "_by_runways")
    input_filename1 = "osn_EIDW_states_TMA_2019_10_week" + str(week) + "_rwy28.csv"
    
    states_df = pd.read_csv(os.path.join(DATA_INPUT_DIR1, input_filename1), sep=' ',
                    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'endDate'],
                    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'endDate':str})
    
    states_df.set_index(['flightId', 'sequence'], inplace=True)
    
    input_filename2 = "week" + str(week)+ "_flight_ids.txt"
    flight_ids_list = open(input_filename2,'r').read().split('\n')
    #print(flight_ids_list)
    
    #dataset_df = pd.DataFrame(columns=['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'endDate'])
    dataset_df = pd.DataFrame()
    count = 0
    number_of_flights = len(states_df.groupby(level='flightId'))  
    
    for flight_id, flight_id_group in states_df.groupby(level='flightId'): 
        count = count + 1
        print(year, month, week, number_of_flights, count, flight_id)
              
        if flight_id in flight_ids_list:
            dataset_df = dataset_df.append(flight_id_group)
    
    filename = "dataset_week" + str(week) + ".csv"
    dataset_df.to_csv(os.path.join(DATA_INPUT_DIR1, filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)
    
def main():
    
    for month in months:
        create_dataset(month, 1)
        create_dataset(month, 2)
        create_dataset(month, 3)
        create_dataset(month, 4)
    
    
main()    

print("--- %s minutes ---" % ((time.time() - start_time)/60))