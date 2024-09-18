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
        nrows=52,  # 52 units in set 3
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
        usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],  # uses all columns

    )
    
    return data

