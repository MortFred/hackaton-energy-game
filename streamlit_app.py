import streamlit as st
import pandas as pd
import altair as alt

import numpy as np
from classes.generation import SolarGenerator

from data.get_demand_curve import get_demand_curve

st.header("hackathon-energy-game")

with st.sidebar:
    st.subheader("Initial game parameters")

    country = st.selectbox("Choose a country", ["Norway"])

    st.text("Energy sources:")
    coal = st.slider("Coal", 0, 100)
    gas = st.slider("Gas", 0, 100)
    oil = st.slider("Oil", 0, 100)
    nuclear = st.slider("Nuclear", 0, 100)
    solar = st.slider("Solar", 0, 100)
    wind = st.slider("Wind", 0, 100)
    hydro = st.slider("Hydro", 0, 100)
    wave = st.slider("Wave", 0, 100)
    tidal = st.slider("Tidal", 0, 100)

    button_display = st.button("Display curves")

if button_display:
    df = pd.DataFrame()

    df_demand = get_demand_curve()
    demand = df_demand["demand"]
    t = np.linspace(0, 24, 24 * 6)
    df_prod = pd.DataFrame({"t": t})
    generation_solar = list(SolarGenerator(peak_value=12000).power.values())

    df_demand = df_demand.set_index("t")
    df_prod = df_prod.set_index("t")
    df_prod["solar"] = generation_solar
    df_prod["generic"] = list(demand)

    with st.empty():
        df_demand["demand"] = np.nan
        df_prod["generic"] = np.nan
        df_prod["solar"] = np.nan
        for seconds in range(len(demand)):
            df_demand["demand"].iloc[0:seconds] = list(demand)[0:seconds]
            df_prod["generic"].iloc[0:seconds] = list(demand)[0:seconds]
            df_prod["solar"].iloc[0:seconds] = generation_solar[0:seconds]

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
