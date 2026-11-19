# Dataset provenance and data dictionary

## Selected external dataset

- Dataset: IBM HR Analytics Employee Attrition
- Upstream repository: https://github.com/IBM/employee-attrition-aif360
- Upstream file: [data/emp_attrition.csv](https://github.com/IBM/employee-attrition-aif360/blob/master/data/emp_attrition.csv)
- Original dataset source stated by IBM: Kaggle, IBM HR Analytics Employee Attrition & Performance
- Upstream dataset terms stated in IBM README: Open Database License (ODbL) for the database and Database Contents License (DbCL) for the contents.
- Upstream project code license: Apache License 2.0. This is separate from the dataset terms.
- Upstream repository is archived. The dataset is a static teaching/example dataset.
- Dataset type: fictional/synthetic HR analytics records. Do not describe these rows as real employees or as records from a real employer.
- Imported file: `data/raw/ibm_hr_attrition.csv`
- Imported row count: 1470
- Imported column count: 35

## Important interpretation limits

This dataset is suitable for demonstrating HR analytics, attrition EDA, classification workflow, model evaluation, and fairness checks. It is not a representative sample of any current company's workforce. It has no reliable time index for calculating a true annual attrition rate. Model results must be described as performance on this benchmark dataset, not as proof of real-world HR outcomes. Avoid using protected or sensitive attributes to make employment decisions. Include a model-card style limitations section and inspect subgroup error rates if building a classifier.

## Data dictionary

| Column | Meaning |
|---|---|
| Age | Employee age in years |
| Attrition | Recorded attrition label (Yes/No), target candidate |
| BusinessTravel | Business travel frequency category |
| DailyRate | Dataset-specific daily rate; currency/unit not defined in upstream README |
| Department | Department category |
| DistanceFromHome | Distance-from-home measure; unit not defined in upstream README |
| Education | Education level code; see scale caveat below |
| EducationField | Education field category |
| EmployeeCount | Constant employee-count field in the source |
| EmployeeNumber | Source record identifier |
| EnvironmentSatisfaction | Satisfaction rating code; scale labels are not defined in the upstream README |
| Gender | Recorded gender category |
| HourlyRate | Dataset-specific hourly rate; currency/unit not defined in upstream README |
| JobInvolvement | Job involvement rating code; scale labels are not defined in the upstream README |
| JobLevel | Job level code |
| JobRole | Job role category |
| JobSatisfaction | Job satisfaction rating code; scale labels are not defined in the upstream README |
| MaritalStatus | Marital status category |
| MonthlyIncome | Dataset-specific monthly income; currency not defined in the upstream README |
| MonthlyRate | Dataset-specific monthly rate; currency/unit not defined in the upstream README |
| NumCompaniesWorked | Number of companies previously worked for |
| Over18 | Source field indicating over-18 status; constant in the supplied data |
| OverTime | Overtime category (Yes/No) |
| PercentSalaryHike | Salary hike percentage |
| PerformanceRating | Performance rating code |
| RelationshipSatisfaction | Relationship satisfaction rating code; scale labels are not defined in the upstream README |
| StandardHours | Standard-hours field; constant in the supplied data |
| StockOptionLevel | Stock-option level code |
| TotalWorkingYears | Total working years |
| TrainingTimesLastYear | Training sessions/times last year |
| WorkLifeBalance | Work-life-balance rating code; scale labels are not defined in the upstream README |
| YearsAtCompany | Years at the company |
| YearsInCurrentRole | Years in current role |
| YearsSinceLastPromotion | Years since last promotion |
| YearsWithCurrManager | Years with current manager |

The upstream README does not define all ordinal code scales, monetary units, or the measurement period. Do not invent those definitions. Preserve raw values and state these limitations in analysis.

## Reproducibility and attribution

The CSV was copied from IBM's public repository. Keep this provenance file with the data. Review the upstream ODbL and DbCL terms before redistributing the dataset or a derivative database. Credit IBM and the original Kaggle dataset source. No endorsement by IBM is implied.
