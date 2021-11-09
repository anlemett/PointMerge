import numpy as np
import pandas as pd
from calendar import monthrange
import os
from shapely.geometry import Point

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

# Vienna RWY 16 transitions

# no sign for lat because of 'N'
# no sign for lon because of 'E'
def dms2dd(as_string):
    degrees = int(as_string[:2])
    minutes = int(as_string[2:4])
    seconds = float(as_string[4:9])
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);

    return dd;

BALAD_5L_lat_dms = ["474600.21","475208.28","480001.58","480641.40","481321.01","482141.30","482746.61","483235.64","483113.99","482625.53","482215.23"]
BALAD_5L_lat = []
for element in BALAD_5L_lat_dms:
    BALAD_5L_lat.append(dms2dd(element))

BALAD_5L_lon_dms = ["161402.56","162943.88","165007.89","164500.42","163951.68","163621.20","163346.76","163144.11","162429.77","162632.83","162816.89"]
BALAD_5L_lon = []
for element in BALAD_5L_lon_dms:
    BALAD_5L_lon.append(dms2dd(element))
    
MABOD_6L_lat_dms = ["483428.41","4828 21.00","481457.85","481321.01","482141.30","482746.61","483235.64","483113.99","482625.53","482215.23"]
MABOD_6L_lat = []
for element in MABOD_6L_lat_dms:
    MABOD_6L_lat.append(dms2dd(element))

MABOD_6L_lon_dms = ["164124.35","164339.00","164830.52","163951.68","163621.20","163346.76","163144.11","162429.77","162632.83","162816.89"]
MABOD_6L_lon = []
for element in MABOD_6L_lon_dms:
    MABOD_6L_lon.append(dms2dd(element))

NERDU_6L_lat_dms = ["482853.39","481741.38","481917.45","482503.52","482951.86","483113.99","482625.53","482215.23"]
NERDU_6L_lat = []
for element in NERDU_6L_lat_dms:
    NERDU_6L_lat.append(dms2dd(element))
    
NERDU_6L_lon_dms = ["160557.34","161319.97","162147.40","161919.46","161715.76","162429.77","162632.83","162816.89"]
NERDU_6L_lon = []
for element in NERDU_6L_lon_dms:
    NERDU_6L_lon.append(dms2dd(element))

PESAT_5L_lat_dms = ["474253.75","480001.58","480641.40","481321.01","482141.30","482746.61","483235.64","483113.99","482625.53","482215.23"]
PESAT_5L_lat = []
for element in PESAT_5L_lat_dms:
    PESAT_5L_lat.append(dms2dd(element))

PESAT_5L_lon_dms = ["170311.37","165007.89","164500.42","163951.68","163621.20","163346.76","163144.11","162429.77","162632.83","162816.89"]
PESAT_5L_lon = []
for element in PESAT_5L_lon_dms:
    PESAT_5L_lon.append(dms2dd(element))
    
one_lon = NERDU_6L_lon[1]
one_lat = NERDU_6L_lat[1]
one_circle_center = Point(one_lon, one_lat)
    
two_lon = NERDU_6L_lon[2]
two_lat = NERDU_6L_lat[2]
two_circle_center = Point(two_lon, two_lat)

new_lon = (NERDU_6L_lon[2] + NERDU_6L_lon[3])/2
new_lat = (NERDU_6L_lat[2] + NERDU_6L_lat[3])/2
new_circle_center = Point(new_lon, new_lat)
    
three_lon = NERDU_6L_lon[3]
three_lat = NERDU_6L_lat[3]
three_circle_center = Point(three_lon, three_lat)

four_lon = PESAT_5L_lon[8]
four_lat = PESAT_5L_lat[8]
four_circle_center = Point(four_lon, four_lat)
    
five_lon = MABOD_6L_lon[0]
five_lat = MABOD_6L_lat[0]
five_circle_center = Point(five_lon, five_lat)

six_lon = MABOD_6L_lon[1]
six_lat = MABOD_6L_lat[1]
six_circle_center = Point(six_lon, six_lat)

seven_lon = PESAT_5L_lon[4]
seven_lat = PESAT_5L_lat[4]
seven_circle_center = Point(seven_lon, seven_lat)
    
eight_lon = PESAT_5L_lon[3]
eight_lat = PESAT_5L_lat[3]
eight_circle_center = Point(eight_lon, eight_lat)
    
nine_lon = MABOD_6L_lon[2]
nine_lat = MABOD_6L_lat[2]
nine_circle_center = Point(nine_lon, nine_lat)

ten_lon = PESAT_5L_lon[5]
ten_lat = PESAT_5L_lat[5]
ten_circle_center = Point(ten_lon, ten_lat)

#radius = 0.05
radius = 0.02

def check_circle_contains_point(circle_center, circle_radius, point): 
   
    if point.distance(circle_center) <= circle_radius:
        return True
    else:
        return False
    
#8
#1 2
#1 3 - remove
#6 7
#6 9
#6 10
#6 4
#6 5
#3 4
  
