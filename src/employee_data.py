"""Reusable validation and descriptive summaries for the employee EDA sample."""
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


def summarize_employee_data(frame: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Return sample-level distribution and group summaries.

    The ID is excluded from measured-variable statistics. Group results are
    descriptive only; no meaning is assigned to group labels or salary units.
    """
    validate_employee_data(frame)
    measures = frame[MEASURE_COLUMNS].apply(pd.to_numeric, errors="raise")

    distribution = measures.agg(
        ["count", "mean", "median", "std", "min", "max"]
    ).T
    distribution["q1"] = measures.quantile(0.25)
    distribution["q3"] = measures.quantile(0.75)
    distribution = distribution[
        ["count", "mean", "median", "std", "min", "q1", "q3", "max"]
    ].round(2)
    distribution.index.name = "measure"

    grouped = frame.groupby("groups", observed=True).agg(
        record_count=("id", "count"),
        mean_age=("age", "mean"),
        mean_healthy_eating=("healthy_eating", "mean"),
        mean_active_lifestyle=("active_lifestyle", "mean"),
        mean_salary_value=("salary", "mean"),
    )
    grouped["record_share_pct"] = (
        grouped["record_count"] / len(frame) * 100
    )
    grouped = grouped[
        [
            "record_count", "record_share_pct", "mean_age",
            "mean_healthy_eating", "mean_active_lifestyle", "mean_salary_value",
        ]
    ].round(2)
    grouped.index.name = "group_label"

    return {"distribution": distribution, "group_summary": grouped}
