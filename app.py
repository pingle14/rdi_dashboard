import streamlit as st
import seaborn as sns
from PIL import Image

from rdi_utils.constants import page_title
from rdi_utils.utils import display_header, do_maps, do_timeline, do_model
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
    option = st.radio("", options=[opt_map, opt_timeline])  # opt_upload

    submitted = st.form_submit_button("Submit")
    if submitted:
        st.session_state["chose_valid_option"] = True

"---"


if st.session_state["chose_valid_option"]:
    st.subheader(option)
    if option == opt_map:
        gdf = load_shp_file("us_pumas_2012_2019/us_pumas_2012_2019.shp")
        do_maps(gdf)

    elif option == opt_timeline:
        do_timeline()

    elif option == opt_upload:
        do_model()
