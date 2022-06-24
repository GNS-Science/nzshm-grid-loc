from shapely.geometry import Point

from nzshm_grid_loc import nzshm_grid_loc
from nzshm_grid_loc.nzshm_grid_loc import diff_grids
from nzshm_grid_loc.grids import make_grid, Grid
from nzshm_grid_loc.io import write_grid, load_grid, grid_to_base64, data_from_base64_zip, latlon_from_base64_zip
from nzshm_grid_loc.geography import Regions
from nzshm_grid_loc.plot_grid import Plot

# nzshm_grid_loc.nzshm_grid_loc.generate_grid("test-grid.csv", 0.1)
# print('a')
# nzshm_grid_loc.nzshm_grid_loc.generate_grid("test-grid-tol01.csv", 0.01)
# print('b')
# nzshm_grid_loc.nzshm_grid_loc.diff_grids("test-grid.csv", "test-grid-tol01.csv")


# hutt_grid = load_grid("hutt_0.1.csv")
# wlg_pred = Regions.WLG.predicate()
# nz_pred = Regions.NZ_SMALL.predicate()
#
#
# def predicate(p: Point) -> bool:
#     return wlg_pred(p) and nz_pred(p)
#
#
# wlg_grid = make_grid(lat_min=-48, lat_max=-34, lon_min=166, lon_max=179, step=0.1) \
#     .filter(predicate) \
#     .add_neighbours()\
#     .difference(hutt_grid)
# write_grid(wlg_grid, "WLG_0.1.csv")
#
# diff_grids("hutt_0.1.csv", "WLG_0.1.csv")

wlg_grid = nzshm_grid_loc.generate_grid("WLG_0.1.csv", 0.1, neighbours=1)
b64_data = grid_to_base64(wlg_grid)
print(b64_data)
# plain = data_from_base64_zip(b64_data)
#points = latlon_from_base64_zip(b64_data)


# print('b')
#
# grid = load_grid("test-grid-tol001.csv")

plot = Plot()
plot.add_geoDataFrame(Regions.NZ.load())
plot.add_geoDataFrame(Regions.NZ_SMALL.load())
plot.add_grid(grid)
plot.show()
#
# from nzshm_grid_loc.geometry_manipulation import simplify_shape
#
# simplify_shape('resources/nz-coastlines-and-islands-polygons-topo-150k.shp')

grid_a = Grid(0.1, {})
grid_c = grid_a.union(grid_b)
grid_d = grid_c.filter(Regions.WLG.predicate())
