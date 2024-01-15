import math

class BaseGenerator:
    def __init__(self, co2_rate=100, nok_rate=100, time_delta=10):
        """
        Initialise values for sinusoidal generator
            Parameters:
                    const (float, int): Baseline output across day [W]
                    range_ (float, int): Deviation either side of output across day [W]
                    peak_time (float, int): Time of day that peak generation occurs [mins]
                    time_delta (float, int): Time between increments [mins]
        """
        # time constants
        self.time_delta = time_delta

        # cost rates
        self.co2_rate = co2_rate
        self.nok_rate = nok_rate

    def get_power(self, time=None):
        """
        Return power generation for given time
            Parameters:
                    time (float, int) [Optional: default = None: Time of day [mins] . If None, return entire day.
            Returns:
                    power (float, dict): power generation at time provided or dict of time [mins] and generation values.
        """
        # return generation for current time
        power = self.power[time] if time else self.power
        return power
    

class SolarGenerator(BaseGenerator):
    def __init__(self, co2_rate=100, nok_rate=100, time_delta=10, const = 100, range_ = 10, peak_time = 4*60):
        super().__init__(co2_rate, nok_rate, time_delta)

        # technology specific constants
        self.const = const
        self.range = range_
        self.peak_time = peak_time

        # claculate power profile
        self.calculate_power_profile()

    def calculate_power_profile(self):
        # calculate daily profile
        self.power = {}
        for i in range(math.ceil(24*60/self.time_delta)+1):
            self.power[self.time_delta*i] = self.const+ self.range*math.cos((self.time_delta*i-self.peak_time)/(60*24)*(2*math.pi))