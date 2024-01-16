import numpy as np
import pandas as pd

from classes.generators import (
    OilGenerator,
    SolarGenerator,
    WindGenerator,
    NuclearGenerator,
)


def calculate_production(solar=1, wind=1, nuclear=1, oil=1):
    t = np.linspace(0, 24 * 7, 24 * 7)
    df_prod = pd.DataFrame({"t": t})
    solar_gen = SolarGenerator(time_steps=t, installed_capacity=solar)
    wind_gen = WindGenerator(time_steps=t, installed_capacity=wind)
    nuc_gen = NuclearGenerator(time_steps=t, installed_capacity=nuclear)
    oil_gen = OilGenerator(time_steps=t, installed_capacity=oil)
    df_prod = df_prod.set_index("t")
    df_prod["nuclear"] = pd.Series(nuc_gen.min_power)
    df_prod["oil"] = pd.Series(oil_gen.min_power)
    df_prod["solar"] = pd.Series(solar_gen.min_power)
    df_prod["wind"] = pd.Series(wind_gen.min_power)

    return df_prod


print(calculate_production(100, 100, 100, 100))
# solar_gen.nok_capex*solar_gen.installed_capacity + solar_gen.nok_opex*solar_total_produced:9.0f
# solar_gen.co2_opex*solar_total_produced:9.0f
