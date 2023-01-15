import streamlit as st

# import io
# import plotly.express as px
# import datetime as dt
# import pandas as pd


#################################################################################
#                                   HEADER                                      #
#################################################################################
def display_header(logo, page_title):
    col0, col1 = st.columns([0.7, 0.3])
    with col0:
        st.markdown(
            """<style> .font {font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} </style>""",
            unsafe_allow_html=True,
        )
        st.markdown('<p class="font">Urban Information Lab</p>', unsafe_allow_html=True)
    with col1:
        st.image(logo)

    st.header(page_title)
    st.markdown("> Insert Description Here")


#################################################################################
#                                 LOAD MAP                                      #
#################################################################################
