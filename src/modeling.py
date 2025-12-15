from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import RobustScaler

from .preprocess import fix_and_log10, median_impute

def score_iforest(cells_df: pd.DataFrame, features: list[str], contamination: float, random_state: int) -> tuple[pd.DataFrame, dict]:
    """
    Returns cells_df with anomaly_score column (higher = more anomalous)
    and meta dict.
    """
    X_log, keep_cols, dropped = fix_and_log10(cells_df, features)
    X_imp = median_impute(X_log)

    scaler = RobustScaler()
    Xs = scaler.fit_transform(X_imp)

    clf = IsolationForest(
        n_estimators=300,
        contamination=contamination,
        random_state=random_state,
        n_jobs=-1
    )
    clf.fit(Xs)

    # sklearn score_samples: higher = less abnormal. invert to "anomaly_score".
    score = -clf.score_samples(Xs)

    out = cells_df.copy()
    out["anomaly_score"] = score

    meta = {
        "features_requested": features,
        "features_used": keep_cols,
        "dropped_all_nonpositive": dropped,
        "contamination": contamination,
        "random_state": random_state,
        "n_cells": int(len(out)),
    }
    return out, meta

def mark_anomalies(df_scored: pd.DataFrame, contamination: float) -> tuple[pd.DataFrame, float]:
    """
    Mark top contamination fraction as anomalies.
    Returns df with is_anomaly and threshold (quantile).
    """
    thr = float(np.quantile(df_scored["anomaly_score"].values, 1.0 - contamination))
    out = df_scored.copy()
    out["is_anomaly"] = (out["anomaly_score"] >= thr).astype(int)
    return out, thr
