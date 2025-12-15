#!/usr/bin/env python
"""CLI-style script. Run from repo root: `python scripts/<name>.py`"""

from pathlib import Path
import geopandas as gpd
from src.config import default_paths, FEATURES_BASELINE, FEATURES_NOAG
from src.fingerprint import cluster_fingerprint

REPO = Path(__file__).resolve().parents[1]
paths = default_paths(REPO)

# baseline
grid_base = gpd.read_file(paths.artifacts_dir / "baseline" / "ntgs_anomaly_grid_1km_stable_baseline.gpkg", layer="iforest_min5_baseline")
anom_base = gpd.read_file(paths.artifacts_dir / "baseline" / "ntgs_anomaly_clusters_baseline.gpkg", layer="clusters_baseline_eps2km")

cluster_fingerprint(
    grid_scored=grid_base,
    anom_with_clusters=anom_base,
    features=FEATURES_BASELINE,
    out_csv=str(paths.artifacts_dir / "baseline" / "cluster_fingerprint_baseline.csv")
)
print("Saved baseline fingerprint CSV")

# noAG
grid_noag = gpd.read_file(paths.artifacts_dir / "robustness_noAG" / "ntgs_anomaly_grid_1km_stable_noAG.gpkg", layer="iforest_min5_noAG")
anom_noag = gpd.read_file(paths.artifacts_dir / "robustness_noAG" / "ntgs_anomaly_clusters_noAG.gpkg", layer="clusters_noAG_eps2km")

cluster_fingerprint(
    grid_scored=grid_noag,
    anom_with_clusters=anom_noag,
    features=FEATURES_NOAG,
    out_csv=str(paths.artifacts_dir / "robustness_noAG" / "cluster_fingerprint_noAG.csv")
)
print("Saved noAG fingerprint CSV")
