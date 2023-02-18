"""Define individual agent class
A module that defines "individuals" that have vectors of attitudes towards behaviours whose evolution
is determined through weighted social interactions.

Author: Daniel Torren Peraire Daniel.Torren@uab.cat dtorrenp@hotmail.com

Created: 10/10/2022
"""

# imports
import numpy as np
import numpy.typing as npt

# modules
class Individual_one_m_green_influencer:

    """
    Class to represent individuals with identities and behaviours

    ...

    Attributes
    ----------

    save_timeseries_data : bool
        whether or not to save data. Set to 0 if only interested in end state of the simulation. If 1 will save
        data into timeseries.
    compression_factor: int
        how often data is saved. If set to 1 its every step, then 10 is every 10th steps. Higher value gives lower
        resolution for graphs but more managable saved or end object size
    t: float
        keep track of time
    M: int
        number of behaviours per individual. These behaviours are meant to represent action decisions that operate under the
        same identity such as the decision to cycle to work or take the car.
    phi_array: npt.NDArray[float]
        list of degree of social susceptibility or conspicous consumption of the different behaviours.
    values: npt.NDArray[float]
        array containing behavioural values, if greater than 0 then the green alternative behaviour is performed and emissions from that behaviour are 0. Domain =  [-1,1]
    av_behaviour_attitude
        mean attitude towards M behaviours at time t
    av_behaviour_value
        mean value towards M behaviours at time t
    av_behaviour_list: list[float]
        time series of past average attitude combined with values depending on action_observation_I, as far back as culture_inertia
    culture: float
        identity of the individual, if > 0.5 it is considered green. Determines who individuals pay attention to. Domain = [0,1]
    total_carbon_emissions: float
        total carbon emissions of that individual due to their behaviour
    history_behaviour_values: list[list[float]]
        timeseries of past behavioural values
    history_behaviour_attitudes: list[list[float]]
        timeseries of past behavioural attitudes
    self.history_behaviour_thresholds: list[list[float]]
        timeseries of past behavioural thresholds, static in the current model version
    self.history_av_behaviour: list[float]
        timeseries of past average behavioural attitudes
    self.history_culture: list[float]
        timeseries of past identity values
    self.history_carbon_emissions: list[float]
        timeseries of past individual total emissions

    Methods
    -------
    update_av_behaviour_list():
        Update moving average of past behaviours, inserting present value and 0th index and removing the oldest value
    calc_culture() -> float:
        Calculate the individual identity from past average attitudes weighted by the truncated quasi-hyperbolic discounting factor
    update_values():
        Update the behavioural values of an individual with the new attitudinal or threshold values
    update_attitudes(social_component):
        Update behavioural attitudes with social influence of neighbours mediated by the social susceptabilty of each behaviour phi
    calc_total_emissions():
        return total emissions of individual based on behavioural values
    save_timeseries_data_individual():
        Save time series data
    next_step(t:float, steps:int, social_component: npt.NDArray):
        Push the individual simulation forwards one time step

    """

    def __init__(
        self,
        individual_params,
        init_data_attitudes,
        init_data_thresholds,
        normalized_discount_vector,
        culture_inertia,
        id_n,
    ):
        """
        Constructs all the necessary attributes for the Individual object.

        Parameters
        ----------
        individual_params: dict,
            useful parameters from the network
        init_data_attitudes: npt.NDArray[float]
            array of inital attitudes generated previously from a beta distribution, evolves over time
        init_data_thresholds: npt.NDArray[float]
            array of inital thresholds generated previously from a beta distribution
        normalized_discount_vector: npt.NDArray[float]
            normalized single row of the discounts to individual memory when considering how the past influences current identity
        culture_inertia: int
            the number of steps into the past that are considered when calculating identity

        """

        self.attitudes = init_data_attitudes
        self.initial_first_attitude = (self.attitudes[0]).copy()
        self.thresholds = init_data_thresholds
        self.normalized_discount_vector = normalized_discount_vector
        self.culture_inertia = culture_inertia

        self.M = individual_params["M"]
        self.t = individual_params["t"]
        self.save_timeseries_data = individual_params["save_timeseries_data"]
        self.compression_factor = individual_params["compression_factor"]
        self.phi_array = individual_params["phi_array"]
        self.alpha_change = individual_params["alpha_change"]

        self.id = id_n

        ###################################################
        self.m_green = 0 # SET IT AS 1 FOR NOW!
        self.green_fountain_state = 1

        self.attitudes[self.m_green] = 1.0
        self.thresholds[self.m_green] = 0.0
        ##################################################

        if self.alpha_change == "behavioural_independence":
            self.attitudes_matrix = np.tile(self.attitudes, (self.culture_inertia,1))
            #print("self.attitudes_matrix",self.attitudes_matrix )
            self.attitudes_star = self.calc_attitudes_star()
            #print("self.attitudes_star", self.attitudes_star)


        self.values = self.attitudes - self.thresholds
        self.av_behaviour = np.mean(self.attitudes)
        self.av_behaviour_list = [self.av_behaviour] * self.culture_inertia
        self.culture = self.calc_culture()
        self.initial_carbon_emissions,self.behavioural_carbon_emissions = self.calc_total_emissions()
        self.total_carbon_emissions = self.initial_carbon_emissions

        if self.save_timeseries_data:
            self.history_behaviour_values = [list(self.values)]
            self.history_behaviour_attitudes = [list(self.attitudes)]
            self.history_behaviour_thresholds = [list(self.thresholds)]
            self.history_av_behaviour = [self.av_behaviour]
            self.history_culture = [self.culture]
            self.history_carbon_emissions = [self.total_carbon_emissions]
            self.history_behavioural_carbon_emissions = [self.behavioural_carbon_emissions]

    def calc_av_behaviour(self):
        self.av_behaviour = np.mean(self.attitudes)

    def update_av_behaviour_list(self):
        """
        Update moving average of past behaviours, inserting present value and 0th index and removing the oldest value

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.av_behaviour_list.pop()
        self.av_behaviour_list.insert(0, self.av_behaviour)

    def calc_culture(self) -> float:
        """
        Calculate the individual identity from past average attitudes weighted by the truncated quasi-hyperbolic discounting factor

        Parameters
        ----------
        None

        Returns
        -------
        float
        """

        return np.matmul(
            self.normalized_discount_vector, self.av_behaviour_list
        )  # here discount list is normalized

    def update_attitudes_matrix(self):       
        #print("popping before ", self.attitudes_matrix, self.attitudes_matrix.shape)
        self.attitudes_matrix =  np.vstack([np.asarray([self.attitudes]), self.attitudes_matrix[:-1,:]])
        #print("popping after ", self.attitudes_matrix, self.attitudes_matrix.shape)

    def calc_attitudes_star(self):
        return np.matmul(
            self.normalized_discount_vector, self.attitudes_matrix
        )  # here discount list is normalized

    def update_values(self):
        """
        Update the behavioural values of an individual with the new attitudinal or threshold values

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.values = self.attitudes - self.thresholds

    def update_attitudes(self, social_component):
        """
        Update behavioural attitudes with social influence of neighbours mediated by the social susceptabilty of each behaviour phi

        Parameters
        ----------
        social_component: npt.NDArray[float]

        Returns
        -------
        None
        """
        self.attitudes = (1 - self.phi_array)*self.attitudes + (self.phi_array)*(social_component)
        self.attitudes[self.m_green] = 1.0

    def calc_total_emissions(self):
        """
        Return total emissions of individual based on behavioural values

        Parameters
        ----------
        None

        Returns
        -------
        float
        """
        behavioural_emissions = [((1-self.values[i])/2) for i in range(self.M)]
        return sum(behavioural_emissions),behavioural_emissions# normalized Beta now used for emissions

    def save_timeseries_data_individual(self):
        """
        Save time series data

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.history_behaviour_values.append(list(self.values))
        self.history_behaviour_attitudes.append(list(self.attitudes))
        self.history_behaviour_thresholds.append(list(self.thresholds))
        self.history_culture.append(self.culture)
        self.history_av_behaviour.append(self.av_behaviour)
        self.history_carbon_emissions.append(self.total_carbon_emissions)
        self.history_behavioural_carbon_emissions.append(self.behavioural_carbon_emissions)

    def next_step(self, t: int, social_component: npt.NDArray):
        """
        Push the individual simulation forwards one time step. Update time, then behavioural values, attitudes and thresholds then calculate
        new identity of agent and save results.

        Parameters
        ----------
        t: float
            Internal time of the simulation
        social_component: npt.NDArray
            NxM Array of the influence of neighbours from imperfect social learning on behavioural attitudes of the individual
        Returns
        -------
        None
        """
        self.t = t

        self.update_values()
        self.update_attitudes(social_component)

        if self.alpha_change == "behavioural_independence":
            self.update_attitudes_matrix()
            self.attitudes_star = self.calc_attitudes_star()
        else:
            self.calc_av_behaviour()
            self.update_av_behaviour_list()
            self.culture = self.calc_culture()

        self.total_carbon_emissions, self.behavioural_carbon_emissions = self.calc_total_emissions()

        if (self.save_timeseries_data) and (self.t % self.compression_factor == 0):
            self.save_timeseries_data_individual()