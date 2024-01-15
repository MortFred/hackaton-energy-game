# pip install streamlit
# streamlit run streamlit_app.py

import streamlit as st

st.header('hackaton-energy-game')

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

    st.button('Display curves')