import sys

import geopandas
import matplotlib.pyplot as plt

data = sys.argv[1]
outfile = sys.argv[2]

df = geopandas.read_file(
    "https://features.hillcrestgeo.ca/fwa/collections/whse_basemapping.fwa_lakes_poly/items.json?filter=gnis_name_1%20like%20%27%25Green%25%27"
)

fig, axs = plt.subplots(6, 3, figsize=(20, 20))
axs = axs.flatten()
for idx in range(len(df)):
    df.iloc[[idx]].plot(ax=axs[idx], color="#90b88d", edgecolor="#639b5f", linewidth=2)
    axs[idx].axis("off")
plt.tight_layout()
plt.savefig(outfile, bbox_inches="tight")
