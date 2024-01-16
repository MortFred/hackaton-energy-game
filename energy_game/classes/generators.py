import os
import random

import numpy as np
import pandas as pd
from scipy.stats import norm

# convert units to SI - https://atb.nrel.gov/electricity/2022/index
USD_KWY = 10.42 / (1e3 * 365.25 * 24 * 3600)
USD_KW = 10.42 / (1e3)
GRAM_MWH = 0.001 / (1e6 * 3600)


class BaseGenerator:
    def __init__(
        self, installed_capacity, min_output, co2_opex, nok_opex, nok_capex, time_steps
    ):
        """
        Initialise values for sinusoidal generator
            Parameters:
                co2_opex (float, int): CO2e per unit energy [kg/J]
                nok_opex (float, int): NOK per unit energy [NOK/J]
                nok_capex (float, int): NOK per installed capacity [NOK/W]
                min_output (float): Proportion of available power that must be generated [-]
                time_steps (list[float]): Time range [hours]
        """
        # capcity constraints
        self.installed_capacity = installed_capacity
        self.min_output = min_output

        # cost rates
        self.co2_opex = co2_opex
        self.nok_opex = nok_opex
        self.nok_capex = nok_capex

        # time constants
        self.time_steps = time_steps

    def calculate_min_power_profile(self):
        """
        Calculate minimum power profile
        """
        self.min_power = {k: v * self.min_output for k, v in self.max_power.items()}

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
        power_total = sum(power) * time_step * 3600

        # total costs
        co2 = power_total * self.co2_opex
        nok = power_total * self.nok_opex + self.installed_capacity * self.nok_capex

        return co2, nok


class SolarGenerator(BaseGenerator):
    def __init__(
        self,
        time_steps,
        installed_capacity,
        co2_opex=41000 * GRAM_MWH,
        nok_opex=19 * USD_KWY,
        nok_capex=1784 * USD_KW,
        min_output=1.0,
        range_=12,
        peak_time=12,
    ):
        super().__init__(
            installed_capacity=installed_capacity,
            min_output=min_output,
            co2_opex=co2_opex,
            nok_opex=nok_opex,
            nok_capex=nok_capex,
            time_steps=time_steps,
        )
        """
        Initialise technology specific values
            Parameters:
                installed_capacity (float, int): Installed capacity [W]
                range_ (float, int): Duration of sunlight [mins]
                peak_time (float, int): Time of day that peak generation occurs [mins]
        """

        # technology specific constants
        self.range = range_
        self.peak_time = peak_time
        self.daily_capcity = np.random.uniform(0.6, 1, int(self.time_steps.max() / 24))

        # calculate values
        self.calculate_max_power_profile()
        self.calculate_min_power_profile()

    def calculate_max_power_profile(self):
        # calculate daily power profile
        max_power = np.zeros_like(self.time_steps)
        for day in range(int(self.time_steps.max() / 24)):
            day_power = norm.pdf(self.time_steps, (day + 0.5) * 24, self.range / 2 / 3)
            day_power = (
                day_power
                / day_power.max()
                * self.daily_capcity[day]
                * self.installed_capacity
            )
            max_power = max_power + day_power
        self.max_power = {k: v for k, v in zip(self.time_steps, max_power)}


class NuclearGenerator(BaseGenerator):
    def __init__(
        self,
        time_steps,
        installed_capacity,
        co2_opex=24000 * GRAM_MWH,
        nok_opex=(146 + 114) / 2 * USD_KWY,
        nok_capex=(7989 + 7442) / 2 * USD_KW,
        min_output=1.0,
    ):
        super().__init__(
            installed_capacity=installed_capacity,
            min_output=min_output,
            co2_opex=co2_opex,
            nok_opex=nok_opex,
            nok_capex=nok_capex,
            time_steps=time_steps,
        )
        """
        Initialise technology specific values
            Parameters:
                installed_capacity (float, int): Peak generation power output [W]
        """

        # calculate values
        self.calculate_max_power_profile()
        self.calculate_min_power_profile()

    def calculate_max_power_profile(self):
        # calculate daily power profile
        self.max_power = {}
        for t in self.time_steps:
            self.max_power[t] = self.installed_capacity


