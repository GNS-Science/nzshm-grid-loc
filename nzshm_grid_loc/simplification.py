import matplotlib.pyplot as plt
from shapely.geometry import Point
import geopandas
import numpy as np
import pandas

# exec(open('scripts/simplification.py').read())

nz = geopandas.read_file('nz-coastlines-and-islands-polygons-topo-150k.shp')
nz.boundary.plot()
nz = nz.simplify(tolerance=0.0003)

nz.boundary.plot()
plt.show()
