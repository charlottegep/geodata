import numpy as np
import geopandas as gpd
import rasterio
import rasterio.plot
from pathlib import Path
from shapely.geometry import Point

from utils.db_utils import GeodataDB

DATASET_PATH = 'dataset/'
DATASET_PREFIX = 'H12482'


def extract_geotiff() -> gpd.GeoDataFrame:
    """
    Extract raw GeoTIFF data, translate x,y image grid coordinates to geographic coordinates, and retrieve the depth
    data from each point
    :return: a GeoDataFrame with the x,y image grid coordinates, the geographic coordinates (EPSG:32618),
    and the depth data for that point
    """
    with rasterio.open(Path(DATASET_PATH) / f'{DATASET_PREFIX}.tiff') as dataset:
        val = dataset.read(1)
        no_data = dataset.nodata
        geometry = [Point(dataset.xy(x, y)[0], dataset.xy(x, y)[1]) for x, y in np.ndindex(val.shape) if
                    val[x, y] != no_data]
        v = [val[x, y] for x, y in np.ndindex(val.shape) if val[x, y] != no_data]
        grid_points = [(x, y) for x, y in np.ndindex(val.shape)]

        gdf = gpd.GeoDataFrame({'grid points': grid_points, 'geometry': geometry, 'data': v})
        gdf.crs = dataset.crs

        return gdf


if __name__ == '__main__':
    result_gdf = extract_geotiff()
    result_gdf.to_csv('results.csv', index=False)

    db = GeodataDB()
    db.dataframe_to_table(result_gdf, DATASET_PREFIX)
