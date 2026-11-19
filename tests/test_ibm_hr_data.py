from pathlib import Path

import pandas as pd
import pytest

from src.ibm_hr_data import (
    EXPECTED_COLUMNS,
    grouped_attrition,
    income_quartile_attrition,
    load_ibm_hr_data,
    summarize_attrition,
    validate_ibm_hr_data,
)

DATA = Path(__file__).resolve().parents[1] / "data" / "raw" / "ibm_hr_attrition.csv"


def test_benchmark_dataset_shape_and_schema():
    frame = pd.read_csv(DATA)
    assert frame.shape == (1470, 35)
    assert frame.columns.tolist() == EXPECTED_COLUMNS


def test_loader_validates_dataset_and_target_categories():
    frame = load_ibm_hr_data(DATA)
    assert len(frame) == 1470
    assert set(frame["Attrition"].unique()) == {"Yes", "No"}


def test_employee_number_is_unique_and_source_has_no_missing_values():
    frame = load_ibm_hr_data(DATA)
    assert frame["EmployeeNumber"].is_unique
    assert not frame.isna().any().any()


def test_constant_source_fields_are_constant():
    frame = load_ibm_hr_data(DATA)
    for column in ("EmployeeCount", "Over18", "StandardHours"):
        assert frame[column].nunique(dropna=False) == 1


@pytest.mark.parametrize(
    ("column", "value", "message"),
    [
        ("Attrition", "Maybe", "Attrition"),
        ("OverTime", "Sometimes", "OverTime"),
        ("Age", -1, "Age"),
        ("MonthlyIncome", -100, "MonthlyIncome"),
        ("EmployeeNumber", 1, "unique"),
        ("Department", "   ", "blank"),
    ],
)
def test_validator_rejects_invalid_values(column, value, message):
    frame = pd.read_csv(DATA)
    frame[column] = frame[column].astype(object)
    frame.loc[1, column] = value
    with pytest.raises(ValueError, match=message):
        validate_ibm_hr_data(frame)


def test_validator_rejects_missing_values():
    frame = pd.read_csv(DATA)
    frame.loc[0, "Department"] = None
    with pytest.raises(ValueError, match="missing"):
        validate_ibm_hr_data(frame)


def test_validator_rejects_changed_schema():
    frame = pd.read_csv(DATA).rename(columns={"Age": "EmployeeAge"})
    with pytest.raises(ValueError, match="schema"):
        validate_ibm_hr_data(frame)


def test_grouped_attrition_percentages_are_consistent():
    frame = load_ibm_hr_data(DATA)
    result = grouped_attrition(frame, "Department")
    assert result["records"].sum() == len(frame)
    assert result["attrition_records"].sum() == frame["Attrition"].eq("Yes").sum()
    assert result["attrition_share_percent"].between(0, 100).all()


def test_income_quartile_table_covers_all_records():
    frame = load_ibm_hr_data(DATA)
    result = income_quartile_attrition(frame)
    assert result["records"].sum() == len(frame)
    assert result["attrition_share_percent"].between(0, 100).all()


def test_summary_excludes_identifier_and_constant_fields_from_numeric_description():
    frame = load_ibm_hr_data(DATA)
    result = summarize_attrition(frame)
    assert result["records"] == 1470
    assert result["fields"] == 35
    assert "EmployeeNumber" not in result["numeric_summary"].columns
    assert "EmployeeCount" not in result["numeric_summary"].columns
    assert "StandardHours" not in result["numeric_summary"].columns
    assert result["attrition_records"] + result["non_attrition_records"] == 1470


def test_analysis_summary_does_not_modify_source_frame():
    frame = load_ibm_hr_data(DATA)
    original = frame.copy(deep=True)
    summarize_attrition(frame)
    pd.testing.assert_frame_equal(frame, original)



def test_income_quartiles_handle_all_tied_values():
    frame = load_ibm_hr_data(DATA)
    frame["MonthlyIncome"] = 5000
    result = income_quartile_attrition(frame)
    assert result["records"].sum() == len(frame)
    assert result["income_quartile"].tolist() == ["Single income value"]


def test_grouped_attrition_rejects_unknown_grouping_column():
    frame = load_ibm_hr_data(DATA)
    with pytest.raises(ValueError, match="Unknown grouping column"):
        grouped_attrition(frame, "NotARealField")


def test_sql_queries_execute_against_imported_benchmark(tmp_path):
    import sqlite3

    sql_path = Path(__file__).resolve().parents[1] / "sql" / "employee_attrition_analysis.sql"
    frame = load_ibm_hr_data(DATA)
    database = tmp_path / "test_employee.db"
    with sqlite3.connect(database) as connection:
        frame.to_sql("employee_attrition", connection, index=False, if_exists="replace")
        connection.executescript(sql_path.read_text(encoding="utf-8"))
        count = connection.execute(
            "SELECT COUNT(*) FROM employee_attrition"
        ).fetchone()[0]
        assert count == 1470


def test_analysis_script_exports_valid_json_tables_and_charts(tmp_path):
    import json
    from scripts.analyze_ibm_hr import run_analysis

    summary = run_analysis(DATA, tmp_path)
    report = json.loads((tmp_path / "attrition_summary.json").read_text(encoding="utf-8"))
    assert summary["records"] == 1470
    assert report["records"] == 1470
    for filename in (
        "by_department.csv",
        "by_job_role.csv",
        "by_overtime.csv",
        "by_job_satisfaction_code.csv",
        "by_income_quartile.csv",
        "attrition_overall.png",
        "attrition_by_department.png",
        "attrition_by_income_quartile.png",
    ):
        assert (tmp_path / filename).is_file()
        assert (tmp_path / filename).stat().st_size > 0
