import math
import numpy as np
import pandas as pd

from scipy.stats import norm

class BaseGenerator:
    def __init__(self, co2_rate=100, nok_rate=100, time_delta=10):
        """
        Initialise values for sinusoidal generator
            Parameters:
                    co2_rate (float, int): CO2e per unit energy [kg/J]
                    nok_rate (float, int): NOK per unit energy [NOK/J]
                    time_delta (float, int): Time between increments [mins]
        """
        # time constants
        self.time_delta = time_delta

        # cost rates
        self.co2_rate = co2_rate
        self.nok_rate = nok_rate

    def calculate_costs(self):
        # calculate finanical and emissions costs
        power_total = sum(self.power.values())*self.time_delta*60
        self.co2 = power_total*self.co2_rate
        self.nok = power_total*self.nok_rate
    

class SolarGenerator(BaseGenerator):
    def __init__(self, co2_rate=100, nok_rate=100, time_delta=10, peak_value = 100, range_ = 12*60, peak_time = 12*60):
        super().__init__(co2_rate, nok_rate, time_delta)
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

        # claculate values
        self.calculate_power_profile()
        self.calculate_costs()

    def calculate_power_profile(self):
        # calculate daily power profile
        self.power = {}
        for i in range(math.ceil(24*60/self.time_delta)+1):
            self.power[self.time_delta*i] = norm.pdf(self.time_delta*i, 12*60, self.range/2/3)
        self.power = {k:v/max(self.power.values())*self.peak_value for k,v in self.power.items()}

class NuclearGenerator(BaseGenerator):
    def __init__(self, co2_rate=100, nok_rate=100, time_delta=10, peak_value = 100):
        super().__init__(co2_rate, nok_rate, time_delta)
        """
        Initialise technology specific values
            Parameters:
                    peak_value (float, int): Peak generation power output [W]
                    range_ (float, int): Duration of sunlight [mins]
                    peak_time (float, int): Time of day that peak generation occurs [mins]
        """

        # technology specific constants
        self.peak_value = peak_value

        # claculate values
        self.calculate_power_profile()
        self.calculate_costs()

    def calculate_power_profile(self):
        # calculate daily power profile
        self.power = {}
        for i in range(math.ceil(24*60/self.time_delta)+1):
            self.power[self.time_delta*i] = self.peak_value