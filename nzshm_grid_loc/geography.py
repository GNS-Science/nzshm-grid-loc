from enum import Enum

from geopandas import GeoDataFrame

from nzshm_grid_loc.io import load_polygon_file


class Regions(Enum):
    """
    Regions that can be used to create and manipulate grids.
    """

    # NZ = 'resources/nz-coastlines-and-islands-polygons-topo-150k.shp'
    NZ_SMALL = 'resources/small-nz.wkt.csv.zip'  # based on nz-coastlines-and-islands-polygons-topo-150k from LINZ
    WLG = 'resources/wellington.geojson'  # Oakley just made this as a test
    BACKARC = 'resources/backarc.geojson'

    def load(self) -> GeoDataFrame:
        """
        Loads the GeoDataFrame associated with this region.
        :return: a GeoDataFrame
        """
        return load_polygon_file(self.value)
