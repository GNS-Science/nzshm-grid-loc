from enum import Enum

from geopandas import GeoDataFrame
from shapely.geometry import Point
from typing import Callable
from nzshm_grid_loc.io import load_polygon_file


class Regions(Enum):
    """
    Regions that can be used to filter grids.
    """
    NZ = 'resources/nz-coastlines-and-islands-polygons-topo-150k.shp'
    NZ_SMALL = 'resources/small-nz.shp'
    WLG = 'resources/wellington.geojson'

    def load(self) -> GeoDataFrame:
        """
        Loads the GeoDataFrame associated with this region.
        :return: a GeoDataFrame
        """
        return load_polygon_file(self.value)

    def predicate(self) -> Callable[[Point], bool]:
        """
        Returns a predicate that can be used to filter grids.
        :return:
        """
        gs = self.load().geometry

        def is_in_nz(p: Point) -> bool:
            for g in gs:
                if g.contains(p):
                    return True
            return False

        return lambda p: is_in_nz(p)

