import pandas as pd
import os

from geopy.distance import geodesic
import pyproj

from shapely.geometry import Point
from shapely.geometry import LineString

from datetime import datetime

import time
start_time = time.time()

year = '2019'
airport_icao = "EIDW"

from constants_EIDW import *

#months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '12', '12']
months = ['10']

DATA_DIR = os.path.join("data", airport_icao)
DATA_DIR = os.path.join(DATA_DIR, year)

geod = pyproj.Geod(ellps='WGS84')   # to determine runways via azimuth
#fwd_azimuth, back_azimuth, distance = geod.inv(lat1, long1, lat2, long2)
rwy10R_azimuth, rwy28L_azimuth, distance = geod.inv(rwy10R_lat[0], rwy10R_lon[0], rwy10R_lat[1], rwy10R_lon[1])
rwy16_azimuth, rwy34_azimuth, distance = geod.inv(rwy16_lat[0], rwy16_lon[0], rwy16_lat[1], rwy16_lon[1])

print(rwy10R_azimuth, rwy28L_azimuth, rwy16_azimuth, rwy34_azimuth)
# ~ -3.15 176.85 -54.07 125.93

def get_all_states(csv_input_file):

    df = pd.read_csv(csv_input_file, sep=' ',
                    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'endDate'],
                    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'endDate':str})
    
    df = df[['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'altitude', 'endDate']]
    
    df.set_index(['flightId', 'sequence'], inplace=True)
    
    return df


def calculate_horizontal_PIs(month):
    
    #DATA_INPUT_DIR = os.path.join(DATA_DIR, "osn_"+ airport_icao + "_states_TMA_" + year)
    #input_filename = "osn_"+ airport_icao + "_states_TMA_" + year + '_' + month + ".csv"
    #input_filename = "osn_"+ airport_icao + "_states_TMA_" + year + '_' + month + "_week1.csv"
    DATA_INPUT_DIR = os.path.join(DATA_DIR, "Dataset")
    input_filename = "dataset.csv"
    full_input_filename = os.path.join(DATA_INPUT_DIR, input_filename)
         
    DATA_OUTPUT_DIR = os.path.join(DATA_DIR, "PIs")
    #output_filename = "PIs_horizontal_by_flight_" + year + '_' +  month + ".csv"
    #output_filename = "PIs_horizontal_by_flight_" + year + '_' +  month + "_week1.csv"
    output_filename = "PIs_horizontal_by_flight_dataset.csv"
    full_output_filename = os.path.join(DATA_OUTPUT_DIR, output_filename)

    states_df = get_all_states(full_input_filename)
    
    number_of_flights = len(states_df.groupby(level='flightId'))
    print(number_of_flights)
        
    horizontal_PIs_df = pd.DataFrame(columns=['flight_id', 'date', 'hour', 
                                   'entry_point', 'runway',
                                   'reference_distance',
                                   'TMA_distance', 'TMA_additional_distance'
                                   ])

    
    flight_id_num = len(states_df.groupby(level='flightId'))

    count = 0
    for flight_id, flight_id_group in states_df.groupby(level='flightId'):
        
        #if flight_id != "191001STK3213":
        #    continue
        
        count = count + 1
        print(year, month, flight_id_num, count, flight_id)

        date_str = states_df.loc[flight_id].head(1)['endDate'].values[0]
        
        end_timestamp = states_df.loc[flight_id]['timestamp'].values[-1]
        end_datetime = datetime.utcfromtimestamp(end_timestamp)
        end_hour_str = end_datetime.strftime('%H')
        
        # Determine Entry Point based on lat, lon
        entry_point = ""
        entry_point_lon = flight_id_group['lon'][0]
        entry_point_lat = flight_id_group['lat'][0]
        
        if entry_point_lon > -6 : # "NIMAT", "BOYNE", "BAGSO", "LIPGO", "ABLIN", "VATRY"
                              # lat: 53.9650, 53.7671, 53.6800, 53.0639, 52.7828, 52.5544
            if entry_point_lat > 53.86:
                entry_point = "NIMAT"
            elif entry_point_lat > 53.72:
                entry_point = "BOYNE"
            elif entry_point_lat > 53.37:
                entry_point = "BAGSO"
            elif entry_point_lat > 53.0:
                entry_point = "LIPGO"
            elif entry_point_lat > 52.77:
                entry_point = "ABLIN"
            else:
                entry_point = "VATRY"            
        else: # lon <= -6 => "BAMLI", "OLAPO", "OSGAR", "SUTEX", "BUNED"
                       # lat: 54.1412, 53.7803, 53.0494, 52.8244, 52.6228
            if entry_point_lat > 53.96:
                entry_point = "BAMLI"
            elif entry_point_lat > 53.41:
                entry_point = "OLAPO"
            elif entry_point_lat > 52.93:
                entry_point = "OSGAR"
            elif entry_point_lat > 52.72:
                entry_point = "SUTEX"
            else:
                entry_point = "BUNED"

        
        
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

        # ~ -3.15 176.85 -54.07 125.93
        if (trajectory_azimuth > -24) and (trajectory_azimuth < 61):
            runway = '10R'
        elif (trajectory_azimuth > -136) and (trajectory_azimuth < -24):
            runway = '16'
        elif (trajectory_azimuth > 61) and (trajectory_azimuth < 152):
            runway = '34'
        else: # 28L
            runway = '28L'
        #print(runway)
        
        # Calculate reference distance based on entry point and runway
        distance_ref = 0

        if entry_point == "NIMAT":
            if runway == "10R":
                #distance_ref = 67.0
                distance_ref = 75.5
            elif runway == "28L":
                #distance_ref = 44.9
                distance_ref = 52
            elif runway == "16":
                #distance_ref = 47.5
                distance_ref = 56.2
            else:
                #distance_ref = 52.8
                distance_ref = 61.4
        elif entry_point == "BOYNE":
            if runway == "10R":
                #distance_ref = 60.0
                distance_ref = 68.5
            elif runway == "28L":
                #distance_ref = 37.9
                distance_ref = 52.9
            elif runway == "16":
                #distance_ref = 40.5
                distance_ref = 49.2
            else:
                #distance_ref = 45.8
                distance_ref = 54.4
        elif entry_point == "BAGSO":
            if runway == "10R":
                #distance_ref = 58.0
                distance_ref = 66.5
            elif runway == "28L":
                #distance_ref = 35.9
                distance_ref = 43
            elif runway == "16":
                #distance_ref = 38.5
                distance_ref = 47.2
            else:
                #distance_ref = 43.8
                distance_ref = 52.4
        elif entry_point == "LIPGO":
            if runway == "10R":
                #distance_ref = 62.0
                distance_ref = 70.5
            elif runway == "28L":
                #distance_ref = 30.9 # !!!The same as ABLIN
                distance_ref = 38
            elif runway == "16":
                #distance_ref = 77.8
                distance_ref = 86.5
            else:
                #distance_ref = 28.2
                distance_ref = 36.8
        elif entry_point == "ABLIN":
            if runway == "10R":
                #distance_ref = 62.0 # !!!The same as LIPGO
                distance_ref = 70.5
            elif runway == "28L":
                #distance_ref = 30.9
                distance_ref = 38
            elif runway == "16":
                #distance_ref = 77.8 # !!!The same as LIPGO
                distance_ref = 86.5
            else:
                #distance_ref = 28.2 # !!!The same as LIPGO
                distance_ref = 36.8
        elif entry_point == "VATRY":
            if runway == "10R":
                #distance_ref = 87.0
                distance_ref = 95.5
            elif runway == "28L":
                #distance_ref = 64.9
                distance_ref = 72
            elif runway == "16":
                #distance_ref = 102.8
                distance_ref = 111.5
            else:
                #distance_ref = 53.2
                distance_ref = 61.8
        elif entry_point == "BAMLI":
            if runway == "10R":
                #distance_ref = 53.0
                distance_ref = 57
            elif runway == "28L":
                #distance_ref = 74.9
                distance_ref = 82
            elif runway == "16":
                #distance_ref = 0 # There should be no these flights
                distance_ref = 0
            else:
                #distance_ref = 88.8
                distance_ref = 97.4
        elif entry_point == "OLAPO":
            if runway == "10R":
                #distance_ref = 58.0
                distance_ref = 66.5
            elif runway == "28L":
                #distance_ref = 79.9
                distance_ref = 87
            elif runway == "16":
                #distance_ref = 36.8
                distance_ref = 45.5
            else:
                #distance_ref = 87.8
                distance_ref = 96.4
        elif entry_point == "OSGAR":
            if runway == "10R":
                #distance_ref = 65.0
                distance_ref = 73.5
            elif runway == "28L":
                #distance_ref = 84.9
                distance_ref = 92
            elif runway == "16":
                #distance_ref = 89.8
                distance_ref = 98.5
            else:
                #distance_ref = 73.2
                distance_ref = 81.8
        elif entry_point == "SUTEX":
            if runway == "10R":
                #distance_ref = 58.0
                distance_ref = 66.5
            elif runway == "28L":
                #distance_ref = 77.9
                distance_ref = 85
            elif runway == "16":
                #distance_ref = 82.8
                distance_ref = 91.5
            else:
                #distance_ref = 66.2
                distance_ref = 74.8
        elif entry_point == "BUNED":
            if runway == "10R":
                #distance_ref = 66.0
                distance_ref = 74.5
            elif runway == "28L":
                #distance_ref = 85.9
                distance_ref = 93
            elif runway == "16":
                #distance_ref = 90.8
                distance_ref = 99.5
            else:
                #distance_ref = 74.2
                distance_ref = 82.8
                
        distance_ref = distance_ref * 1.852 * 1000 # NM to meters

        # For 28L
        #if runway == "28L":
        #    descent_end_altitude = 2500
        # For 10R/16/34
        #else:
        #    descent_end_altitude = 3000
        #descent_end_altitude = descent_end_altitude / 3.281 # feet to meters        
        #flight_id_df = flight_id_group[flight_id_group['altitude']>descent_end_altitude]
        flight_id_df = flight_id_group

        distance_sum = 0

        df_length = len(flight_id_df)
        
        for seq, row in flight_id_df.groupby(level='sequence'):
             
            if seq == 0:
                previous_point = (row['lat'].values[0], row['lon'].values[0])
                continue
            
            current_point = (row['lat'].values[0], row['lon'].values[0])
            
            distance_sum = distance_sum + geodesic(previous_point, current_point).meters
            previous_point = current_point
            #print(distance_sum, current_point)

        distance_str = "{0:.3f}".format(distance_sum)
        
        add_distance = distance_sum - distance_ref
        add_distance_str = "{0:.3f}".format(add_distance)
        
        horizontal_PIs_df = horizontal_PIs_df.append({'flight_id': flight_id, 'date': date_str, 'hour': end_hour_str,
                                'reference_distance': distance_ref,
                                'TMA_distance': distance_str,
                                'TMA_additional_distance': add_distance_str,
                                'entry_point': entry_point,
                                'runway': runway}, ignore_index=True)

    horizontal_PIs_df.to_csv(full_output_filename, sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)


def main():
    
    for month in months:
        calculate_horizontal_PIs(month)
    
    
main()    

print("--- %s minutes ---" % ((time.time() - start_time)/60))