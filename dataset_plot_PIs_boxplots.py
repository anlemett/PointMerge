import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import statistics

year = '2019'

#PIs_type = "vertical"
PI_vertical = "time_on_levels_percent"
#PI_y_label = "Time Flown Level [%]"
#PI_vertical = "time_on_levels"
#PI_y_label = "Time on levels [min]"

PIs_type = "horizontal"
PI_horizontal1 = "50NM_additional_distance"
PI_horizontal2 = "TMA_additional_distance"
PI_y_label = "Additional Distance [NM]"


datasets = ["EIDW_TT", "ESSA_TT", "LOWW_TT", "EIDW_PM", "LOWW_TB"]

PIs_dict = {}

'''
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
'''
for dataset in datasets:
    if dataset == "EIDW_TT":
        dataset_name = "EIDW_50NM_rwy_dataset_TT"
        DATA_DIR = os.path.join("data", "EIDW_50NM_rwy")
    elif dataset == "ESSA_TT":
        dataset_name = "ESSA_dataset_TT"       
        DATA_DIR = os.path.join("data", "ESSA")
    elif dataset == "LOWW_TT":
        dataset_name = "LOWW_dataset_TT"
        DATA_DIR = os.path.join("data", "LOWW")
    elif dataset == "EIDW_PM":
        dataset_name = "EIDW_50NM_rwy_dataset_PM"
        DATA_DIR = os.path.join("data", "EIDW_50NM_rwy")  
    else: # TB
        dataset_name = "LOWW_50NM_rwy_dataset_TB"
        DATA_DIR = os.path.join("data", "LOWW_50NM_rwy")
    DATA_DIR = os.path.join(DATA_DIR, year)
    DATA_PIs_DIR = os.path.join(DATA_DIR, "PIs")

    

    if PIs_type == "vertical":
        input_filename = dataset_name + "_PIs_vertical_by_flight.csv"
        full_input_filename = os.path.join(DATA_PIs_DIR, input_filename)
        PIs_vertical_df = pd.read_csv(full_input_filename, sep=' ')
        PIs_dict[dataset] = PIs_vertical_df[PI_vertical]
        
    else: # horizontal
        input_filename = dataset_name + "_PIs_horizontal_by_flight.csv"
        full_input_filename = os.path.join(DATA_PIs_DIR, input_filename)
        PIs_horizontal_df = pd.read_csv(full_input_filename, sep=' ')
        #if airport_icao == "EIDW":
        if dataset == "ESSA_TT":
            PIs_dict[dataset] = PIs_horizontal_df[PI_horizontal2]/1852
        elif dataset == "LOWW_TT":
            PIs_dict[dataset] = PIs_horizontal_df[PI_horizontal2]/1852
        elif dataset == "EIDW_TT":
            PIs_dict[dataset] = PIs_horizontal_df[PI_horizontal1]/1852
        elif dataset == "LOWW_PM":
            PIs_dict[dataset] = PIs_horizontal_df[PI_horizontal1]/1852
        else: #TB
            PIs_dict[dataset] = PIs_horizontal_df[PI_horizontal1]/1852
            
    PI_median = PIs_dict[dataset].median()
    PI_mean = PIs_dict[dataset].mean()
    PI_std = statistics.stdev(PIs_dict[dataset])
    PI_min = PIs_dict[dataset].min()
    PI_max = PIs_dict[dataset].max()
        
    print(PI_median, PI_mean, PI_std, PI_min, PI_max)
   
#print(PIs_dict.values())         
#colors = [0 154 178;255 213 0;178 0 77]./255;

#fig, ax = plt.subplots(1, 1,figsize=(7,8))
fig, ax = plt.subplots(1, 1,figsize=(4,3))

colors = [(178/255, 0.0, 77/255), (1.0, 213/255, 0.0), (0.0, 154/255, 178/255), (178/255, 0.0, 77/255), (0.0, 154/255, 178/255)]

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
    
ax.set_xticklabels(["TT", "TT", "TT", "PM", "TB"], fontsize=10)
plt.ylabel(PI_y_label, fontsize=15)
plt.yticks(fontsize=10)
#plt.subplots_adjust(left=0.16, right=0.99, top=0.99, bottom=0.14)
plt.subplots_adjust(left=0.18, right=0.99, top=0.99, bottom=0.14)

# plot legend
import matplotlib.patches as mpatches
handles = []
color_patch = mpatches.Patch(color=colors[0], alpha = 0.5, label='EIDW')
handles += [color_patch]
color_patch = mpatches.Patch(color=colors[1], alpha = 0.5, label='ESSA')
handles += [color_patch]
color_patch = mpatches.Patch(color=colors[2], alpha = 0.5, label='LOWW')
handles += [color_patch]
plt.legend(handles=handles, fontsize=8, edgecolor="black", loc="best", bbox_to_anchor=(0.0, 0.5, 0.5, 0.5))
plt.show()