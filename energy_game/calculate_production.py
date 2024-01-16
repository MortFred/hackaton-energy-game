import numpy as np
import pandas as pd


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
    return df_prod


def calculate_cost_score(df_prod, ENERGY_PRODUCERS):
    nok = 0
    co2 = 0
    for key, producer in ENERGY_PRODUCERS.items():
        nok += producer.calculate_costs(df_prod[key])[0]
        co2 += producer.calculate_costs(df_prod[key])[1]

    return nok, co2
