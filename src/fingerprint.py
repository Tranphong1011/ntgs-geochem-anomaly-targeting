from __future__ import annotations
import pandas as pd
from .preprocess import fix_and_log10, median_impute

def cluster_fingerprint(grid_scored: pd.DataFrame, anom_with_clusters: pd.DataFrame, features: list[str], out_csv: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Per-cluster fingerprint: median(log10(feature))_cluster - median(log10(feature))_background
    Writes long CSV: cluster_id, element, delta_log10
    """
    X_bg, keep_cols, dropped = fix_and_log10(grid_scored, features)
    X_bg = median_impute(X_bg)
    bg_med = X_bg.median(numeric_only=True)

    cl = anom_with_clusters[anom_with_clusters["cluster_id"] != -1].copy()
    X_cl, keep_cols2, dropped2 = fix_and_log10(cl, features)
    X_cl = median_impute(X_cl)
    X_cl["cluster_id"] = cl["cluster_id"].to_numpy()

    cl_med = X_cl.groupby("cluster_id")[keep_cols2].median(numeric_only=True)
    delta = cl_med.subtract(bg_med[keep_cols2], axis=1)

    delta_long = (
        delta.reset_index()
             .melt(id_vars="cluster_id", var_name="element", value_name="delta_log10")
             .sort_values(["cluster_id","delta_log10"], ascending=[True, False])
    )
    delta_long.to_csv(out_csv, index=False)
    return delta, delta_long
