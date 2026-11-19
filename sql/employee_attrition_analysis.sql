-- SQLite starter analysis for the IBM HR Attrition benchmark.
-- Import data/raw/ibm_hr_attrition.csv into a table named employee_attrition first.
-- Example (sqlite3 CLI): .mode csv / .import --skip 1 data/raw/ibm_hr_attrition.csv employee_attrition
-- Dataset fields and source limitations: docs/DATASET_PROVENANCE.md

-- 1. Overall attrition count and rate in this static benchmark sample.
SELECT
    COUNT(*) AS employee_records,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_records,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_share_pct
FROM employee_attrition;

-- 2. Attrition by department. Small groups should be interpreted cautiously.
SELECT
    Department,
    COUNT(*) AS records,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_records,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_share_pct
FROM employee_attrition
GROUP BY Department
ORDER BY attrition_share_pct DESC;

-- 3. Attrition by overtime category.
SELECT
    OverTime,
    COUNT(*) AS records,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_share_pct
FROM employee_attrition
GROUP BY OverTime
ORDER BY attrition_share_pct DESC;

-- 4. Attrition by job satisfaction code. Upstream scale labels are undocumented.
SELECT
    JobSatisfaction,
    COUNT(*) AS records,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_share_pct
FROM employee_attrition
GROUP BY JobSatisfaction
ORDER BY JobSatisfaction;

-- 5. Compare median-like income groups with explicit sample quartile boundaries.
WITH income_bands AS (
    SELECT *,
        NTILE(4) OVER (ORDER BY MonthlyIncome) AS income_quartile
    FROM employee_attrition
)
SELECT
    income_quartile,
    COUNT(*) AS records,
    ROUND(AVG(CASE WHEN Attrition = 'Yes' THEN 1.0 ELSE 0.0 END) * 100, 2) AS attrition_share_pct
FROM income_bands
GROUP BY income_quartile
ORDER BY income_quartile;

-- Caution: these are descriptive associations in a static, synthetic benchmark.
-- They do not establish causes, current workforce rates, or actionable employment rules.
