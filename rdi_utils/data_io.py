import streamlit as st
import pandas as pd
import logging
import geopandas as gpd


def load_full_csv(path: str):
    df = None
    success = False
    try:
        df = pd.read_csv(path)
        success = True
    except Exception as e:
        logging.info(f"This data {path} is unavailable. {e}")
    return df, success


@st.cache(ttl=24 * 3600)
def load_shp_file(path):
    gdf = None
    try:
        gdf = gpd.read_file(path)
        gdf["STATE"] = gdf.apply(lambda row: int(row.STATEFP10), axis=1)
        gdf["PUMA"] = gdf.apply(lambda row: int(row.PUMACE10), axis=1)
        gdf["MERGE_CODE"] = gdf.apply(lambda row: f"{row.STATE}_{row.PUMA}", axis=1)
        gdf = gdf[["STATE", "PUMA", "MERGE_CODE", "geometry"]]
    except Exception as e:
        st.warning(f"Could not load shp file at {path}. {e}")
    return gdf


@st.cache(ttl=24 * 3600)
def convert_df(df, mode="csv"):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    if mode == "csv":
        return df.to_csv(index=False).encode("utf-8")
    elif mode == "pickle":
        return df.to_pickle()
    return None
