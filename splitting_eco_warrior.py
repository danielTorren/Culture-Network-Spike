"""Run multiple simulations varying two parameters
A module that use input data to generate data from multiple social networks varying two properties
between simulations so that the differences may be compared. These multiple runs can either be single 
shot runs or taking the average over multiple runs. Useful for comparing the influences of these parameters
on each other to generate phase diagrams.

TWO MODES 
    The two parameters can be varied covering a 2D plane of points. This can either be done in SINGLE = True where individual 
    runs are used as the output and gives much greater variety of possible plots but all these plots use the same initial
    seed. Alternatively can be run such that multiple averages of the simulation are produced and then the data accessible 
    is the emissions, mean identity, variance of identity and the coefficient of variance of identity.

Author: Daniel Torren Peraire Daniel.Torren@uab.cat dtorrenp@hotmail.com

Created: 10/10/2022
"""

# imports
import matplotlib.pyplot as plt
import json
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.cm import get_cmap
from resources.plot import (
    live_print_culture_timeseries,
    print_culture_timeseries_vary_array,
    live_print_culture_timeseries_vary,
    live_compare_plot_animate_behaviour_scatter,
    live_compare_animate_culture_network_and_weighting,
    live_compare_animate_weighting_matrix,
    live_compare_animate_behaviour_matrix,
    # live_print_heterogenous_culture_momentum_double,
    live_average_multirun_double_phase_diagram_mean,
    live_average_multirun_double_phase_diagram_mean_alt,
    live_average_multirun_double_phase_diagram_C_of_V_alt,
    live_average_multirun_double_phase_diagram_C_of_V,
    double_phase_diagram,
    double_phase_diagram_using_meanandvariance,
    double_matrix_plot,
    multi_line_matrix_plot,
    multi_line_matrix_plot_difference,
    multi_line_matrix_plot_difference_percentage,
    multi_line_matrix_plot_divide_through,
    double_matrix_plot_ab,
    double_matrix_plot_cluster,
    double_matrix_plot_cluster_ratio,
    double_matrix_plot_cluster_multi,
    double_matrix_plot_cluster_var_multi,
    double_contour_plot_cluster,
    plot_culture_time_series_emissions,
    plot_behaviours_time_series_emissions,
    plot_behaviours_time_series_emissions_and_culture,
    plot_emissions_distance,
    plot_emissions_multi_ab,
    plot_emissions_multi_ab_relative,
)
from resources.utility import (
    createFolder,
    generate_vals_variable_parameters_and_norms,
    save_object,
    load_object,
    produce_name_datetime,
    calc_num_clusters_set_bandwidth,
)
from resources.multi_run_2D_param import (
    generate_title_list,
    shot_two_dimensional_param_run,
    load_data_shot,
    av_two_dimensional_param_run,
    load_data_av,
    reshape_results_matricies,
    produce_param_list_n_double,
)
from resources.run import (
    single_stochstic_emissions_run,
    multi_stochstic_emissions_run,
    generate_data,
    parallel_run,
)
import numpy as np



#fileName_no_identity = "results/splitting_eco_warriors_multi_set_N_10_49_28__08_01_2023"#this is the NO identity one
#fileName = "results/splitting_eco_warriors_multi_set_N_10_48_11__08_01_2023"#this is the identity one
#fileName = "results/splitting_eco_warriors_multi_17_39_29__07_01_2023"#this is the NO identity one

fileName = "results/splitting_eco_warriors_distance_single_17_31_07__30_01_2023"#timer seriess fro distances 

#"results/splitting_eco_warriors_single_time_series_17_43_32__24_01_2023"#TIME SERIES RUN

#"results/twoD_Average_confirmation_bias_M_200_3000_20_70_20_5"#"results/twoD_Average_confirmation_bias_a_attitude_200_3000_20_64_64_5"#"
#"results/twoD_Average_confirmation_bias_a_attitude_200_3000_20_64_64_5"
#"results/twoD_Average_action_observation_I_a_attitude_200_2000_20_64_64_5"
#twoD_Average_M_confirmation_bias_200_2000_20_40_64_5
#twoD_Average_homophily_confirmation_bias_200_2000_20_64_64_5
#twoD_Average_M_confirmation_bias_200_2000_20_10_402_5

