#!/usr/bin/env python
"""CLI-style script. Run from repo root: `python scripts/<name>.py`"""

from pathlib import Path
import geopandas as gpd
from src.config import default_paths, ClusterConfig
from src.clustering import dbscan_clusters, clusters_to_polygons, top_targets_table
from src.io import write_gpkg

REPO = Path(__file__).resolve().parents[1]
paths = default_paths(REPO)
c = ClusterConfig()

# baseline
grid_base = gpd.read_file(paths.artifacts_dir / "baseline" / "ntgs_anomaly_grid_1km_stable_baseline.gpkg", layer="iforest_min5_baseline")
anom = grid_base[grid_base["is_anomaly"] == 1].copy()
anom = dbscan_clusters(anom, eps_m=c.eps_m, min_samples=c.min_samples)

polys, cents = clusters_to_polygons(anom, buffer_m=c.buffer_m)

out_clusters = paths.artifacts_dir / "baseline" / "ntgs_anomaly_clusters_baseline.gpkg"
write_gpkg(anom, out_clusters, layer="clusters_baseline_eps2km")
out_targets = paths.artifacts_dir / "baseline" / "ntgs_target_clusters_baseline.gpkg"
write_gpkg(polys, out_targets, layer="baseline_polygons")
write_gpkg(cents, out_targets, layer="baseline_centroids_wgs84")

top_targets_table(cents, out_csv=str(paths.artifacts_dir / "baseline" / "top_targets_baseline.csv"))
print("Saved:", out_clusters)
print("Saved:", out_targets)

# noAG
grid_noag = gpd.read_file(paths.artifacts_dir / "robustness_noAG" / "ntgs_anomaly_grid_1km_stable_noAG.gpkg", layer="iforest_min5_noAG")
anom2 = grid_noag[grid_noag["is_anomaly"] == 1].copy()
anom2 = dbscan_clusters(anom2, eps_m=c.eps_m, min_samples=c.min_samples)
polys2, cents2 = clusters_to_polygons(anom2, buffer_m=c.buffer_m)

out_clusters2 = paths.artifacts_dir / "robustness_noAG" / "ntgs_anomaly_clusters_noAG.gpkg"
write_gpkg(anom2, out_clusters2, layer="clusters_noAG_eps2km")
out_targets2 = paths.artifacts_dir / "robustness_noAG" / "ntgs_target_clusters_noAG.gpkg"
write_gpkg(polys2, out_targets2, layer="noAG_polygons")
write_gpkg(cents2, out_targets2, layer="noAG_centroids_wgs84")

top_targets_table(cents2, out_csv=str(paths.artifacts_dir / "robustness_noAG" / "top_targets_noAG.csv"))
print("Saved:", out_clusters2)
print("Saved:", out_targets2)
