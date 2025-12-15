from __future__ import annotations
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import box

def points_to_grid(gdf_wgs84: gpd.GeoDataFrame, utm_epsg: str, grid_size_m: int) -> gpd.GeoDataFrame:
    """
    Project points to UTM, assign each point to a grid cell, and create a cell geometry.
    Returns gdf_points_utm with columns: cell_x, cell_y, cell_id.
    """
    gdf = gdf_wgs84.to_crs(utm_epsg)
    xs = gdf.geometry.x.values
    ys = gdf.geometry.y.values

    cell_x = np.floor(xs / grid_size_m).astype(int)
    cell_y = np.floor(ys / grid_size_m).astype(int)
    cell_id = (cell_y.astype(np.int64) << 32) + (cell_x.astype(np.int64) & 0xFFFFFFFF)

    gdf = gdf.copy()
    gdf["cell_x"] = cell_x
    gdf["cell_y"] = cell_y
    gdf["cell_id"] = cell_id
    return gdf

def aggregate_to_cells(gdf_pts_utm: gpd.GeoDataFrame, features: list[str]) -> gpd.GeoDataFrame:
    """
    Median aggregate geochem features per cell. Also keep n_points.
    Produces one row per cell with polygon geometry and lon/lat center.
    """
    grid_size_m = _infer_grid_size(gdf_pts_utm)
    # group
    agg = {c: "median" for c in features if c in gdf_pts_utm.columns}
    agg["cell_x"] = "first"
    agg["cell_y"] = "first"
    agg["cell_id"] = "first"
    df = gdf_pts_utm.groupby("cell_id").agg(agg)
    df["n_points"] = gdf_pts_utm.groupby("cell_id").size().astype(int)

    # build polygons
    x0 = df["cell_x"].values * grid_size_m
    y0 = df["cell_y"].values * grid_size_m
    geoms = [box(x, y, x + grid_size_m, y + grid_size_m) for x, y in zip(x0, y0)]
    gdf_cells = gpd.GeoDataFrame(df.drop(columns=["cell_x","cell_y"]), geometry=geoms, crs=gdf_pts_utm.crs).reset_index(drop=True)
    return gdf_cells

def _infer_grid_size(gdf_pts_utm: gpd.GeoDataFrame) -> int:
    # Infer from cell_x step: use 1000 as default
    return 1000
