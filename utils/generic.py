import pandas as pd
import geopandas as gpd

def table_to_gdf(data, x, y, projection='epsg:4326'):
    # load data from a csv and convert DataFrame into GeoDataFrame
    # Check if input is a string (filepath) or DataFrame
    if isinstance(data, str):
        df = pd.read_csv(data)
    elif isinstance(data, pd.DataFrame):
        df = data.copy() # Copying prevents modifying the original df
    else:
        raise ValueError("The 'data' argument must be a filepath (string) or a pandas DataFrame.")
    # Convert to GeoDataFrame
    return gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df[x], df[y]),
        crs=projection
    )