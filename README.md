# Employee Data Science Project

## Project overview

A Python exploratory data analysis (EDA) project using a small employee-style dataset. It validates data quality, describes measured variables, compares supplied group labels and explores associations. This repository does not contain a machine-learning prediction model.

## Dataset and limitations

The committed CSV contains 50 records and six columns:

| Column | Meaning in this file |
|---|---|
| `id` | Record identifier, excluded from measured-variable statistics |
| `groups` | Categorical label, meaning not documented |
| `age` | Age value |
| `healthy_eating` | Numeric score, scale not documented |
| `active_lifestyle` | Numeric score, scale not documented |
| `salary` | Numeric value, currency/unit not documented |

The original source, sampling method, group definitions, salary unit and score scales are unavailable. Treat all findings as descriptive patterns in this sample, not as representative workforce statistics or evidence of causation. Group comparisons are not fair-pay comparisons.

## Analysis workflow

1. Load the committed CSV.
2. Validate the exact schema, missing/non-finite values, unique IDs and basic value domains.
3. Inspect descriptive statistics and distributions, excluding the ID.
4. Compare record counts, sample shares and mean values across the supplied group labels.
5. Examine correlations as sample associations only.
6. Record limitations and avoid unsupported workforce-level conclusions.

## Reusable analysis module

`src/employee_data.py` provides:

- `validate_employee_data(frame)`: validates the six-column schema and basic data quality without modifying the input.
- `summarize_employee_data(frame)`: returns a distribution table with mean, median, standard deviation, quartiles and range, plus a group summary with record counts, sample shares and descriptive averages.

The summary function deliberately excludes `id` from measured-variable statistics. It preserves the supplied group labels and does not infer their meaning.

## Run locally

Run commands from the repository root:

```bash
python -m pip install pandas numpy matplotlib seaborn jupyter pytest
python -m pytest -q
jupyter notebook "Employee_Data_Science_Project_FINAL (1).ipynb"
```

Run the notebook from the repository root so it can locate `Employee Dataset.csv`.

## Known sample observations

- 50 records and 6 columns.
- No missing values or exact duplicate rows in the committed CSV.
- Four distinct values in `groups`.
- Mean age: 31.88.
- Mean healthy_eating score: 4.92.
- Mean active_lifestyle score: 5.90.
- Mean salary value: 2,027.50, unit not supplied.
- The sample correlation between `healthy_eating` and `salary` is approximately 0.76. This is association, not causation.

## Limitations and future improvements

- Identify and document the original dataset source and sampling method.
- Define the salary unit, group labels and score scales before interpreting them.
- Use a larger, documented and appropriately sampled dataset before making workforce-level claims.
- Define a valid prediction question and evaluation design before adding machine learning.

## Author

Srishti Pandey, MCA Data Science
