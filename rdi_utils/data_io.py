import streamlit as st
import pandas as pd
import logging
import geopandas as gpd
import numpy as np


def load_full_csv(path: str):
    df = None
    success = False
    try:
        df = pd.read_csv(path)
        success = True
    except Exception as e:
        logging.info(f"This data {path} is unavailable. {e}")
    return df, success


def load_shp_file(path):
    gdf = None
    try:
        gdf = gpd.read_file(path)
    except Exception as e:
        st.warning(f"Could not load shp file at {path}. {e}")
    return gdf
