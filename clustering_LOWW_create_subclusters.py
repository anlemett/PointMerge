import numpy as np
import pandas as pd
import os

from shapely.geometry import Point
from shapely.geometry import Polygon

import time
start_time = time.time()

year = '2019'

number_of_clusters = 9
problematic_cluster_number = 6

input_filename = "LOWW_dataset_TT_TMA_borders_clusters_" + str(number_of_clusters) + ".csv"


DATA_DIR = os.path.join("data", "LOWW")
DATA_DIR = os.path.join(DATA_DIR, year)
DATASET_DATA_DIR = os.path.join(DATA_DIR, "Dataset")
CLUSTERS_DATA_DIR = os.path.join(DATASET_DATA_DIR, "LOWW_dataset_TT_clusters")
DATA_DIR = os.path.join(DATA_DIR, "Clustering")

cluster_states_filename = "LOWW_dataset_TT_cluster" + str(problematic_cluster_number) + "_old.csv"
cluster_states_df = pd.read_csv(os.path.join(CLUSTERS_DATA_DIR, cluster_states_filename), sep=' ',
                                 names = ['flight_id', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'date'])
cluster_states_df.set_index(['flight_id'], inplace=True)
number_of_flights = len(cluster_states_df.groupby(level='flight_id'))
print(number_of_flights)


filename = "LOWW_dataset_TT_problematic_cluster_flight_ids.txt"
cluster_flight_ids_set = set(open(os.path.join(CLUSTERS_DATA_DIR, filename) ,'r').read().split('\n'))

filename = "LOWW_dataset_TT_problematic_cluster_flight_ids_subcluster.txt"
sub_cluster1_flight_ids_set = set(open(os.path.join(CLUSTERS_DATA_DIR, filename) ,'r').read().split('\n'))
sub_cluster2_flight_ids_set = cluster_flight_ids_set - sub_cluster1_flight_ids_set
print(len(sub_cluster1_flight_ids_set))
print(len(sub_cluster2_flight_ids_set))
subcluster1_df = cluster_states_df.loc[sub_cluster1_flight_ids_set]
subcluster2_df = cluster_states_df.loc[sub_cluster2_flight_ids_set]

subcluster1_filename = "LOWW_dataset_TT_cluster" + str(problematic_cluster_number) + ".csv"
subcluster1_df.to_csv(os.path.join(CLUSTERS_DATA_DIR, subcluster1_filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)
subcluster2_filename = "LOWW_dataset_TT_cluster" + str(number_of_clusters + 1) + ".csv"
subcluster2_df.to_csv(os.path.join(CLUSTERS_DATA_DIR, subcluster2_filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)

clustering_filename_old = "LOWW_dataset_TT_TMA_borders_clusters_" + str(number_of_clusters) + ".csv"
clustering_filename_new = "LOWW_dataset_TT_TMA_borders_clusters_" + str(number_of_clusters+1) + ".csv"

points_df = pd.read_csv(os.path.join(DATA_DIR, clustering_filename_old), sep=' ')
points_df.set_index(['flight_id'], inplace=True)

for flight_id, row in points_df.iterrows():
    if flight_id in cluster_flight_ids_set:
        if flight_id in sub_cluster2_flight_ids_set:
            points_df.loc[flight_id,'cluster'] = int(number_of_clusters + 1)

            
# make new cluster centroids

def centroid(lons, lats):
    _len = len(lons)
    centroid_x = sum(lons)/_len
    centroid_y = sum(lats)/_len
    return [centroid_x, centroid_y]

subcluster1_points_df = points_df[points_df['cluster']==problematic_cluster_number]
lats = subcluster1_points_df['lat'].to_list()
lons = subcluster1_points_df['lon'].to_list()

center_lon, center_lat = centroid(lons, lats)

for flight_id, row in points_df.iterrows():
    if row['cluster']==problematic_cluster_number:
        points_df.loc[flight_id,'center_lon'] = center_lon
        points_df.loc[flight_id,'center_lat'] = center_lat

subcluster2_points_df = points_df[points_df['cluster']==number_of_clusters+1]
lats2 = subcluster2_points_df['lat'].to_list()
lons2 = subcluster2_points_df['lon'].to_list()

center_lon, center_lat = centroid(lons2, lats2)

for flight_id, row in points_df.iterrows():
    if row['cluster']==number_of_clusters+1:
        points_df.loc[flight_id,'center_lon'] = center_lon
        points_df.loc[flight_id,'center_lat'] = center_lat

points_df.to_csv(os.path.join(DATA_DIR, clustering_filename_new), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = True)   


