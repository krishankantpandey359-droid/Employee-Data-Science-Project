"""Validation and descriptive analysis for the IBM HR Attrition benchmark."""
from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

EXPECTED_COLUMNS = [
    "Age", "Attrition", "BusinessTravel", "DailyRate", "Department",
    "DistanceFromHome", "Education", "EducationField", "EmployeeCount",
    "EmployeeNumber", "EnvironmentSatisfaction", "Gender", "HourlyRate",
    "JobInvolvement", "JobLevel", "JobRole", "JobSatisfaction",
    "MaritalStatus", "MonthlyIncome", "MonthlyRate", "NumCompaniesWorked",
    "Over18", "OverTime", "PercentSalaryHike", "PerformanceRating",
    "RelationshipSatisfaction", "StandardHours", "StockOptionLevel",
    "TotalWorkingYears", "TrainingTimesLastYear", "WorkLifeBalance",
    "YearsAtCompany", "YearsInCurrentRole", "YearsSinceLastPromotion",
    "YearsWithCurrManager",
]
NUMERIC_COLUMNS = [
    "Age", "DailyRate", "DistanceFromHome", "Education", "EmployeeCount",
    "EmployeeNumber", "EnvironmentSatisfaction", "HourlyRate", "JobInvolvement",
    "JobLevel", "JobSatisfaction", "MonthlyIncome", "MonthlyRate",
    "NumCompaniesWorked", "PercentSalaryHike", "PerformanceRating",
    "RelationshipSatisfaction", "StandardHours", "StockOptionLevel",
    "TotalWorkingYears", "TrainingTimesLastYear", "WorkLifeBalance",
    "YearsAtCompany", "YearsInCurrentRole", "YearsSinceLastPromotion",
    "YearsWithCurrManager",
]
IDENTIFIER_COLUMNS = ["EmployeeNumber"]
CONSTANT_COLUMNS = ["EmployeeCount", "Over18", "StandardHours"]
ATTRITION_LABELS = {"Yes", "No"}


def validate_ibm_hr_data(frame: pd.DataFrame) -> pd.DataFrame:
    """Validate benchmark schema and basic domains without mutating the input."""
    if not isinstance(frame, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")
    if frame.empty:
        raise ValueError("IBM HR dataset is empty.")
    if frame.columns.tolist() != EXPECTED_COLUMNS:
        raise ValueError("IBM HR dataset schema or column order does not match the documented 35-column schema.")
    if frame.isna().any().any():
        raise ValueError("IBM HR dataset contains missing values.")
    for column in ("Attrition", "OverTime"):
        values = set(frame[column].astype(str).str.strip().unique())
        if values != ATTRITION_LABELS:
            raise ValueError(f"{column} must contain only Yes and No.")
    for column in frame.select_dtypes(include=["object", "string"]).columns:
        if frame[column].astype(str).str.strip().eq("").any():
            raise ValueError(f"{column} contains blank category values.")
    numeric = frame[NUMERIC_COLUMNS].apply(pd.to_numeric, errors="coerce")
    if numeric.isna().any().any():
        raise ValueError("IBM HR numeric fields contain non-numeric values.")
    if not np.isfinite(numeric.to_numpy(dtype=float)).all():
        raise ValueError("IBM HR numeric fields contain non-finite values.")
    if numeric["EmployeeNumber"].duplicated().any():
        raise ValueError("EmployeeNumber values must be unique.")
    if (numeric["Age"] <= 0).any():
        raise ValueError("Age must be greater than zero.")
    if (numeric["MonthlyIncome"] < 0).any():
        raise ValueError("MonthlyIncome must not be negative.")
    for column in CONSTANT_COLUMNS:
        if frame[column].nunique(dropna=False) != 1:
            raise ValueError(f"{column} is expected to be constant in this supplied benchmark.")
    return frame


def load_ibm_hr_data(path: str | Path) -> pd.DataFrame:
    """Load and validate the IBM HR benchmark CSV."""
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(f"IBM HR dataset not found: {source}")
    frame = pd.read_csv(source)
    validate_ibm_hr_data(frame)
    return frame


def grouped_attrition(frame: pd.DataFrame, column: str) -> pd.DataFrame:
    """Calculate descriptive attrition counts and shares for one category."""
    validate_ibm_hr_data(frame)
    if column not in frame.columns:
        raise ValueError(f"Unknown grouping column: {column}")
    grouped = frame.groupby(column, dropna=False).agg(
        records=("Attrition", "size"),
        attrition_records=("Attrition", lambda values: int(values.eq("Yes").sum())),
    ).reset_index()
    grouped["attrition_share_percent"] = (
        grouped["attrition_records"] / grouped["records"] * 100
    ).round(2)
    return grouped.sort_values(
        ["attrition_share_percent", "records"], ascending=[False, False]
    ).reset_index(drop=True)


def income_quartile_attrition(frame: pd.DataFrame) -> pd.DataFrame:
    """Compare attrition shares across sample-defined MonthlyIncome quartiles."""
    validate_ibm_hr_data(frame)
    result = frame[["MonthlyIncome", "Attrition"]].copy()
    quartile_codes = pd.qcut(
        result["MonthlyIncome"], q=4, labels=False, duplicates="drop"
    )
    actual_quartiles = int(quartile_codes.nunique(dropna=True))
    quartile_names = {
        code: (
            "Q1 (lowest)" if code == 0 else
            "Q4 (highest)" if code == actual_quartiles - 1 else
            f"Q{code + 1}"
        )
        for code in range(actual_quartiles)
    }
    result["income_quartile"] = quartile_codes.map(quartile_names)
    grouped = result.groupby("income_quartile", observed=True).agg(
        records=("Attrition", "size"),
        attrition_records=("Attrition", lambda values: int(values.eq("Yes").sum())),
        median_income_value=("MonthlyIncome", "median"),
    ).reset_index()
    grouped["attrition_share_percent"] = (
        grouped["attrition_records"] / grouped["records"] * 100
    ).round(2)
    return grouped


def summarize_attrition(frame: pd.DataFrame) -> dict:
    """Return sample-level attrition metrics and descriptive group tables."""
    validate_ibm_hr_data(frame)
    total = len(frame)
    attrition_records = int(frame["Attrition"].eq("Yes").sum())
    measures = [
        column for column in NUMERIC_COLUMNS
        if column not in IDENTIFIER_COLUMNS + CONSTANT_COLUMNS
    ]
    numeric_summary = frame[measures].describe().round(2)
    return {
        "records": int(total),
        "fields": int(frame.shape[1]),
        "attrition_records": attrition_records,
        "non_attrition_records": int(total - attrition_records),
        "attrition_share_percent": round(attrition_records / total * 100, 2),
        "by_department": grouped_attrition(frame, "Department"),
        "by_job_role": grouped_attrition(frame, "JobRole"),
        "by_overtime": grouped_attrition(frame, "OverTime"),
        "by_job_satisfaction_code": grouped_attrition(frame, "JobSatisfaction"),
        "by_income_quartile": income_quartile_attrition(frame),
        "numeric_summary": numeric_summary,
        "numeric_measure_columns": measures,
        "identifier_excluded_from_numeric_summary": IDENTIFIER_COLUMNS,
        "constant_fields_excluded_from_numeric_summary": CONSTANT_COLUMNS,
        "interpretation_note": (
            "Descriptive results for this static public benchmark sample only. "
            "They do not estimate a current employer attrition rate, establish causes, "
            "or justify employment decisions. Monetary units and some ordinal scale "
            "labels are not defined in the upstream documentation."
        ),
    }
