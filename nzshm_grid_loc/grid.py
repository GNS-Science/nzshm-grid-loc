from typing import Any, Callable, Iterable, Union

import numpy as np
from geopandas import GeoDataFrame
from shapely.geometry import Point


class Grid:
    """
    An immutable collection of grid points.
    Iterating over a grid will result in shapely.geometry.Point objects.
    """

    step: float
    precision: int
    points: set = set()
    attributes: dict = {}

    def __init__(self, step: float, points: Union[set, list, Iterable], attributes: dict = {}):
        """
        Creates a Grid instance.
        :param step: the step distance
        :param points: either a set of lat/lon tuples or a sequence of Points
        """
        self.step = step
        self.precision = get_precision(step)
        self.attributes = attributes
        if not points:
            self.points = set()
        elif isinstance(points, set):
            self.points = points
        else:
            points = list(points)
            if isinstance(points[0], Point):
                self.points = set()
                for p in points:
                    self.points.add((p.x, p.y))
            elif isinstance(points[0], tuple):
                self.points = set(points)
            else:
                assert False

    @classmethod
    def for_bounds(cls, lat_min: float, lat_max: float, lon_min: float, lon_max: float, step: float) -> 'Grid':
        """
        Creates a new grid based on a bounding box.
        The grid is equidistant (in degrees, not km)
        :param lat_min: the minimum latitude
        :param lat_max: the maximum latitude
        :param lon_min: the minimum longitude
        :param lon_max: the maximum longitude
        :param step: distance between points in degrees
        :return: the grid
        """
        precision = get_precision(step)

        points = set()
        for lat in np.arange(lat_min, lat_max, step):
            for lon in np.arange(lon_min, lon_max, step):
                points.add((round(lon, precision), round(lat, precision)))

        return cls(step, points)

    @classmethod
    def for_polygon(cls, step: float, gdf: GeoDataFrame) -> 'Grid':
        """
        Creates a new grid with a gdf as the bounds.
        :param step: distance between grid points in degrees
        :param gdf: a GeoDataFrame with polygons
        :return: the grid
        """
        bounds = [int(value / step) * step for value in gdf.total_bounds]
        return cls.for_bounds(bounds[1], bounds[3] + step, bounds[0], bounds[2] + step, step).intersection(gdf)

    def __iter__(self):
        for p in sorted(self.points):
            yield Point(p[0], p[1])

    def __len__(self):
        return len(self.points)

    def add_neighbours(self) -> 'Grid':
        """
        Ensures that each grid point is surrounded by 8 grid neighbours.
        :return: the new grid
        """
        points = set()

        def add_point(lat: float, lon: float) -> None:
            points.add((round(lat, self.precision), round(lon, self.precision)))

        def neighbours(lat: float, lon: float) -> None:
            add_point(lat - self.step, lon + self.step)
            add_point(lat - self.step, lon)
            add_point(lat - self.step, lon - self.step)

            add_point(lat, lon + self.step)
            add_point(lat, lon)
            add_point(lat, lon - self.step)

            add_point(lat + self.step, lon + self.step)
            add_point(lat + self.step, lon)
            add_point(lat + self.step, lon - self.step)

        for point in self.points:
            neighbours(point[0], point[1])

        return Grid(self.step, points, self.attributes)

    def union(self, other: Union['Grid', GeoDataFrame]) -> 'Grid':
        """
        Creates a grid that is the union of this grid and the other grid.
        :param other: a grid
        :return: the new grid
        """
        if isinstance(other, GeoDataFrame):
            other = Grid.for_polygon(self.step, other)
        return Grid(self.step, self.points.union(other.points), {**self.attributes, **other.attributes})

    def intersection(self, other: Union['Grid', GeoDataFrame]) -> 'Grid':
        """
        Creates a grid that us the intersection of this grid and the other grid.
        :param other: a grid
        :return: the new grid
        """
        if isinstance(other, GeoDataFrame):
            return self.__clip(other, True)
        return Grid(self.step, self.points.intersection(other.points), self.attributes)

    def difference(self, other: Union['Grid', GeoDataFrame]) -> 'Grid':
        """
        Creates a grid that is the difference of this grid and the other grid.
        :param other: a grid
        :return: the new grid
        """
        if isinstance(other, GeoDataFrame):
            return self.__clip(other, False)
        return Grid(self.step, self.points.difference(other.points), self.attributes)

    def filter(self, fn: Callable[[Point], bool]) -> 'Grid':
        """
        Only keeps the points for which fn(point) is True.
        :param fn: the filter function
        :return: the new grid
        """
        return Grid(self.step, filter(fn, self), self.attributes)

    def __clip(self, gdf: GeoDataFrame, inside: bool) -> 'Grid':
        """
        Returns a new Grid with all points of this Grid that are inside gdf
        Implementation of intersection
        :param gdf: a GeoDataFrame of polygons
        :return: the clipped Grid
        """
        gs = gdf.geometry

        def predicate(p: Point) -> bool:
            for g in gs:
                if g.contains(p):
                    return inside
            return not inside

        return self.filter(predicate)

    def annotate(self, name: str, value: Any, clip: GeoDataFrame = None) -> 'Grid':
        """
        Adds an attribute with the specified name and value to each point.
        If clip is specified, only sets the attribute for points in the clip polygons.
        :param name: the name of the attribute
        :param value: the value of the attribute
        :param clip: optional clip polygons
        :return: a new grid with the new attribute
        """
        ps = self if clip is None else self.intersection(clip)
        attributes = dict(self.attributes)
        for p in ps:
            attrs = self.get_attributes(p)
            attrs[name] = value
            attributes[(p.x, p.y)] = attrs
        return Grid(self.step, list(self), attributes)

    def get_attributes(self, point: Union[tuple, Point]):
        """
        Returns a copy of a dictionary of all attributes for the specified point
        :param point: a point
        :return: a copy af the attributes dictionary
        """
        if isinstance(point, Point):
            point = (point.x, point.y)
        return dict(self.attributes.get(point, {}))


def get_precision(step: float) -> int:
    s = str(step)
    return len(s) - s.find('.') - 1
