from geopandas import read_file

from nzshm_grid_loc.io import gdf_to_wkt_zip, load_polygon_file
from nzshm_grid_loc.plot_grid import Plot


def simplify_shape(file_in: str, tolerance=0.01, max_rows=50, visual_check=True) -> None:
    """
    Loads a shapefile and creates a simpler version.
    This function is made especially for grid filters, and the resulting polygons will be slightly larger than the
    original ones.
    :param file_in: path ot a shapefile
    :param tolerance: This is in the units of the shapefile and is used to create a buffer and then simplify the shape
    :param max_rows: if the shapefile has more than one shape in it, take only the "max_rows" largest ones.
    :param visual_check: if True, show a plot of the old and new shapes.
    :return: None
    """
    original = read_file(file_in)
    original['Area'] = original['geometry'].area
    df = original.sort_values(by=['Area'], ascending=False)[:max_rows]
    df = df.drop(['Area'], axis=1)
    df = df.reset_index(drop=True)
    clip_box = load_polygon_file('resources/nz_bbox.geojson')
    df = df.clip(clip_box)
    df['geometry'] = df.geometry.buffer(tolerance)
    df['geometry'] = df.geometry.simplify(tolerance=tolerance)

    file_out = "small-nz.wkt.csv"
    gdf_to_wkt_zip(df, file_out, tolerance)

    if visual_check:
        zgdf = load_polygon_file(file_out + '.zip')
        plot = Plot()
        plot.add_geoDataFrame(original, color='r')
        plot.add_geoDataFrame(df, color='g')
        plot.add_geoDataFrame(zgdf, color='b')
        plot.show()
