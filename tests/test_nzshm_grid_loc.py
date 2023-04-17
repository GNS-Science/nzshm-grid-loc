#!/usr/bin/env python
"""Tests for `nzshm_grid_loc` package."""
from geopandas import GeoDataFrame


def test_main_module_import():
    import nzshm_grid_loc as ngl

    assert ngl.__name__ == "nzshm_grid_loc"


def test_top_level_module_members():
    import nzshm_grid_loc as ngl

    assert ngl.Regions.NZ_SMALL is not None


def test_load_region():
    import nzshm_grid_loc as ngl

    nzsmall = ngl.Regions.NZ_SMALL.load()
    assert isinstance(nzsmall, GeoDataFrame)
