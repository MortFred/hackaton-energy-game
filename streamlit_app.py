# pip install streamlit
# streamlit run streamlit_app.py

import streamlit as st

st.header('hackaton-energy-game')

with st.sidebar:
    st.text('Initial game parameters')

    st.selectbox('Choose a country', ['Norway'])

    st.button('Display curves')