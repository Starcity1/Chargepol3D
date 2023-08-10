"""
ChargePol3D.main - Create a 3D scatterplot of the chargepol data overseeing the houston map.4
Usage ::
python main.py <path_to_chargepol_file>
"""

import itertools
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
import cartopy.feature as feature
import cartopy.io.shapereader as shapereader
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
from cartopy.mpl.patch import geos_to_path
import cartopy.crs as ccrs
import sys

# Other scripts
import prepare_data as chargepol_loader

TEXAS_MAP_PATH = 'Texas_County_Boundaries_Detailed/County.shp'
RED = [1, 0.062, 0.019, .5]
BLUE = [0.062, 0.019, 1, .5]

def plot(longitude, latitude, altitude):
    pass

if __name__ == "__main__":
    chargepol_path = sys.argv[-1]

    # chargepol_data will be a dictionary of the form:
    # chargepol = {"Timestamp": time,  # Time of event
    #              "Charge": chargeEvent,  # Type of charge, length and starting altitude
    #              "Location": longLat  # Longitude and altitude of charge
    #              }
    chargepol_data = chargepol_loader.get_data(chargepol_path)
    time = chargepol_data["Timestamp"]
    longitude = [lonlat[1] for lonlat in chargepol_data["Location"]]
    latitude = [lonlat[0] for lonlat in chargepol_data["Location"]]
    altitude = [charge[1] + charge[2] for charge in chargepol_data["Charge"]]  # Note! Here we are simply plotting the Zmax value.

    # creating figure and shapefile projection.
    fig = plt.figure(figsize=(11, 7))
    ax = Axes3D(fig, xlim=[-98, -92], ylim=[28, 32])
    ax.set_zlim(bottom=0)

    target_projection = ccrs.PlateCarree()
    county_lines = feature.ShapelyFeature(shapereader.Reader(TEXAS_MAP_PATH).geometries(), ccrs.PlateCarree(),
                                           facecolor='none', edgecolor='black', lw=1)


    geoms = county_lines.geometries()

    geoms = [target_projection.project_geometry(geom, county_lines.crs)
             for geom in geoms]

    paths = list(itertools.chain.from_iterable(geos_to_path(geom) for geom in geoms))

    # At this point, we start working around mpl3d's slightly broken interfaces.
    # So we produce a LineCollection rather than a PathCollection.
    segments = []
    for path in paths:
        vertices = [vertex for vertex, _ in path.iter_segments()]
        vertices = np.asarray(vertices)
        segments.append(vertices)

    lc = LineCollection(segments, color='black')

    ax.add_collection3d(lc)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Height')

    plt.show()