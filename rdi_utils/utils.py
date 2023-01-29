import streamlit as st
import io
import pandas as pd
import pickle
import shap
import xgboost

from rdi_utils.data_io import load_full_csv
from rdi_utils.forms import pick_state, pick_year, pick_field
from rdi_utils.plots import plot_timeline, plot_colormap

# import io
# import plotly.express as px
# import datetime as dt



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
#                                 Do MAPPS                                      #
#################################################################################
def do_maps(gdf):
    cols = st.columns([0.3, 0.7])
    year = None
    field = None
    with cols[0]:
        # Pick Year
        year = pick_year()

        # Pick Color Col
        field = pick_field()

        # Have download Button
        with open("data/full_rdi_values.csv") as f:
            st.download_button(
                label="Download Full RDI Values",
                data=f,
                file_name="full_rdi_values.csv",
                mime="text/csv",
            )



    with cols[1]:
        if year != None and field != None:
            plot_colormap(gdf, year, field)




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

#################################################################################
#                                 Do Model                                      #
#################################################################################
def do_model():
    model_sfxs = {'Model for 2005 - 2009':'2005', 'Model for 2010 - 2019':'2012'}

    st.markdown("#### Choose a Input File")
    uploaded_file = st.file_uploader("")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(df)

        # Opens the given pickle file as a dict of xgobjects
        pickle_dict = open('models/xg_mdl_w_shap_1_18_23.pkl', 'rb')
        pickle_dict = pickle.load(pickle_dict)

        # User selects a year-range of interest (aka pre or post 2010)
        st.markdown("#### Choose a Model")
        model_option = st.radio("", options = model_sfxs.keys())

        # Based on year-range, choose appropriate model and explainer object
        classifier = pickle_dict[f'mdl{model_sfxs[model_option]}']
        st.text(classifier)

        explainer = pickle_dict[f'exp{model_sfxs[model_option]}']

        # Print prediction for every row in sample input (see above slack message)
        # if st.button("Predict"):
        #     for i, row in df.iterrows():
        #         prediction = classifier.predict(row)
        #         print(prediction)

        #
        #     results = []
        #     for i, row in df.iterrows():
        #         prediction = classifier.predict([row])
        #         print(prediction)
