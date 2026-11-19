# Employee Data Science Project

## Project overview

A beginner-level exploratory data analysis (EDA) project using Python. It inspects a small employee-style dataset, checks data quality, summarises variables and explores descriptive relationships.

This repository does not contain a machine-learning prediction model.

## Dataset

The notebook reads the committed `Employee Dataset.csv` file directly. The CSV is the single source of truth, avoiding a separate embedded copy inside the notebook.

The supplied CSV contains 50 records and six columns:

- `id`: record identifier
- `groups`: categorical group label
- `age`: age value
- `healthy_eating`: numeric score, scale not documented
- `active_lifestyle`: numeric score, scale not documented
- `salary`: numeric value, currency/unit not documented

The original data source, sampling method, salary unit, group definitions and score scales are not provided. Treat all findings as descriptive patterns in this sample, not as representative workforce statistics.

## Analysis workflow

1. Load the committed CSV.
2. Inspect shape, columns and data types.
3. Validate required fields and numeric values.
4. Check missing values, duplicate rows and ID uniqueness.
5. Generate descriptive statistics.
6. Plot distributions for measured numeric fields, excluding the ID.
7. Visualise the categorical group field.
8. Examine correlations among measured numeric fields.
9. Compare record counts and descriptive averages across the supplied group labels.
10. Summarise the sample and document limitations.

## Main sample observations

- 50 records and 6 columns.
- No missing values or exact duplicate rows in the supplied data.
- Four distinct values in the `groups` column.
- Mean age: 31.88.
- Mean healthy_eating score: 4.92.
- Mean active_lifestyle score: 5.90.
- Mean salary value: 2,027.50, unit not supplied.

The sample correlation between `healthy_eating` and `salary` is approximately 0.76. Correlation does not establish causation. The identifier is excluded from descriptive numeric analysis because it is not a measured attribute.

### Group-level summary

The notebook compares record counts and mean age, lifestyle scores and salary values for each supplied group label. These are descriptive sample summaries only. The dataset does not define what the group labels mean or specify the salary unit, so the table must not be interpreted as a fair-pay comparison or a population-level finding.

## Run the notebook

Run from the repository root so the notebook can find `Employee Dataset.csv`.

```bash
python -m pip install pandas numpy matplotlib seaborn jupyter nbconvert pytest
python -m pytest -q
jupyter notebook "Employee_Data_Science_Project_FINAL (1).ipynb"
```

Open the notebook and run all cells from top to bottom. The notebook reports a clear error if the CSV is missing from the working directory.

## Limitations and future improvements

- Add the original dataset source and data dictionary.
- Document the salary unit and scoring scales.
- Explain what the `groups` labels represent.
- Use a larger, documented and appropriately sampled dataset before making workforce-level claims.
- Define a valid prediction question and evaluation design before adding machine learning.

## Author

Srishti Pandey, MCA Data Science


## Group-level descriptive comparison

The notebook compares record counts and mean age, healthy-eating score, active-lifestyle score and salary value for each supplied group label. These are descriptive sample summaries only. The dataset does not define the group labels or salary unit, so the results are not a fair-pay comparison or population-level finding.

## Validation implementation

The reusable validator in `src/employee_data.py` checks the exact six-column schema, missing and non-finite values, unique IDs, positive ages and non-negative salary values. The test suite includes invalid-value and non-mutation checks. It deliberately does not impose score ranges because the source does not document their scales.
