from logging import raiseExceptions
import numpy.typing as npt
import numpy as np
from scipy.stats import gmean

class Individual:

    """
    Class for indivduals
    """

    def __init__(
        self, individual_params, init_data_attracts, init_data_thresholds, normalized_discount_vector , culture_momentum
    ):
        
        self.init_thresholds = init_data_thresholds


        self.attracts = init_data_attracts
        self.thresholds = init_data_thresholds

        self.normalized_discount_vector = normalized_discount_vector
        #print(self.normalized_discount_vector, sum(self.normalized_discount_vector))

        self.culture_momentum = culture_momentum
        #self.culture_momentum = individual_params["culture_momentum"]
        #self.discount_list = individual_params["discount_list"]
        #self.sum_discount_list = sum(self.discount_list)
        
        self.M = individual_params["M"]
        self.t = individual_params["t"]
        self.delta_t = individual_params["delta_t"]
        self.save_data = individual_params["save_data"]
        self.carbon_intensive_list = individual_params["carbon_emissions"]
        self.carbon_price_state = individual_params["carbon_price_state"]
        self.information_provision_state = individual_params["information_provision_state"]
        self.averaging_method = individual_params["averaging_method"]
        self.compression_factor = individual_params["compression_factor"]
        self.phi_array = individual_params["phi_array"]

        if self.averaging_method == "Threshold weighted arithmetic":
            self.threshold_sum = sum(self.init_thresholds)
            self.threshold_weighting_array = self.init_thresholds/self.threshold_sum
        

        if self.carbon_price_state:
            self.carbon_price = individual_params["carbon_price"]

        if self.information_provision_state:
            self.attract_information_provision_list = individual_params["attract_information_provision_list"]
            self.nu = individual_params["nu"]
            self.eta = individual_params["eta"]
            self.t_IP_list = individual_params["t_IP_list"]

        self.values = self.attracts - self.thresholds

        if self.information_provision_state:
            self.information_provision = self.calc_information_provision()
        
        self.total_carbon_emissions = self.update_total_emissions()
        self.av_behaviour = self.update_av_behaviour()
        #self.total_carbon_emissions, self.av_behaviour  = self.update_total_emissions_av_behaviour()

        self.av_behaviour_list = [self.av_behaviour]*self.culture_momentum
        self.culture = self.calc_culture()

        if self.save_data:
            self.history_behaviour_values = [list(self.values)]
            self.history_behaviour_attracts = [list(self.attracts)]
            self.history_behaviour_thresholds = [list(self.thresholds)]
            self.history_av_behaviour = [self.av_behaviour]
            self.history_culture = [self.culture]
            self.history_carbon_emissions = [self.total_carbon_emissions]
            if self.information_provision_state:
                self.history_information_provision = [self.information_provision]

    def update_av_behaviour_list(self):
        self.av_behaviour_list.pop()
        self.av_behaviour_list.insert(0,self.av_behaviour)

    def calc_culture(self) -> float:
        return np.matmul(self.normalized_discount_vector, self.av_behaviour_list)#here discount list is normalized

    def update_values(self):
        self.values = self.attracts - self.thresholds

    def update_attracts(self,social_component):
        if self.information_provision_state:
            self.attracts = self.attracts*(1 - self.phi_array*self.delta_t) + self.phi_array*self.delta_t*(social_component) + self.information_provision  
        else:
            self.attracts = self.attracts*(1 - self.phi_array*self.delta_t) + self.phi_array*self.delta_t*(social_component)  

    def update_thresholds(self):
        for m in range(self.M):
            if self.init_thresholds[m] < self.carbon_price*self.carbon_intensive_list[m]:
                self.thresholds[m] = 0 
            else:
                self.thresholds[m] = self.init_thresholds[m] - self.carbon_price*self.carbon_intensive_list[m]

    def update_total_emissions(self):
        total_emissions = 0  # calc_carbon_emission
        for i in range(self.M):
            if (self.values[i] <= 0):  # calc_carbon_emissions if less than or equal to 0 then it is a less environmetally friendly behaviour(brown)
                total_emissions += self.carbon_intensive_list[i]  # calc_carbon_emissions
        return total_emissions
    
    def update_total_emissions_alt(self):
        total_emissions = sum(self.carbon_intensive_list[i] for i in range(self.M) if self.values[i] <= 0)
        return total_emissions

    def update_av_behaviour(self):
        if self.averaging_method == "Arithmetic":
            return np.mean(self.attracts)
        elif self.averaging_method == "Geometric":
            return gmean(self.attracts)
        elif self.averaging_method == "Quadratic":
            return np.sqrt(np.mean(self.attracts**2))
        elif self.averaging_method == "Threshold weighted arithmetic":
            return np.matmul(self.threshold_weighting_array, self.attracts)#/(self.M)
        else:
            raiseExceptions("Invalid averaging method choosen try: Arithmetic or Geometric")

    def calc_information_provision_boost(self,i):
        return self.attract_information_provision_list[i]*(1 - np.exp(-self.nu*(self.attract_information_provision_list[i] - self.attracts[i])))

    def calc_information_provision_decay(self,i):
        return self.information_provision[i]*np.exp(-self.eta*(self.t - self.t_IP_list[i]))

    def calc_information_provision(self):
        #print("time; ",self.t_IP_list)
        information_provision = []
        for i in range(self.M):
            if self.t_IP_list[i] == self.t:
                information_provision.append(self.calc_information_provision_boost(i))
            elif self.t_IP_list[i] < self.t and self.information_provision[i] > 0.00000001:
                information_provision.append(self.calc_information_provision_decay(i))
            else:
                information_provision.append(0) #this means that no information provision policy is ever present in this behaviour
        
        #print("information_provision:",information_provision)
        return np.array(information_provision)

    def update_information_provision(self):
        for i in range(self.M):
            if self.t_IP_list[i] == self.t:
                self.information_provision[i] = self.calc_information_provision_boost(i)
            elif self.t_IP_list[i] < self.t and self.information_provision[i] > 0.00000001:
                self.information_provision[i] = self.calc_information_provision_decay(i)
            else:
                self.information_provision[i] = 0 #this means that no information provision policy is ever present in this behaviour

    def save_data_individual(self):
        self.history_behaviour_values.append(list(self.values))
        #print("test", list(self.attracts)[0])
        self.history_behaviour_attracts.append(list(self.attracts))
        self.history_behaviour_thresholds.append(list(self.thresholds))
        self.history_culture.append(self.culture)
        self.history_av_behaviour.append(self.av_behaviour)
        self.history_carbon_emissions.append(self.total_carbon_emissions)
        if self.information_provision_state:
            self.history_information_provision.append(self.information_provision)

    def next_step(self, t:float,steps: int,  social_component: npt.NDArray):
        self.t = t
        self.steps = steps

        if self.information_provision_state:
            self.update_information_provision()

        self.update_values()
        #print("before", self.attracts)
        self.update_attracts(social_component)

        if self.carbon_price_state:
            self.update_thresholds()

        self.total_carbon_emissions = self.update_total_emissions()
        self.av_behaviour = self.update_av_behaviour()

        self.update_av_behaviour_list()

        self.culture = self.calc_culture()
        #print("inv culture", self.culture)
        if self.save_data:
            if self.steps%self.compression_factor == 0:
                self.save_data_individual()
        


