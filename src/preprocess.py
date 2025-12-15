from __future__ import annotations
import numpy as np
import pandas as pd

def replace_nonpositive_with_half_minpos(s: pd.Series) -> pd.Series:
    """
    Many geochem columns contain <=0 values due to detection limits (e.g., -0.1).
    For log10 transform, replace non-positive with (min_positive / 2).
    """
    x = s.copy()
    x = pd.to_numeric(x, errors="coerce")
    pos = x[x > 0]
    if pos.empty:
        return x  # caller should drop this column if desired
    min_pos = float(pos.min())
    repl = min_pos / 2.0
    x.loc[x <= 0] = repl
    return x

def fix_and_log10(df: pd.DataFrame, features: list[str]) -> tuple[pd.DataFrame, list[str], list[str]]:
    """
    Returns X (log10 transformed), keep_cols, dropped_all_nonpos.
    Only keeps columns present in df.
    """
    keep = [c for c in features if c in df.columns]
    dropped = []
    out = {}
    for c in keep:
        s = pd.to_numeric(df[c], errors="coerce")
        # if no positive values, drop
        if not (s > 0).any():
            dropped.append(c)
            continue
        s2 = replace_nonpositive_with_half_minpos(s)
        out[c] = np.log10(s2.astype(float))
    X = pd.DataFrame(out, index=df.index)
    keep2 = [c for c in keep if c not in dropped]
    return X, keep2, dropped

def median_impute(X: pd.DataFrame) -> pd.DataFrame:
    """Median imputation for missing values."""
    return X.fillna(X.median(numeric_only=True))
