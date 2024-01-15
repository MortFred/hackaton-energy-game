import streamlit as st
import pandas as pd

import numpy as np

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
    df = pd.DataFrame()
    df['coal'] = [coal] * 31
    df['gas'] = [gas] * 31
    df['oil'] = [oil] * 31
    df['nuclear'] = [nuclear] * 31
    df['solar'] = [solar] * 31
    df['wind'] = [wind] * 31
    df['hydro'] = [hydro] * 31
    df['wave'] = [wave] * 31
    df['tidal'] = [tidal] * 31

    df['_total'] = [coal + gas + oil + nuclear + solar + wind + hydro + wave + tidal] * 31

    st.line_chart(df)

demand_curve = get_demand_curve()

with st.empty():
    t, demand = get_demand_curve()
    df = pd.DataFrame({"t": t, "demand": demand})
    df["demand"] = np.nan
    df = df.set_index("t")
    for seconds in range(len(demand)):
        df["demand"].iloc[0:seconds] = demand[0:seconds]
        st.line_chart(df)
    st.write("✔️ 1 minute over!")