def create_dataset(month, week):
    
    DATA_INPUT_DIR = os.path.join(DATA_DIR, "osn_"+ airport_icao + "_states_50NM_" + year)
    DATA_INPUT_DIR = os.path.join(DATA_INPUT_DIR, "osn_LOWW_states_50NM_2019_10_week" + str(week) + "_by_runways")
    input_filename = "osn_LOWW_states_50NM_2019_10_week" + str(week) + "_rwy16.csv"
    
    states_df = pd.read_csv(os.path.join(DATA_INPUT_DIR, input_filename), sep=' ',
                    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'],
                    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'beginDate':str, 'endDate':str})
    
    states_df.set_index(['flightId', 'sequence'], inplace=True)
    

    dataset_df = pd.DataFrame()
    count = 0
    number_of_flights = len(states_df.groupby(level='flightId'))  
    
    trombone_flights_ids = []
    not_trombone_flights_ids = []
    
    for flight_id, flight_df in states_df.groupby(level='flightId'): 
        count = count + 1
        #print(year, month, week, number_of_flights, count, flight_id)
        
        keep = False
    
        for seq, row in flight_df.groupby(level='sequence'):
            lat = row.loc[(flight_id, seq)]['lat']
            lon = row.loc[(flight_id, seq)]['lon']
            if (check_circle_contains_point(eight_circle_center, radius, Point(lon, lat))):
                keep = True
                break
        if keep:
            trombone_flights_ids.append(flight_id)
            continue
        
        for seq, row in flight_df.groupby(level='sequence'):
            lat = row.loc[(flight_id, seq)]['lat']
            lon = row.loc[(flight_id, seq)]['lon']
            if (check_circle_contains_point(one_circle_center, radius, Point(lon, lat))):
                keep = True
                break
            
        if keep:
        
            keep = False
            for seq, row in flight_df.groupby(level='sequence'):
                lat = row.loc[(flight_id, seq)]['lat']
                lon = row.loc[(flight_id, seq)]['lon']
                if (check_circle_contains_point(two_circle_center, radius, Point(lon, lat))):
                    keep = True
                    break
                '''if (check_circle_contains_point(three_circle_center, radius, Point(lon, lat))):
                    keep = True
                    break'''

            if keep:
                trombone_flights_ids.append(flight_id)
                continue
            
                '''keep = False
                for seq, row in flight_df.groupby(level='sequence'):
                    lat = row.loc[(flight_id, seq)]['lat']
                    lon = row.loc[(flight_id, seq)]['lon']
                    if (check_circle_contains_point(new_circle_center, radius, Point(lon, lat))):
                        keep = True
                        break
                    
                if keep:
                    trombone_flights_ids.append(flight_id)
                    continue'''


        
        for seq, row in flight_df.groupby(level='sequence'):
            lat = row.loc[(flight_id, seq)]['lat']
            lon = row.loc[(flight_id, seq)]['lon']
            if (check_circle_contains_point(six_circle_center, radius, Point(lon, lat))):
                keep = True
                break
            
        if keep:
        
            keep = False
            for seq, row in flight_df.groupby(level='sequence'):
                lat = row.loc[(flight_id, seq)]['lat']
                lon = row.loc[(flight_id, seq)]['lon']
                if (check_circle_contains_point(seven_circle_center, radius, Point(lon, lat))):
                    keep = True
                    break
                if (check_circle_contains_point(nine_circle_center, radius, Point(lon, lat))):
                    keep = True
                    break
                if (check_circle_contains_point(ten_circle_center, radius, Point(lon, lat))):
                    keep = True
                    break
                if (check_circle_contains_point(four_circle_center, radius, Point(lon, lat))):
                    keep = True
                    break
                if (check_circle_contains_point(five_circle_center, radius, Point(lon, lat))):
                    keep = True
                    break

            if keep:
                trombone_flights_ids.append(flight_id)
                continue
        
        
        for seq, row in flight_df.groupby(level='sequence'):
            lat = row.loc[(flight_id, seq)]['lat']
            lon = row.loc[(flight_id, seq)]['lon']
            if (check_circle_contains_point(three_circle_center, radius, Point(lon, lat))):
                keep = True
                break
            
        if keep:
            
            keep = False
            for seq, row in flight_df.groupby(level='sequence'):
                lat = row.loc[(flight_id, seq)]['lat']
                lon = row.loc[(flight_id, seq)]['lon']
                if (check_circle_contains_point(four_circle_center, radius, Point(lon, lat))):
                    keep = True
                    break
 
            if keep:
                trombone_flights_ids.append(flight_id)
                continue
        
        not_trombone_flights_ids.append(flight_id)
    
    
    # save ids of the trombone fligths
    filename = "week" + str(week)+ "_50NM_trombone_ids.txt"
    file_to_write = open(os.path.join(DATASET_DIR, filename),'w')

    for element in trombone_flights_ids:
        file_to_write.write(element + "\n")
    file_to_write.close()
        
    # save ids of the trombone fligths
    filename = "week" + str(week)+ "_50NM_not_trombone_ids.txt"
    file_to_write = open(os.path.join(DATASET_DIR, filename),'w')

    for element in not_trombone_flights_ids:
        file_to_write.write(element + "\n")
    file_to_write.close()

        
def main():
    
    for month in months:
        create_dataset(month, 1)
        create_dataset(month, 2)
        create_dataset(month, 3)
        create_dataset(month, 4)
    
    
main()    

print("--- %s minutes ---" % ((time.time() - start_time)/60))