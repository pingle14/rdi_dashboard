import streamlit as st
import numpy as np
from rdi_utils.constants import states

column_round = np.vectorize(lambda x, digits: round(x, digits))


def pick_state():
    st.markdown("#### Choose a State")
    state = st.selectbox(
        "", states.values(), index=list(states.values()).index("Texas")
    )
    return state


def pick_field():
    pass
