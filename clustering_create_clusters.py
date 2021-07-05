import numpy as np
import pandas as pd
from shapely.geometry import Point
import os
from sklearn.cluster import KMeans

import time
start_time = time.time()

year = '2019'
#airport_icao = "EIDW"
airport_icao = "ESSA"
#airport_icao = "LOWW"

number_of_clusters = 8

#input_filename = "EIDW_dataset_TT_circle40_points.csv"
#input_filename = "EIDW_dataset_PM_circle40_points.csv"
#input_filename = airport_icao + "_dataset_PM_TMA_borders_points.csv"
input_filename = airport_icao + "_dataset_TT_TMA_borders_points.csv"

#output_filename = "EIDW_dataset_TT_circle40_clusters.csv"
#output_filename = "EIDW_dataset_PM_circle40_clusters_" + str(number_of_clusters) + ".csv"
#output_filename = airport_icao + "_dataset_PM_TMA_borders_clusters_" + str(number_of_clusters) + ".csv"
output_filename = airport_icao + "_dataset_TT_TMA_borders_clusters_" + str(number_of_clusters) + ".csv"



DATA_DIR = os.path.join("data", airport_icao)
DATA_DIR = os.path.join(DATA_DIR, year)
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

points_df['cluster'] = clusters

def getClusterLon(cluster):
    return kmeans.cluster_centers_[int(cluster), 0]

def getClusterLat(cluster):
    return kmeans.cluster_centers_[int(cluster), 1]

points_df['center_lon'] = points_df.apply(lambda row: getClusterLon(row['cluster']), axis=1)
points_df['center_lat'] = points_df.apply(lambda row: getClusterLat(row['cluster']), axis=1)

points_df.to_csv(os.path.join(DATA_DIR, output_filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = True)   
