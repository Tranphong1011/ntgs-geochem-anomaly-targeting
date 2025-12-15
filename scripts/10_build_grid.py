#!/usr/bin/env python
"""CLI-style script. Run from repo root: `python scripts/<name>.py`"""

from pathlib import Path
import geopandas as gpd
from src.config import default_paths, GridConfig, FEATURES_BASELINE
from src.grid import points_to_grid, aggregate_to_cells
from src.io import write_gpkg

REPO = Path(__file__).resolve().parents[1]
paths = default_paths(REPO)
cfg = GridConfig()

gdf = gpd.read_file(paths.raw_gpkg)
if gdf.crs is None:
    gdf = gdf.set_crs("EPSG:4283")

gdf_pts = points_to_grid(gdf, cfg.utm_epsg, cfg.grid_size_m)
cells = aggregate_to_cells(gdf_pts, FEATURES_BASELINE)  # include baseline features; noAG is subset anyway

out = paths.artifacts_dir / "baseline" / "grid_cells_1km.gpkg"
write_gpkg(cells, out, layer="cells_1km")
print("Saved:", out)
