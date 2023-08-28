import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

from mpl_toolkits.basemap import Basemap


def generate_3d_plot(
    file_path,
    lon_range,
    lat_range,
    end_time,
    start_time=0,
    zmin=0,
    zmax=None,
    show_counties=True,
    fill_land=False,
):
    """
    Generates a 3D plot of the chargepol data.
    :param file_path: path to the chargepol csv file
    :param lon_range: longitude range (min, max)
    :param lat_range: latitude range (min, max)
    :param end_time: end time (seconds)
    :param start_time: start time (seconds)
    :param zmin: minimum altitude
    :param zmax: maximum altitude
    :param show_counties: whether to show county lines
    :param fill_land: whether to fill land bodies
    """

    # Load Data
    data = pd.read_csv(file_path, comment="#")
    data["zmax"] = data["zwidth"] + data["zmin"]

    # Load Ligtning Locations
    positive = (
        data.loc[
            (data["charge"] == "pos") & (data["time"].between(start_time, end_time))
        ]
        .reset_index()
        .loc[:, ["lon", "lat", "zmax"]]
    )
    negetive = (
        data.loc[
            (data["charge"] == "neg") & (data["time"].between(start_time, end_time))
        ]
        .reset_index()
        .loc[:, ["lon", "lat", "zmax"]]
    )

    if not zmax:
        zmax = max(positive["zmax"].max(), negetive["zmax"].max()) + 0.5

    # Initialize figure
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d", zlim=[zmin, zmax])

    # Initialize basemap with range
    bm = Basemap(
        llcrnrlon=lon_range[0],
        urcrnrlon=lon_range[1],
        llcrnrlat=lat_range[0],
        urcrnrlat=lat_range[1],
        projection="cyl",
        ax=ax,
        resolution="h",  # c (crude, the default), l (low), i (intermediate), h (high), f (full)
    )

    # Add maps to basemap
    ax.add_collection3d(bm.drawcoastlines(linewidth=0.25), zs=zmin)
    ax.add_collection3d(bm.drawcountries(linewidth=0.35), zs=zmin)
    ax.add_collection3d(bm.drawstates(), zs=zmin)
    if show_counties:
        ax.add_collection3d(bm.drawcounties(linewidth=0.1), zs=zmin)

    if fill_land:
        # Fill land bodies
        polys = []
        for polygon in bm.landpolygons:
            polys.append(polygon.get_coords())

        lc = PolyCollection(polys, edgecolor="black", facecolor="#DDDDDD", closed=False)

        ax.add_collection3d(lc)

    # Add labels
    # Labels and ticks
    ax.set_xlabel("Longitude (°E)", labelpad=10)
    ax.set_ylabel("Latitude (°N)", labelpad=10)
    ax.set_zlabel("Altitude (km)", labelpad=10)
    # Add meridian and parallel gridlines
    lon_step = 1
    lat_step = 1
    meridians = np.arange(lon_range[0], lon_range[1] + lon_step, lon_step)
    parallels = np.arange(lat_range[0], lat_range[1] + lat_step, lat_step)
    ax.set_yticks(parallels)
    ax.set_yticklabels(parallels)
    ax.set_xticks(meridians)
    ax.set_xticklabels(meridians)

    # Plot Ligtning Locations
    pos = np.array(positive)
    ax.scatter(pos[:, 0], pos[:, 1], pos[:, 2], c="r", zorder=20)

    neg = np.array(negetive)
    ax.scatter(neg[:, 0], neg[:, 1], neg[:, 2], c="b", zorder=20)

    return fig


if __name__ == "__main__":
    plot = generate_3d_plot(
        "chargepol.csv",
        lon_range=[-98, -92],
        lat_range=[28, 32],
        zmin=0,
        zmax=None,
        start_time=0,
        end_time=1000,
        show_counties=False,
    )

    plt.show()
