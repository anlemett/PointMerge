import pandas as pd
import os
import matplotlib.pyplot as plt

year = '2019'

PIs_type = "vertical"
PI_vertical = "time_on_levels_percent"
#PI_vertical = "time_on_levels"

#PIs_type = "horizontal"
PI_horizontal = "TMA_additional_distance_percent"
#PI_horizontal = "TMA_additional_distance"


airport_icaos = ["EIDW", "ESSA", "LOWW"]

for airport_icao in airport_icaos:
    DATA_DIR = os.path.join("data", airport_icao)
    DATA_DIR = os.path.join(DATA_DIR, year)
    DATA_PIs_DIR = os.path.join(DATA_DIR, "PIs")

    dataset_name = airport_icao + "_dataset_TT"

    if PIs_type == "vertical":
        input_filename = dataset_name + "_PIs_vertical_by_flight.csv"
        full_input_filename = os.path.join(DATA_PIs_DIR, input_filename)
        PIs_vertical_df = pd.read_csv(full_input_filename, sep=' ')
        PIs_vertical = PIs_vertical_df[PI_vertical]
        PIs_vertical_max = max(PIs_vertical)
        max_PI_df = PIs_vertical_df[PIs_vertical_df[PI_vertical]==PIs_vertical_max]
        print(max_PI_df.head())
        # EIDW:  191024RYR153 (1.0)
        # ESSA: 191017BLX228, 191017SAS2472, 191027SAS2471 (0.6)
        # LOWW: 191022SWR1576, 191026AUA83D, 191026EWG8KP (0.8)
    else: # horizontal
        input_filename = dataset_name + "_PIs_horizontal_by_flight.csv"
        full_input_filename = os.path.join(DATA_PIs_DIR, input_filename)
        PIs_horizontal_df = pd.read_csv(full_input_filename, sep=' ')
        

