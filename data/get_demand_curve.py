
import pandas as pd
import numpy as np
import os 

def get_demand_curve():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    norway_data = pd.read_excel(dir_path + "/norway_demand.xlsx")

    t = np.linspace(0,24, 24*6)
    demand = np.interp(t, np.arange(0, 23), norway_data.iloc[:,2])

    return pd.DataFrame({"t": t, "demand": demand})
    
