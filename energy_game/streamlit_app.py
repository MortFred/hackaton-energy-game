import math
import streamlit as st
import pandas as pd
import altair as alt

import numpy as np
from data.get_demand_curve import get_demand_curve
from calculate_production import calculate_cost_score, calculate_production
from classes.generators import (
    CoalGenerator,
    GasGenerator,
    NuclearGenerator,
    OilGenerator,
    SolarGenerator,
    WindGenerator,
)

st.header("Energy Grid Game")

df_demand = get_demand_curve()
max_demand = max(df_demand["demand"])
coal = 0
gas = 0
oil = 0
nuclear = 0
solar = 0
wind = 0
hydro = 0


with st.sidebar:
    st.subheader("Energy Mix")
    coal = st.number_input("Coal (MW)", value=coal)
    gas = st.number_input("Gas (MW)", value=gas)
    oil = st.number_input("Oil (MW)", value=oil)
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

demand = df_demand["demand"]
t = np.linspace(0, 24 * 7, 24 * 7)
df_prod = pd.DataFrame({"t": t})

ENERGY_PRODUCERS = {
    "solar": SolarGenerator(time_steps=t, installed_capacity=solar),
    "wind": WindGenerator(time_steps=t, installed_capacity=wind),
    "oil": OilGenerator(time_steps=t, installed_capacity=oil),
    "gas": GasGenerator(time_steps=t, installed_capacity=gas),
    "coal": CoalGenerator(time_steps=t, installed_capacity=coal),
    "nuclear": NuclearGenerator(time_steps=t, installed_capacity=nuclear),
}

PRIORITY_LIST = ["nuclear", "solar", "hydro", "wind", "gas", "coal", "oil"]

df_demand = df_demand.set_index("t")
df_prod = calculate_production(ENERGY_PRODUCERS, df_demand, PRIORITY_LIST)
co2, nok = calculate_cost_score(df_prod=df_prod, ENERGY_PRODUCERS=ENERGY_PRODUCERS)

cont1 = st.container()
with cont1:
    col1, col2, col3 = st.columns(3)
cont2 = st.container()

with col1:
    st.write(f"Price score: {nok:9.0f}")
with col2:
    st.write(f"CO2 score: {co2:9.0f}")
with col3:
    st.write(f"Stability score: {100}")

with st.empty():
    df_demand["demand"] = np.nan
    output = df_prod.copy()

    # output["nuclear"] = np.nan
    # output["oil"] = np.nan
    output["wind"] = np.nan
    output["solar"] = np.nan
    for hour in range(0, len(demand), 3):
        df_demand["demand"].iloc[0:hour] = list(demand)[0:hour]
        output["solar"].iloc[0:hour] = df_prod["solar"].iloc[0:hour]
        output["wind"].iloc[0:hour] = df_prod["wind"].iloc[0:hour]
        # output["oil"].iloc[0:hour] = df_prod["oil"].iloc[0:hour]
        # output["nuclear"].iloc[0:hour] = df_prod["nuclear"].iloc[0:hour]

        st.altair_chart(
            alt.layer(
                alt.Chart(
                    pd.melt(output.reset_index(), id_vars=["t"]),
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
