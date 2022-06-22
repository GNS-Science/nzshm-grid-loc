from shapely.geometry import Point
import geopandas
import numpy as np
import pandas
from nzshm_grid_loc.neighbours import add_neighbours
import nzshm_grid_loc.regions

# exec(open('scripts/make-grid.py').read())

step = 0.1
precision = 1
tolerance = 0.0003
#region = scripts.regions.load_wellington()
region = ["NZ"]


def load_nz(tolerance):
    nz = geopandas.read_file('nz-coastlines-and-islands-polygons-topo-150k.shp')
    nz = nz.simplify(tolerance=tolerance)

    def area_sort(polygon):
        return polygon.area
    nz = sorted(nz.geometry, key=area_sort)[-6:]
    nz.reverse()
    return nz


nz = load_nz(tolerance)


def is_in_nz(p):
    for g in nz:
        if g.contains(p):
            return True
    return False


def make_grid(step, precision):
    result = []
    for lon in np.arange(166, 179, step):
        print('.', end="")
        for lat in np.arange(-48, -34, step):
            p = Point(lon, lat)
#            if region[1].contains(p) and is_in_nz(p):
            if is_in_nz(p):
                result.append([round(lon, precision), round(lat, precision)])
    print()
    return result


file_name = "grids/grid-"+region[0]+"-"+str(step)+"-"+str(tolerance)+".csv"

df = pandas.DataFrame(make_grid(step, precision))
df.to_csv(file_name, index=False, header=False)

file_name = add_neighbours(step, precision, file_name)
add_neighbours(step, precision, file_name)
