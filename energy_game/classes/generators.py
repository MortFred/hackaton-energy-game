import math

import numpy as np
from scipy.stats import norm


class BaseGenerator:
    def __init__(self, co2_opex, nok_opex, nok_capex, min_output, time_steps):
        """
        Initialise values for sinusoidal generator
            Parameters:
                co2_opex (float, int): CO2e per unit energy [kg/J]
                nok_opex (float, int): NOK per unit energy [NOK/J]
                nok_capex (float, int): NOK per installed capacity [NOK/W]
                min_output (float): Proportion of available power that must be generated [-]
                time_steps (list[float]): Time range [hours]
        """
        # time constants
        self.time_steps = time_steps

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
        time_step = list(set(np.diff(self.time_steps).round(8)))
        assert len(time_step) == 1
        time_step = time_step[0]
        power_total = sum(power)*time_step*3600

        # total costs
        co2 = power_total*self.co2_opex
        nok = power_total*self.nok_opex + self.nok_capex

        return co2, nok


class SolarGenerator(BaseGenerator):
    def __init__(self, time_steps, installed_capacity, co2_opex=100, nok_opex=100, nok_capex=100, min_output=1., range_ = 12, peak_time = 12):
        super().__init__(co2_opex=co2_opex, nok_opex=nok_opex, nok_capex=nok_capex, min_output=min_output, time_steps=time_steps)
        """
        Initialise technology specific values
            Parameters:
                installed_capacity (float, int): Installed capacity [W]
                range_ (float, int): Duration of sunlight [mins]
                peak_time (float, int): Time of day that peak generation occurs [mins]
        """

        # technology specific constants
        self.installed_capacity = installed_capacity
        self.range = range_
        self.peak_time = peak_time
        self.daily_capcity = np.random.uniform(0.6,1,int(self.time_steps.max()/24))

        # calculate values
        self.calculate_max_power_profile()
        self.calculate_min_power_profile()

    def calculate_max_power_profile(self):

        # calculate daily power profile
        max_power = np.zeros_like(self.time_steps)
        for day in range(int(self.time_steps.max()/24)):
            day_power = norm.pdf(self.time_steps, (day+0.5)*24, self.range/2/3)
            day_power = day_power/day_power.max()*self.daily_capcity[day]
            max_power = max_power + day_power
        self.max_power = {k:v for k,v in zip(self.time_steps, max_power)}

class NuclearGenerator(BaseGenerator):
    def __init__(self, time_steps, installed_capacity, co2_opex=100, nok_opex=100, nok_capex=100, min_output=1.):
        super().__init__(co2_opex=co2_opex, nok_opex=nok_opex, nok_capex=nok_capex, min_output=min_output, time_steps=time_steps)
        """
        Initialise technology specific values
            Parameters:
                installed_capacity (float, int): Peak generation power output [W]
                range_ (float, int): Duration of sunlight [mins]
                peak_time (float, int): Time of day that peak generation occurs [mins]
        """

        # technology specific constants
        self.installed_capacity = installed_capacity

        # calculate values
        self.calculate_max_power_profile()
        self.calculate_min_power_profile()

    def calculate_max_power_profile(self):
        # calculate daily power profile
        self.max_power = {}
        for t in self.time_steps:
            self.max_power[t] = self.installed_capacity