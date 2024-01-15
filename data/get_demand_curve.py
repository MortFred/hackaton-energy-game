
import pandas as pd
import numpy as np
import os 

def get_demand_curve():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    norway_data = pd.read_excel(dir_path + "/norway_demand.xlsx")

    t = np.linspace(0,24, 360)
    demand = np.interp(t, np.arange(0, 23), norway_data.iloc[:,2])
    # dp = np.polyfit(range(0, len(norway_data)), norway_data.iloc[:,2], 4)
    # print(dp)
    # demand = []
    # t = np.arange(len(norway_data))
    # demand = t**4*dp[0] + t**3*dp[1] + t**2*dp[2] + t*dp[3] + dp[4]


    # return pd.DataFrame(demand)
    return t, demand
print(get_demand_curve())
