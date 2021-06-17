import pandas as pd
import os

from datetime import datetime
import calendar

import time
start_time = time.time()

year = '2019'
airport_icao = "LOWW"

from constants_LOWW import *

#months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '12', '12']
months = ['10']

DATA_DIR = os.path.join("data", airport_icao)
DATA_DIR = os.path.join(DATA_DIR, year)

def get_all_states(csv_input_file):

    df = pd.read_csv(csv_input_file, sep=' ',
                    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'endDate'],
                    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'endDate':str})
    
    df.set_index(['flightId', 'sequence'], inplace=True)
    
    return df


def remove_ground_movements(month, week):
    
    DATA_INPUT_DIR = os.path.join(DATA_DIR, "osn_"+ airport_icao + "_states_TMA_" + year + '_origin')
    input_filename = "osn_"+ airport_icao + "_states_TMA_" + year + '_' + month + "_week" + str(week) + ".csv"
    full_input_filename = os.path.join(DATA_INPUT_DIR, input_filename)
         
    DATA_OUTPUT_DIR = os.path.join(DATA_DIR, "osn_"+ airport_icao + "_states_TMA_" + year)
    if not os.path.exists(DATA_OUTPUT_DIR):
        os.makedirs(DATA_OUTPUT_DIR)
    output_filename = "osn_"+ airport_icao + "_states_TMA_" + year + '_' + month + "_week" + str(week) + ".csv"
    full_output_filename = os.path.join(DATA_OUTPUT_DIR, output_filename)

    states_df = get_all_states(full_input_filename)
    
    number_of_flights = len(states_df.groupby(level='flightId'))
    print(number_of_flights)
        
    flight_id_num = len(states_df.groupby(level='flightId'))

    new_states_df = pd.DataFrame()
    count = 0
    
    for flight_id, flight_id_df in states_df.groupby(level='flightId'):
        
        count = count + 1
        print(year, month, week, flight_id_num, count, flight_id)
        
        new_flight_df = pd.DataFrame()
        
        for seq, row in flight_id_df.groupby(level='sequence'):
            
            if row['altitude'].values[0] > 50: # 100 ???
                new_flight_df = new_flight_df.append(row)
            else:
                break
            
        new_states_df = new_states_df.append(new_flight_df)

    new_states_df.to_csv(full_output_filename, sep=' ', encoding='utf-8', float_format='%.3f', header=False, index=True)


    
def main():
    
    for month in months:
        number_of_weeks = (5, 4)[month == '02' and not calendar.isleap(int(year))]
        
        for week in range(0, number_of_weeks):
        
            remove_ground_movements(month, week+1)
               
    
main()    

print("--- %s minutes ---" % ((time.time() - start_time)/60))