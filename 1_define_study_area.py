# This script defines the study area for the project by selecting HUC12 watersheds
# that intersect with counties bordering the Mississippi River.
# It aggregates counties into qualitative regions and assigns each HUC12 to a region
# based on the largest area of intersection.

import geopandas as gpd
import rasterio
from utils.config import root_dir

# Configurations
raster_filepath = (
    root_dir + "data_input/das_population/Dasymetric_Population_CONUS_2010_V3.tif"
)
aoi_counties_filepath = root_dir + "results/aoi_county_boundaries.gpkg"
wbdhuc12_filepath = root_dir + "data_input/watershed_boundaries/WBD_National_GDB.gdb"
out_filepath = root_dir + "results/aoi_huc12_boundaries.gpkg"

# use the CRS of the gridded dataset (EPA population layer)
target_crs = rasterio.open(raster_filepath).crs
# initial study area - 126 counties that border Mississippi River, previously assigned to a Qualitative Region
aoi_counties = gpd.read_file(aoi_counties_filepath)
# aggregate to qualitative regions
aoi_regions = aoi_counties[["Region", "geometry"]].dissolve(by="Region").reset_index()
# read the national HUC12 data
wbdhuc12 = gpd.read_file(wbdhuc12_filepath, bbox=aoi_regions, engine="fiona")
# select WBD HUC12 that interect counties
wbdhuc12_selection = gpd.sjoin(
    wbdhuc12, aoi_regions.to_crs(wbdhuc12.crs), predicate="intersects"
)
# calculate intersection area for each combination of HUC12 and Region
aoi_regions = aoi_regions.to_crs(target_crs)
wbdhuc12_selection = wbdhuc12_selection.to_crs(target_crs)
wbdhuc12_selection["intersection_area"] = wbdhuc12_selection.apply(
    lambda x: sum(
        aoi_regions[aoi_regions["Region"] == x.Region]
        .geometry.intersection(x.geometry)
        .area
    ),
    axis=1,
)
# filter out duplicates - keep QR region assignment by highest captured area
final_selection = (
    wbdhuc12_selection.sort_values("intersection_area", ascending=False)
    .drop_duplicates("huc12")
    .sort_index()
)
print(f"Got {len(final_selection)} rows")
# keep only some columns
cols = ["huc12", "name", "areasqkm", "states", "geometry", "Region"]
final_selection = final_selection[cols].copy()
# save to a file
final_selection.to_file(out_filepath)
