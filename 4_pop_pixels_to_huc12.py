# This script uses gridded population layers (rasters at 30-m resolution)
# and aggregate pixels to HUC12 units

import geopandas as gpd
import rasterio
from rasterstats import zonal_stats
from rasterstats.io import bounds_window
from utils.config import root_dir

# Configurations
huc12_filepath = root_dir + "results/aoi_huc12_boundaries.gpkg"
var_filepath = root_dir + "data_processed/MissRivStates_gridded_pop_{}_{}.tif"
out_filepath = root_dir + "results/huc12_demographics.csv"
study_periods = ["2008_2012", "2013_2017", "2018_2022"]
variables = [
    "total",
    "share_nonhsp_white",
    "share_black",
    "share_native",
    "share_asian",
    "share_hispanic",
    "share_below_poverty",
    "share_2_above_poverty",
]

# Load study area
huc12 = gpd.read_file(huc12_filepath)

for study_period in study_periods:
    print("\nProcessing", study_period)
    print("Computing zonal population statistics")
    # define crs and window of raster files
    with rasterio.open(var_filepath.format(study_period, "total")) as src:
        # this is defined to later read a subset of the raster file - it's faster than the entire raster
        window = bounds_window(huc12.total_bounds, src.transform)
        window_affine = src.window_transform(window)
    # process each variable
    for var in variables:
        print(var)
        src = rasterio.open(var_filepath.format(study_period, var))
        array = src.read(1, window=window)
        if var == "total":
            agg_stats = "sum"
        else:
            agg_stats = "mean"
        stats = zonal_stats(
            huc12, array, affine=window_affine, nodata=src.nodata, stats=[agg_stats]
        )
        huc12[f"{study_period}_{var}"] = [s[agg_stats] for s in stats]

# save results to a tabular format
# geometries can be dropped (will join to the boundaries file as needed)
huc12.drop(columns=["geometry"]).to_csv(out_filepath)
