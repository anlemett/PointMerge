import pandas as pd
import os
import matplotlib.pyplot as plt

year = '2019'
airport_icao = "ESSA"
#PIs_type = "vertical"
#PI_y_label = "Time on levels [min]"
PIs_type = "horizontal"
PI_y_label = "Additional distance [m]"

if airport_icao == "EIDW":
    number_of_clusters = 10
elif airport_icao == "ESSA":
    number_of_clusters = 6
elif airport_icao == "LOWW":
    number_of_clusters = 10

DATA_DIR = os.path.join("data", airport_icao)
DATA_DIR = os.path.join(DATA_DIR, year)
DATA_PIs_DIR = os.path.join(DATA_DIR, "PIs")

dataset_name = airport_icao + "_dataset_TT"

PIs_by_cluster_dict = {}

for i in range(0, number_of_clusters):
    input_filename = dataset_name + "_PIs_" + PIs_type + "_by_flight_cluster" + str(i+1) + ".csv"
    full_input_filename = os.path.join(DATA_PIs_DIR, input_filename)
    PIs_by_clusters_df = pd.read_csv(full_input_filename, sep=' ')

    if PIs_type == "vertical":
        PIs_by_cluster_dict[i+1] = PIs_by_clusters_df['time_on_levels_percent']
    else: # horizontal
        #PIs_by_cluster_dict[i+1] = PIs_by_clusters_df['TMA_additional_distance_percent']
        PIs_by_cluster_dict[i+1] = PIs_by_clusters_df['TMA_additional_distance']

fig, ax = plt.subplots(1, 1,figsize=(8,4))
ax.boxplot(PIs_by_cluster_dict.values())
ax.set_xticklabels(PIs_by_cluster_dict.keys())
plt.ylabel(PI_y_label, fontsize=15) 
plt.show()