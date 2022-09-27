from geopandas import GeoDataFrame
from shapely.geometry import Point, Polygon
from shapely.validation import make_valid

from nzshm_grid_loc import nzshm_grid_loc
from nzshm_grid_loc.nzshm_grid_loc import diff_grids
from nzshm_grid_loc.grid import Grid
from nzshm_grid_loc.io import write_grid, load_grid, grid_to_base64, latlon_from_base64_zip, \
    write_attr_grid_to_file, write_attr_grid, load_polygon_file, gdf_to_wkt_zip
from nzshm_grid_loc.geography import Regions
from nzshm_grid_loc.plot_grid import Plot
from nzshm_grid_loc.geometry_manipulation import simplify_shape, remove_holes, remove_holes_from_nz
from scripts import nz_backarc_01deg_1n

#nz_backarc_01deg_1n()

nz = Regions.NZ_SMALL.load()
nz = remove_holes_from_nz(nz)
gdf_to_wkt_zip(nz, "nz_small_no_holes.wkt.csv", 0.01)
nz = load_polygon_file("nz_small_no_holes.wkt.csv.zip")

plot = Plot()
plot.add_geoDataFrame(Regions.NZ_SMALL.load(), color="r")
plot.add_geoDataFrame(nz, color="g")
plot.show()


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
