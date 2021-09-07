import pandas as pd
import os

from datetime import datetime

import time
start_time = time.time()

year = '2019'
#airport_icao = "ESSA"
#airport_icao = "LOWW"
airport_icao = "EIDW"

if airport_icao == "EIDW":
    from constants_EIDW import *
elif airport_icao == "ESSA":
    from constants_ESSA import *
elif airport_icao == "LOWW":
    from constants_LOWW import *

DATA_DIR = os.path.join("data", airport_icao)
DATA_DIR = os.path.join(DATA_DIR, year)


def get_all_states(csv_input_file):

    df = pd.read_csv(csv_input_file, sep=' ',
                    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'endDate'],
                    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'endDate':str})
    
    df = df[['flightId', 'sequence', 'timestamp', 'altitude', 'velocity', 'endDate']]
    
    df.set_index(['flightId', 'sequence'], inplace=True)
    
    return df


def calculate_number_of_flights():
    
    DATA_INPUT_DIR = os.path.join(DATA_DIR, "Dataset")
    dataset_name = airport_icao + "_dataset_PM"
    #dataset_name = airport_icao + "_dataset_TT"
    input_filename = dataset_name + ".csv"

    full_input_filename = os.path.join(DATA_INPUT_DIR, input_filename)
         
    states_df = get_all_states(full_input_filename)

   
    
    flight_id_num = len(states_df.groupby(level='flightId'))
    print(dataset_name, flight_id_num)


    
calculate_number_of_flights()    

print("--- %s minutes ---" % ((time.time() - start_time)/60))