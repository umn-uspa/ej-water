# This script aggregates RSEI flowline data to HUC12 subwatersheds for specified study periods.

import geopandas as gpd
from utils.rsei_utils import aggregate_RSEI
from utils.config import root_dir

# Configurations
huc12_filepath = root_dir + "results/aoi_huc12_boundaries.gpkg"
out_filepath = root_dir + "results/huc12_rsei_toxconc_weighted.csv"
study_periods = ["2008_2012", "2013_2017", "2018_2022"]
target_crs = "EPSG:5070"

# Load study area
huc12 = gpd.read_file(huc12_filepath)
huc12 = huc12.to_crs(target_crs)

for study_period in study_periods:
    print("\nProcessing", study_period)
    years = list(
        range(int(study_period.split("_")[0]), int(study_period.split("_")[1]) + 1)
    )
    print(years)
    # aggregate rsei to 5-year period
    # this sums up on-site and off-site and averages over years in the study period
    print("Aggregate RSEI flowlines to study period and to HUC12 units")
    flowlines = aggregate_RSEI(years, selection_aoi=huc12, universe="core01")
    # Ensure both GDFs are in the same projected CRS (EPSG:5070)
    # This is critical for accurate length calculations in meters
    flowlines = flowlines.to_crs(target_crs)
    # Intersect the two layers
    # This 'cuts' the flowlines at the polygon boundaries and
    # attaches the polygon's unique ID (e.g., 'huc12') to each line segment.
    intersected = gpd.overlay(flowlines, huc12, how="intersection")
    # Calculate the length of the clipped river segments
    intersected["length"] = intersected.geometry.length
    # Calculate weighted concentrations (Concentration * Segment Length)
    intersected["TOXCONC_weighed"] = intersected["TOXCONC"] * intersected["length"]
    # Aggregate the data by the huc12 id
    # We need the sum of the weighted values and the sum of lengths for each polygon.
    grouped = intersected.groupby("huc12").agg(
        {"TOXCONC_weighed": "sum", "length": "sum"}
    )
    # Calculate the final length-weighted average
    grouped[f"{study_period}_TOXCONC"] = grouped["TOXCONC_weighed"] / grouped["length"]
    # Bring the results back to your original Polygons GeoDataFram
    huc12[f"{study_period}_TOXCONC"] = huc12["huc12"].map(
        grouped[f"{study_period}_TOXCONC"]
    )


# save results to a tabular format
# geometries can be dropped (will join to the boundaries file as needed)
huc12.drop(columns=["geometry"]).to_csv(out_filepath)
