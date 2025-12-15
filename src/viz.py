from __future__ import annotations
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

try:
    import contextily as ctx
    HAS_BASEMAP = True
except Exception:
    HAS_BASEMAP = False

def _add_basemap(ax):
    if HAS_BASEMAP:
        ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, attribution_size=6)

def map_anomaly_score(grid: gpd.GeoDataFrame, out_png: str, title: str):
    fig, ax = plt.subplots(figsize=(11,11))
    grid.plot(column="anomaly_score", ax=ax, legend=True, linewidth=0, alpha=0.95)
    _add_basemap(ax)
    ax.set_title(title)
    ax.set_axis_off()
    plt.tight_layout()
    plt.savefig(out_png, dpi=300)
    plt.close()

def map_targets(grid: gpd.GeoDataFrame, polys: gpd.GeoDataFrame, cents_wgs: gpd.GeoDataFrame,
                out_png: str, title: str, label_n: int = 10):
    # CRS
    if HAS_BASEMAP:
        grid_p = grid.to_crs("EPSG:3857")
        polys_p = polys.to_crs("EPSG:3857")
        cents = cents_wgs.copy()
        cents = cents.set_geometry(gpd.points_from_xy(cents["lon"], cents["lat"]), crs="EPSG:4326").to_crs("EPSG:3857")
    else:
        grid_p = grid
        polys_p = polys.to_crs(grid.crs)
        cents = cents_wgs.copy()
        cents = cents.set_geometry(gpd.points_from_xy(cents["lon"], cents["lat"]), crs="EPSG:4326").to_crs(grid.crs)

    fig, ax = plt.subplots(figsize=(11,11))
    grid_p.plot(column="anomaly_score", ax=ax, alpha=0.25, linewidth=0, legend=False)
    polys_p.plot(column="priority_score", ax=ax, alpha=0.55, edgecolor="black", linewidth=0.4, legend=True)
    top = cents.sort_values("priority_score", ascending=False).head(label_n)
    for _, r in top.iterrows():
        ax.annotate(str(int(r["cluster_id"])),
                    xy=(r.geometry.x, r.geometry.y),
                    xytext=(-3,2),
                    textcoords="offset points",
                    fontsize=6,
                    ha="center", va="center")
    _add_basemap(ax)
    ax.set_title(title)
    ax.set_axis_off()
    plt.tight_layout()
    plt.savefig(out_png, dpi=300)
    plt.close()

def map_robustness(polys_base: gpd.GeoDataFrame, polys_noag: gpd.GeoDataFrame, extent_ref: gpd.GeoDataFrame,
                   out_png: str, title: str):
    if HAS_BASEMAP:
        base = polys_base.to_crs("EPSG:3857")
        noag = polys_noag.to_crs("EPSG:3857")
        ref = extent_ref.to_crs("EPSG:3857")
    else:
        base = polys_base
        noag = polys_noag.to_crs(polys_base.crs)
        ref = extent_ref

    fig, ax = plt.subplots(figsize=(11,11))
    xmin, ymin, xmax, ymax = ref.total_bounds
    ax.set_xlim(xmin, xmax); ax.set_ylim(ymin, ymax)
    base.plot(ax=ax, alpha=0.35, edgecolor="black", linewidth=0.4)
    noag.boundary.plot(ax=ax, linewidth=1.0)
    _add_basemap(ax)
    ax.set_title(title)
    ax.set_axis_off()
    plt.tight_layout()
    plt.savefig(out_png, dpi=300)
    plt.close()

def plot_score_hist(grid: gpd.GeoDataFrame, out_png: str, title: str):
    fig, ax = plt.subplots(figsize=(9,5))
    ax.hist(grid["anomaly_score"].values, bins=60)
    ax.set_title(title)
    ax.set_xlabel("anomaly_score (higher = more anomalous)")
    ax.set_ylabel("count")
    plt.tight_layout()
    plt.savefig(out_png, dpi=300)
    plt.close()

def plot_npoints_scatter(grid: gpd.GeoDataFrame, out_png: str, title: str):
    fig, ax = plt.subplots(figsize=(9,5))
    ax.scatter(grid["n_points"], grid["anomaly_score"], s=6)
    ax.set_xscale("log")
    ax.set_title(title)
    ax.set_xlabel("n_points in cell")
    ax.set_ylabel("anomaly_score")
    plt.tight_layout()
    plt.savefig(out_png, dpi=300)
    plt.close()

def plot_fingerprint_heatmap(fp_long: pd.DataFrame, out_png: str, title: str):
    mat = fp_long.pivot_table(index="cluster_id", columns="element", values="delta_log10", aggfunc="mean")
    mat = mat.loc[mat.index.sort_values()]
    fig, ax = plt.subplots(figsize=(12,6))
    img = ax.imshow(mat.values, aspect="auto")
    ax.set_title(title)
    ax.set_yticks(np.arange(len(mat.index)))
    ax.set_yticklabels(mat.index.astype(int))
    ax.set_xticks(np.arange(len(mat.columns)))
    ax.set_xticklabels(mat.columns, rotation=90)
    fig.colorbar(img, ax=ax, fraction=0.02, pad=0.02, label="delta_log10")
    plt.tight_layout()
    plt.savefig(out_png, dpi=300)
    plt.close()
