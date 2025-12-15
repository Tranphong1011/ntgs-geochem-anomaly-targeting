#!/usr/bin/env python
"""CLI-style script. Run from repo root: `python scripts/<name>.py`"""

from pathlib import Path
import geopandas as gpd
from src.config import default_paths, ModelConfig, FEATURES_BASELINE
from src.modeling import score_iforest, mark_anomalies
from src.io import write_gpkg

REPO = Path(__file__).resolve().parents[1]
paths = default_paths(REPO)
m = ModelConfig()

# you can also load from grid_cells_1km.gpkg if you saved it; here we assume you re-aggregate earlier step
cells = gpd.read_file(paths.artifacts_dir / "baseline" / "grid_cells_1km.gpkg", layer="cells_1km")

# min_points filter
cells = cells[cells["n_points"] >= 5].copy()

scored, meta = score_iforest(cells, FEATURES_BASELINE, m.contamination, m.random_state)
scored, thr = mark_anomalies(scored, m.contamination)
meta["threshold"] = thr
meta["min_points"] = 5
meta["n_anomaly_cells"] = int(scored["is_anomaly"].sum())

out = paths.artifacts_dir / "baseline" / "ntgs_anomaly_grid_1km_stable_baseline.gpkg"
write_gpkg(scored, out, layer="iforest_min5_baseline")
print("Saved:", out)
print("Meta:", meta)
