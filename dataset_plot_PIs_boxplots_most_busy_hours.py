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


PIs_dict = {}

dataset_name = "EIDW_dataset_PM"
DATA_DIR = os.path.join("data", "EIDW")
DATA_DIR = os.path.join(DATA_DIR, year)
DATA_PIs_DIR = os.path.join(DATA_DIR, "PIs")


dataset_name = "EIDW_dataset_TT"

# 04.10 16:00 (EIDW TT)

if PIs_type == "vertical":
    input_filename = dataset_name + "_PIs_vertical_by_flight.csv"
    full_input_filename = os.path.join(DATA_PIs_DIR, input_filename)
    PIs_vertical_df = pd.read_csv(full_input_filename, sep=' ')
    PIs_vertical_df = PIs_vertical_df[PIs_vertical_df['begin_date']==191004]
    PIs_vertical_df = PIs_vertical_df[PIs_vertical_df['begin_hour']==16]
    PIs_dict["EIDW"] = PIs_vertical_df[PI_vertical]
else: # horizontal
    input_filename = dataset_name + "_PIs_horizontal_by_flight.csv"
    full_input_filename = os.path.join(DATA_PIs_DIR, input_filename)
    PIs_horizontal_df = pd.read_csv(full_input_filename, sep=' ')
    PIs_horizontal_df = PIs_horizontal_df[PIs_horizontal_df['begin_date']==191004]
    PIs_horizontal_df = PIs_horizontal_df[PIs_horizontal_df['begin_hour']==16]
    PIs_dict["EIDW"] = PIs_horizontal_df[PI_horizontal]

dataset_name = "ESSA_dataset_TT"
DATA_DIR = os.path.join("data", "ESSA")
DATA_DIR = os.path.join(DATA_DIR, year)
DATA_PIs_DIR = os.path.join(DATA_DIR, "PIs")

# 03.10 18:00 (ESSA)

if PIs_type == "vertical":
    input_filename = dataset_name + "_PIs_vertical_by_flight.csv"
    full_input_filename = os.path.join(DATA_PIs_DIR, input_filename)
    PIs_vertical_df = pd.read_csv(full_input_filename, sep=' ')
    PIs_vertical_df = PIs_vertical_df[PIs_vertical_df['begin_date']==191003]
    PIs_vertical_df = PIs_vertical_df[PIs_vertical_df['begin_hour']==18]
    PIs_dict["ESSA"] = PIs_vertical_df[PI_vertical]
else: # horizontal
    input_filename = dataset_name + "_PIs_horizontal_by_flight.csv"
    full_input_filename = os.path.join(DATA_PIs_DIR, input_filename)
    PIs_horizontal_df = pd.read_csv(full_input_filename, sep=' ')
    PIs_horizontal_df = PIs_horizontal_df[PIs_horizontal_df['begin_date']==191003]
    PIs_horizontal_df = PIs_horizontal_df[PIs_horizontal_df['begin_hour']==18]
    PIs_dict["ESSA"] = PIs_horizontal_df[PI_horizontal]

dataset_name = "LOWW_dataset_TT"
DATA_DIR = os.path.join("data", "LOWW")
DATA_DIR = os.path.join(DATA_DIR, year)
DATA_PIs_DIR = os.path.join(DATA_DIR, "PIs")

# 17.10 17:00 (LOWW)
# 20.10 6:00 (LOWW)

if PIs_type == "vertical":
    input_filename = dataset_name + "_PIs_vertical_by_flight.csv"
    full_input_filename = os.path.join(DATA_PIs_DIR, input_filename)
    PIs_vertical_df = pd.read_csv(full_input_filename, sep=' ')
    date_df = PIs_vertical_df[PIs_vertical_df['begin_date']==191017]
    hour_df = date_df[date_df['begin_hour']==17]
    PIs_dict["LOWW 17.10 17-18"] = hour_df[PI_vertical]
    date_df = PIs_vertical_df[PIs_vertical_df['begin_date']==191020]
    hour_df = date_df[date_df['begin_hour']==6]
    PIs_dict["LOWW 20.10 6-7"] = hour_df[PI_vertical]
else: # horizontal
    input_filename = dataset_name + "_PIs_horizontal_by_flight.csv"
    full_input_filename = os.path.join(DATA_PIs_DIR, input_filename)
    PIs_horizontal_df = pd.read_csv(full_input_filename, sep=' ')
    date_df = PIs_horizontal_df[PIs_horizontal_df['begin_date']==191017]
    hour_df = date_df[date_df['begin_hour']==17]
    PIs_dict["LOWW 17.10 17-18"] = hour_df[PI_horizontal]
    date_df = PIs_horizontal_df[PIs_horizontal_df['begin_date']==191020]
    hour_df = date_df[date_df['begin_hour']==6]
    PIs_dict["LOWW 20.10 6-7"] = hour_df[PI_horizontal]

fig, ax = plt.subplots(1, 1,figsize=(8,4))
ax.boxplot(PIs_dict.values())
ax.set_xticklabels(PIs_dict.keys(), fontsize=8)
plt.ylabel(PI_y_label, fontsize=15) 
plt.show()