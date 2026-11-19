# Employee Data Science Project

## Project overview

A beginner-level exploratory data analysis (EDA) project using Python. It inspects a small employee-style dataset, checks data quality, summarizes variables and explores descriptive relationships.

This repository does not contain a machine-learning prediction model.

## Dataset

The committed `Employee Dataset.csv` contains 50 records and six columns:

- `id`: record identifier
- `groups`: categorical group label
- `age`: age value
- `healthy_eating`: numeric score, scale not documented
- `active_lifestyle`: numeric score, scale not documented
- `salary`: numeric value, currency/unit not documented

The original data source, sampling method, salary unit, group definitions and score scales are not provided. Treat all findings as descriptive patterns in this sample, not as representative workforce statistics.

## Analysis workflow

1. Load and validate the committed CSV.
2. Inspect shape, columns, data types, missing values and duplicate rows.
3. Summarize measured numeric fields, excluding the record identifier.
4. Compare group counts and group-wise count, mean, median and standard deviation.
5. Calculate Spearman rank correlations among measured numeric fields.
6. Flag potential 1.5-IQR outliers for review without deleting records.
7. Document the sample limitations and avoid causal or population-level claims.

## Reusable analysis

`src/employee_data.py` provides:

- `validate_employee_data(frame)`: checks schema, missing/non-finite values, unique IDs, positive ages and non-negative salary values.
- `summarize_employee_sample(frame)`: returns overall statistics, group-wise summaries, Spearman correlations and IQR review flags.

IQR flags identify observations for inspection. They do not establish that a record is wrong, and no record is automatically removed.

## Run locally

```bash
python -m pip install pandas numpy matplotlib seaborn jupyter nbconvert pytest
python -m pytest -q
jupyter notebook "Employee_Data_Science_Project_FINAL (1).ipynb"
```

Run the notebook from the repository root so it can locate the CSV.

## Limitations and future improvements

- Add the original dataset source and a data dictionary.
- Document salary units and lifestyle score scales.
- Explain the supplied group labels.
- Use a larger, documented and appropriately sampled dataset before making workforce-level claims.
- Define a valid prediction question and evaluation design before adding machine learning.

## Author

Srishti Pandey, MCA Data Science
