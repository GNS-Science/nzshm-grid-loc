import geopandas


def load_wellington():
    return [
        "Wellington",
        geopandas.read_file('wellington.geojson').geometry[0]]
