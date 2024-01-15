import math

class Generator:
    def init(self, const = 100, coef_sin = 100, coef_cos = 50, time = 0, time_delta = 10):
        # generation curve coefficients (sinusoidal variatiosn for now)
        self.const = const
        self.coef_sin = coef_sin
        self.coef_cos = coef_cos
        # time parameters
        self.time = time
        self.time_delta = time_delta

    def __call__(self):
        # calculate generation
        gen = self.const + self.coef_sin*math.sin((self.time/24*60)/(2*math.pi)) + self.coef_cos*math.cos((self.time/24*60)/(2*math.pi))

        # increment time
        self.time = self.time + self.time_delta

        return gen
