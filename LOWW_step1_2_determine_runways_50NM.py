import pandas as pd
import os

import pyproj

from datetime import datetime
import calendar

import time
start_time = time.time()

year = '2019'
airport_icao = "LOWW"

from constants_LOWW import *

#months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '12', '12']
months = ['10']

#DATA_DIR = os.path.join("data", airport_icao + "_50NM")
DATA_DIR = os.path.join("data", airport_icao + "_50NM_rwy")
DATA_DIR = os.path.join(DATA_DIR, year)

geod = pyproj.Geod(ellps='WGS84')   # to determine runways via azimuth
#fwd_azimuth, back_azimuth, distance = geod.inv(lat1, long1, lat2, long2)
rwy_16_azimuth, rwy_34_azimuth, distance = geod.inv(rwy_16_34_lat[0], rwy_16_34_lon[0], rwy_16_34_lat[1], rwy_16_34_lon[1])
rwy_11_azimuth, rwy_29_azimuth, distance = geod.inv(rwy_11_29_lat[0], rwy_11_29_lon[0], rwy_11_29_lat[1], rwy_11_29_lon[1])

print(rwy_16_azimuth, rwy_34_azimuth, rwy_11_azimuth, rwy_29_azimuth)
# ~ -69.28 110.71 -13.4 166.6

def get_all_states(csv_input_file):

    df = pd.read_csv(csv_input_file, sep=' ',
                    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'],
                    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'beginDate':str, 'endDate':str})
    
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
        
    runways_df = pd.DataFrame(columns=['flight_id', 'date', 'hour', 
                                   'runway'
                                   ])

    
    flight_id_num = len(states_df.groupby(level='flightId'))

    count = 0
    for flight_id, flight_id_group in states_df.groupby(level='flightId'):
        
        count = count + 1
        print(airport_icao, year, month, week, flight_id_num, count, flight_id)

        date_str = states_df.loc[flight_id].head(1)['endDate'].values[0]
        
        end_timestamp = states_df.loc[flight_id]['timestamp'].values[-1]
        end_datetime = datetime.utcfromtimestamp(end_timestamp)
        end_hour_str = end_datetime.strftime('%H')
        
        # Determine Runway based on lat, lon
        
        runway = ""
        
        df = flight_id_group[flight_id_group['altitude']>350]
        
        trajectory_point_last = [df['lat'][-1], df['lon'][-1]]

        # 60 seconds before:
        trajectory_point_before_last = [df['lat'][-30], df['lon'][-30]]
        
        #fwd_azimuth, back_azimuth, distance = geod.inv(lat1, long1, lat2, long2)
        trajectory_azimuth, temp1, temp2 = geod.inv(trajectory_point_before_last[0],
                                                    trajectory_point_before_last[1],
                                                    trajectory_point_last[0],
                                                    trajectory_point_last[1])

        # print(rwy_16_azimuth, rwy_34_azimuth, rwy_11_azimuth, rwy_29_azimuth)
        # ~ -69.28 110.71 -13.4 166.6
        runway = ""
        if (trajectory_azimuth > -132) and (trajectory_azimuth <= -42 ): 
            runway = '16'
        elif (trajectory_azimuth > 48) and (trajectory_azimuth <= 138):
            runway = '34'
        elif (trajectory_azimuth > -42) and (trajectory_azimuth <= 48):
            runway = '11'
        elif (trajectory_azimuth > 138) and (trajectory_azimuth <= 180) or (trajectory_azimuth > -180) and (trajectory_azimuth <= -132):
        #else:
            runway = '29'
        #print(runway)
        
        runways_df = runways_df.append({'flight_id': flight_id, 'date': date_str, 'hour': end_hour_str,
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
    
    entry_points_and_runways_df = pd.read_csv(full_input_filename2, sep=' ', dtype=str)
    entry_points_and_runways_df.set_index(['flight_id'], inplace=True)

    rwy_16_df = pd.DataFrame()
    rwy_34_df = pd.DataFrame()
    rwy_11_df = pd.DataFrame()
    rwy_29_df = pd.DataFrame()

    count = 0
    for flight_id, flight_id_group in states_df.groupby(level='flightId'):
        
        count = count + 1
        print(airport_icao, year, month, week, number_of_flights, count, flight_id)

        runway = entry_points_and_runways_df.loc[flight_id][['runway']].values[0]

        if runway == "16":
            rwy_16_df = rwy_16_df.append(flight_id_group)
        elif runway == "34":
            rwy_34_df = rwy_34_df.append(flight_id_group)
        elif runway == "11":
            rwy_11_df = rwy_11_df.append(flight_id_group)
        else: # "29"
            rwy_29_df = rwy_29_df.append(flight_id_group)

    DATA_OUTPUT_DIR = os.path.join(DATA_DIR, "osn_"+ airport_icao + "_states_50NM_" + year)
    DATA_OUTPUT_DIR = os.path.join(DATA_OUTPUT_DIR, "osn_"+ airport_icao + "_states_50NM_" + year + "_" + month + "_week" + str(week) + "_by_runways")
    if not os.path.exists(DATA_OUTPUT_DIR):
        os.makedirs(DATA_OUTPUT_DIR)
    output_filename = "osn_"+ airport_icao + "_states_50NM_" + year + '_' + month + "_week" + str(week)
    full_output_filename = os.path.join(DATA_OUTPUT_DIR, output_filename)

    rwy_16_df.to_csv(full_output_filename + "_rwy16.csv", sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)
    rwy_34_df.to_csv(full_output_filename + "_rwy34.csv", sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)
    rwy_11_df.to_csv(full_output_filename + "_rwy11.csv", sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)
    rwy_29_df.to_csv(full_output_filename + "_rwy29.csv", sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)
    
    
def main():
    
    for month in months:
        number_of_weeks = (5, 4)[month == '02' and not calendar.isleap(int(year))]
        #number_of_weeks = 1
        
        for week in range(0, number_of_weeks):
        
            determine_runways(month, week+1)
            
            create_runways_files(month, week+1)
    
    
main()    

print("--- %s minutes ---" % ((time.time() - start_time)/60))