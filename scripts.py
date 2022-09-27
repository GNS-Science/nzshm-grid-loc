from nzshm_grid_loc.geography import Regions
from nzshm_grid_loc.grid import Grid
from nzshm_grid_loc.io import write_attr_grid


def nz_backarc_02deg_1n():
    """
    Create backarc2_02deg_1n.csv file for OQ
    :return:
    """
    grid = Grid \
        .for_polygon(0.2, Regions.NZ_SMALL.load()) \
        .add_neighbours() \
        .annotate("backarc", "0") \
        .annotate("backarc", "1", clip=Regions.BACKARC.load())

    write_attr_grid(grid, "backarc2_02deg_1n.csv", ["lon", "lat", "backarc"])


def nz_backarc_01deg_1n():
    """
    Create backarc2_01deg_1n.csv file for OQ
    :return:
    """
    grid = Grid \
        .for_polygon(0.1, Regions.NZ_SMALL.load()) \
        .add_neighbours() \
        .annotate("backarc", "0") \
        .annotate("backarc", "1", clip=Regions.BACKARC.load())

    write_attr_grid(grid, "backarc2_01deg_1n.csv", ["lon", "lat", "backarc"])
