import streamlit as st
import io

from rdi_utils.data_io import load_full_csv
from rdi_utils.forms import pick_state
from rdi_utils.plots import plot_timeline

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
#                                 Do TIMELN                                     #
#################################################################################
def do_timeline():
    timeline_df, success = load_full_csv("data/timeline_df.csv")
    if success:
        cols = st.columns([0.3, 0.7])
        state = None
        with cols[0]:
            state = pick_state()

            with open("data/timeline_df.csv") as f:
                st.download_button(
                    label="Download RDI Quantiles",
                    data=f,
                    file_name="rdi_full_timeline.csv",
                    mime="text/csv",
                )

            with cols[1]:
                fig, plt_title = plot_timeline(timeline_df, state)
                st.plotly_chart(fig, use_container_width=True)

                # Download Plot as HTML
                buffer = io.StringIO()
                fig.write_html(buffer, include_plotlyjs="cdn")
                html_bytes = buffer.getvalue().encode()

                st.download_button(
                    label=f"Download Plot ({plt_title}) as HTML",
                    data=html_bytes,
                    file_name=f"{plt_title}.html",
                    mime="text/html",
                )

    else:
        st.error("Timeline File Failed to Load")
