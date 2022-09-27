import csv
import io
import zipfile
from typing import Tuple, Union

import geopandas
import pandas
from geopandas import GeoDataFrame
from nzshm_common.util import compress_string, decompress_string
from shapely import wkt
from shapely.geometry import Point

from nzshm_grid_loc.grid import Grid, get_precision


def load_grid(file_name: str, lat_first=False) -> Grid:
    """
    Loads a grid from a CSV file.
    It is assumed there are not headers, and that the first two columns are the lat/lon values.
    :param file_name: a path to a CSV file
    :param lat_first: if true, it is assumed that the order is (lat, lon), otherwise (lon, lat)
    :return: a Grid object
    """
    points = []
    with open(file_name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        if lat_first:
            for row in reader:
                points.append(Point(float(row[1]), float(row[0])))
        else:
            for row in reader:
                points.append(Point(float(row[0]), float(row[1])))
    return Grid(-1, points)


def write_grid(grid: Grid, file_name: str, lat_first=False) -> None:
    """
    Writes a grid to a CSV file.
    :param grid: a grid object
    :param file_name: the file name
    :param lat_first: if true, written as (lat, lon), otherwise (lon,lat)
    :return: None
    """
    with open(file_name, 'w') as out:
        write_grid_to_file(grid, out, lat_first=lat_first)


def write_grid_to_file(grid: Grid, out, lat_first=False) -> None:
    """
    Writes a grid to a CSV file.
    :param grid: a grid object
    :param out: a file name or a file
    :param lat_first: if true, written as (lat, lon), otherwise (lon,lat)
    :return: None
    """
    writer = csv.writer(out)
    for point in grid:
        if lat_first:
            writer.writerow([point.y, point.x])
        else:
            writer.writerow([point.x, point.y])


def write_attr_grid(grid: Grid, file_name: str, columns=("lat", "lon")) -> None:
    """
    Writes a grid to a CSV file.
    :param columns:
    :param grid: a grid object
    :param file_name: the file name
    :param lat_first: if true, written as (lat, lon), otherwise (lon,lat)
    :return: None
    """
    with open(file_name, 'w') as out:
        write_attr_grid_to_file(grid, out, columns=columns)


def write_attr_grid_to_file(grid: Grid, out, columns=("lat", "lon")) -> None:
    """
    Writes a grid to a CSV file.
    :param grid: a grid object
    :param out: a file name or a file
    :param columns: a list of column headers. Will also be used to look up any attributes
    :return: None
    """
    writer = csv.writer(out)
    writer.writerow(columns)
    for point in grid:
        row = []
        attrs = grid.get_attributes(point)
        for col in columns:
            if col == "lat" or col == "latitude":
                row.append(point.y)
            elif col == "lon" or col == "longitude":
                row.append(point.x)
            else:
                row.append(attrs.get(col, ""))
        writer.writerow(row)


def load_polygon_file(file_name: str) -> GeoDataFrame:
    """
    Loads a polygon file into a GeodataFrame. Can load everything that geopandas can read plus .wkt.csv and .wkt.csv.zip
    :param file_name: path to a geometry file
    :return: a GeoDataFrame
    """
    file: Union[str, io.BytesIO] = file_name
    if file_name.endswith('.zip'):
        file_name, file = load_zip(file_name)

    if file_name.endswith(".wkt.csv"):
        return load_wkt_csv(file)
    else:
        return geopandas.read_file(file)


def load_zip(file_name: str) -> Tuple[str, io.BytesIO]:
    """
    Extracts a file from a zip file. The file that is extracted must have a file name equal to the name of the zip file
    minus '.zip'
    :param file_name: the file name of the zip file
    :return: the inner file name and an io.BytesIO object with the file data
    """
    with open(file_name, 'rb') as f:
        with zipfile.ZipFile(f) as fz:
            inner_file_name = fz.namelist()[0]
            data = io.BytesIO(fz.read(inner_file_name))
    return inner_file_name, data


def write_zip(file_name: str, inner_file_name: str, data: Union[bytes, str]) -> None:
    """
    Writes a zip file. The zip file will be called file_name + ".zip"
    :param file_name: the file name of the file inside the zip file.
    :param inner_file_name: the file name of the file to be stored inside the zip file
    :param data: the data
    :return: None
    """
    with open(file_name + '.zip', 'wb') as f:
        with zipfile.ZipFile(f, 'w', compression=zipfile.ZIP_LZMA) as zf:
            zf.writestr(inner_file_name, data)
            zf.close()


def load_wkt_csv(file_name_or_file):
    """
    Loads a CSV with a "geometry" column that has WKT values in a GeoDataFrame
    :param file_name_or_file:
    :return:
    """
    df = pandas.read_csv(file_name_or_file)
    df['geometry'] = df['geometry'].apply(wkt.loads)
    gdf = geopandas.GeoDataFrame(df, crs='epsg:4326')
    return gdf


def gdf_to_wkt_zip(gdf: GeoDataFrame, file_out: str, tolerance: float):
    """
    Helper function to write a GeoDataFrame to a CSV containing WKT shapes.
    :param gdf:
    :param file_out:
    :param tolerance:
    :return:
    """
    precision = get_precision(tolerance) + 1
    a = gdf.to_wkt(rounding_precision=precision)
    sio = io.StringIO()
    a.to_csv(sio)
    data = sio.getvalue()
    data = data.replace(', ', ',')
    write_zip(file_out, file_out, data)


def print_b64_as_py(b64: str, width=60) -> None:
    """
    Takes a long b64-encoded string and prints it as a python string with the specified max width.
    This is a convenience function for embedding large base64-encided strings in python files.
    :param b64: the input string
    :param width: the max width of the output strings
    :return: None
    """
    result = '(\n'
    for chunk in [b64[i : i + width] for i in range(0, len(b64), width)]:
        result += "'" + chunk + "'\n"
    result += ')'
    print(result)


def grid_to_base64(grid: Grid, lat_first=False) -> None:
    """
    Takes a grid and prints a python definition of a base64-encoded zipped version of it.
    :param grid: the grid
    :param lat_first: whether to print latitude first
    :return: None
    """
    plain_grid = io.StringIO()
    write_grid_to_file(grid, plain_grid, lat_first=lat_first)
    encoded = compress_string(plain_grid.getvalue())
    print_b64_as_py(encoded)


def latlon_from_base64_zip(b64_data: str) -> list:
    """
    Takes a zipped and base64-encoded string and returns a list of lat/lons
    (or lon/lats, depending on how the data was written)
    :param b64_data: a zipped and base64-encoded string
    :return: a list of lat/lon pairs
    """
    data = decompress_string(b64_data)
    result = []
    for row in csv.reader(io.StringIO(data)):
        result.append((float(row[0]), float(row[1])))
    return result
