##############################################################################

#airport_icao = "ESSA"
#airport_icao = "ESGG"
#airport_icao = "EIDW" # Dublin
airport_icao = "LOWW" # Vienna

year = '2019'

#months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
months = ['10']

##############################################################################

import os

DATA_DIR = os.path.join("data", airport_icao)
DATA_DIR = os.path.join(DATA_DIR, year)

INPUT_DIR = os.path.join(DATA_DIR, "osn_" + airport_icao + "_states_TMA_" + year)
OUTPUT_DIR = os.path.join(DATA_DIR, "osn_" + airport_icao + "_states_TMA_after_filtering_" + year)

if not os.path.exists(INPUT_DIR):
    os.makedirs(INPUT_DIR)
    
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# flights with the last altitude value less than this value are considered as 
# landed and with complete data
descent_end_altitude = 600 #meters, ?make less?

import pandas as pd
import numpy as np
import calendar

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

if airport_icao == "ESSA":
    from constants_ESSA import *
elif airport_icao == "ESGG":
    from constants_ESGG import *
elif airport_icao == "EIDW":
    from constants_EIDW import *
elif airport_icao == "LOWW":
    from constants_LOWW import *
    
import time
start_time = time.time()


for month in months:
    print(month)
    
    #number_of_weeks = (5, 4)[month == '02' and not calendar.isleap(int(year))]
    number_of_weeks = 1
        
    for week in range(0, number_of_weeks):
        
        print(airport_icao, year, month, week+1)
        
        #filename = 'osn_' + airport_icao + '_states_TMA_' + year + '_' + month + '_week' + str(week + 1) + '.csv'
        filename = 'osn_' + airport_icao + '_states_TMA_' + year + '_' + month + '_week' + str(week + 1) + '_old.csv'
        
        full_filename = os.path.join(INPUT_DIR, filename)
        
        
        df = pd.read_csv(full_filename, sep=' ',
                                 names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'endDate'],
                                 dtype={'sequence':int, 'timestamp':int, 'rawAltitude':int, 'altitude':float, 'endDate':str})

        df.set_index(['flightId', 'sequence'], inplace = True)

        flight_id_num = len(df.groupby(level='flightId'))
        count = 0

        for flight_id, flight_id_group in df.groupby(level='flightId'):
            
            count = count + 1
            print(airport_icao, year, month, week+1, flight_id_num, count, flight_id)
            
            ###################################################################
            # Short callsign (non-commercial flights):
            ###################################################################

            callsign = flight_id[6:]
            if len(callsign)<=3: #usually commercial callsigns' length is 6 or 7, sometimes - 5 or 4
                df = df.drop(flight_id)
                continue
            
            ###################################################################
            # Last altitude too big (incomplete data or bad smoothing):
            ###################################################################
            
            altitudes = flight_id_group['altitude']
            last_height = altitudes.tolist()[-1]
            
            if last_height > descent_end_altitude:
                df = df.drop(flight_id)
                continue

            ###################################################################
            # First altitude too small (departure and arrival at the same airport):
            ###################################################################
            
            altitudes = flight_id_group['altitude']
            first_height = altitudes.tolist()[0]
            
            if first_height < descent_end_altitude:
                df = df.drop(flight_id)
                continue
            
            #flight_states_df = df.loc[(flight_id, ), :]
            
            ###################################################################
            # Latitude or longitude = 0:
            ###################################################################
            
            bad_lat_lon_df = flight_id_group[(flight_id_group["lat"]==0) | (flight_id_group["lon"]==0)]
            if not bad_lat_lon_df.empty:
                df = df.drop(flight_id)
                continue
            
            ###################################################################
            # Latitude or longitude outside of TMA too much
            ###################################################################
            
            lon_min = min(TMA_lon) - 0.5
            lon_max = max(TMA_lon) + 0.5
            lat_min = min(TMA_lat) - 0.5
            lat_max = max(TMA_lat) + 0.5
            
            rect_lon = [lon_min, lon_min, lon_max, lon_max, lon_min]
            rect_lat = [lat_min, lat_max, lat_max, lat_min, lat_min]
            
            lons_lats_vect = np.column_stack((rect_lon, rect_lat)) # Reshape coordinates
            polygon = Polygon(lons_lats_vect) # create polygon

      
            flight_states_df = flight_id_group.copy() 
            
            flight_states_df.reset_index(drop = False, inplace = True)
            df_len = len(flight_states_df)
            flight_states_df.set_index('sequence', inplace=True)
            
            remove = 0
            if not flight_states_df.empty:
                
                for seq, row in flight_states_df.iterrows():
                    
                    point = Point(row["lon"], row["lat"])
                    
                    if not polygon.contains(point):
                        remove = 1
                        break
                        
            if remove == 1:
                df = df.drop(flight_id)
                continue
        
        
        filename = 'osn_' + airport_icao + '_states_TMA_' + year + '_' + month + '_week' + str(week + 1) + '.csv'

        full_filename = os.path.join(OUTPUT_DIR, filename)
        
        df.to_csv(full_filename, sep=' ', encoding='utf-8', float_format='%.3f', header=False, index=True)

print((time.time()-start_time)/60)