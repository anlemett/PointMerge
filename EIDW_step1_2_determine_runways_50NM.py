import pandas as pd
import os

import pyproj

from datetime import datetime
import calendar

import time
start_time = time.time()

year = '2019'
airport_icao = "EIDW"

from constants_EIDW import *

#months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '12', '12']
months = ['10']

DATA_DIR = os.path.join("data", airport_icao + "_50NM")
DATA_DIR = os.path.join(DATA_DIR, year)

geod = pyproj.Geod(ellps='WGS84')   # to determine runways via azimuth
#fwd_azimuth, back_azimuth, distance = geod.inv(lat1, long1, lat2, long2)
rwy10R_azimuth, rwy28L_azimuth, distance = geod.inv(rwy10R_lat[0], rwy10R_lon[0], rwy10R_lat[1], rwy10R_lon[1])
rwy16_azimuth, rwy34_azimuth, distance = geod.inv(rwy16_lat[0], rwy16_lon[0], rwy16_lat[1], rwy16_lon[1])

print(rwy10R_azimuth, rwy28L_azimuth, rwy16_azimuth, rwy34_azimuth)
# ~ -3.15 176.85 -54.07 125.93

def get_all_states(csv_input_file):

    df = pd.read_csv(csv_input_file, sep=' ',
                    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'],
                    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':int, 'altitude':float, 'velocity':float, 'beginDate':str, 'endDate':str})
    
    df.set_index(['flightId', 'sequence'], inplace=True)
    
    return df


def determine_runways(month, week):
    
    DATA_INPUT_DIR = os.path.join(DATA_DIR, "osn_"+ airport_icao + "_states_50NM_" + year)
    input_filename = "osn_"+ airport_icao + "_states_50NM_" + year + '_' + month + "_week" + str(week) + ".csv"
    full_input_filename = os.path.join(DATA_INPUT_DIR, input_filename)
         
    DATA_OUTPUT_DIR = os.path.join(DATA_DIR, "PIs")
    if not os.path.exists(DATA_OUTPUT_DIR):
        os.makedirs(DATA_OUTPUT_DIR)
    output_filename = "runways_" + year + '_' +  month + "_week" + str(week) + ".csv"
    full_output_filename = os.path.join(DATA_OUTPUT_DIR, output_filename)

    states_df = get_all_states(full_input_filename)
    
    number_of_flights = len(states_df.groupby(level='flightId'))
    print(number_of_flights)
        
    runways_df = pd.DataFrame(columns=['flight_id', 'date', 'hour', 'runway'])
    
    flight_id_num = len(states_df.groupby(level='flightId'))

    count = 0
    for flight_id, flight_id_group in states_df.groupby(level='flightId'):
        
        count = count + 1
        print(year, month, week, flight_id_num, count, flight_id)

        date_str = states_df.loc[flight_id].head(1)['endDate'].values[0]
        
        end_timestamp = states_df.loc[flight_id]['timestamp'].values[-1]
        end_datetime = datetime.utcfromtimestamp(end_timestamp)
        end_hour_str = end_datetime.strftime('%H')
        
        
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
        if (trajectory_azimuth > -24) and (trajectory_azimuth <= 61):
            runway = '10R'
        elif (trajectory_azimuth > -136) and (trajectory_azimuth <= -24):
            runway = '16'
        elif (trajectory_azimuth > 61) and (trajectory_azimuth <= 152):
            runway = '34'
        else: # 28L
            runway = '28L'
        #print(runway)
        
        runways_df = runways_df.append({'flight_id': flight_id, 'date': date_str,
                                        'hour': end_hour_str,
                                        'runway': runway}, ignore_index=True)

    runways_df.to_csv(full_output_filename, sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)

def create_runways_files(month, week):
    
    DATA_INPUT_DIR1 = os.path.join(DATA_DIR, "osn_"+ airport_icao + "_states_50NM_" + year)
    input_filename1 = "osn_"+ airport_icao + "_states_50NM_" + year + '_' + month + "_week" + str(week) + ".csv"
    full_input_filename1 = os.path.join(DATA_INPUT_DIR1, input_filename1)
    
    states_df = get_all_states(full_input_filename1)
    
    number_of_flights = len(states_df.groupby(level='flightId'))
    
    DATA_INPUT_DIR2 = os.path.join(DATA_DIR, "PIs")
    input_filename2 = "runways_" + year + '_' +  month + "_week" + str(week) + ".csv"
    full_input_filename2 = os.path.join(DATA_INPUT_DIR2, input_filename2)
    
    runways_df = pd.read_csv(full_input_filename2, sep=' ')
    runways_df.set_index(['flight_id'], inplace=True)

    rwy10_df = pd.DataFrame()
    rwy28_df = pd.DataFrame()
    rwy16_df = pd.DataFrame()
    rwy34_df = pd.DataFrame()
    
    count = 0
    for flight_id, flight_id_group in states_df.groupby(level='flightId'):
        count = count + 1
        print(year, month, week, number_of_flights, count, flight_id)

        runway = runways_df.loc[flight_id][['runway']].values[0]
    
        if runway == "10R":
            rwy10_df = rwy10_df.append(flight_id_group)
        elif runway == "28L":
            rwy28_df = rwy28_df.append(flight_id_group)
        elif runway == "16":
            rwy16_df = rwy16_df.append(flight_id_group)
        else:
            rwy34_df = rwy34_df.append(flight_id_group)

    DATA_OUTPUT_DIR = os.path.join(DATA_DIR, "osn_"+ airport_icao + "_states_50NM_" + year)
    DATA_OUTPUT_DIR = os.path.join(DATA_OUTPUT_DIR, "osn_"+ airport_icao + "_states_50NM_" + year + "_" + month + "_week" + str(week) + "_by_runways")
    if not os.path.exists(DATA_OUTPUT_DIR):
        os.makedirs(DATA_OUTPUT_DIR)
    output_filename = "osn_"+ airport_icao + "_states_50NM_" + year + '_' + month + "_week" + str(week)
    full_output_filename = os.path.join(DATA_OUTPUT_DIR, output_filename)

    rwy10_df.to_csv(full_output_filename + "_rwy10R.csv", sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)
    rwy28_df.to_csv(full_output_filename + "_rwy28L.csv", sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)
    rwy16_df.to_csv(full_output_filename + "_rwy16.csv", sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)
    rwy34_df.to_csv(full_output_filename + "_rwy34.csv", sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)

    
def main():
    
    for month in months:
        number_of_weeks = (5, 4)[month == '02' and not calendar.isleap(int(year))]
        #number_of_weeks = 1
        
        for week in range(0, number_of_weeks):
        #for week in range(1, number_of_weeks):
        
            determine_runways(month, week+1)
                       
            create_runways_files(month, week+1)
    
    
main()    

print("--- %s minutes ---" % ((time.time() - start_time)/60))