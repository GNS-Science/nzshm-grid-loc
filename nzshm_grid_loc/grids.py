from typing import Callable, Union, Iterable

import numpy as np
from shapely.geometry import Point


class Grid:
    """
    An immutable collection of grid points.
    Iterating over a grid will result in shapely.geometry.Point objects.
    """
    step: float
    precision: int
    points_set = None
    points_iterable = None

    def __init__(self, step: float, points: Union[set, list, Iterable]):
        """
        Creates a Grid instance.
        :param step: the step distance
        :param points: either a set of lat/lon tuples or a sequence of Points
        """
        self.step = step
        self.precision = get_precision(step)
        if isinstance(points, set):
            self.points_set = points
        else:
            self.points_iterable = list(points)

    def __get_points_set(self) -> set:
        if self.points_set is None:
            self.points_set = set()
            for p in self.points_iterable:
                self.points_set.add((p.x, p.y))
        return self.points_set

    def __iter__(self):
        if self.points_iterable is None:
            for p in sorted(self.points_set):
                yield Point(p[0], p[1])
        else:
            for p in self.points_iterable:
                yield p

    def __len__(self):
        if self.points_set is None:
            return len(self.points_iterable)
        else:
            return len(self.points_set)

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

        if self.points_iterable is None:
            for point in self.points_set:
                neighbours(point[0], point[1])
        else:
            for point in self.points_iterable:
                neighbours(point.x, point.y)

        return Grid(self.step, points)

    def union(self, other: 'Grid') -> 'Grid':
        """
        Creates a grid that is the union of this grid and the other grid.
        :param other: a grid
        :return: the new grid
        """
        return Grid(self.step, self.__get_points_set().union(other.__get_points_set()))

    def intersection(self, other: 'Grid') -> 'Grid':
        """
        Creates a grid that us the intersection of this grid and the other grid.
        :param other: a grid
        :return: the new grid
        """
        return Grid(self.step, self.__get_points_set().intersection(other.__get_points_set()))

    def difference(self, other: 'Grid') -> 'Grid':
        """
        Creates a grid that is the difference of this grid and the other grid.
        :param other: a grid
        :return: the new grid
        """
        return Grid(self.step, self.__get_points_set().difference(other.__get_points_set()))

    def filter(self, fn: Callable[[Point], bool]) -> 'Grid':
        """
        Only keeps the points for which fn(point) is True.
        :param fn: the filter function
        :return: the new grid
        """
        return Grid(self.step, filter(fn, self))


def get_precision(step: float) -> int:
    s = str(step)
    return len(s) - s.find('.') - 1


def make_grid(lat_min: float, lat_max: float, lon_min: float, lon_max: float, step: float) -> Grid:
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

    return Grid(step, points)
