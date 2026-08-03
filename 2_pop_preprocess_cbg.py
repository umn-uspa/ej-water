# In this script we select demographic/socioeconomic variables of interest
# pre-compute their shares of total population, and join attribute and spatial CBG-Level data

import os
import pandas as pd
import geopandas as gpd
from utils.config import root_dir

# Configurations
datadir = root_dir + f"data_input/cbg_demographics/"
out_filename = root_dir + "data_processed/NHGIS_cbg_MissRiv_{}.gpkg"
data_dictionary = {
    "2008_2012": {
        "boundary_filepath": "US_blck_grp_2012.shp",
        "table_filepath": "nhgis0058_ds191_20125_blck_grp.csv",
        "code_race": "QSQ",
        "code_ethnicity": "QSY",
        "code_poverty": "QUV",
    },
    "2013_2017": {
        "boundary_filepath": "US_blck_grp_2017.shp",
        "table_filepath": "nhgis0057_ds233_20175_blck_grp.csv",
        "code_race": "AHY2",
        "code_ethnicity": "AHZA",
        "code_poverty": "AH1J",
    },
    "2018_2022": {
        "boundary_filepath": "US_blck_grp_2022.shp",
        "table_filepath": "nhgis0056_ds262_20225_blck_grp.csv",
        "code_race": "AQNG",
        "code_ethnicity": "AQNO",
        "code_poverty": "AQPZ",
    },
}
# 10 states of interest - those intersect Mississippi River
state_ids = ["05", "17", "19", "21", "22", "27", "28", "29", "47", "55"]

# Data processing starts here
for study_period, metadata in data_dictionary.items():
    print("\nProcessing", study_period, metadata)
    boundary_filepath = metadata["boundary_filepath"]
    table_filepath = metadata["table_filepath"]
    CR = metadata["code_race"]
    CE = metadata["code_ethnicity"]
    CP = metadata["code_poverty"]
    # open national shapefile
    cbg_gdf = gpd.read_file(datadir + boundary_filepath)
    # select 10 states of interest
    cbg_gdf_selected = cbg_gdf[cbg_gdf["STATEFP"].isin(state_ids)]
    print(f"Count of all CBGs in the US: {len(cbg_gdf)}")
    print(f"Count of CBGs in the 10 states of interest: {len(cbg_gdf_selected)}")
    # open table
    cbg_table = pd.read_csv(datadir + table_filepath)
    print(f"CBG table records: {len(cbg_table)}")
    # perform join to combine spatial and attribute info
    joined = cbg_gdf_selected.merge(cbg_table, on="GISJOIN").copy()
    print(f"Count of CBGs in the study area after join: {len(joined)}")
    print("Compute race and ethnicity shares")
    shares = pd.DataFrame(
        {
            "total": joined[f"{CR}E001"],
            "share_black": joined[f"{CR}E003"] / joined[f"{CR}E001"],
            "share_native": joined[f"{CR}E004"] / joined[f"{CR}E001"],
            "share_asian": joined[f"{CR}E005"] / joined[f"{CR}E001"],
            "share_hispanic": joined[f"{CE}E012"] / joined[f"{CE}E001"],
            "share_nonhsp_white": joined[f"{CE}E003"] / joined[f"{CE}E001"],
            "share_2_above_poverty": joined[f"{CP}E008"] / joined[f"{CP}E001"],
            "share_below_poverty": (joined[f"{CP}E002"] + joined[f"{CP}E003"])
            / joined[f"{CP}E001"],
        },
        index=joined.index,
    )
    joined = pd.concat([joined, shares], axis=1).copy()
    print("Saving to a file")
    joined.to_file(out_filename.format(study_period))
