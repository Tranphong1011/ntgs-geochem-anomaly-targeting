from __future__ import annotations
import numpy as np
import pandas as pd
import geopandas as gpd
from sklearn.cluster import DBSCAN
from shapely.geometry import Point
from shapely.ops import unary_union

def dbscan_clusters(anom_cells: gpd.GeoDataFrame, eps_m: float, min_samples: int) -> gpd.GeoDataFrame:
    """
    Cluster anomaly cells using DBSCAN on cell centroids (UTM meters).
    Returns anom_cells with cluster_id.
    """
    gdf = anom_cells.copy()
    cent = gdf.geometry.centroid
    X = np.c_[cent.x.values, cent.y.values]
    model = DBSCAN(eps=eps_m, min_samples=min_samples, metric="euclidean")
    labels = model.fit_predict(X)
    gdf["cluster_id"] = labels
    return gdf

def clusters_to_polygons(anom_with_clusters: gpd.GeoDataFrame, buffer_m: float) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    """
    Make one polygon per cluster (excluding -1), and centroids (WGS84 columns lon/lat).
    Returns (polygons_utm, centroids_wgs84)
    """
    gdf = anom_with_clusters[anom_with_clusters["cluster_id"] != -1].copy()
    polys = []
    rows = []
    for cid, grp in gdf.groupby("cluster_id"):
        geom = unary_union(grp.geometry.values).buffer(buffer_m)
        polys.append(geom)
        rows.append({
            "cluster_id": int(cid),
            "n_cells": int(len(grp)),
            "mean_score": float(grp["anomaly_score"].mean()),
            "max_score": float(grp["anomaly_score"].max()),
            "mean_points": float(grp["n_points"].mean()),
        })

    poly_gdf = gpd.GeoDataFrame(rows, geometry=polys, crs=gdf.crs)
    poly_gdf["priority_score"] = poly_gdf["n_cells"] * poly_gdf["mean_score"]

    # centroids: keep lon/lat columns for easy table export
    cent_utm = poly_gdf.copy()
    cent_utm["geometry"] = cent_utm.geometry.centroid
    cent_wgs = cent_utm.to_crs("EPSG:4326")
    cent_wgs["lon"] = cent_wgs.geometry.x
    cent_wgs["lat"] = cent_wgs.geometry.y
    return poly_gdf, cent_wgs

def top_targets_table(centroids_wgs84: gpd.GeoDataFrame, out_csv: str | None = None) -> pd.DataFrame:
    cols = ["cluster_id","n_cells","mean_score","max_score","mean_points","lon","lat","priority_score"]
    df = centroids_wgs84[cols].sort_values("priority_score", ascending=False).reset_index(drop=True)
    if out_csv:
        df.to_csv(out_csv, index=False)
    return df
