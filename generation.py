import math

class Generation:
    def __init__(self, const=100, range_=10, peak_time = 0, time_delta=10):
        # generation constants for sine shaped generation curve
        self.const = const
        self.range = range_
        self.peak_time = peak_time

        # time constants
        self.time_delta = time_delta

        # calculate daily profile
        self.power = {}
        for i in range(math.ceil(24*60/self.time_delta)+1):
            self.power[self.time_delta*i] = self.const+ self.range*math.cos((self.time_delta*i-self.peak_time)/(60*24)*(2*math.pi))

    def get_power(self, time=None):
        # calculate generation for current time
        return self.power[time] if time else self.power