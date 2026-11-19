from pathlib import Path

import numpy as np
import pandas as pd
import pytest

DATA_PATH = Path(__file__).resolve().parents[1] / "Employee Dataset.csv"
EXPECTED_COLUMNS = ["id", "groups", "age", "healthy_eating", "active_lifestyle", "salary"]
NUMERIC_COLUMNS = ["id", "age", "healthy_eating", "active_lifestyle", "salary"]


def load_data():
    return pd.read_csv(DATA_PATH)


def test_dataset_shape_and_schema():
    df = load_data()
    assert df.shape == (50, 6)
    assert df.columns.tolist() == EXPECTED_COLUMNS


def test_identifiers_are_unique_and_complete():
    df = load_data()
    assert df["id"].notna().all()
    assert df["id"].is_unique


def test_numeric_columns_are_finite_and_complete():
    df = load_data()
    numeric = df[NUMERIC_COLUMNS].apply(pd.to_numeric, errors="raise")
    assert numeric.notna().all().all()
    assert np.isfinite(numeric.to_numpy(dtype=float)).all()


def test_age_and_salary_domain_constraints():
    df = load_data()
    assert (df["age"] > 0).all()
    assert (df["salary"] >= 0).all()


def test_group_labels_are_present():
    df = load_data()
    assert df["groups"].notna().all()
    assert df["groups"].astype(str).str.strip().ne("").all()


def test_dataset_has_no_exact_duplicate_rows():
    df = load_data()
    assert not df.duplicated().any()


def test_dataset_is_not_modified_by_loader():
    before = load_data()
    after = load_data()
    pd.testing.assert_frame_equal(before, after)


from src.employee_data import validate_employee_data


def test_validator_accepts_repository_dataset():
    assert validate_employee_data(load_data()).shape == (50, 6)


@pytest.mark.parametrize(
    ("column", "value", "message"),
    [
        ("age", 0, "Age"),
        ("salary", -1, "Salary"),
        ("groups", "   ", "blank"),
        ("age", "not-a-number", "non-numeric"),
        ("salary", float("inf"), "non-finite"),
    ],
)
def test_validator_rejects_invalid_values(column, value, message):
    df = load_data()
    df[column] = df[column].astype(object)
    df.loc[0, column] = value
    with pytest.raises(ValueError, match=message):
        validate_employee_data(df)


def test_validator_rejects_duplicate_ids():
    df = load_data()
    df.loc[1, "id"] = df.loc[0, "id"]
    with pytest.raises(ValueError, match="unique"):
        validate_employee_data(df)


def test_validator_does_not_mutate_input():
    df = load_data()
    original = df.copy(deep=True)
    validate_employee_data(df)
    pd.testing.assert_frame_equal(df, original)


from src.employee_data import summarize_employee_sample


def test_sample_summary_is_unit_neutral_and_complete():
    result = summarize_employee_sample(load_data())
    assert result["record_count"] == 50
    assert sum(result["group_counts"].values()) == 50
    assert set(result["numeric_summary"]) == {
        "age", "healthy_eating", "active_lifestyle", "salary"
    }
    assert "do not establish causation" in result["interpretation_note"]


def test_sample_summary_rejects_invalid_input():
    df = load_data()
    df.loc[0, "age"] = 0
    with pytest.raises(ValueError, match="Age"):
        summarize_employee_sample(df)


def test_sample_summary_normalizes_group_label_whitespace():
    df = load_data()
    original_a_count = int(df["groups"].eq("A").sum())
    df.loc[0, "groups"] = " A "
    result = summarize_employee_sample(df)
    assert result["group_counts"]["A"] == original_a_count
    assert sum(result["group_counts"].values()) == len(df)