class WindGenerator(BaseGenerator):
    def __init__(
        self,
        time_steps,
        installed_capacity,
        co2_opex=11000 * GRAM_MWH,
        nok_opex=(116 + 75) / 2 * USD_KWY,
        nok_capex=(5908 + 3285) / 2 * USD_KW,
        min_output=1.0,
    ):
        super().__init__(
            installed_capacity=installed_capacity,
            min_output=min_output,
            co2_opex=co2_opex,
            nok_opex=nok_opex,
            nok_capex=nok_capex,
            time_steps=time_steps,
        )
        """
        Initialise technology specific values
            Parameters:
                installed_capacity (float, int): Peak generation power output [W]
        """

        # calculate values
        self.calculate_max_power_profile()
        self.calculate_min_power_profile()

    def calculate_max_power_profile(self, seed=1250):
        # set seed
        random.seed(seed)

        # laod data
        dir_path = os.path.dirname(os.path.realpath(__file__))
        wind = pd.read_csv(
            dir_path
            + "/../data/Solar_and_WindOnOffshore__watt_produced_per_watt_installed.csv"
        )
        offset = random.randrange(0, len(wind) - 168, 24)

        # calculate daily power profile
        self.max_power = (
            wind["offshoreWind"].iloc[offset + 0 : offset + 168]
            * self.installed_capacity
        ).to_dict()


class OilGenerator(BaseGenerator):
    def __init__(
        self,
        time_steps,
        installed_capacity,
        co2_opex=780_000 * GRAM_MWH,
        nok_opex=(141 + 74) / 2 * USD_KWY * 1.15,
        nok_capex=(5327 + 3075) / 2 * USD_KW * 1.15,
        min_output=0.1,
    ):
        super().__init__(
            installed_capacity=installed_capacity,
            min_output=min_output,
            co2_opex=co2_opex,
            nok_opex=nok_opex,
            nok_capex=nok_capex,
            time_steps=time_steps,
        )
        """
        Initialise technology specific values
            Parameters:
                installed_capacity (float, int): Peak generation power output [W]
        """

        # calculate values
        self.calculate_max_power_profile()
        self.calculate_min_power_profile()

    def calculate_max_power_profile(self):
        # calculate daily power profile
        self.max_power = {}
        for t in self.time_steps:
            self.max_power[t] = self.installed_capacity


class CoalGenerator(BaseGenerator):
    def __init__(
        self,
        time_steps,
        installed_capacity,
        co2_opex=980_000 * GRAM_MWH,
        nok_opex=(141 + 74) / 2 * USD_KWY,
        nok_capex=(5327 + 3075) / 2 * USD_KW,
        min_output=0.32,
    ):
        super().__init__(
            installed_capacity=installed_capacity,
            min_output=min_output,
            co2_opex=co2_opex,
            nok_opex=nok_opex,
            nok_capex=nok_capex,
            time_steps=time_steps,
        )
        """
        Initialise technology specific values
            Parameters:
                installed_capacity (float, int): Peak generation power output [W]
        """

        # calculate values
        self.calculate_max_power_profile()
        self.calculate_min_power_profile()

    def calculate_max_power_profile(self):
        # calculate daily power profile
        self.max_power = {}
        for t in self.time_steps:
            self.max_power[t] = self.installed_capacity


class GasGenerator(BaseGenerator):
    def __init__(
        self,
        time_steps,
        installed_capacity,
        co2_opex=430_000 * GRAM_MWH,
        nok_opex=(59 + 21) / 2 * USD_KWY,
        nok_capex=(2324 + 922) / 2 * USD_KW,
        min_output=0.35,
    ):
        super().__init__(
            installed_capacity=installed_capacity,
            min_output=min_output,
            co2_opex=co2_opex,
            nok_opex=nok_opex,
            nok_capex=nok_capex,
            time_steps=time_steps,
        )
        """
        Initialise technology specific values
            Parameters:
                installed_capacity (float, int): Peak generation power output [W]
        """

        # calculate values
        self.calculate_max_power_profile()
        self.calculate_min_power_profile()

    def calculate_max_power_profile(self):
        # calculate daily power profile
        self.max_power = {}
        for t in self.time_steps:
            self.max_power[t] = self.installed_capacity
