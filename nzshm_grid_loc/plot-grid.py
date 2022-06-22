import matplotlib.pyplot as plt
import geopandas
import csv
import pandas
from shapely.geometry import Point

# exec(open('scripts/plot-grid.py').read())
import scripts.regions

nz = geopandas.read_file('nz-coastlines-and-islands-polygons-topo-150k.shp')
region = scripts.regions.load_wellington();
# nz.plot()
# csv = pandas.read_csv('test.csv')
# points = []
# for p in csv.iloc:
#     points.append(Point(p['lon'], p['lat']))
#
# df = geopandas.GeoDataFrame()
# df = df.set_geometry(points)
#df.plot()
#plt.show()

xlim = [163, 180]
ylim = [-50, -32]


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


set_plot_formatting()


fig, ax = plt.subplots(1, 1 )
#fig.set_size_inches(8, 16)
fig.set_facecolor('white')

x = []
y = []

with open('test-wellington-0.01-0.0003.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        y.append(float(row[0]))
        x.append(float(row[1]))



nz.boundary.plot(ax=ax, color='k')

df = geopandas.GeoDataFrame()
df = df.set_geometry([region[1]])

df.boundary.plot(ax=ax, color='g')

ax.plot(x, y, '.', color='r')


ax.set_xlim(xlim)
ax.set_ylim(ylim)

fig.show()
