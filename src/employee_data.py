"""Reusable schema and quality checks for the employee EDA sample."""
from __future__ import annotations

import numpy as np
import pandas as pd

EXPECTED_COLUMNS = [
    "id", "groups", "age", "healthy_eating", "active_lifestyle", "salary"
]
NUMERIC_COLUMNS = ["id", "age", "healthy_eating", "active_lifestyle", "salary"]


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
