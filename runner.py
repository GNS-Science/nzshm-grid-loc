from geopandas import GeoDataFrame
from shapely.geometry import Point, Polygon

from nzshm_grid_loc import nzshm_grid_loc
from nzshm_grid_loc.nzshm_grid_loc import diff_grids
from nzshm_grid_loc.grid import Grid
from nzshm_grid_loc.io import write_grid, load_grid, grid_to_base64, data_from_base64_zip, latlon_from_base64_zip, \
    write_attr_grid_to_file, write_attr_grid, load_polygon_file
from nzshm_grid_loc.geography import Regions
from nzshm_grid_loc.plot_grid import Plot
from nzshm_grid_loc.geometry_manipulation import simplify_shape


grid = Grid\
    .for_polygon(0.2, Regions.NZ_SMALL.load())\
    .add_neighbours()\
    .annotate("backarc", "0")\
    .annotate("backarc", "1", clip=Regions.BACKARC.load())

write_attr_grid(grid, "backarc2_02deg_1n.csv", ["lon", "lat", "backarc"])

# nz = Regions.NZ_SMALL.load()
#
# clipBox = load_polygon_file('resources/nz_bbox.geojson')
#
# nz = nz.clip(clipBox)
#
# plot = Plot()
# plot.add_geoDataFrame(nz)
# plot.show()

# simplify_shape('resources/nz-coastlines-and-islands-polygons-topo-150k.shp')


# grid_gdf = make_grid_for_gdf(0.5, Regions.NZ_SMALL.load())
# grid_old = nzshm_grid_loc.generate_grid("all_nz.csv", 0.5, neighbours=0)
#
# diff_grids(grid_gdf, grid_old)


#  backarc
# nz_grid = nzshm_grid_loc.generate_grid("all_nz.csv", 0.2, neighbours=1)
# nz_grid = nz_grid.annotate("backarc", "0").annotate("backarc", "1", clip=Regions.BACKARC.load())
#
# write_attr_grid(nz_grid, "backarc_02deg_1n.csv", ["lon", "lat", "backarc"])

# plot = Plot()
# plot.add_geoDataFrame(Regions.NZ.load())
# plot.add_grid(backarc_grid)
# plot.show()
