from network import Network
import time

if __name__ == "__main__":
    # Params
    save_data = True
    opinion_dynamics =  "DEGROOT" #  "DEGROOT"  "SELECT"
    carbon_price_state = False
    information_provision_state = False
    linear_alpha_diff_state = False#if true use the exponential form instead like theo
    homophily_state = True
    alpha_change = True

    #Social emissions model
    K = 6  # k nearest neighbours INTEGER
    M = 3  # number of behaviours
    N = 20  # number of agents
    total_time = 10

    delta_t = 0.1  # time step size
    culture_momentum_real = 5# real time over which culture is calculated for INTEGER, NEEDS TO BE MROE THAN DELTA t

    prob_rewire = 0.2  # re-wiring probability?

    alpha_attract = 1#2  ##inital distribution parameters - doing the inverse inverts it!
    beta_attract = 1#3
    alpha_threshold = 1#3
    beta_threshold = 1#2

    time_steps_max = int(
        total_time / delta_t
    )  # number of time steps max, will stop if culture converges

    set_seed = 1  ##reproducibility INTEGER
    phi_list_lower,phi_list_upper = 0.1,1
    learning_error_scale = 0.05  # 1 standard distribution is 2% error
    carbon_emissions = [1]*M

    inverse_homophily = 1#0.2

    discount_factor = 0.6
    present_discount_factor = 0.8

    confirmation_bias = 1.5

    #Infromation provision parameters
    if information_provision_state:
        nu = 1# how rapidly extra gains in attractiveness are made
        eta = 0.2#decay rate of information provision boost
        attract_information_provision_list = np.array([0.5*(1/delta_t)]*M)#
        t_IP_matrix = np.array([[],[],[]]) #REAL TIME; list stating at which time steps an information provision policy should be aplied for each behaviour

    #Carbon price parameters
    if carbon_price_state:
        carbon_price_policy_start = 5#in simualation time to start the policy
        carbon_price_init = 0.0#
        #social_cost_carbon = 0.5
        carbon_price_gradient = 0#social_cost_carbon/time_steps_max# social cost of carbon/total time

    params = {
        "opinion_dynamics": opinion_dynamics,
        "save_data": save_data, 
        "time_steps_max": time_steps_max, 
        "carbon_price_state" : carbon_price_state,
        "information_provision_state" : information_provision_state,
        "linear_alpha_diff_state": linear_alpha_diff_state,
        "homophily_state": homophily_state,
        "alpha_change" : alpha_change,
        "delta_t": delta_t,
        "phi_list_lower": phi_list_lower,
        "phi_list_upper": phi_list_upper,
        "N": N,
        "M": M,
        "K": K,
        "prob_rewire": prob_rewire,
        "set_seed": set_seed,
        "culture_momentum_real": culture_momentum_real,
        "learning_error_scale": learning_error_scale,
        "alpha_attract": alpha_attract,
        "beta_attract": beta_attract,
        "alpha_threshold": alpha_threshold,
        "beta_threshold": beta_threshold,
        "carbon_emissions" : carbon_emissions,
        "discount_factor": discount_factor,
        "inverse_homophily": inverse_homophily,#1 is total mixing, 0 is no mixing
        "present_discount_factor": present_discount_factor,
        "confirmation_bias": confirmation_bias,
    }
    
    #start_time = time.time()
    social_network = Network(params)
    
    #### RUN TIME STEPS
    time_counter = 0
    while time_counter < params["time_steps_max"]:
        social_network.next_step()
        time_counter += 1
    
    #print(
    #    "SIMULATION time taken: %s minutes" % ((time.time() - start_time) / 60),
    #    "or %s s" % ((time.time() - start_time)),
    #)

 