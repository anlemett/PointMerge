import pandas as pd
import os
import matplotlib.pyplot as plt

year = '2019'

PIs_type = "vertical"
#PI_vertical = "time_on_levels_percent"
#PI_y_label = "Time on levels [%]"
PI_vertical = "time_on_levels"
PI_y_label = "Time on levels [min]"

#PIs_type = "horizontal"
#PI_horizontal = "TMA_additional_distance_percent"
#PI_y_label = "Additional distance [%]"
PI_horizontal = "TMA_additional_distance"
#PI_y_label = "Additional distance [m]"


airport_icaos = ["EIDW", "ESSA", "LOWW"]

PIs_dict = {}

DATA_DIR = os.path.join("data", "EIDW")
DATA_DIR = os.path.join(DATA_DIR, year)
DATA_PIs_DIR = os.path.join(DATA_DIR, "PIs")

dataset_name = "EIDW_dataset_PM"

if PIs_type == "vertical":
    input_filename = dataset_name + "_PIs_vertical_by_flight.csv"
    full_input_filename = os.path.join(DATA_PIs_DIR, input_filename)
    PIs_vertical_df = pd.read_csv(full_input_filename, sep=' ')
    PIs_dict["EIDW PM"] = PIs_vertical_df[PI_vertical]
else: # horizontal
    input_filename = dataset_name + "_PIs_horizontal_by_flight.csv"
    full_input_filename = os.path.join(DATA_PIs_DIR, input_filename)
    PIs_horizontal_df = pd.read_csv(full_input_filename, sep=' ')
    PIs_dict["EIDW PM"] = PIs_horizontal_df[PI_horizontal]

for airport_icao in airport_icaos:
    DATA_DIR = os.path.join("data", airport_icao)
    DATA_DIR = os.path.join(DATA_DIR, year)
    DATA_PIs_DIR = os.path.join(DATA_DIR, "PIs")

    dataset_name = airport_icao + "_dataset_TT"

    if PIs_type == "vertical":
        input_filename = dataset_name + "_PIs_vertical_by_flight.csv"
        full_input_filename = os.path.join(DATA_PIs_DIR, input_filename)
        PIs_vertical_df = pd.read_csv(full_input_filename, sep=' ')
        PIs_dict[airport_icao] = PIs_vertical_df[PI_vertical]
    else: # horizontal
        input_filename = dataset_name + "_PIs_horizontal_by_flight.csv"
        full_input_filename = os.path.join(DATA_PIs_DIR, input_filename)
        PIs_horizontal_df = pd.read_csv(full_input_filename, sep=' ')
        PIs_dict[airport_icao] = PIs_horizontal_df[PI_horizontal]

fig, ax = plt.subplots(1, 1,figsize=(8,4))
ax.boxplot(PIs_dict.values())
ax.set_xticklabels(PIs_dict.keys())
plt.ylabel(PI_y_label, fontsize=15) 
plt.show()