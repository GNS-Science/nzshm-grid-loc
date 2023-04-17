import os
import pathlib
from enum import Enum

from geopandas import GeoDataFrame

from nzshm_grid_loc.io import load_polygon_file

RESOURCES_FOLDER = pathlib.Path(pathlib.PurePath(os.path.realpath(__file__)).parent, 'resources')


class Regions(Enum):
    """
    Regions that can be used to create and manipulate grids.
    """

    # NZ = 'resources/nz-coastlines-and-islands-polygons-topo-150k.shp'
    NZ_SMALL = (
        str(RESOURCES_FOLDER) + '/small-nz.wkt.csv.zip'
    )  # based on nz-coastlines-and-islands-polygons-topo-150k from LINZ
    WLG = str(RESOURCES_FOLDER) + '/wellington.geojson'  # Oakley just made this as a test
    BACKARC = str(RESOURCES_FOLDER) + '/backarc.geojson'

    def load(self) -> GeoDataFrame:
        """
        Loads the GeoDataFrame associated with this region.
        :return: a GeoDataFrame
        """
        return load_polygon_file(self.value)
