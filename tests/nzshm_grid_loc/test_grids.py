import pytest
from shapely.geometry import Point

from nzshm_grid_loc.grids import Grid, make_grid

a = Point(1, 2)
b = Point(2, 3)
c = Point(3, 3)
d = Point(4, 5)


def test_grid_union():
    grid_a = Grid(1, [a, b, c])
    grid_b = Grid(1, [b, c, d])
    result = grid_a.union(grid_b)
    assert [a, b, c, d] == list(result)
    assert [a, b, c] == list(grid_a)


def test_grid_difference():
    grid_a = Grid(1, [a, b, c])
    grid_b = Grid(1, [b, c, d])
    result = grid_a.difference(grid_b)
    assert [a] == list(result)
    assert [a, b, c] == list(grid_a)


def test_grid_intersection():
    grid_a = Grid(1, [a, b, c])
    grid_b = Grid(1, [b, c, d])
    result = grid_a.intersection(grid_b)
    assert [b, c] == list(result)
    assert [a, b, c] == list(grid_a)


def test_grid_neighbours():
    grid = Grid(1, [c])
    n_1 = grid.add_neighbours()
    expected = [Point(x, y) for x, y in
                [[2, 2], [2, 3], [2, 4],
                 [3, 2], [3, 3], [3, 4],
                 [4, 2], [4, 3], [4, 4]]]
    assert expected == list(n_1)
    assert [c] == list(grid)

    grid = Grid(1, [Point(3, 3), Point(3, 4)])
    n_2 = grid.add_neighbours()
    expected = [Point(x, y) for x, y in
                [[2, 2], [2, 3], [2, 4], [2, 5],
                 [3, 2], [3, 3], [3, 4], [3, 5],
                 [4, 2], [4, 3], [4, 4], [4, 5]]]
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
    grid = make_grid(0, 2, 0, 2, 0.5)
    expected = [Point(x, y) for x, y in
                [(0.0, 0.0), (0.0, 0.5), (0.0, 1.0), (0.0, 1.5),
                 (0.5, 0.0), (0.5, 0.5), (0.5, 1.0), (0.5, 1.5),
                 (1.0, 0.0), (1.0, 0.5), (1.0, 1.0), (1.0, 1.5),
                 (1.5, 0.0), (1.5, 0.5), (1.5, 1.0), (1.5, 1.5)]]
    assert expected == list(grid)
