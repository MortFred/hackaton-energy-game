import os
import random
import pandas as pd
from classes.generators import BaseGenerator


class WindGenerator(BaseGenerator):
    def __init__(
        self,
        co2_opex=100,
        nok_opex=100,
        nok_capex=100,
        min_output=1.0,
        time_delta=10,
        peak_value=100,
    ):
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

    def calculate_max_power_profile(self, seed=1250):
        # calculate daily power profile
        self.max_power = {}
        random.seed(seed)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        wind = pd.read_csv(
            dir_path
            + "/../data/Solar_and_WindOnOffshore__watt_produced_per_watt_installed.csv"
        )
        offset = random.randrange(0, len(wind) - 168, 24)

        self.max_power = (
            wind["offshoreWind"].iloc[offset + 0 : offset + 168] * self.peak_value
        )
