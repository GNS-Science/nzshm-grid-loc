import pytest
from geopandas import GeoDataFrame
from shapely.geometry import Point, Polygon

from nzshm_grid_loc.grid import Grid

a = Point(1, 2)
b = Point(2, 3)
c = Point(3, 3)
d = Point(4, 5)

poly = Polygon([[3.5, 3.5], [5.5, 3.5], [5.5, 7.5], [3.5, 5.5]])
gdf = GeoDataFrame()
gdf.geometry = [poly]


def test_grid_create():
    grid_a = Grid(1, [a])
    grid_b = Grid(1, [(1, 2)])
    grid_c = Grid(1, {(1, 2)})
    with pytest.raises(AssertionError):
        Grid(1, [1, 2])
    assert [a] == list(grid_a)
    assert [a] == list(grid_b)
    assert [a] == list(grid_c)


def test_grid_union():
    grid_a = Grid(1, [a, b, c])
    grid_b = Grid(1, [b, c, d])
    result = grid_a.union(grid_b)
    assert [a, b, c, d] == list(result)
    assert [a, b, c] == list(grid_a)


def test_grid_union_gdf():
    grid_a = Grid(1, [a, b, c])
    grid_b = Grid.for_polygon(1, gdf)
    result = grid_a.union(gdf)
    assert list(grid_a.union(grid_b)) == list(result)


def test_grid_difference():
    grid_a = Grid(1, [a, b, c])
    grid_b = Grid(1, [b, c, d])
    result = grid_a.difference(grid_b)
    assert [a] == list(result)
    assert [a, b, c] == list(grid_a)


def test_grid_difference_poly():
    grid_a = Grid(1, [a, b, c, d])
    result = grid_a.difference(gdf)
    assert [a, b, c] == list(result)


def test_grid_intersection():
    grid_a = Grid(1, [a, b, c])
    grid_b = Grid(1, [b, c, d])
    result = grid_a.intersection(grid_b)
    assert [b, c] == list(result)
    assert [a, b, c] == list(grid_a)


def test_grid_intersection_poly():
    grid_a = Grid(1, [a, b, c, d])
    result = grid_a.intersection(gdf)
    assert [d] == list(result)


def test_grid_neighbours():
    grid = Grid(1, [c])
    n_1 = grid.add_neighbours()
    expected = [Point(x, y) for x, y in [[2, 2], [2, 3], [2, 4], [3, 2], [3, 3], [3, 4], [4, 2], [4, 3], [4, 4]]]
    assert expected == list(n_1)
    assert [c] == list(grid)

    grid = Grid(1, [Point(3, 3), Point(3, 4)])
    n_2 = grid.add_neighbours()
    expected = [
        Point(x, y)
        for x, y in [[2, 2], [2, 3], [2, 4], [2, 5], [3, 2], [3, 3], [3, 4], [3, 5], [4, 2], [4, 3], [4, 4], [4, 5]]
    ]
    assert expected == list(n_2)

    grid = Grid(1, [])
    n_3 = grid.add_neighbours()
    assert [] == list(n_3)


def test_grid_filter():
    grid = Grid(1, [a, b, c, d])
    grid_f = grid.filter(lambda p: (p.x + p.y) > 5)
    assert [c, d] == list(grid_f)
    assert [a, b, c, d] == list(grid)


def test_make_grid():
    grid = Grid.for_bounds(0, 2, 0, 2, 0.5)
    expected = [
        Point(x, y)
        for x, y in [
            (0.0, 0.0),
            (0.0, 0.5),
            (0.0, 1.0),
            (0.0, 1.5),
            (0.5, 0.0),
            (0.5, 0.5),
            (0.5, 1.0),
            (0.5, 1.5),
            (1.0, 0.0),
            (1.0, 0.5),
            (1.0, 1.0),
            (1.0, 1.5),
            (1.5, 0.0),
            (1.5, 0.5),
            (1.5, 1.0),
            (1.5, 1.5),
        ]
    ]
    assert expected == list(grid)


def test_make_grid_gdf():
    poly = Polygon([[5.5, 5.5], [7.5, 5.5], [7.5, 7.5], [5.5, 7.5]])
    gdf = GeoDataFrame()
    gdf.geometry = [poly]
    grid = Grid.for_polygon(1, gdf)
    expected = [Point(x, y) for x, y in [[6.0, 6.0], [6.0, 7.0], [7.0, 6.0], [7.0, 7.0]]]
    assert expected == list(grid)


def test_annotate():
    grid_a = Grid(1, [a, b, c, d]).annotate("a", 1)
    grid_b = grid_a.annotate("a", 2, clip=gdf)
    assert {"a": 1} == grid_b.get_attributes(a)
    assert {"a": 2} == grid_b.get_attributes(d)
    assert {"a": 2} == grid_b.get_attributes((d.x, d.y))
