from __future__ import annotations
from pathlib import Path
import geopandas as gpd

def read_points_gpkg(path: str | Path, layer: str | None = None) -> gpd.GeoDataFrame:
    """Read NTGS points as GeoDataFrame. Expects geometry column present."""
    path = Path(path)
    gdf = gpd.read_file(path, layer=layer) if layer else gpd.read_file(path)
    if gdf.crs is None:
        # Most NTGS layers are EPSG:4283 (GDA94) but keep it explicit if missing
        gdf = gdf.set_crs("EPSG:4283")
    return gdf

def write_gpkg(gdf: gpd.GeoDataFrame, path: str | Path, layer: str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    gdf.to_file(path, layer=layer, driver="GPKG")
