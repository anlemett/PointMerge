import pandas as pd
import os

from geopy.distance import geodesic
import pyproj

from shapely.geometry import Point
from shapely.geometry import LineString

from datetime import datetime

import time
start_time = time.time()

year = '2020'
airport_icao = "ESSA"

if airport_icao == "ESSA":
    from constants_ESSA import *

#months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '12', '12']
months = ['05']

DATA_DIR = os.path.join("data", airport_icao)
DATA_DIR = os.path.join(DATA_DIR, year)

geod = pyproj.Geod(ellps='WGS84')   # to determine runways via azimuth
#fwd_azimuth, back_azimuth, distance = geod.inv(lat1, long1, lat2, long2)
rwy08_azimuth, rwy26_azimuth, distance = geod.inv(rwy08_lat[0], rwy08_lon[0], rwy08_lat[1], rwy08_lon[1])
rwy01L_azimuth, rwy19R_azimuth, distance = geod.inv(rwy01L_lat[0], rwy01L_lon[0], rwy01L_lat[1], rwy01L_lon[1])
rwy01R_azimuth, rwy19L_azimuth, distance = geod.inv(rwy01R_lat[0], rwy01R_lon[0], rwy01R_lat[1], rwy01R_lon[1])

#print(rwy08_azimuth, rwy26_azimuth, rwy01L_azimuth, rwy19R_azimuth, rwy01R_azimuth, rwy19L_azimuth)
# ~ 7 -173 70 -110 70 -110

#point1 = [59.537, 17.9]
#point2 = [59.766, 17.98]
#fwd_azimuth, back_azimuth, distance = geod.inv(point1[0], point1[1], point2[0], point2[1])
#print(fwd_azimuth, back_azimuth)

#Point1 = Point(point1[1], point1[0])
#Point2 = Point(point2[1], point2[0])

a = (rwy01L_lon[0], rwy01L_lat[0])
b = (rwy01L_lon[1], rwy01L_lat[1])
# distance between runways - 2 km
offset_length = 0.018 #approximate 1 km in longitude degrees, when latitude is 60N

ab = LineString([a, b])
cd = ab.parallel_offset(offset_length)
Point1 = cd.boundary[0]
Point2 = cd.boundary[1]
print(Point1, Point2)


# Check the sign of the determninant of 
# | x2-x1  x3-x1 |
# | y2-y1  y3-y1 |
# It will be positive for points on one side, and negative on the other (0 on the line)
def is_left(Point3):
    if ((Point2.x - Point1.x)*(Point3.y - Point1.y) - (Point2.y - Point1.y)*(Point3.x - Point1.x)) < 0:
        return True
    else:
        return False

#descent part ends at 1800 feet
descent_end_altitude = 1800 / 3.281
    

