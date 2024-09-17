import os

import altair as alt
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

st.set_page_config(layout="wide", page_title="TFT Set 3 Dashboard", page_icon=":penguin:")

# LOAD DATA ONCE
@st.cache_resource
def load_data():
    path = "Set3Champions.csv"
    if not os.path.isfile(path):
        path = f"https://github.com/swooshoo/set3carousel{path}"

    data = pd.read_csv(
        path,
        nrows=100000,  # approx. 10% of data
        names=[
            "unit",
            "cost",
            "health",
            "armor",
            "magic_resist"
            "attack",
            "attack_range",
            "attack_speed",
            
        ],  # specify names directly since they don't change
        skiprows=1,  # don't read header since names specified directly
        usecols=[0, 1, 2],  # doesn't load last column, constant value "B02512"
        parse_dates=[
            "date/time"
        ],  # set as datetime instead of converting after the fact
    )

    return data