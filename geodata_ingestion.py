import numpy as np
import geopandas as gpd
import rasterio
import rasterio.plot
from pathlib import Path
from shapely.geometry import Point


DATASET_PATH = 'dataset/'
DATASET_PREFIX = 'H12482'


def extract_geotiff():
    with rasterio.open(Path(DATASET_PATH) / f'{DATASET_PREFIX}.tiff') as dataset:
        val = dataset.read(1)
        no_data = dataset.nodata
        geometry = [Point(dataset.xy(x, y)[0], dataset.xy(x, y)[1]) for x, y in np.ndindex(val.shape) if
                    val[x, y] != no_data]
        v = [val[x, y] for x, y in np.ndindex(val.shape) if val[x, y] != no_data]
        grid_points = [[x, y] for x, y in np.ndindex(val.shape)]

        df = gpd.GeoDataFrame({'grid points': grid_points, 'geometry': geometry, 'data': v})
        df.crs = dataset.crs

        return df


if __name__ == '__main__':
    results = extract_geotiff()
    results.to_csv('results.csv', index=False)
    results.to_file('points.shp', driver='ESRI Shapefile')
