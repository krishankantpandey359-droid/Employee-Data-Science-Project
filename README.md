# Employee Attrition and Workforce EDA Portfolio Project

## Project overview

This repository contains two separate analysis tracks:

1. Primary: IBM HR Analytics Attrition benchmark, with 1,470 records and 35 fields. This is the main HR analytics project.
2. Supplementary: the original 50-record employee-style sample and its beginner EDA notebook. This sample is retained unchanged as a separate exercise.

The IBM benchmark is a static public example dataset. It is not a live company dataset and does not represent a current workforce.

## Primary project: IBM HR Attrition benchmark

Dataset: `data/raw/ibm_hr_attrition.csv`  
Rows: 1,470  
Columns: 35  
Target: `Attrition` (Yes/No)

Source, license notes, and field definitions: [Dataset provenance and data dictionary](docs/DATASET_PROVENANCE.md).

### Business questions

- What is the attrition share in the supplied benchmark sample?
- How does attrition share vary by department and job role?
- How does it differ between overtime categories?
- How do job-satisfaction code groups compare?
- How does it vary across sample income quartiles?

These are descriptive comparisons. They do not demonstrate causes or justify decisions about real employees.

### Verified benchmark findings

The CI-verified descriptive results are recorded in [reports/IBM_HR_Attrition_Findings.md](reports/IBM_HR_Attrition_Findings.md). They include attrition share by department, overtime, and sample-defined income quartile, with counts and interpretation limits.

Latest successful main-branch workflow run verified on 26 November 2026: [GitHub Actions run #45799982238](https://github.com/krishankantpandey359-droid/Employee-Data-Science-Project/actions/runs/45799982238). This confirms the configured automated checks, not every manual or deployment feature.

### Primary analysis files

- `IBM_HR_Attrition_Analysis.ipynb`: main, reproducible EDA notebook.
- `src/ibm_hr_data.py`: schema validation and reusable summaries.
- `scripts/analyze_ibm_hr.py`: command-line script that produces CSV, JSON, and chart outputs.
- `sql/employee_attrition_analysis.sql`: five SQLite business-analysis queries.
- `tests/test_ibm_hr_data.py`: tests for the 1,470-row benchmark dataset.

Run the primary notebook from the repository root:

```bash
jupyter notebook IBM_HR_Attrition_Analysis.ipynb
```

Run the reproducible analysis script:

```bash
python scripts/analyze_ibm_hr.py
```

Outputs are written to `outputs/`.

### Run SQL locally

With SQLite installed:

```bash
sqlite3 employee_attrition.db
```

Inside SQLite:

Create the database table with Python:

```python
import sqlite3
import pandas as pd

frame = pd.read_csv("data/raw/ibm_hr_attrition.csv")
with sqlite3.connect("employee_attrition.db") as connection:
    frame.to_sql("employee_attrition", connection, if_exists="replace", index=False)
```

Then execute the SQL file:

```bash
sqlite3 employee_attrition.db < sql/employee_attrition_analysis.sql
```

Confirm the imported table has 1,470 records and 35 columns before interpreting query results.

## Supplementary project: original 50-row employee-style sample

The original `Employee Dataset.csv` and `Employee_Data_Science_Project_FINAL (1).ipynb` remain as a separate beginner-level EDA exercise.

This sample contains 50 records and six fields: `id`, `groups`, `age`, `healthy_eating`, `active_lifestyle`, and `salary`. Its source, sampling method, salary unit, group meanings and score scales are undocumented. Interpret it only as a supplied exercise sample.

The existing `src/employee_data.py` module is specific to this six-column sample. It does not validate the IBM benchmark. The IBM-specific logic is kept separately in `src/ibm_hr_data.py`.

Run the supplementary notebook from the repository root:

```bash
jupyter notebook "Employee_Data_Science_Project_FINAL (1).ipynb"
```

## Setup and tests

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

The GitHub Actions workflow runs both datasets' tests, executes both notebooks, runs the primary analysis script, and preserves executed notebook and analysis outputs as workflow artifacts.

## Dataset provenance and responsible use

The IBM source repository's README lists separate Open Database License (ODbL) and Database Contents License (DbCL) terms for the dataset. Its Apache-2.0 code license is separate from the data terms. Review the upstream terms before redistributing the dataset or derived database. See [docs/DATASET_PROVENANCE.md](docs/DATASET_PROVENANCE.md).

The source is a static public benchmark/example dataset. The upstream documentation does not establish that it represents a current or identifiable real-world workforce. Results describe this dataset only. They do not estimate a current employer's attrition rate. Satisfaction code labels and monetary units are not fully documented. Do not invent their meanings. Do not use these results or any future model to make real hiring, promotion, compensation, or termination decisions.

## Author

Srishti Pandey, MCA Data Science

## Latest GitHub Actions validation

Latest successful main-branch workflow run checked on 24 November 2026: [Open workflow run #45798999167](https://github.com/krishankantpandey359-droid/Employee-Data-Science-Project/actions/runs/45798999167). This run verifies the current README and configured project checks; it is separate from the historical findings artifact above.
