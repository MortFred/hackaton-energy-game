import numpy as np
import pandas as pd

from classes.generators import SolarGenerator, WindGenerator, NuclearGenerator


def calculate_production(solar=1, wind=1):
    t = np.linspace(0, 24 * 7, 24 * 7)
    df_prod = pd.DataFrame({"t": t})
    solar_gen = SolarGenerator(time_steps=t, installed_capacity=solar)
    wind_gen = WindGenerator(peak_value=wind)
    generation_solar = list(solar_gen.max_power.values())
    generation_wind = list(wind_gen.max_power.values())
    df_prod = df_prod.set_index("t")
    df_prod["wind"] = generation_wind
    df_prod["solar"] = generation_solar

    return df_prod


# solar_gen.nok_capex*solar_gen.installed_capacity + solar_gen.nok_opex*solar_total_produced:9.0f
# solar_gen.co2_opex*solar_total_produced:9.0f
