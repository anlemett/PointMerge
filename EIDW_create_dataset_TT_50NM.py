import numpy as np
import pandas as pd
from calendar import monthrange
import os

import time
start_time = time.time()

year = '2019'
airport_icao = "EIDW"

from constants_EIDW import *

months = ['10']

DATA_DIR = os.path.join("data", airport_icao + "_50NM_rwy")
#DATA_DIR = os.path.join("data", airport_icao + "_50NM")
DATA_DIR = os.path.join(DATA_DIR, year)
DATA_OUTPUT_DIR = os.path.join(DATA_DIR, "Dataset")
STATES_DIR = os.path.join(DATA_DIR, "osn_EIDW_states_50NM_2019")

week1_states_dir = os.path.join(STATES_DIR, "osn_EIDW_states_50NM_2019_10_week1_by_runways")
filename = os.path.join(week1_states_dir, "osn_EIDW_states_50NM_2019_10_week1_rwy28L.csv")
week1_rwy28L_df = pd.read_csv(filename, sep=' ',
                            names = ['flight_id', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'])
week1_rwy28L_df.set_index(['flight_id', 'sequence'], inplace = True)


week2_states_dir = os.path.join(STATES_DIR, "osn_EIDW_states_50NM_2019_10_week2_by_runways")
filename = os.path.join(week2_states_dir, "osn_EIDW_states_50NM_2019_10_week2_rwy28L.csv")
week2_rwy28L_df = pd.read_csv(filename, sep=' ',
                            names = ['flight_id', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'])
week2_rwy28L_df.set_index(['flight_id', 'sequence'], inplace = True)


week3_states_dir = os.path.join(STATES_DIR, "osn_EIDW_states_50NM_2019_10_week3_by_runways")
filename = os.path.join(week3_states_dir, "osn_EIDW_states_50NM_2019_10_week3_rwy28L.csv")
week3_rwy28L_df = pd.read_csv(filename, sep=' ',
                            names = ['flight_id', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'])
week3_rwy28L_df.set_index(['flight_id', 'sequence'], inplace = True)


week4_states_dir = os.path.join(STATES_DIR, "osn_EIDW_states_50NM_2019_10_week4_by_runways")
filename = os.path.join(week4_states_dir, "osn_EIDW_states_50NM_2019_10_week4_rwy28L.csv")
week4_rwy28L_df = pd.read_csv(filename, sep=' ',
                            names = ['flight_id', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'])
week4_rwy28L_df.set_index(['flight_id', 'sequence'], inplace = True)


frames = [week1_rwy28L_df, week2_rwy28L_df, week3_rwy28L_df, week4_rwy28L_df]
rwy28L_df = pd.concat(frames)
num_flights = len(rwy28L_df.groupby(level='flight_id'))
print(num_flights)


PIs_DIR = os.path.join(DATA_DIR, "PIs")

filename = os.path.join(PIs_DIR, "PIs_vertical_by_hour_2019_10_week1_rwy28L.csv")
vertical_PIs_by_hour_week1_rwy28L_df = pd.read_csv(filename, sep=' ')

filename = os.path.join(PIs_DIR, "PIs_vertical_by_hour_2019_10_week2_rwy28L.csv")
vertical_PIs_by_hour_week2_rwy28L_df = pd.read_csv(filename, sep=' ')

filename = os.path.join(PIs_DIR, "PIs_vertical_by_hour_2019_10_week3_rwy28L.csv")
vertical_PIs_by_hour_week3_rwy28L_df = pd.read_csv(filename, sep=' ')

filename = os.path.join(PIs_DIR, "PIs_vertical_by_hour_2019_10_week4_rwy28L.csv")
vertical_PIs_by_hour_week4_rwy28L_df = pd.read_csv(filename, sep=' ')

frames = [vertical_PIs_by_hour_week1_rwy28L_df, vertical_PIs_by_hour_week2_rwy28L_df, vertical_PIs_by_hour_week3_rwy28L_df, vertical_PIs_by_hour_week4_rwy28L_df]
vertical_PIs_by_hour_rwy28L_df = pd.concat(frames)


filename = os.path.join(PIs_DIR, "PIs_vertical_by_flight_2019_10_week1_rwy28L.csv")
vertical_PIs_by_flight_week1_rwy28L_df = pd.read_csv(filename, sep=' ')

filename = os.path.join(PIs_DIR, "PIs_vertical_by_flight_2019_10_week2_rwy28L.csv")
vertical_PIs_by_flight_week2_rwy28L_df = pd.read_csv(filename, sep=' ')

filename = os.path.join(PIs_DIR, "PIs_vertical_by_flight_2019_10_week3_rwy28L.csv")
vertical_PIs_by_flight_week3_rwy28L_df = pd.read_csv(filename, sep=' ')

filename = os.path.join(PIs_DIR, "PIs_vertical_by_flight_2019_10_week4_rwy28L.csv")
vertical_PIs_by_flight_week4_rwy28L_df = pd.read_csv(filename, sep=' ')

frames = [vertical_PIs_by_flight_week1_rwy28L_df, vertical_PIs_by_flight_week2_rwy28L_df, vertical_PIs_by_flight_week3_rwy28L_df, vertical_PIs_by_flight_week4_rwy28L_df]
vertical_PIs_by_flight_rwy28L_df = pd.concat(frames)


# drop 0.7 percentile

df = vertical_PIs_by_hour_rwy28L_df

df = df[df['number_of_flights_by_end']>0]
p1 = df["50NM_time_mean"].quantile(0.7) # 16.98 min, 2468 flights out of 7748 flights for 50NM
                                        # 17.42 min, 2609 flights out of 7741 flights for 50NM_rwy

df = df.loc[(df['50NM_time_mean'] > p1)]
print(p1)

# extract the flights for given hours

df = df.rename(columns = {'date': 'end_date', 'hour': 'end_hour'}, inplace = False)

print(df.head(1))
print(vertical_PIs_by_flight_rwy28L_df.head(1))

df_inner = pd.merge(df, vertical_PIs_by_flight_rwy28L_df, on=['end_date', 'end_hour'], how='inner')
df_inner = df_inner[['flight_id']]
print(len(df_inner))

flight_ids_list = df_inner['flight_id'].to_list()

print(len(flight_ids_list))

#exit(0)

dataset_df = pd.DataFrame()
count = 0
number_of_flights = len(rwy28L_df.groupby(level='flight_id'))  
 
for flight_id, flight_id_group in rwy28L_df.groupby(level='flight_id'): 
    count = count + 1
    print(number_of_flights, count, flight_id)
              
    if flight_id in flight_ids_list:
        dataset_df = dataset_df.append(flight_id_group)
    
filename = "EIDW_50NM_dataset_TT_1.csv"
dataset_df.to_csv(os.path.join(DATA_OUTPUT_DIR, filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)
    
print("--- %s minutes ---" % ((time.time() - start_time)/60))