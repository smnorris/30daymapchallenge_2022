import sys

import geopandas
import matplotlib.pyplot as plt

data = sys.argv[1]
outfile = sys.argv[2]


def saanich_gdf(layer, bbox):
    """
    Given a layer name and a bounding box,
    pull data from Saanich and retain only features intersecting the bbox
    """
    xmin, ymin, xmax, ymax = bbox
    url = "https://map.saanich.ca/gisdata"
    return geopandas.read_file(f"/vsizip//vsicurl/{url}/{layer}/{layer}SHP.zip").cx[
        xmin:xmax, ymin:ymax
    ]


# define a small bounding box around the Victoria Ukranian Cultural Centre
bbox = (472294, 5366189, 472542, 5366376)

# get some data
buildings = saanich_gdf("Buildings", bbox)
parcels = saanich_gdf("Parcels", bbox)
zoning = saanich_gdf("Zoning", bbox)
streetlights = saanich_gdf("Streetlights", bbox)

# make a simple plot
xmin, ymin, xmax, ymax = bbox
xlim = [xmin, xmax]
ylim = [ymin, ymax]
ax = zoning.plot(column="TYPE", cmap="Set3", alpha=0.1)
parcels.plot(ax=ax, color="grey", alpha=0.1, edgecolor="black", linewidth=1)
buildings.plot(ax=ax, color="black", alpha=0.6)
streetlights.plot(ax=ax, color="black", alpha=0.6)
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_axis_off()
plt.savefig(outfile, bbox_inches="tight")
