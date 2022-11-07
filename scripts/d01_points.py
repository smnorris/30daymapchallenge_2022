import os
import sys

from matplotlib import pyplot
import geopandas
import rasterio
from rasterio.plot import show
from rasterio.windows import from_bounds

import bcdata

data = sys.argv[1]
outfile = sys.argv[2]

# load hydrography from data directory
waterbodies = geopandas.read_file(
    os.path.join(data, "AC_1M_Waterbodies_shp/AC_1M_Waterbodies.shp")
).to_crs("EPSG:3005")
rivers = geopandas.read_file(
    os.path.join(data, "AC_1M_Rivers_dense_shp/AC_1M_Rivers_dense.shp")
).to_crs("EPSG:3005")


# get Bulkley watershed group polygon
wsg = bcdata.get_data(
    "whse_basemapping.fwa_watershed_groups_poly",
    query="WATERSHED_GROUP_CODE='BULK'",
    as_gdf=True,
    crs="EPSG:3005",
)

# Get points
# Request known and potential barriers to fish passage on streams potentially accessible to
# salmon in Bulkley Watershed (not including Morice), downloaded from pg_fs interface to bcfishpass

barriers = geopandas.read_file(
    "https://features.hillcrestgeo.ca/bcfishpass/collections/bcfishpass.crossings/items.json?filter=watershed_group_code=%27BULK%27%20and%20barrier_status%20in%20(%27BARRIER%27,%27POTENTIAL%27)%20and%20access_model_ch_co_sk%20is%20not%20null"
).to_crs("EPSG:3005")

# get bounds from watershed group polygon
xmin, ymin, xmax, ymax = tuple(list(wsg.bounds.itertuples(index=False))[0])

# load a subset of the hillshade based on the bounds
with rasterio.open(
    "https://www.hillcrestgeo.ca/projects/bc_hillshade/bc_hshd_eduard_l1.tif"
) as src:
    win = from_bounds(xmin, ymin, xmax, ymax, src.transform)
    win_transform = src.window_transform(win)
    hillshade = src.read(
        1,
        window=win,
    )

# make the map!
fig, ax = pyplot.subplots(figsize=(15, 15))
xlim = [xmin, xmax]
ylim = [ymin, ymax]
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.xaxis.set_ticklabels([])
ax.yaxis.set_ticklabels([])
ax.set_xticks([])
ax.set_yticks([])

show(hillshade, alpha=0.2, cmap="gray", ax=ax, transform=win_transform)
waterbodies.plot(ax=ax, color="#9dd7fd", edgecolor="#9dd7fd", alpha=0.4)
waterbodies.plot(ax=ax, edgecolor="#9dd7fd", alpha=0.6, facecolor="none")
rivers.plot(ax=ax, edgecolor="#9dd7fd", alpha=0.6)
wsg.plot(ax=ax, edgecolor="gray", alpha=0.4, linewidth=2, facecolor="none")
barriers.plot(
    ax=ax, color="#f85a65", edgecolor="white", zorder=100
)  # ensure pts are plotted on top.

# dump to file
pyplot.savefig(outfile, bbox_inches="tight")
