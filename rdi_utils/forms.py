import streamlit as st
import numpy as np
from rdi_utils.constants import states
import pandas as pd

column_round = np.vectorize(lambda x, digits: round(x, digits))


def pick_state():
    st.markdown("#### Choose a State")
    state = st.selectbox(
        "", states.values(), index=list(states.values()).index("Texas")
    )
    return state


def pick_year():
    st.markdown("#### Choose a Year")
    df = pd.read_csv("data/full_rdi_values.csv", usecols=["year"])
    ymin = max(2010, min(df.year))
    ymax = max(df.year)
    options = [ int(yr) for yr in range(int(ymin), int(ymax + 1)) ]
    year = st.selectbox("", options)
    return year


def pick_field():
    st.markdown("#### Choose a Field")
    ignored_cols = ['STATE', 'PUMA', 'year', 'MERGE_CODE', 'state_name', 'state_code']
    df = pd.read_csv("data/full_rdi_values.csv", nrows=0, usecols=lambda x: x not in ignored_cols)
    field = st.selectbox("", df.columns)
    st.warning("Insert description of what this means lol")
    return field
