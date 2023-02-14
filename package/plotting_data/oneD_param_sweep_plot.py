"""Plot multiple single simulations varying a single parameter

Author: Daniel Torren Peraire Daniel.Torren@uab.cat dtorrenp@hotmail.com

Created: 10/10/2022
"""

# imports
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
from package.resources.utility import load_object
from package.resources.plot import (
    live_print_culture_timeseries,
    print_live_intial_culture_networks_and_culture_timeseries,

)

def main(
    fileName = "results/one_param_sweep_single_17_43_28__31_01_2023",
    GRAPH_TYPE = 0,
    node_size = 100,
    round_dec = 2,
    dpi_save = 1200,
    ) -> None: 

    cmap = LinearSegmentedColormap.from_list(
        "BrownGreen", ["sienna", "whitesmoke", "olivedrab"], gamma=1
    )
    norm_zero_one = Normalize(vmin=0, vmax=1)

    ############################

    data_list = load_object(fileName + "/Data", "data_list")
    property_varied = load_object(fileName + "/Data", "property_varied")
    property_varied_title = load_object(fileName + "/Data", "property_varied_title")
    property_values_list = load_object(fileName + "/Data", "property_values_list")


    if GRAPH_TYPE == 0:
        #FOR POLARISATION A,B PLOT
        live_print_culture_timeseries(fileName, data_list, property_varied, dpi_save)
    elif GRAPH_TYPE == 1:
        #FOR HOMOPHILY PLOT
        print_live_intial_culture_networks_and_culture_timeseries(fileName, data_list, dpi_save, property_values_list, property_varied_title, norm_zero_one, cmap, node_size,round_dec)
    plt.show()
