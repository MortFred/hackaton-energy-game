import numpy as np
import pandas as pd

# from classes.generators import (
#     CoalGenerator,
#     GasGenerator,
#     NuclearGenerator,
#     OilGenerator,
#     SolarGenerator,
#     WindGenerator,
# )

# t = np.linspace(0, 24 * 7, 24 * 7)
# ENERGY_PRODUCERS = {
#     # "solar": SolarGenerator(time_steps=t, installed_capacity=100),
#     # "wind": WindGenerator(time_steps=t, installed_capacity=100),
#     "oil": OilGenerator(time_steps=t, installed_capacity=100),
#     "gas": GasGenerator(time_steps=t, installed_capacity=100),
#     "coal": CoalGenerator(time_steps=t, installed_capacity=100),
#     "nuclear": NuclearGenerator(time_steps=t, installed_capacity=100),
# }
# PRIORITY_LIST = ["nuclear", "solar", "hydro", "wind", "gas", "coal", "oil"]
# demand = pd.DataFrame({"t": t})
# demand["demand"] = 200


def calculate_production(ENERGY_PRODUCERS, df_demand, priority_list):
    t = np.linspace(0, 24 * 7, 24 * 7)
    df_prod = pd.DataFrame({"t": t})
    df_prod = df_prod.set_index("t")

    df_prod["total"] = 0
    for name, producer in ENERGY_PRODUCERS.items():
        df_prod[name] = producer.min_power.values()
        df_prod[name + "_max"] = producer.max_power.values()
        df_prod["total"] += list(producer.min_power.values())

    for name in priority_list:
        if name not in df_prod:
            continue
        for i, row in enumerate(df_demand["demand"]):
            missing_prod = row - df_prod["total"].iloc[i]
            if missing_prod > 0:
                delta = df_prod[name + "_max"].iloc[i] - df_prod[name].iloc[i]
                df_prod[name].iloc[i] += min(missing_prod, delta)
                df_prod["total"].iloc[i] += min(missing_prod, delta)

    remove_cols = [name + "_max" for name in priority_list if name in df_prod]
    remove_cols += ["total"]
    df_prod = df_prod.drop(axis=1, labels=remove_cols)
    print(df_prod)
    return df_prod


# calculate_production(ENERGY_PRODUCERS, demand, PRIORITY_LIST)

# solar_gen.nok_capex*solar_gen.installed_capacity + solar_gen.nok_opex*solar_total_produced:9.0f
# solar_gen.co2_opex*solar_total_produced:9.0f
