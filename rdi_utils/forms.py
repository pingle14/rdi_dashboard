import streamlit as st
from rdi_utils.constants import states
import pandas as pd
import logging


def pick_state():
    st.markdown("#### Choose a State")
    state = st.selectbox(
        "", states.values(), index=list(states.values()).index("Texas")
    )
    return state


def pick_year(ymin, ymax):
    st.markdown("#### Choose a Year")
    options = [int(yr) for yr in range(int(ymin), int(ymax + 1))]
    year = st.selectbox("", options)
    return year


def pick_field(metadata, meta_success):
    st.markdown("#### Choose a Field")
    ignored_cols = ["STATE", "PUMA", "year", "MERGE_CODE", "state_name", "state_code"]
    df = pd.read_csv(
        "data/full_rdi_values.csv", nrows=0, usecols=lambda x: x not in ignored_cols
    )
    field = st.selectbox("", df.columns)

    if meta_success:
        try:
            row = metadata[metadata["col_name"] == field].iloc[0]
            formatted_name = row[1]
            desc = row[2]
            st.warning(f"**{formatted_name}** (`{field}`) -- {desc}")
        except Exception as e:
            logging.info(f"pick_field Exception: Could not load metadata ...\n\t{e}")

    return field, formatted_name
