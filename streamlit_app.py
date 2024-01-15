import streamlit as st
import pandas as pd
from generation import Generation
import altair as alt

import numpy as np
from classes.generation import Generation

from data.get_demand_curve import get_demand_curve

st.header('hackathon-energy-game')

with st.sidebar:
    st.subheader('Initial game parameters')

    country = st.selectbox('Choose a country', ['Norway'])

    st.text('Energy sources:')
    coal = st.slider('Coal', 0, 100)
    gas = st.slider('Gas', 0, 100)
    oil = st.slider('Oil', 0, 100)
    nuclear = st.slider('Nuclear', 0, 100)
    solar = st.slider('Solar', 0, 100)
    wind = st.slider('Wind', 0, 100)
    hydro = st.slider('Hydro', 0, 100)
    wave = st.slider('Wave', 0, 100)
    tidal = st.slider('Tidal', 0, 100)

    button_display = st.button('Display curves')

if button_display:
    days = 145
    df = pd.DataFrame()
    df['coal'] = [coal] * days
    df['gas'] = [gas] * days
    df['oil'] = [oil] * days
    df['nuclear'] = [nuclear] * days
    df['solar'] = [solar] * days
    df['wind'] = [wind] * days
    df['hydro'] = [hydro] * days
    df['wave'] = [wave] * days
    df['tidal'] = [tidal] * days

    df['_total'] = [coal + gas + oil + nuclear + solar + wind + hydro + wave + tidal] * days

    generation_coal = Generation(range_=0).get_power()
    generation_gas = Generation(range_=10).get_power()
    generation_oil = Generation(range_=20).get_power()
    generation_nuclear = Generation(range_=30).get_power()
    generation_solar = Generation(range_=40).get_power()
    generation_wind = Generation(range_=50).get_power()
    generation_hydro = Generation(range_=60).get_power()
    generation_wave = Generation(range_=70).get_power()
    generation_tidal = Generation(range_=80).get_power()

    df['labels'] = [int(k)/10 for k in generation_coal.keys()]

    df['demand_coal'] = generation_coal.values()
    df['demand_gas'] = generation_gas.values()
    df['demand_oil'] = generation_oil.values()
    df['demand_nuclear'] = generation_nuclear.values()
    df['demand_solar'] = generation_solar.values()
    df['demand_wind'] = generation_wind.values()
    df['demand_hydro'] = generation_hydro.values()
    df['demand_wave'] = generation_wave.values()
    df['demand_tidal'] = generation_tidal.values()

    df = df.set_index('labels')

    st.altair_chart(
        alt.Chart(
            pd.melt(
                df.reset_index(),
                id_vars=["labels"]
            ),
                width=640, height=480
        )
        .mark_area()
        .encode(
            alt.X("labels", title=""),
            alt.Y("value", title="", stack=True),
            alt.Color("variable", title="", type="nominal"),
            opacity={"value": 0.7},
            # tooltip=["index", "value", "variable"]
        ).interactive()
    )


demand_curve = get_demand_curve()
gen = Generation()

with st.empty():
    df = get_demand_curve()
    df_gen = gen.get_power()
    demand = df["demand"]
    generation = df_gen["power"]
    df["demand"] = np.nan
    df["generation"] = np.nan
    df = df.set_index("t")
    df_gen = df_gen.set_index("t")
    for seconds in range(len(demand)):
        df["demand"].iloc[0:seconds] = demand[0:seconds]
        df["generation"].iloc[0:seconds] = generation[0:seconds]
        st.line_chart(df, df_gen)
    st.write("✔️ 1 minute over!")
