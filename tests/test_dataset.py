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
