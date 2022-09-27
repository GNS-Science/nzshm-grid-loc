import io
from pathlib import Path

from shapely.geometry import Point
from nzshm_common.util import compress_string
from nzshm_grid_loc.grid import Grid
from nzshm_grid_loc.io import (
    load_grid,
    write_grid,
    write_zip,
    load_zip,
    load_wkt_csv,
    write_grid_to_file,
    latlon_from_base64_zip,
)

temp_file_count = 0

a = Point(1, 2)
b = Point(3, 4)
c = Point(2, 1)
d = Point(4, 3)


def tmp_file_path(temp_path: Path) -> Path:
    global temp_file_count
    temp_file_count += 1
    return temp_path / ("tempFile" + str(temp_file_count))


def test_load_csv(tmp_path):
    tmp_file = tmp_file_path(tmp_path)
    tmp_file.write_text("1,2\n3,4")

    grid = load_grid(str(tmp_file))
    assert [a, b] == list(grid)
    grid = load_grid(str(tmp_file), lat_first=True)
    assert [c, d] == list(grid)


def test_write_csv(tmp_path):
    tmp_file = tmp_file_path(tmp_path)
    grid = Grid(1, [a, b])

    write_grid(grid, str(tmp_file))
    assert "1.0,2.0\n3.0,4.0\n" == tmp_file.read_text()
    write_grid(grid, str(tmp_file), lat_first=True)
    assert "2.0,1.0\n4.0,3.0\n" == tmp_file.read_text()


def test_read_write_zip(tmp_path):
    tmp_file = tmp_file_path(tmp_path)
    content = b'Hello World!'

    write_zip(str(tmp_file), str(tmp_file), content)
    actual_name, actual_data = load_zip(str(tmp_file) + '.zip')
    assert str(tmp_file) == actual_name
    assert content == actual_data.read()


def test_load_wkt_csv(tmp_path):
    tmp_file = tmp_file_path(tmp_path)
    content = 'name,geometry\na,"POINT(1 2)"\nb,"POINT(3 4)"'
    tmp_file.write_text(content)

    gdf = load_wkt_csv(tmp_file)
    assert [a, b] == gdf.geometry.to_list()
    assert ['a', 'b'] == gdf['name'].to_list()


def test_base64zip():
    expected = [(1, 2), (3, 4), (5, 6), (7, 8)]
    grid = Grid(1, set(expected))
    out_file = io.StringIO()
    write_grid_to_file(grid, out_file)
    base64_zip = compress_string(out_file.getvalue())
    actual = latlon_from_base64_zip(base64_zip)
    assert expected == actual
