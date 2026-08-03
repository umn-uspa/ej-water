# This script disaggregates CBG-level data
# to 30-m pixels using EPA-produced dasymetric population layer

import geopandas as gpd
import rasterio
from rasterstats import zonal_stats
from rasterio import features
import numpy as np
import numpy.ma as ma
import rasterio.mask as rmask
from utils.config import root_dir
from utils.generic import gdf_bounds_to_box

# Configurations
raster_filepath = (
    root_dir + "data_input/das_population/Dasymetric_Population_CONUS_2010_V3.tif"
)
cbg_filepath = root_dir + "data_processed/NHGIS_cbg_MissRiv_{}.gpkg"
out_filepath = root_dir + "data_processed/MissRivStates_gridded_pop_{}_{}.tif"
study_periods = ["2008_2012", "2013_2017", "2018_2022"]
variables = [
    "total",
    "share_nonhsp_white",
    "share_black",
    "share_native",
    "share_asian",
    "share_hispanic",
    "share_below_poverty",
    "share_2_below_poverty",
    "share_2_above_poverty",
]


# Custom function for this script
def rasterize_demographics(gdf, var, study_period, epa_array, epa_transform, epa_dst):
    print(f"Processing {var}")
    if var == "total":
        gdf["scale_factor"] = gdf["total"] / gdf["EPA_total"]
        gdf["scale_factor"] = gdf["scale_factor"].fillna(0)
        geom_value = (
            (geom, value) for geom, value in zip(gdf.geometry, gdf["scale_factor"])
        )
    else:
        # create tuples of geometry-value pairs, where value is the attribute value that needs to be rasterized
        geom_value = ((geom, value) for geom, value in zip(gdf.geometry, gdf[var]))
    # rasterize vector features using the shape and transform of the raster
    rasterized = features.rasterize(
        geom_value,
        out_shape=(epa_array.shape[0], epa_array.shape[1]),
        transform=epa_transform,
        fill=epa_dst.nodata,
        all_touched=False,
    )
    if var == "total":
        # masking and scaling
        rasterized = np.where(epa_array == epa_dst.nodata, np.nan, rasterized)
        rasterized = ma.masked_equal(rasterized, epa_dst.nodata)
        rasterized = epa_array * rasterized
    else:
        # masking unpopulated
        rasterized = np.where(epa_array > 0, rasterized, np.nan)
        rasterized = ma.masked_equal(rasterized, epa_dst.nodata)
    print(f"Saving results")
    with rasterio.open(
        out_filepath.format(study_period, var),
        "w",
        compress="lzw",
        driver="GTiff",
        transform=epa_transform,
        dtype=rasterized.dtype,
        count=1,
        height=rasterized.shape[0],
        width=rasterized.shape[1],
        nodata=epa_dst.nodata,
        crs=epa_dst.crs,
        BIGTIFF="YES",
    ) as dst:
        dst.write(rasterized, indexes=1)


# Data processing starts here
for study_period in study_periods[:1]:
    print("\nProcessing", study_period)
    print("Load CBGs")
    gdf = gpd.read_file(cbg_filepath.format(study_period))
    print("Open and load EPA dasymetric raster")
    # open EPA dasymetric raster
    epa_dst = rasterio.open(raster_filepath)
    # prep spatial extent
    gdf = gdf.to_crs(epa_dst.crs)
    # create a bounding box shape from the total bounds
    bbox = gdf_bounds_to_box(gdf)
    # load array values ONLY within spatial extent of interest
    # (entire national array will take too long and is unnecessary)
    epa_array, epa_transform = rmask.mask(
        epa_dst, [bbox], crop=True, all_touched=False, indexes=1
    )
    print("Compute total population from the EPA at cbg level")
    stats = zonal_stats(
        gdf, epa_array, affine=epa_transform, nodata=epa_dst.nodata, stats=["sum"]
    )
    gdf["EPA_total"] = [s["sum"] for s in stats]
    print("Rasterizing demographic/socioeconomic characteristics")
    for var in variables[:1]:
        rasterize_demographics(
            gdf, var, study_period, epa_array, epa_transform, epa_dst
        )
