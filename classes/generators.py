import math

from scipy.stats import norm


class BaseGenerator:
    def __init__(self, co2_opex=100, nok_opex=100, nok_capex=100, min_output=1., time_delta=10):
        """
        Initialise values for sinusoidal generator
            Parameters:
                co2_opex (float, int): CO2e per unit energy [kg/J]
                nok_opex (float, int): NOK per unit energy [NOK/J]
                nok_capex (float, int): NOK per installed capacity [NOK/W]
                min_output (float): Proportion of available power that must be generated [-]
                time_delta (float, int): Time between increments [mins]
        """
        # time constants
        self.time_delta = time_delta

        # capcity constraints
        self.min_output = min_output

        # cost rates
        self.co2_opex = co2_opex
        self.nok_opex = nok_opex
        self.nok_capex = nok_capex


    def calculate_min_power_profile(self):
        """
        Calculate minimum power profile
        """
        self.min_power = {k:v*self.min_output for k,v in self.max_power.items()}
    

    def calculate_costs(self, power):
        """
        Calculate finanical and emissions costs
            Parameters:
                power (list[float]): power generated for each time increment [W]
            Returns:
                co2 (float): total CO2e generated [kg]
                nok (float): total NOK spent [NOK]
        """
        # total power generated
        power_total = sum(power)*self.time_delta*60

        # total costs
        co2 = power_total*self.co2_opex
        nok = power_total*self.nok_opex + self.nok_capex

        return co2, nok


class SolarGenerator(BaseGenerator):
    def __init__(self, co2_opex=100, nok_opex=100, nok_capex=100, min_output=1., time_delta=10, peak_value = 100, range_ = 12*60, peak_time = 12*60):
        super().__init__(co2_opex, nok_opex, nok_capex, min_output, time_delta)
        """
        Initialise technology specific values
            Parameters:
                peak_value (float, int): Peak generation power output [W]
                range_ (float, int): Duration of sunlight [mins]
                peak_time (float, int): Time of day that peak generation occurs [mins]
        """

        # technology specific constants
        self.peak_value = peak_value
        self.range = range_
        self.peak_time = peak_time

        # calculate values
        self.calculate_max_power_profile()
        self.calculate_min_power_profile()

    def calculate_max_power_profile(self):
        # calculate daily power profile
        self.max_power = {}
        for i in range(math.ceil(24*60/self.time_delta)+1):
            self.max_power[self.time_delta*i] = norm.pdf(self.time_delta*i, 12*60, self.range/2/3)
        self.max_power = {k:v/max(self.max_power.values())*self.peak_value for k,v in self.max_power.items()}

class NuclearGenerator(BaseGenerator):
    def __init__(self, co2_opex=100, nok_opex=100, nok_capex=100, min_output=1., time_delta=10, peak_value = 100):
        super().__init__(co2_opex, nok_opex, nok_capex, min_output, time_delta)
        """
        Initialise technology specific values
            Parameters:
                peak_value (float, int): Peak generation power output [W]
                range_ (float, int): Duration of sunlight [mins]
                peak_time (float, int): Time of day that peak generation occurs [mins]
        """

        # technology specific constants
        self.peak_value = peak_value

        # calculate values
        self.calculate_max_power_profile()
        self.calculate_min_power_profile()

    def calculate_max_power_profile(self):
        # calculate daily power profile
        self.max_power = {}
        for i in range(math.ceil(24*60/self.time_delta)+1):
            self.max_power[self.time_delta*i] = self.peak_value