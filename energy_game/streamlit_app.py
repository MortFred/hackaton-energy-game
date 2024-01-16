import math
import streamlit as st
import pandas as pd
import altair as alt

import numpy as np
from classes.generators import SolarGenerator
from classes.wind_power import WindGenerator
from data.get_demand_curve import get_demand_curve

st.header("Energy Grid Game")

df_demand = get_demand_curve()
max_demand = max(df_demand["demand"])
coal = 0
gas = 0
nuclear = 0
solar = 0
wind = 0
hydro = 0


with st.sidebar:
    st.subheader("Energy Mix")
    coal = st.number_input("Coal (MW)", value=coal)
    gas = st.number_input("Gas (MW)", value=gas)
    nuclear = st.number_input("Nuclear (MW)", value=nuclear)
    solar = st.number_input("Solar (MW)", value=solar)
    wind = st.number_input("Wind (MW)", value=wind)
    hydro = st.number_input("Hydro (MW)", value=hydro, max_value=500)

    total_production = coal + gas + nuclear + solar + wind + hydro
    if total_production < math.ceil(max_demand):
        st.write(f"Installed Capacity: :red[{total_production}]/{max_demand:5.0f}")
    else:
        st.write(f"Installed Capacity: :green[{total_production}]/{max_demand:5.0f}")

    button_display = st.button("Run Simulation")

# if button_display:
df = pd.DataFrame()

demand = df_demand["demand"]
t = np.linspace(0, 24 * 7, 24 * 7)
df_prod = pd.DataFrame({"t": t})
solar_gen = SolarGenerator(time_steps=t, installed_capacity=solar)
wind_gen = WindGenerator(peak_value=wind)
generation_solar = list(solar_gen.max_power.values())
generation_wind = list(wind_gen.max_power)

df_demand = df_demand.set_index("t")
df_prod = df_prod.set_index("t")
df_prod["wind"] = wind
df_prod["solar"] = generation_solar

cont1 = st.container()
with cont1:
    col1, col2, col3 = st.columns(3)
cont2 = st.container()

solar_total_produced = sum(df_prod["solar"])
with col1:
    st.write(
        f"Price score: {solar_gen.nok_capex*solar_gen.installed_capacity + solar_gen.nok_opex*solar_total_produced:9.0f}"
    )
with col2:
    st.write(f"CO2 score: {solar_gen.co2_opex*solar_total_produced:9.0f}")
with col3:
    st.write(f"Stability score: {100}")

with st.empty():
    df_demand["demand"] = np.nan
    df_prod["solar"] = np.nan
    df_prod["wind"] = np.nan
    for hour in range(0, len(demand), 3):
        df_demand["demand"].iloc[0:hour] = list(demand)[0:hour]
        df_prod["solar"].iloc[0:hour] = generation_solar[0:hour]
        df_prod["wind"].iloc[0:hour] = generation_wind[0:hour]

        st.altair_chart(
            alt.layer(
                alt.Chart(
                    pd.melt(df_prod.reset_index(), id_vars=["t"]),
                    width=640,
                    height=480,
                )
                .mark_area()
                .encode(
                    alt.X("t", title=""),
                    alt.Y("value", title="", stack=True),
                    alt.Color("variable", title="", type="nominal"),
                    opacity={"value": 0.7},
                )
                .interactive(),
                alt.Chart(pd.melt(df_demand.reset_index(), id_vars=["t"]))
                .mark_line()
                .encode(
                    alt.X("t", title=""),
                    alt.Y("value", title="", stack=True),
                    alt.Color("variable", title="", type="nominal"),
                    opacity={"value": 0.7},
                )
                .interactive(),
            )
        )
