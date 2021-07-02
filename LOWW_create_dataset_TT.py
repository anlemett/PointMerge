import numpy as np
import pandas as pd
from calendar import monthrange
import os

import time
start_time = time.time()

year = '2019'
airport_icao = "LOWW"

from constants_LOWW import *

months = ['10']

DATA_DIR = os.path.join("data", airport_icao)
DATA_DIR = os.path.join(DATA_DIR, year)
DATA_OUTPUT_DIR = os.path.join(DATA_DIR, "Dataset")


filename = "data/LOWW/2019/osn_LOWW_states_TMA_2019/osn_LOWW_states_TMA_2019_10_week1_by_runways/osn_LOWW_states_TMA_2019_10_week1_rwy_16.csv"
week1_rwy16_df = pd.read_csv(filename, sep=' ',
                            names = ['flight_id', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'date'])
week1_rwy16_df.set_index(['flight_id', 'sequence'], inplace = True)
num_flights1 = len(week1_rwy16_df.groupby(level='flight_id'))

filename = "data/LOWW/2019/osn_LOWW_states_TMA_2019/osn_LOWW_states_TMA_2019_10_week2_by_runways/osn_LOWW_states_TMA_2019_10_week2_rwy_16.csv"
week2_rwy16_df = pd.read_csv(filename, sep=' ',
                            names = ['flight_id', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'date'])
week2_rwy16_df.set_index(['flight_id', 'sequence'], inplace = True)
num_flights2 = len(week2_rwy16_df.groupby(level='flight_id'))

filename = "data/LOWW/2019/osn_LOWW_states_TMA_2019/osn_LOWW_states_TMA_2019_10_week3_by_runways/osn_LOWW_states_TMA_2019_10_week3_rwy_16.csv"
week3_rwy16_df = pd.read_csv(filename, sep=' ',
                            names = ['flight_id', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'date'])
week3_rwy16_df.set_index(['flight_id', 'sequence'], inplace = True)
num_flights3 = len(week3_rwy16_df.groupby(level='flight_id'))

filename = "data/LOWW/2019/osn_LOWW_states_TMA_2019/osn_LOWW_states_TMA_2019_10_week4_by_runways/osn_LOWW_states_TMA_2019_10_week4_rwy_16.csv"
week4_rwy16_df = pd.read_csv(filename, sep=' ',
                            names = ['flight_id', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'date'])
week4_rwy16_df.set_index(['flight_id', 'sequence'], inplace = True)
num_flights4 = len(week4_rwy16_df.groupby(level='flight_id'))

frames = [week1_rwy16_df, week2_rwy16_df, week3_rwy16_df, week4_rwy16_df]
rwy16_df = pd.concat(frames)
num_flights = len(rwy16_df.groupby(level='flight_id'))
print(num_flights)


filename = "data/LOWW/2019/PIs/PIs_vertical_by_hour_2019_10_week1_rwy_16.csv"
vertical_PIs_by_hour_week1_rwy16_df = pd.read_csv(filename, sep=' ')

filename = "data/LOWW/2019/PIs/PIs_vertical_by_hour_2019_10_week2_rwy_16.csv"
vertical_PIs_by_hour_week2_rwy16_df = pd.read_csv(filename, sep=' ')

filename = "data/LOWW/2019/PIs/PIs_vertical_by_hour_2019_10_week3_rwy_16.csv"
vertical_PIs_by_hour_week3_rwy16_df = pd.read_csv(filename, sep=' ')

filename = "data/LOWW/2019/PIs/PIs_vertical_by_hour_2019_10_week4_rwy_16.csv"
vertical_PIs_by_hour_week4_rwy16_df = pd.read_csv(filename, sep=' ')

frames = [vertical_PIs_by_hour_week1_rwy16_df, vertical_PIs_by_hour_week2_rwy16_df, vertical_PIs_by_hour_week3_rwy16_df, vertical_PIs_by_hour_week4_rwy16_df]
vertical_PIs_by_hour_week_rwy16_df = pd.concat(frames)

filename = "data/LOWW/2019/PIs/PIs_vertical_by_flight_2019_10_week1_rwy_16.csv"
vertical_PIs_by_flight_week1_rwy16_df = pd.read_csv(filename, sep=' ')

filename = "data/LOWW/2019/PIs/PIs_vertical_by_flight_2019_10_week2_rwy_16.csv"
vertical_PIs_by_flight_week2_rwy16_df = pd.read_csv(filename, sep=' ')

filename = "data/LOWW/2019/PIs/PIs_vertical_by_flight_2019_10_week3_rwy_16.csv"
vertical_PIs_by_flight_week3_rwy16_df = pd.read_csv(filename, sep=' ')

filename = "data/LOWW/2019/PIs/PIs_vertical_by_flight_2019_10_week4_rwy_16.csv"
vertical_PIs_by_flight_week4_rwy16_df = pd.read_csv(filename, sep=' ')

frames = [vertical_PIs_by_flight_week1_rwy16_df, vertical_PIs_by_flight_week2_rwy16_df, vertical_PIs_by_flight_week3_rwy16_df, vertical_PIs_by_flight_week4_rwy16_df]
vertical_PIs_by_flight_rwy16_df = pd.concat(frames)



# remove outliers
df = vertical_PIs_by_hour_week_rwy16_df
#p1 = df["TMA_time_mean"].quantile(0.5) # 0 min, 4190 flights
#p1 = df["TMA_time_mean"].quantile(0.6) # 12.4 min, 3925 flights
#p1 = df["TMA_time_mean"].quantile(0.7) # 13.3 min, 3171 flights

df = df[df['number_of_flights_by_end']>0]
#p1 = df["TMA_time_mean"].quantile(0.5) # 13.9 min, 2564 flights
#p1 = df["TMA_time_mean"].quantile(0.6) # 14.3 min, 2081 flights
p1 = df["TMA_time_mean"].quantile(0.7) #  15.2 min, 1666 flights
df = df.loc[(df['TMA_time_mean'] > p1)]
#df = df.loc[(df['TMA_time_mean'] > 15)]
print(p1)

df = df.rename(columns = {'hour': 'end_hour'}, inplace = False)

print(df.head(1))
print(vertical_PIs_by_flight_rwy16_df.head(1))

df_inner = pd.merge(df, vertical_PIs_by_flight_rwy16_df, on=['date', 'end_hour'], how='inner')
df_inner = df_inner[['flight_id']]
print(len(df_inner))

flight_ids_list = df_inner['flight_id'].to_list()
print(len(flight_ids_list))

dataset_df = pd.DataFrame()
count = 0
number_of_flights = len(rwy16_df.groupby(level='flight_id'))  

for flight_id, flight_id_group in rwy16_df.groupby(level='flight_id'): 
    count = count + 1
    print(number_of_flights, count, flight_id)
              
    if flight_id in flight_ids_list:
        dataset_df = dataset_df.append(flight_id_group)
    
filename = "LOWW_dataset_TT.csv"
dataset_df.to_csv(os.path.join(DATA_OUTPUT_DIR, filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)
