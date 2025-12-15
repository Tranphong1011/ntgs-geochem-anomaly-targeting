from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Paths:
    repo_root: Path
    raw_gpkg: Path
    artifacts_dir: Path
    figures_dir: Path

@dataclass(frozen=True)
class GridConfig:
    utm_epsg: str = "EPSG:32753"   # UTM zone 53S fits NT reasonably
    grid_size_m: int = 1000        # 1 km grid

@dataclass(frozen=True)
class ModelConfig:
    contamination: float = 0.03
    random_state: int = 42

@dataclass(frozen=True)
class ClusterConfig:
    eps_m: int = 2000
    min_samples: int = 3
    buffer_m: int = 500            # for nicer polygons

# Feature sets
FEATURES_BASELINE = [
    "CU_PPM","PB_PPM","ZN_PPM","AU_PPB","AS_PPM","MN_PPM","FE_PCT",
    "CO_PPM","NI_PPM","AG_PPM","MO_PPM","U_PPM","CR_PPM","BI_PPM"
]
FEATURES_NOAG = [
    "CU_PPM","PB_PPM","ZN_PPM","AU_PPB","AS_PPM","MN_PPM","FE_PCT",
    "CO_PPM","NI_PPM","MO_PPM","U_PPM","CR_PPM","BI_PPM"
]

def default_paths(repo_root: str | Path) -> Paths:
    repo_root = Path(repo_root).resolve()
    return Paths(
        repo_root=repo_root,
        raw_gpkg=repo_root / "data" / "raw" / "ntgs_stream_sediments.gpkg",
        artifacts_dir=repo_root / "artifacts",
        figures_dir=repo_root / "figures",
    )
