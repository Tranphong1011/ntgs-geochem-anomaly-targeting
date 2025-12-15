#!/usr/bin/env python
"""CLI-style script. Run from repo root: `python scripts/<name>.py`"""

from pathlib import Path
import pandas as pd
import geopandas as gpd
from src.config import default_paths

REPO = Path(__file__).resolve().parents[1]
paths = default_paths(REPO)

gdf = gpd.read_file(paths.raw_gpkg)
print("rows:", len(gdf), "cols:", len(gdf.columns))
print("CRS:", gdf.crs)

print("lon min/max:", float(gdf["LONGITUDE"].min()), float(gdf["LONGITUDE"].max()))
print("lat min/max:", float(gdf["LATITUDE"].min()), float(gdf["LATITUDE"].max()))

dup_xy = gdf.duplicated(subset=["LONGITUDE","LATITUDE"]).sum()
print("duplicate coordinate rows:", int(dup_xy))

print("UNIQ_ID unique:", gdf["UNIQ_ID"].is_unique if "UNIQ_ID" in gdf.columns else "N/A")
