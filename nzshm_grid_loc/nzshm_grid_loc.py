"""Main module."""
from typing import Union

from nzshm_grid_loc.geography import Regions
from nzshm_grid_loc.grid import Grid
from nzshm_grid_loc.io import load_grid, write_grid
from nzshm_grid_loc.plot_grid import Plot


def generate_grid(
    file_name: str,
    step: float,
    lat_min=-48,
    lat_max=-34,
    lon_min=166,
    lon_max=179,
    neighbours=2,
    clip=Regions.NZ_SMALL.load(),
) -> Grid:
    """
    Generate a grid for NZ
    :param clip:
    :param file_name: file name for the grid to be stored under
    :param step: step size for the new grid
    :param lat_min:
    :param lat_max:
    :param lon_min:
    :param lon_max:
    :param neighbours: number of neighbour iterations
    :param clip: clipping geometry, must be GeoDataFrame of polygons
    :return: None
    """

    grid = Grid.for_bounds(lat_min, lat_max, lon_min, lon_max, step)
    grid = grid.intersection(clip)
    for n in range(neighbours):
        grid = grid.add_neighbours()
    write_grid(grid, file_name)
    return grid


def diff_grids(grid_a: Union[str, Grid], grid_b: Union[str, Grid]) -> None:
    """
    Load two grids and create a visual diff
    :param grid_a: a grid or a file name of a grid file
    :param grid_b: a grid or a file name of a grid file
    :return: None
    """
    grid = grid_a if isinstance(grid_a, Grid) else load_grid(grid_a)
    grid_new = grid_b if isinstance(grid_b, Grid) else load_grid(grid_b)

    grid_intersection = grid.intersection(grid_new)
    grid_diff1 = grid.difference(grid_new)
    grid_diff2 = grid_new.difference(grid)

    print("grid a          : " + str(len(grid)))
    print("grid b          : " + str(len(grid_new)))
    print("in both         : " + str(len(grid_intersection)))
    print("in a but not b  : " + str(len(grid_diff1)))
    print("in b but not a  : " + str(len(grid_diff2)))

    plot = Plot()
    plot.add_geoDataFrame(Regions.NZ_SMALL.load())
    plot.add_grid(grid_intersection, color='y')
    plot.add_grid(grid_diff1, color='r')
    plot.add_grid(grid_diff2, color='g')
    plot.show()
