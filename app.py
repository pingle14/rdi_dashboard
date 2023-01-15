import streamlit as st
import seaborn as sns
from PIL import Image
import plotly.express as px
import geopandas as gpd

from rdi_utils.constants import page_title
from rdi_utils.utils import display_header
from rdi_utils.data_io import load_shp_file

sns.set()

# Header
st.set_page_config(page_icon="🤘", page_title=page_title, layout="wide")
logo = Image.open("ut_logo.png")

m = st.markdown(
    """
    <style>
    div.stDownloadButton > button:first-child {
        background-color: #b07a05;
        color: white;
        height: 5em;
        width: 100%;
        border-radius:10px;
        border:3px
        font-size:16px;
        font-weight: bold;
        margin: auto;
        display: block;
    }

    div.stDownloadButton > button:hover {
        background:linear-gradient(to bottom, #b07a05 5%, #f7d499 100%);
        background-color:#b07a05;
    }

    div.stForm {
        .stFormSubmitButton > button:first-child {
            background-color: #b07a05;
            color: white;
            height: 5em;
            width: 100%;
            border-radius:10px;
            border:3px
            font-size:16px;
            font-weight: bold;
            margin: auto;
            display: block;
        }

        .stFormSubmitButton > button:hover {
            background:linear-gradient(to bottom, #b07a05 5%, #f7d499 100%);
            background-color:#b07a05;
        }
    }
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>""",
    unsafe_allow_html=True,
)

#################################################################################
#                                 SESSION STS                                   #
#################################################################################
if "chose_valid_option" not in st.session_state:
    st.session_state["chose_valid_option"] = False
# if "chose_valid_location" not in st.session_state:
#     st.session_state["chose_valid_location"] = False
# if "chose_valid_data_src" not in st.session_state:
#     st.session_state["chose_valid_data_src"] = False
# if "found_zipcodes" not in st.session_state:
#     st.session_state["found_zipcodes"] = False
# if "housing_data_availalbe" not in st.session_state:
#     st.session_state["housing_data_availalbe"] = False
# if "housing_shp_loaded" not in st.session_state:
#     st.session_state["housing_shp_loaded"] = False

#################################################################################
#                                 LAYOUT                                        #
#################################################################################
display_header(logo, page_title)

opt_map = "Map RDI/year across the US"
opt_timeline = "Visualize how RDI changes over time for each state"
opt_upload = "Upload your own data and get SHAP Values from our model"

option = None
with st.form("choose_option"):
    st.markdown("")
    st.subheader("What do you wish to explore?")
    option = st.radio("", options=[opt_map, opt_timeline, opt_upload])

    submitted = st.form_submit_button("Submit")
    if submitted:
        st.session_state["chose_valid_option"] = True

"---"


"""
TODO:
Split Features Dset bw pre + post 2010
Merge respective shp with features dsetstuff in jupyter notebook

Save this into gdf that i can load --> do this


"""


gdf = load_shp_file("us_pumas_2012_2019/us_pumas_2012_2019.shp")
# gdf = gdf[gdf.year == 2006]
fig = px.choropleth_mapbox(
    gdf,
    geojson=gdf.geometry,
    locations=gdf.index,
    # color=filtered_gdf[selected_median],
    color_continuous_scale="amp",
    # center={"lat": center_lat, "lon": center_lon},
    mapbox_style="open-street-map",
    # zoom=zoom_level,
    opacity=0.75,
    # title=colorbar_title,
)
fig.update_traces(marker_line_width=0.001, marker_line_color="black")
fig.update_layout(
    height=600,
    title_font_size=16,
    # title_text=plt_title,
    title_xanchor="center",
    title_x=0.5,
    title_yanchor="top",
    title_y=0.9,
    title_font_color="peachpuff",
    paper_bgcolor="black",
    # coloraxis_colorbar={
    #     "title": formatted_median_name,
    # },
)

st.plotly_chart(fig, use_container_width=True)


if st.session_state["chose_valid_option"]:
    st.subheader(option)
    if option == opt_map:
        "Put map stuff here ... Load Chungus d-set"
    elif option == opt_timeline:
        "Put timeline ... load condensed d-set"
    elif option == opt_upload:
        "put upload ... Load pickle"
