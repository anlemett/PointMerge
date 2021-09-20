import pandas as pd
import os

from datetime import datetime

import time
start_time = time.time()

year = '2019'
airport_icao = "LOWW"
PIs_type = "vertical"
#PIs_type = "horizontal"

if airport_icao == "EIDW":
    number_of_clusters = 10
elif airport_icao == "ESSA":
    number_of_clusters = 6
elif airport_icao == "LOWW":
    number_of_clusters = 10

DATA_DIR = os.path.join("data", airport_icao)
DATA_DIR = os.path.join(DATA_DIR, year)



def split():
    
    #dataset_name = airport_icao + "_dataset_PM"
    dataset_name = airport_icao + "_dataset_TT"
         
    DATA_PIs_DIR = os.path.join(DATA_DIR, "PIs")
    input_filename = dataset_name + "_PIs_" + PIs_type + "_by_flight.csv"
    full_input_filename = os.path.join(DATA_PIs_DIR, input_filename)
    
    df_PIs_by_flight = pd.read_csv(full_input_filename, sep=' ')
    df_PIs_by_flight.set_index(['flight_id'], inplace=True)

    CLUSTERS_DIR = os.path.join(DATA_DIR, "Clustering")
    clusters_filename = dataset_name + "_TMA_borders_clusters_" + str(number_of_clusters) + ".csv"
    full_clusters_filename = os.path.join(CLUSTERS_DIR, clusters_filename)
    
    df_clusters = pd.read_csv(full_clusters_filename, sep=' ')
    df_clusters.set_index(['flight_id'], inplace=True)
    
    df_PIs_by_flights_by_clusters_list = []
    for i in range(0,number_of_clusters):
        df_PIs_by_flights_by_clusters_list.append(pd.DataFrame())

    for flight_id, flight_id_group in df_PIs_by_flight.groupby(level='flight_id'):
        
        cluster = int(df_clusters.loc[flight_id]['cluster'])
        df_PIs_by_flights_by_clusters_list[cluster-1] = df_PIs_by_flights_by_clusters_list[cluster-1].append(flight_id_group)
        
        
    for i in range(0,number_of_clusters):
        output_filename = dataset_name + "_PIs_" + PIs_type + "_by_flight_cluster" + str(i+1) + ".csv"
        full_output_filename = os.path.join(DATA_PIs_DIR, output_filename)
        df_PIs_by_flights_by_clusters_list[i].to_csv(full_output_filename, sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=True)
   
    
split()    

print("--- %s minutes ---" % ((time.time() - start_time)/60))