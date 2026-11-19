"""Reusable schema and quality checks for the employee EDA sample."""
from __future__ import annotations

import numpy as np
import pandas as pd

EXPECTED_COLUMNS = [
    "id", "groups", "age", "healthy_eating", "active_lifestyle", "salary"
]
NUMERIC_COLUMNS = ["id", "age", "healthy_eating", "active_lifestyle", "salary"]
MEASURE_COLUMNS = ["age", "healthy_eating", "active_lifestyle", "salary"]


def validate_employee_data(frame: pd.DataFrame) -> pd.DataFrame:
    """Validate the sample without mutating it; return the original frame."""
    if not isinstance(frame, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")
    if frame.empty:
        raise ValueError("Employee dataset is empty.")
    if frame.columns.tolist() != EXPECTED_COLUMNS:
        raise ValueError(f"Expected columns in this order: {EXPECTED_COLUMNS}")
    if frame.isna().any().any():
        raise ValueError("Employee dataset contains missing values.")
    if frame["groups"].astype(str).str.strip().eq("").any():
        raise ValueError("Group labels must not be blank.")

    numeric = frame[NUMERIC_COLUMNS].apply(pd.to_numeric, errors="coerce")
    if numeric.isna().any().any():
        raise ValueError("Numeric fields contain non-numeric values.")
    if not np.isfinite(numeric.to_numpy(dtype=float)).all():
        raise ValueError("Numeric fields contain non-finite values.")
    if numeric["id"].duplicated().any():
        raise ValueError("Employee IDs must be unique.")
    if (numeric["age"] <= 0).any():
        raise ValueError("Age values must be greater than zero.")
    if (numeric["salary"] < 0).any():
        raise ValueError("Salary values must not be negative.")

    return frame


def _iqr_outlier_counts(numeric: pd.DataFrame) -> dict:
    """Count exploratory 1.5-IQR outliers; do not remove or alter records."""
    counts = {}
    for column in MEASURE_COLUMNS:
        q1 = float(numeric[column].quantile(0.25))
        q3 = float(numeric[column].quantile(0.75))
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        counts[column] = {
            "count": int(((numeric[column] < lower) | (numeric[column] > upper)).sum()),
            "lower_fence": round(lower, 3),
            "upper_fence": round(upper, 3),
        }
    return counts


def summarize_employee_sample(frame: pd.DataFrame) -> dict:
    """Return unit-neutral descriptive summaries without causal claims."""
    validate_employee_data(frame)
    numeric = frame[MEASURE_COLUMNS].apply(pd.to_numeric, errors="raise")
    group_labels = frame["groups"].astype("string").str.strip()
    normalized = numeric.assign(_group=group_labels)

    grouped = normalized.groupby("_group", observed=True)[MEASURE_COLUMNS].agg(
        ["count", "mean", "median", "std"]
    ).round(3)
    group_summary = {
        str(group): {
            metric: {
                statistic: (None if pd.isna(value) else round(float(value), 3))
                for statistic, value in statistics.items()
            }
            for metric, statistics in metrics.items()
        }
        for group, metrics in grouped.groupby(level=0, axis=1)
        for metric, statistics in metrics.items()
    }

    group_counts = group_labels.value_counts(dropna=False).sort_index()
    return {
        "record_count": int(len(frame)),
        "group_counts": {str(key): int(value) for key, value in group_counts.items()},
        "numeric_summary": numeric.describe(percentiles=[0.25, 0.5, 0.75]).round(3).to_dict(),
        "group_numeric_summary": group_summary,
        "iqr_outlier_review": _iqr_outlier_counts(numeric),
        "correlations": numeric.corr(method="spearman").round(4).to_dict(),
        "interpretation_note": (
            "Descriptive statistics for this supplied sample only. "
            "Salary units, group meanings, and score scales are undocumented. "
            "IQR flags are review indicators, not proof of data errors. "
            "Correlations do not establish causation."
        ),
    }
