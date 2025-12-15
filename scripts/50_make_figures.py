#!/usr/bin/env python
"""CLI-style script. Run from repo root: `python scripts/<name>.py`"""

from pathlib import Path
import pandas as pd
import geopandas as gpd

from src.config import default_paths
from src.viz import (
    map_anomaly_score, map_targets, map_robustness,
    plot_score_hist, plot_npoints_scatter, plot_fingerprint_heatmap
)

REPO = Path(__file__).resolve().parents[1]
paths = default_paths(REPO)
paths.figures_dir.mkdir(parents=True, exist_ok=True)

grid_base = gpd.read_file(paths.artifacts_dir / "baseline" / "ntgs_anomaly_grid_1km_stable_baseline.gpkg", layer="iforest_min5_baseline")
targets_base = gpd.read_file(paths.artifacts_dir / "baseline" / "ntgs_target_clusters_baseline.gpkg", layer="baseline_polygons")
cent_base = gpd.read_file(paths.artifacts_dir / "baseline" / "ntgs_target_clusters_baseline.gpkg", layer="baseline_centroids_wgs84")
targets_noag = gpd.read_file(paths.artifacts_dir / "robustness_noAG" / "ntgs_target_clusters_noAG.gpkg", layer="noAG_polygons")

fp_base = pd.read_csv(paths.artifacts_dir / "baseline" / "cluster_fingerprint_baseline.csv")

map_anomaly_score(grid_base, str(paths.figures_dir/"fig1_anomaly_score_baseline.png"),
                  "Anomaly score (Isolation Forest) — NTGS Stream Sediments (1 km grid, baseline)")
map_targets(grid_base, targets_base, cent_base, str(paths.figures_dir/"fig2_target_clusters_baseline.png"),
            "Target clusters (baseline) — polygons colored by priority_score; labels shifted up-left")
map_robustness(targets_base, targets_noag, grid_base, str(paths.figures_dir/"fig3_robustness_overlay.png"),
               "Robustness overlay — Baseline polygons (fill) vs noAG polygons (outline)")
plot_score_hist(grid_base, str(paths.figures_dir/"fig4_hist_anomaly_score_baseline.png"),
                "Distribution of anomaly_score (baseline)")
plot_npoints_scatter(grid_base, str(paths.figures_dir/"fig5_scatter_npoints_vs_score.png"),
                     "n_points vs anomaly_score (baseline)")
plot_fingerprint_heatmap(fp_base, str(paths.figures_dir/"fig6_fingerprint_heatmap_baseline.png"),
                         "Cluster fingerprint heatmap (baseline): median(log10) cluster - background")

print("Saved figures to:", paths.figures_dir)
