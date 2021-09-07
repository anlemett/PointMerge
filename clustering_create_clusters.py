import numpy as np
import pandas as pd
from shapely.geometry import Point
import os
from sklearn.cluster import KMeans

import time
start_time = time.time()

year = '2019'
airport_icao = "EIDW"
#airport_icao = "ESSA"
#airport_icao = "LOWW"

#number_of_clusters = 9
number_of_clusters = 10

#input_filename = airport_icao + "_dataset_PM_TMA_borders_points.csv"
#input_states_filename = airport_icao + "_dataset_PM"
#output_filename = airport_icao + "_dataset_PM_TMA_borders_clusters_" + str(number_of_clusters) + ".csv"

input_filename = airport_icao + "_dataset_TT_TMA_borders_points.csv"
input_states_filename = airport_icao + "_dataset_TT"
output_filename = airport_icao + "_dataset_TT_TMA_borders_clusters_" + str(number_of_clusters) + ".csv"


DATA_DIR = os.path.join("data", airport_icao)
DATA_DIR = os.path.join(DATA_DIR, year)
DATASET_DATA_DIR = os.path.join(DATA_DIR, "Dataset")
DATA_DIR = os.path.join(DATA_DIR, "Clustering")

points_df = pd.read_csv(os.path.join(DATA_DIR, input_filename), sep=' ')
points_df.set_index(['flight_id'], inplace=True)

number_of_flights = len(points_df.groupby(level='flight_id'))
print(number_of_flights)

points = np.zeros(shape=(number_of_flights, 2))

i = 0
for flight_id, row in points_df.iterrows():
    
    points[i] = [row['lon'], row['lat']]
    i = i + 1
    
# create kmeans object
kmeans = KMeans(n_clusters=number_of_clusters)

# fit kmeans object to data
kmeans.fit(points)

# save new clusters
clusters = kmeans.fit_predict(points)

clusters = clusters

points_df['cluster'] = clusters

def getClusterLon(cluster):
    return kmeans.cluster_centers_[int(cluster), 0]

def getClusterLat(cluster):
    return kmeans.cluster_centers_[int(cluster), 1]

points_df['center_lat'] = points_df.apply(lambda row: getClusterLat(row['cluster']), axis=1)
points_df['center_lon'] = points_df.apply(lambda row: getClusterLon(row['cluster']), axis=1)


# Creating cluster states files
clusters_df_list = []
for i in range(0, number_of_clusters):
    df = pd.DataFrame()
    clusters_df_list.append(df)

states_df = pd.read_csv(os.path.join(DATASET_DATA_DIR, input_states_filename + ".csv"), sep=' ',
    names = ['flight_id', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'date'])
states_df.set_index(['flight_id', 'sequence'], inplace = True)


for flight_id, row in points_df.iterrows():  
    row_cluster = int(row['cluster'])
    #flight_df = states_df.loc[flight_id]
    flight_df = states_df[states_df.index.get_level_values('flight_id') == flight_id]
    clusters_df_list[row_cluster] = clusters_df_list[row_cluster].append(flight_df)
    
CLUSTERS_DATA_DIR = os.path.join(DATASET_DATA_DIR, input_states_filename + "_clusters")
if not os.path.exists(CLUSTERS_DATA_DIR):
    os.makedirs(CLUSTERS_DATA_DIR)
    
for i in range(0, number_of_clusters):
    output_states_filename = input_states_filename + "_cluster" + str(i+1) + ".csv"
    clusters_df_list[i].to_csv(os.path.join(CLUSTERS_DATA_DIR, output_states_filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)
   
    
def fixClusterNumber(cluster):
    return int(cluster + 1)

points_df['cluster'] = points_df.apply(lambda row: fixClusterNumber(row['cluster']), axis=1)

points_df.to_csv(os.path.join(DATA_DIR, output_filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = True)   






