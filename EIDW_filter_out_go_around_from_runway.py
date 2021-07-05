import numpy as np
import pandas as pd
from shapely.geometry import Point
import os

import time
start_time = time.time()

year = '2019'
airport_icao = "EIDW"

from constants_EIDW import *

# Runway 28L
rwy28L_lon = -6.290075
rwy28L_lat = 53.42243

left_circle_center = Point(-6.35, 53.42)
left_circle_radius = 0.052

down_circle_center = Point(-6.23, 53.35)
down_circle_radius = 0.029

up_circle_center = Point(-6.14, 53.46)
up_circle_radius = 0.028

left_circle2_center = Point(-6.3, 53.45)
left_circle2_radius = 0.029

up_circle2_center = Point(-6.1, 53.46)
up_circle2_radius = 0.023

def check_circle_contains_point(circle_center, circle_radius, point): 
   
    if point.distance(circle_center) < circle_radius:
        return True
    else:
        return False


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
    filename = "EIDW_dataset_TT.csv"

    states_df = pd.read_csv(os.path.join(DATA_INPUT_DIR, filename), sep=' ',
                    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'endDate'],
                    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'endDate':str})
    states_df.set_index(['flightId', 'sequence'], inplace=True)

    number_of_flights = len(states_df.groupby(level='flightId'))
    count = 0

    flight_id_list = []
    for flight_id, flight_df in states_df.groupby(level='flightId'):
    
        count = count + 1
        print(number_of_flights, count)
    
        drop = False
    
        for seq, row in flight_df.groupby(level='sequence'):
            lat = row.loc[(flight_id, seq)]['lat']
            lon = row.loc[(flight_id, seq)]['lon']
            if (check_circle_contains_point(left_circle_center, left_circle_radius, Point(lon, lat))):
                drop = True
                break
            if (check_circle_contains_point(up_circle_center, up_circle_radius, Point(lon, lat))):
                drop = True
                break
            if (check_circle_contains_point(down_circle_center, down_circle_radius, Point(lon, lat))):
                drop = True
                break
            if (check_circle_contains_point(left_circle2_center, left_circle2_radius, Point(lon, lat))):
                drop = True
                break
            if (check_circle_contains_point(up_circle2_center, up_circle2_radius, Point(lon, lat))):
                drop = True
                break
        if drop:  
            states_df = states_df.drop(flight_id)
            flight_id_list.append(flight_id)
    
    number_of_flights = len(states_df.groupby(level='flightId'))
    print(number_of_flights)
    
    filename = "EIDW_dataset_TT2.csv"
    states_df.to_csv(os.path.join(DATA_OUTPUT_DIR, filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)

    flight_id_set = set(flight_id_list)
    filename = "EIDW_dataset_TT_remove_flight_ids.txt"
    with open(os.path.join(DATA_OUTPUT_DIR, filename), 'w') as filehandle:
        for listitem in flight_id_set:
            filehandle.write('%s\n' % listitem)

def main():
    filter_out()
    #for week in range (1,5):
    #    filter_out("10", week)
    
    
main()

print("--- %s minutes ---" % ((time.time() - start_time)/60))