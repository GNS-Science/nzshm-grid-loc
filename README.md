# NZSHM Grid Loc


[![pypi](https://img.shields.io/pypi/v/nzshm-grid-loc.svg)](https://pypi.org/project/nzshm-grid-loc/)
[![python](https://img.shields.io/pypi/pyversions/nzshm-grid-loc.svg)](https://pypi.org/project/nzshm-grid-loc/)
[![Build Status](https://github.com/GNS-Science/nzshm-grid-loc/actions/workflows/dev.yml/badge.svg)](https://github.com/GNS-Science/nzshm-grid-loc/actions/workflows/dev.yml)
[![codecov](https://codecov.io/gh/GNS-Science/nzshm-grid-loc/branch/main/graphs/badge.svg)](https://codecov.io/github/GNS-Science/nzshm-grid-loc)



Scripts to generate and manipulate NZSHM hazard grid locations


* Documentation: <https://GNS-Science.github.io/nzshm-grid-loc>
* GitHub: <https://github.com/GNS-Science/nzshm-grid-loc>
* PyPI: <https://pypi.org/project/nzshm-grid-loc/>
* Free software: GPL-3.0-only


## Examples

Grid generation:

```python
# create a NZ grid at 0.1 degree spacing
nz_grid = Grid.for_polygon(0.1, Regions.NZ_SMALL.load())
```

Grid operations:

```python
grid_c = grid_a.union(grid_b)
grid_d = grid_c.difference(grid_e)
# set operations also work with GeoDataFrame objects
grid_f = grid_d.difference(Regions.WLG.load())
```

Grid plotting:
```python
plot = Plot()
plot.add_geoDataFrame(Regions.NZ.load())
plot.add_geoDataFrame(Regions.WLG.load())
plot.add_grid(grid)
plot.show()
```

Visual diff:

```python
# show a visual diff of the hutt and WLG grids
diff_grids("hutt_0.1.csv", "WLG_0.1.csv")
```

IO:

```python
write_grid(nz_grid, "NZ_0.1.csv")

grid = load_grid("NZ_0.1.csv")
```

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.
