import pandas as pd
import os
import matplotlib.pyplot as plt

year = '2019'

#PIs_type = "vertical"
PI_vertical = "time_on_levels_percent"
#PI_y_label = "Time on levels [%]"
#PI_vertical = "time_on_levels"
#PI_y_label = "Time on levels [min]"

PIs_type = "horizontal"
PI_horizontal = "additional_distance"
PI_y_label = "Additional distance [NM]"


PIs_dict = {}

DATA_DIR = os.path.join("data", "EIDW" + "_50NM_rwy")
DATA_DIR = os.path.join(DATA_DIR, year)
DATA_PIs_DIR = os.path.join(DATA_DIR, "PIs")

#dataset_name = "EIDW_50NM_rwy_dataset_TT"
dataset_name = "EIDW_50NM_rwy_dataset_PM"

# 01.10 12:00 (EIDW, TT)

if PIs_type == "vertical":
    input_filename = dataset_name + "_PIs_vertical_by_flight.csv"
    full_input_filename = os.path.join(DATA_PIs_DIR, input_filename)
    PIs_vertical_df = pd.read_csv(full_input_filename, sep=' ')
    PIs_vertical_df = PIs_vertical_df[PIs_vertical_df['begin_date']==191001]
    PIs_vertical_df = PIs_vertical_df[PIs_vertical_df['begin_hour']==12]
    PIs_dict["EIDW"] = PIs_vertical_df[PI_vertical]
else: # horizontal
    input_filename = dataset_name + "_PIs_horizontal_by_flight.csv"
    full_input_filename = os.path.join(DATA_PIs_DIR, input_filename)
    PIs_horizontal_df = pd.read_csv(full_input_filename, sep=' ')
    PIs_horizontal_df = PIs_horizontal_df[PIs_horizontal_df['begin_date']==191001]
    PIs_horizontal_df = PIs_horizontal_df[PIs_horizontal_df['begin_hour']==12]
    PIs_horizontal_df = PIs_horizontal_df.rename(columns = {'50NM_additional_distance': 'additional_distance'})
    PIs_dict["EIDW"] = PIs_horizontal_df[PI_horizontal]/1852

dataset_name = "ESSA_dataset_TT"
DATA_DIR = os.path.join("data", "ESSA")
DATA_DIR = os.path.join(DATA_DIR, year)
DATA_PIs_DIR = os.path.join(DATA_DIR, "PIs")

# 15.10 14:00 (ESSA)

if PIs_type == "vertical":
    input_filename = dataset_name + "_PIs_vertical_by_flight.csv"
    full_input_filename = os.path.join(DATA_PIs_DIR, input_filename)
    PIs_vertical_df = pd.read_csv(full_input_filename, sep=' ')
    PIs_vertical_df = PIs_vertical_df[PIs_vertical_df['begin_date']==191015]
    PIs_vertical_df = PIs_vertical_df[PIs_vertical_df['begin_hour']==14]
    PIs_dict["ESSA"] = PIs_vertical_df[PI_vertical]
else: # horizontal
    input_filename = dataset_name + "_PIs_horizontal_by_flight.csv"
    full_input_filename = os.path.join(DATA_PIs_DIR, input_filename)
    PIs_horizontal_df = pd.read_csv(full_input_filename, sep=' ')
    PIs_horizontal_df = PIs_horizontal_df[PIs_horizontal_df['begin_date']==191015]
    PIs_horizontal_df = PIs_horizontal_df[PIs_horizontal_df['begin_hour']==14]
    PIs_horizontal_df = PIs_horizontal_df.rename(columns = {'TMA_additional_distance': 'additional_distance'})
    PIs_dict["ESSA"] = PIs_horizontal_df[PI_horizontal]/1852

#dataset_name = "LOWW_dataset_TT"
#DATA_DIR = os.path.join("data", "LOWW")
dataset_name = "LOWW_50NM_rwy_dataset_TB"
DATA_DIR = os.path.join("data", "LOWW_50NM_rwy")
DATA_DIR = os.path.join(DATA_DIR, year)
DATA_PIs_DIR = os.path.join(DATA_DIR, "PIs")

# 13.10 7:00 (LOWW)

if PIs_type == "vertical":
    input_filename = dataset_name + "_PIs_vertical_by_flight.csv"
    full_input_filename = os.path.join(DATA_PIs_DIR, input_filename)
    PIs_vertical_df = pd.read_csv(full_input_filename, sep=' ')
    PIs_vertical_df = PIs_vertical_df[PIs_vertical_df['begin_date']==191013]
    PIs_vertical_df = PIs_vertical_df[PIs_vertical_df['begin_hour']==7]
    PIs_dict["LOWW"] = PIs_vertical_df[PI_vertical]
else: # horizontal
    input_filename = dataset_name + "_PIs_horizontal_by_flight.csv"
    full_input_filename = os.path.join(DATA_PIs_DIR, input_filename)
    PIs_horizontal_df = pd.read_csv(full_input_filename, sep=' ')
    PIs_horizontal_df = PIs_horizontal_df[PIs_horizontal_df['begin_date']==191013]
    PIs_horizontal_df = PIs_horizontal_df[PIs_horizontal_df['begin_hour']==7]
    #PIs_horizontal_df = PIs_horizontal_df.rename(columns = {'TMA_additional_distance': 'additional_distance'})
    PIs_horizontal_df = PIs_horizontal_df.rename(columns = {'50NM_additional_distance': 'additional_distance'})
    PIs_dict["LOWW"] = PIs_horizontal_df[PI_horizontal]/1852


#fig, ax = plt.subplots(1, 1,figsize=(8,4))
#ax.boxplot(PIs_dict.values())
#ax.set_xticklabels(PIs_dict.keys())
#plt.ylabel(PI_y_label, fontsize=15) 
#plt.show()

fig, ax = plt.subplots(1, 1,figsize=(7,8))

colors = [(178/255, 0.0, 77/255), (1.0, 213/255, 0.0), (0.0, 154/255, 178/255)]

medianprops = dict(linestyle='-', linewidth=1, color='red')
flierprops = dict(marker='o', markerfacecolor='green', markersize=12,
                  markeredgecolor='none')

box_plot = ax.boxplot(PIs_dict.values(), sym='+', medianprops=medianprops, patch_artist=True)

for patch, color in zip(box_plot['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.5)
    
for flier, color in zip(box_plot['fliers'], colors):
    flier.set(markeredgecolor = color, alpha = 0.5)
    
for whisker in box_plot['whiskers']:
    whisker.set(linestyle ="--")
    
ax.set_xticklabels(PIs_dict.keys(), fontsize=15)
plt.ylabel(PI_y_label, fontsize=20)
plt.yticks(fontsize=15)
plt.subplots_adjust(left=0.11, right=0.99, top=0.99, bottom=0.07)
#plt.subplots_adjust(left=0.13, right=0.99, top=0.99, bottom=0.07)
plt.show()
