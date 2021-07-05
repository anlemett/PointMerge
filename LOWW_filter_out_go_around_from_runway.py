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
    DATA_INPUT_DIR = os.path.join(DATA_DIR, "Dataset")
    #DATA_INPUT_DIR = os.path.join(DATA_DIR, "osn_"+ airport_icao + "_states_TMA_" + year)
    #DATA_INPUT_DIR = os.path.join(DATA_INPUT_DIR, "osn_"+ airport_icao + "_states_TMA_" + year + "_" + month + "_week" + str(week) + "_by_runways")

    DATA_OUTPUT_DIR = os.path.join(DATA_DIR, "Dataset")
    #DATA_OUTPUT_DIR = os.path.join(DATA_DIR, "osn_"+ airport_icao + "_states_TMA_" + year)
    #DATA_OUTPUT_DIR = os.path.join(DATA_OUTPUT_DIR, "osn_"+ airport_icao + "_states_TMA_" + year + "_" + month + "_week" + str(week) + "_by_runways")
    #DATA_OUTPUT_DIR = os.path.join(DATA_OUTPUT_DIR, "filter_out_go_around_from_runway")


    #filename = "osn_"+ airport_icao + "_states_TMA_" + year + "_" + month + "_week" + str(week) + "_rwy28"
    filename = "LOWW_dataset_TT.csv"

    states_df = pd.read_csv(os.path.join(DATA_INPUT_DIR, filename), sep=' ',
                    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'endDate'],
                    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'endDate':str})
    states_df.set_index(['flightId', 'sequence'], inplace=True)

    number_of_flights = len(states_df.groupby(level='flightId'))
    count = 0

    flight_id_list = []
    altitude_threshold = 500
    for flight_id, flight_df in states_df.groupby(level='flightId'):
    
        count = count + 1
        print(number_of_flights, count)
    
        drop = False
    
        min_altitude = 0
        for seq, row in flight_df.groupby(level='sequence'):
            if seq == 0:
                min_altitude = row.loc[(flight_id, seq)]['altitude']
                continue
            row_altitude = row.loc[(flight_id, seq)]['altitude']

            if row_altitude < min_altitude:
                min_altitude = row.loc[(flight_id, seq)]['altitude']
            elif row_altitude - min_altitude > altitude_threshold:
                drop = True
                break
        if drop:  
            states_df = states_df.drop(flight_id)
            flight_id_list.append(flight_id)
    
    number_of_flights = len(states_df.groupby(level='flightId'))
    print(number_of_flights)
    
    filename = "LOWW_dataset_TT2.csv"
    states_df.to_csv(os.path.join(DATA_OUTPUT_DIR, filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)

    flight_id_set = set(flight_id_list)
    filename = "LOWW_dataset_TT_remove_flight_ids.txt"
    with open(os.path.join(DATA_OUTPUT_DIR, filename), 'w') as filehandle:
        for listitem in flight_id_set:
            filehandle.write('%s\n' % listitem)

def main():
    filter_out()
    #for week in range (1,5):
    #    filter_out("10", week)
    
    
main()

print("--- %s minutes ---" % ((time.time() - start_time)/60))