# run bools
RUN = 1 # run or load in previously saved data

SINGLE = 0 # determine if you runs single shots or study the averages over multiple runs for each experiment
MULTI_THETA_M = 0
MULTI = 0
SINGLE_TIME_SERIES = 0
DISTANCE_SINGLE_TIME_SERIES = 0
MULTI_A_B = 1

multi_line_plot = 0
DUAL_plot = 0



###PLOT STUFF
dpi_save = 1200
round_dec = 2
cmap_weighting = "Reds"
cmap_edge = get_cmap("Greys")

norm_zero_one = Normalize(vmin=0, vmax=1)

if __name__ == "__main__":
    if SINGLE:
        if RUN:
            # load base params
            f_base_params = open("constants/base_params.json")
            base_params = json.load(f_base_params)
            f_base_params.close()
            base_params["time_steps_max"] = int(base_params["total_time"] / base_params["delta_t"])

            # load variable params
            variable_parameters_dict = {
                "col":{"property":"confirmation_bias","min":0, "max":100 , "title": r"Confirmation bias, $\\theta$","divisions": "linear", "reps": 100},  
                "row":{"property":"green_N","min":0, "max": 100, "title": "Eco warrior count","divisions": "linear", "reps": 100}, 
            }

            variable_parameters_dict = generate_vals_variable_parameters_and_norms(
                variable_parameters_dict
            )

            root = "splitting_eco_warriors_single"
            fileName = produce_name_datetime(root)
            print("fileName:", fileName)
            #print("fileName: ", fileName)

            params_dict_list = produce_param_list_n_double(base_params, variable_parameters_dict)

            emissions_list = single_stochstic_emissions_run(params_dict_list)

            matrix_emissions = emissions_list.reshape((variable_parameters_dict["row"]["reps"], variable_parameters_dict["col"]["reps"]))

            createFolder(fileName)
    
            save_object(base_params, fileName + "/Data", "base_params")
            save_object(variable_parameters_dict, fileName + "/Data", "variable_parameters_dict")
            save_object(matrix_emissions, fileName + "/Data", "matrix_emissions")

        else:
            base_params = load_object(fileName + "/Data", "base_params")
            print("alpha state: ", base_params["alpha_change"])
            variable_parameters_dict = load_object(fileName + "/Data", "variable_parameters_dict")
            matrix_emissions = load_object(fileName + "/Data", "matrix_emissions")
    elif MULTI_THETA_M:
        if RUN:
            # load base params
            f_base_params = open("constants/base_params.json")
            base_params = json.load(f_base_params)
            f_base_params.close()
            base_params["time_steps_max"] = int(base_params["total_time"] / base_params["delta_t"])
            base_params["seed_list"] = list(range(5))
            print("seed list: ",base_params["seed_list"])

            base_params["green_N"] = 20 # this is 10%
            # load variable params
            variable_parameters_dict = {
                "col":{"property":"confirmation_bias","min":0, "max":50 , "title": r"Confirmation bias, $\\theta$","divisions": "linear", "reps": 50},  
                "row":{"property":"M","min":1, "max": 11, "title": "M","divisions": "linear", "reps": 10}, 
            }

            variable_parameters_dict = generate_vals_variable_parameters_and_norms(
                variable_parameters_dict
            )

            root = "splitting_eco_warriors_multi_set_N"
            fileName = produce_name_datetime(root)
            print("fileName:", fileName)
            #print("fileName: ", fileName)

            params_dict_list = produce_param_list_n_double(base_params, variable_parameters_dict)

            emissions_list = multi_stochstic_emissions_run(params_dict_list)

            matrix_emissions = emissions_list.reshape((variable_parameters_dict["row"]["reps"], variable_parameters_dict["col"]["reps"]))

            createFolder(fileName)
    
            save_object(base_params, fileName + "/Data", "base_params")
            save_object(variable_parameters_dict, fileName + "/Data", "variable_parameters_dict")
            save_object(matrix_emissions, fileName + "/Data", "matrix_emissions")

        else:
            base_params = load_object(fileName + "/Data", "base_params")
            print("alpha state: ", base_params["alpha_change"])
            variable_parameters_dict = load_object(fileName + "/Data", "variable_parameters_dict")
            matrix_emissions = load_object(fileName + "/Data", "matrix_emissions")
    elif MULTI:#multi run
        if RUN:
            # load base params
            f_base_params = open("constants/base_params.json")
            base_params = json.load(f_base_params)
            f_base_params.close()
            base_params["time_steps_max"] = int(base_params["total_time"] / base_params["delta_t"])
            base_params["seed_list"] = list(range(5))
            print("seed list: ",base_params["seed_list"])
            # load variable params
            variable_parameters_dict = {
                "col":{"property":"confirmation_bias","min":0, "max":100 , "title": r"Confirmation bias, $\\theta$","divisions": "linear", "reps": 40},  
                "row":{"property":"green_N","min":0, "max": 100, "title": "Eco warrior count","divisions": "linear", "reps": 40}, 
            }

            variable_parameters_dict = generate_vals_variable_parameters_and_norms(
                variable_parameters_dict
            )

            root = "splitting_eco_warriors_multi"
            fileName = produce_name_datetime(root)
            print("fileName:", fileName)
            #print("fileName: ", fileName)

            params_dict_list = produce_param_list_n_double(base_params, variable_parameters_dict)

            emissions_list = multi_stochstic_emissions_run(params_dict_list)

            matrix_emissions = emissions_list.reshape((variable_parameters_dict["row"]["reps"], variable_parameters_dict["col"]["reps"]))

            createFolder(fileName)
    
            save_object(base_params, fileName + "/Data", "base_params")
            save_object(variable_parameters_dict, fileName + "/Data", "variable_parameters_dict")
            save_object(matrix_emissions, fileName + "/Data", "matrix_emissions")

        else:
            base_params = load_object(fileName + "/Data", "base_params")
            print("alpha state: ", base_params["alpha_change"])
            variable_parameters_dict = load_object(fileName + "/Data", "variable_parameters_dict")
            matrix_emissions = load_object(fileName + "/Data", "matrix_emissions")
    elif SINGLE_TIME_SERIES:
        if RUN:
            #f = open("constants/base_params.json")
            base_params = {
                "save_timeseries_data": 1, 
                "degroot_aggregation": 1,
                "network_structure": "small_world",
                "alpha_change" : 1.0,
                "guilty_individuals": 0,
                "moral_licensing": 0,
                "immutable_green_fountains": 1,
                "polarisation_test": 0,
                "total_time": 3000,
                "delta_t": 1.0,
                "phi_lower": 0.01,
                "phi_upper": 0.05,
                "compression_factor": 10,
                "seed_list": [1,2,3,4,5],
                "set_seed": 1,
                "N": 200,
                "M": 3,
                "K": 20,
                "prob_rewire": 0.1,
                "culture_momentum_real": 1000,
                "learning_error_scale": 0.02,
                "discount_factor": 0.95,
                "homophily": 0.95,
                "homophilly_rate" : 1,
                "confirmation_bias": 20,
                "a_attitude": 1,
                "b_attitude": 1,
                "a_threshold": 1,
                "b_threshold": 1,
                "action_observation_I": 0.0,
                "action_observation_S": 0.0,
                "green_N": 20,
                "guilty_individual_power": 0
            }
            base_params["time_steps_max"] = int(base_params["total_time"] / base_params["delta_t"])

            #fileName = produceName(params, params_name)
            root = "splitting_eco_warriors_single_time_series"
            fileName = produce_name_datetime(root)
            print("fileName:", fileName)
            ##############################################################################
            #CULTURED RUN
            Data_culture = generate_data(base_params)  # run the simulation
            #NO CULTURE RUN
            base_params["alpha_change"] = 2.0
            Data_no_culture = generate_data(base_params)  # run the simulation


            createFolder(fileName)
            save_object(Data_culture, fileName + "/Data", "Data_culture")
            save_object(Data_no_culture, fileName + "/Data", "Data_no_culture")
            save_object(base_params, fileName + "/Data", "base_params")
        else:
            Data_culture = load_object( fileName + "/Data", "Data_culture")
            Data_no_culture = load_object( fileName + "/Data", "Data_no_culture")
            base_params = load_object( fileName + "/Data", "base_params")
    elif DISTANCE_SINGLE_TIME_SERIES:
        if RUN:
            #f = open("constants/base_params.json")
            base_params = {
                "save_timeseries_data": 1, 
                "degroot_aggregation": 1,
                "network_structure": "small_world",
                "alpha_change" : 1.0,
                "guilty_individuals": 0,
                "moral_licensing": 0,
                "immutable_green_fountains": 1,
                "polarisation_test": 0,
                "total_time": 3000,
                "delta_t": 1.0,
                "phi_lower": 0.01,
                "phi_upper": 0.05,
                "compression_factor": 10,
                "seed_list": [1,2,3,4,5],
                "set_seed": 1,
                "N": 200,
                "M": 3,
                "K": 20,
                "prob_rewire": 0.1,
                "culture_momentum_real": 1000,
                "learning_error_scale": 0.02,
                "discount_factor": 0.95,
                "homophily": 0.95,
                "homophilly_rate" : 1,
                "confirmation_bias": 20,
                "a_attitude": 1,
                "b_attitude": 1,
                "a_threshold": 1,
                "b_threshold": 1,
                "action_observation_I": 0.0,
                "action_observation_S": 0.0,
                "green_N": 20,
                "guilty_individual_power": 0
            }
            base_params["time_steps_max"] = int(base_params["total_time"] / base_params["delta_t"])

            ###############################################################
            init_attitudes_list = [[2,5],[2,2],[5,2]]

            params_list_culture = []

            for i in init_attitudes_list:
                #print("i",i)
                base_params["a_attitude"] = i[0]
                base_params["b_attitude"] = i[1]
                params_list_culture.append(base_params.copy())

            params_list_no_culture  = []
            base_params["alpha_change"] = 2.0
            for i in init_attitudes_list:
                #print("i",i)
                base_params["a_attitude"] = i[0]
                base_params["b_attitude"] = i[1]
                params_list_no_culture.append(base_params.copy())
            #############################################################

            #fileName = produceName(params, params_name)
            root = "splitting_eco_warriors_distance_single"
            fileName = produce_name_datetime(root)
            print("fileName:", fileName)

            ##############################################################################
            #CULTURED RUN
            data_list_culture = parallel_run(params_list_culture)
            #NO CULTURE RUN
            data_list_no_culture = parallel_run(params_list_no_culture)

            createFolder(fileName)
            save_object(data_list_culture, fileName + "/Data", "data_list_culture")
            save_object(data_list_no_culture, fileName + "/Data", "data_list_no_culture")
            save_object(base_params, fileName + "/Data", "base_params")
            save_object(init_attitudes_list,fileName + "/Data", "init_attitudes_list")
        else:
            data_list_culture = load_object( fileName + "/Data", "data_list_culture")
            data_list_no_culture  = load_object( fileName + "/Data", "data_list_no_culture")
            base_params = load_object( fileName + "/Data", "base_params")
            init_attitudes_list = load_object(fileName + "/Data", "init_attitudes_list")
    elif MULTI_A_B:
        if RUN:
            #f = open("constants/base_params.json")
            base_params = {
                "save_timeseries_data": 1, 
                "degroot_aggregation": 1,
                "network_structure": "small_world",
                "alpha_change" : 1.0,
                "guilty_individuals": 0,
                "moral_licensing": 0,
                "immutable_green_fountains": 1,
                "polarisation_test": 0,
                "total_time": 3000,
                "delta_t": 1.0,
                "phi_lower": 0.01,
                "phi_upper": 0.05,
                "compression_factor": 10,
                "seed_list": [1,2,3,4,5, 6, 7, 8, 9, 10],
                "set_seed": 1,
                "N": 200,
                "M": 3,
                "K": 20,
                "prob_rewire": 0.1,
                "culture_momentum_real": 1000,
                "learning_error_scale": 0.02,
                "discount_factor": 0.95,
                "homophily": 0.95,
                "homophilly_rate" : 1,
                "confirmation_bias": 20,
                "a_attitude": 1,
                "b_attitude": 1,
                "a_threshold": 1,
                "b_threshold": 1,
                "action_observation_I": 0.0,
                "action_observation_S": 0.0,
                "green_N": 20,
                "guilty_individual_power": 0
            }
            base_params["time_steps_max"] = int(base_params["total_time"] / base_params["delta_t"])

            ###############################################################

            def gen_atttiudes_list(mean_list, sum_a_b):
                init_attitudes_list = []
                for i in mean_list:
                    a = i*sum_a_b
                    b = sum_a_b - a
                    init_attitudes_list.append([a,b])
                return init_attitudes_list
            
            mean_list = np.linspace(0.01,0.99, 100)
            sum_a_b = 7

            init_attitudes_list = gen_atttiudes_list(mean_list, sum_a_b)# GET THE LIST

            params_list_culture = []

            for i in init_attitudes_list:
                #print("i",i)
                base_params["a_attitude"] = i[0]
                base_params["b_attitude"] = i[1]
                params_list_culture.append(base_params.copy())

            params_list_no_culture  = []
            base_params["alpha_change"] = 2.0
            for i in init_attitudes_list:
                #print("i",i)
                base_params["a_attitude"] = i[0]
                base_params["b_attitude"] = i[1]
                params_list_no_culture.append(base_params.copy())
            #############################################################

            #fileName = produceName(params, params_name)
            root = "splitting_eco_warriors_distance_reps"
            fileName = produce_name_datetime(root)
            print("fileName:", fileName)

            ##############################################################################
            #CULTURED RUN
            emissions_list_culture = multi_stochstic_emissions_run(params_list_culture)
            #data_list_culture = parallel_run(params_list_culture)
            #NO CULTURE RUN
            #data_list_no_culture = parallel_run(params_list_no_culture)
            emissions_list_no_culture = multi_stochstic_emissions_run(params_list_no_culture)

            createFolder(fileName)
            save_object(mean_list, fileName + "/Data", "mean_list")
            save_object(sum_a_b , fileName + "/Data", "sum_a_b ")
            save_object(emissions_list_culture, fileName + "/Data", "emissions_list_culture")
            save_object(emissions_list_no_culture, fileName + "/Data", "emissions_list_no_culture")
            save_object(base_params, fileName + "/Data", "base_params")
            save_object(init_attitudes_list,fileName + "/Data", "init_attitudes_list")
        else:
            emissions_list_culture = load_object( fileName + "/Data", "emissions_list_culture")
            emissions_list_no_culture  = load_object( fileName + "/Data", "emissions_list_no_culture")
            base_params = load_object( fileName + "/Data", "base_params")
            init_attitudes_list = load_object(fileName + "/Data", "init_attitudes_list")
            mean_list = load_object(fileName + "/Data", "mean_list")
            sum_a_b = load_object(fileName + "/Data", "sum_a_b ")

    if multi_line_plot:
        col_dict = variable_parameters_dict["col"]
        row_dict = variable_parameters_dict["row"]

        #### FOR confimation bias vs attitude polarisation
        index_len_x_matrix = col_dict["reps"]
        max_x_val = col_dict["max"]
        min_x_val = col_dict["min"]
        col_ticks_label = list(range(min_x_val, max_x_val, 10))#[-10,0,10,20,30,40,50,60,70,80,90]#[-10,0,10,20,30,40,50,60]#[col_dict["vals"][x] for x in range(len(col_dict["vals"]))  if x % select_val_x == 0]
        col_ticks_pos = list(range(min_x_val, max_x_val, 10))#[-10,0,10,20,30,40,50,60,70,80,90]#[int(round(index_len_x_matrix*((x - min_x_val)/(max_x_val- min_x_val)))) for x in col_ticks_label]#[0,30,70,50]#[0,10,20,30,40,50,60,70]#[x for x in range(len(col_dict["vals"]))  if x % select_val_x == 0]
        print("out col_ticks_pos",col_ticks_pos)

                
        index_len_y_matrix =row_dict["reps"]
        max_y_val = row_dict["max"]
        min_y_val = row_dict["min"]
        row_ticks_label = list(range(min_y_val, max_y_val, 10))#[0.05,0.25,0.50,0.75,1.00,1.25,1.50,1.75,2.00]#[-10,0,10,20,30,40,50,60]#[col_dict["vals"][x] for x in range(len(col_dict["vals"]))  if x % select_val_x == 0]
        row_ticks_pos = list(range(min_y_val, max_y_val, 10))#[0.05,0.25,0.50,0.75,1.00,1.25,1.50,1.75,2.00]#[int(round(index_len_y_matrix*((y - min_y_val)/(max_y_val- min_y_val)))) for y in col_ticks_label]#[0,30,70,50]#[0,10,20,30,40,50,60,70]#[x for x in range(len(col_dict["vals"]))  if x % select_val_x == 0]
        
        #print("row",row_ticks_pos,row_ticks_label)
        #print("col",col_ticks_pos,col_ticks_label)

        row_label = r"Number of behaviours per agent, M"#r"Eco-warriors count"#r"Number of behaviours per agent, M"
        col_label = r'Confirmation bias, $\theta$'#r'Confirmation bias, $\theta$'
        y_label = r"Final emissions, $E$"#r"Identity variance, $\sigma^2$"
        
        multi_line_matrix_plot(fileName,matrix_emissions, col_dict["vals"], row_dict["vals"],"emissions", get_cmap("plasma"),dpi_save,col_ticks_pos, col_ticks_label, row_ticks_pos, row_ticks_label, 0, col_label, row_label, y_label)#y_ticks_pos, y_ticks_label
        multi_line_matrix_plot(fileName,matrix_emissions, col_dict["vals"], row_dict["vals"],"emissions", get_cmap("plasma"),dpi_save,col_ticks_pos, col_ticks_label, row_ticks_pos, row_ticks_label, 1, col_label, row_label, y_label)#y_ticks_pos, y_ticks_label
        #multi_line_matrix_plot(fileName, Z, col_vals, row_vals,  Y_param, cmap, dpi_save, col_ticks_pos, col_ticks_label, row_ticks_pos, row_ticks_label,col_axis_x, col_label, row_label, y_label)
        
    #### two D plot of emissions with confimation bias and number of eco warriors
    if DUAL_plot:
        col_dict = variable_parameters_dict["col"]
        row_dict = variable_parameters_dict["row"]

        #### FOR confimation bias vs attitude polarisation
        index_len_x_matrix = col_dict["reps"]
        max_x_val = col_dict["max"]
        min_x_val = col_dict["min"]
        col_ticks_label = list(range(min_x_val, max_x_val, 10))#[-10,0,10,20,30,40,50,60,70,80,90]#[-10,0,10,20,30,40,50,60]#[col_dict["vals"][x] for x in range(len(col_dict["vals"]))  if x % select_val_x == 0]
        col_ticks_pos = list(range(min_x_val, max_x_val, 10))#[-10,0,10,20,30,40,50,60,70,80,90]#[int(round(index_len_x_matrix*((x - min_x_val)/(max_x_val- min_x_val)))) for x in col_ticks_label]#[0,30,70,50]#[0,10,20,30,40,50,60,70]#[x for x in range(len(col_dict["vals"]))  if x % select_val_x == 0]
        print("out col_ticks_pos",col_ticks_pos)

                
        index_len_y_matrix =row_dict["reps"]
        max_y_val = row_dict["max"]
        min_y_val = row_dict["min"]
        row_ticks_label = list(range(min_y_val, max_y_val, 10))#[0.05,0.25,0.50,0.75,1.00,1.25,1.50,1.75,2.00]#[-10,0,10,20,30,40,50,60]#[col_dict["vals"][x] for x in range(len(col_dict["vals"]))  if x % select_val_x == 0]
        row_ticks_pos = list(range(min_y_val, max_y_val, 10))#[0.05,0.25,0.50,0.75,1.00,1.25,1.50,1.75,2.00]#[int(round(index_len_y_matrix*((y - min_y_val)/(max_y_val- min_y_val)))) for y in col_ticks_label]#[0,30,70,50]#[0,10,20,30,40,50,60,70]#[x for x in range(len(col_dict["vals"]))  if x % select_val_x == 0]
        
        #print("row",row_ticks_pos,row_ticks_label)
        #print("col",col_ticks_pos,col_ticks_label)

        row_label = r"Number of behaviours per agent, M"#r"Eco-warriors count"#
        col_label = r'Confirmation bias, $\theta$'#r'Confirmation bias, $\theta$'
        y_label = r"Change in final emissions, $\Delta E$"#r"Identity variance, $\sigma^2$"

        base_params_no_identity = load_object(fileName_no_identity + "/Data", "base_params")
        #print("alpha state no identity: ", base_params_no_identity["alpha_change"])
        variable_parameters_dict_no_identity = load_object(fileName_no_identity + "/Data", "variable_parameters_dict")
        matrix_emissions_no_identity = load_object(fileName_no_identity + "/Data", "matrix_emissions")
        
        #print(type( matrix_emissions))
        #print(matrix_emissions.shape)
        
        difference_emissions_matrix = matrix_emissions - matrix_emissions_no_identity

        difference_emissions_matrix_percentage = ((matrix_emissions - matrix_emissions_no_identity)/matrix_emissions_no_identity)*100
        #print("difference_emissions_matrix_percentage", difference_emissions_matrix_percentage)
        #print(difference_emissions_matrix, difference_emissions_matrix.shape)

        #multi_line_matrix_plot_difference(fileName,difference_emissions_matrix, col_dict["vals"], row_dict["vals"],"emissions", get_cmap("plasma"),dpi_save,col_ticks_pos, col_ticks_label, row_ticks_pos, row_ticks_label, 0, col_label, row_label, y_label)#y_ticks_pos, y_ticks_label
        #multi_line_matrix_plot_difference(fileName,difference_emissions_matrix, col_dict["vals"], row_dict["vals"],"emissions", get_cmap("plasma"),dpi_save,col_ticks_pos, col_ticks_label, row_ticks_pos, row_ticks_label, 1, col_label, row_label, y_label)#y_ticks_pos, y_ticks_label


        #multi_line_matrix_plot_difference_percentage(fileName,difference_emissions_matrix_percentage, col_dict["vals"], row_dict["vals"],"emissions", get_cmap("plasma"),dpi_save,col_ticks_pos, col_ticks_label, row_ticks_pos, row_ticks_label, 0, col_label, row_label, y_label)#y_ticks_pos, y_ticks_label
        multi_line_matrix_plot_difference_percentage(fileName,difference_emissions_matrix_percentage, col_dict["vals"], row_dict["vals"],"emissions", get_cmap("plasma"),dpi_save,col_ticks_pos, col_ticks_label, row_ticks_pos, row_ticks_label, 1, col_label, row_label, y_label)#y_ticks_pos, y_ticks_label

        #double_matrix_plot(fileName,difference_emissions_matrix, y_label, "emissions",variable_parameters_dict, get_cmap("plasma"),dpi_save,col_ticks_pos,row_ticks_pos,col_ticks_label,row_ticks_label)
        #double_matrix_plot(fileName,difference_emissions_matrix_percentage, y_label, "emissions_percent",variable_parameters_dict, get_cmap("plasma"),dpi_save,col_ticks_pos,row_ticks_pos,col_ticks_label,row_ticks_label)
    if SINGLE_TIME_SERIES:
        #plot_culture_time_series_emissions(fileName,Data_culture, Data_no_culture, dpi_save)
        #plot_behaviours_time_series_emissions(fileName,Data_culture, Data_no_culture, dpi_save)
        plot_behaviours_time_series_emissions_and_culture(fileName,Data_culture, Data_no_culture, dpi_save)

    if DISTANCE_SINGLE_TIME_SERIES:
        plot_emissions_distance(fileName,data_list_culture, data_list_no_culture,init_attitudes_list, dpi_save)

    if MULTI_A_B:
        #plot_emissions_multi_ab(fileName, emissions_list_culture, emissions_list_no_culture, mean_list, dpi_save)
        plot_emissions_multi_ab_relative(fileName, emissions_list_culture, emissions_list_no_culture, mean_list, dpi_save)
    plt.show()
