import matplotlib.pyplot as plt
from geopandas import GeoDataFrame

from nzshm_grid_loc.grid import Grid


def set_plot_formatting():
    # set up plot formatting
    SMALL_SIZE = 12
    MEDIUM_SIZE = 16
    BIGGER_SIZE = 25
    plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
    plt.rc('axes', titlesize=MEDIUM_SIZE)  # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title


class Plot:
    """
    Helper class to draw plots for debugging in equirectangular projection
    https://en.wikipedia.org/wiki/Equirectangular_projection
    """

    def __init__(self, lon_min=163, lon_max=180, lat_min=-50, lat_max=-32):
        self.lon_lim = [lon_min, lon_max]
        self.lat_lim = [lat_min, lat_max]
        set_plot_formatting()
        self.fig, self.ax = plt.subplots(1, 1)
        self.fig.set_facecolor('white')
        self.ax.set_xlim(self.lon_lim)
        self.ax.set_ylim(self.lat_lim)

    def add_grid(self, grid: Grid, color='r') -> None:
        """
        Adds the points of a grid to the map.
        :param grid: the grid
        :param color: a matplotlib color
        :return: None
        """
        x = []
        y = []
        for p in grid:
            x.append(p.x)
            y.append(p.y)
        self.ax.plot(x, y, '.', color=color)

    def add_geoDataFrame(self, df: GeoDataFrame, color='k') -> None:
        """
        Adds the boundary of a GeoDataFrame to the map
        :param df: the GeoDataFrame
        :param color: a matplotlib color
        :return: None
        """
        df.boundary.plot(ax=self.ax, color=color)

    def get_ax(self):
        return self.ax

    def show(self) -> None:
        """
        Display the map on screen.
        :return: None
        """
        self.fig.show()
