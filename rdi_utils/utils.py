import streamlit as st
import io
import pandas as pd
import pickle
import shap
import xgboost as xgb
from rdi_utils.data_io import load_full_csv, convert_df
from rdi_utils.forms import pick_state, pick_year, pick_field
from rdi_utils.plots import plot_timeline, plot_colormap
from rdi_utils.constants import descriptions


#################################################################################
#                                   HEADER                                      #
#################################################################################
def display_header(logo, page_title):
    col0, col1 = st.columns([0.7, 0.3])
    with col0:
        st.markdown(
            """<style> .font {font-size:45px ; font-family: 'Cooper Black'; color: #FF9633;} </style>""",
            unsafe_allow_html=True,
        )
        st.markdown(f'<p class="font">{page_title}</p>', unsafe_allow_html=True)
    with col1:
        st.image(logo)

    st.markdown(f"> {descriptions['header']} ")


#################################################################################
#                                 Do MAPPS                                      #
#################################################################################
def do_maps(gdf):
    st.markdown(f"> {descriptions['map']} ")

    cols = st.columns([0.3, 0.7])
    metadata, meta_success = load_full_csv("data/rdi_metadata.csv")
    year = None
    field = None
    with cols[0]:
        # Pick Year
        df = pd.read_csv("data/full_rdi_values.csv", usecols=["year"])
        ymin = max(2010, min(df.year))
        ymax = max(df.year)
        year = pick_year(ymin, ymax)

        # Pick Color Col
        field, formatted_name = pick_field(metadata, meta_success)

        # Have download Button
        with open("data/full_rdi_values.csv") as f:
            st.download_button(
                label="Download Full RDI Values",
                data=f,
                file_name="full_rdi_values.csv",
                mime="text/csv",
            )

    with cols[1]:
        if year is not None and field is not None:
            plot_colormap(gdf, year, field, formatted_name)


#################################################################################
#                                 Do TIMELN                                     #
#################################################################################
def do_timeline():
    st.markdown(f"> {descriptions['timeline']} ")
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
    st.markdown(f"> {descriptions['model']} ")

    st.markdown("#### Upload a Input File")
    st.markdown("##### This [sample_csv](https://github.com/A-Good-System-for-Smart-Cities/rdi_dashboard/blob/main/data/sample_input.csv) exemplifies how the input file should look.")

    uploaded_file = st.file_uploader("")
    if uploaded_file is not None:
        ymin, ymax = 2005, 2019
        year = pick_year(ymin, ymax)
        model_path = f"models/xg_{year}.json"

        acsX, success = load_full_csv(uploaded_file)

        if(success):
            try:
                # Opens the given pickle file as a dict of xgobjects
                model = xgb.XGBRegressor()
                model.load_model(model_path)

                # User selects a year-range of interest (aka pre or post 2010)
                explainer = shap.TreeExplainer(model, acsX)
                shap_year = explainer.shap_values(acsX)

                shap_csv = convert_df(pd.DataFrame(shap_year))

                # Print prediction for every row in sample input (see above slack message)
                st.download_button(
                    label=f"Calculate and Download Predictions",
                    data=shap_csv,
                    file_name=f"{year}_shap_values.csv",
                    mime="text/csv",
                )
            except Exception as e:
                st.warning("Something went wrong with the file")

        else:
            st.warning("Something went wrong with the file")