def get_all_states(csv_input_file):

    df = pd.read_csv(csv_input_file, sep=' ',
                    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'endDate'],
                    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'endDate':str})
    
    df = df[['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'altitude', 'endDate']]
    
    # maybe need for distance calculation but not for runway determination
    #df = df[df['altitude']>descent_end_altitude]
    
    df.set_index(['flightId', 'sequence'], inplace=True)
    
    return df


def calculate_horizontal_PIs(month):
    
    DATA_INPUT_DIR = os.path.join(DATA_DIR, "osn_"+ airport_icao + "_states_TMA_" + year)
    input_filename = "osn_"+ airport_icao + "_states_TMA_" + year + '_' + month + ".csv"
    full_input_filename = os.path.join(DATA_INPUT_DIR, input_filename)
         
    DATA_OUTPUT_DIR = os.path.join(DATA_DIR, "PIs")
    output_filename = "PIs_horizontal_by_flight_" + year + '_' +  month + ".csv"
    full_output_filename = os.path.join(DATA_OUTPUT_DIR, output_filename)

    #number_of_flights = len(states_df.groupby(level='flightId'))
    
    states_df = get_all_states(full_input_filename)
        
    horizontal_PIs_df = pd.DataFrame(columns=['flight_id', 'date', 'hour', 
                                   'entry_point', 'runway',
                                   'TMA_distance', 'TMA_additional_distance'
                                   ])

    
    flight_id_num = len(states_df.groupby(level='flightId'))

    count = 0
    for flight_id, flight_id_group in states_df.groupby(level='flightId'):
        
        #if flight_id != '200528VAS816':
        #if flight_id != '200526SAS532':
        #    continue
        
        count = count + 1
        print(year, month, flight_id_num, count, flight_id)

        distance_sum = 0

        df_length = len(flight_id_group)
        
        for seq, row in flight_id_group.groupby(level='sequence'):
             
            if seq == 0:
                previous_point = (row['lat'].values[0], row['lon'].values[0])
                continue
            
            current_point = (row['lat'].values[0], row['lon'].values[0])
            
            distance_sum = distance_sum + geodesic(previous_point, current_point).meters
            previous_point = current_point


        distance_str = "{0:.3f}".format(distance_sum)

        date_str = states_df.loc[flight_id].head(1)['endDate'].values[0]
        
        #end_timestamp = states_opensky_df.loc[flight_id]['timestamp'].values[-1].item(0)
        end_timestamp = states_df.loc[flight_id]['timestamp'].values[-1]
        end_datetime = datetime.utcfromtimestamp(end_timestamp)
        end_hour_str = end_datetime.strftime('%H')
        
        # Determine Entry Point based on lat, lon
        entry_point = ""
        entry_point_lon = flight_id_group['lon'][0]
        entry_point_lat = flight_id_group['lat'][0]
        
        if entry_point_lon < ELTOK_lon + (XILAN_lon - ELTOK_lon)/5:
            entry_point = "ELTOK"
        elif entry_point_lon > XILAN_lon - (XILAN_lon - ELTOK_lon)/5:
            entry_point = "XILAN"
        elif entry_point_lat < NILUG_lat + (HMR_lat - NILUG_lat)/2:
            entry_point = "NILUG"
        else:
            entry_point = "HMR"
        
        
        # Determine Runway based on lat, lon
        
        runway = ""
        trajectory_point_last = [flight_id_group['lat'][-1], flight_id_group['lon'][-1]]
        # 30 seconds before:
        trajectory_point_before_last = [flight_id_group['lat'][-30], flight_id_group['lon'][-30]]
        
        #fwd_azimuth, back_azimuth, distance = geod.inv(lat1, long1, lat2, long2)
        trajectory_azimuth, temp1, temp2 = geod.inv(trajectory_point_before_last[0],
                                                    trajectory_point_before_last[1],
                                                    trajectory_point_last[0],
                                                    trajectory_point_last[1])

        if (trajectory_azimuth > -50) and (trajectory_azimuth < 40):
            runway = '08'
        elif ((trajectory_azimuth > -180) and (trajectory_azimuth < -140)) or ((trajectory_azimuth > 130) and (trajectory_azimuth < 180)):
            runway = '26'
        elif (trajectory_azimuth > 40) and (trajectory_azimuth < 130): #01L or 01R
            Point3 = Point(trajectory_point_last[1], trajectory_point_last[0])
            if is_left(Point3):
                runway = '01L'
            else:
                runway = '01R'
        else: # 19L or 19R
            Point3 = Point(trajectory_point_last[1], trajectory_point_last[0])
            if is_left(Point3):
                runway = '19R'
            else:
                runway = '19L'    
        #print(runway)
        
        # TODO: Calculate reference distance based on entry point and runway
        distance_ref = 0
        
        add_distance = distance_sum - distance_ref
        add_distance_str = "{0:.3f}".format(add_distance)
        
        horizontal_PIs_df = horizontal_PIs_df.append({'flight_id': flight_id, 'date': date_str, 'hour': end_hour_str,
                                'TMA_distance': distance_str,
                                'TMA_additional_distance': add_distance_str,
                                'entry_point': entry_point,
                                'runway': runway}, ignore_index=True)

    horizontal_PIs_df.to_csv(full_output_filename, sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)

# TODO: check HMR_19L, XILAN_08, XILAN_26 (1 flight)

def main():
    
    for month in months:
        calculate_horizontal_PIs(month)
    
    
main()    

print("--- %s minutes ---" % ((time.time() - start_time)/60))