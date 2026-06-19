-- 03_analysis_queries.sql
-- Analysis queries for synthetic VFC-style provider non-compliance data.

-- Annual trend
SELECT
    budget_period,
    COUNT(*) AS analytic_complete_n,
    SUM(overall_non_compliant_flag) AS non_compliant_n,
    ROUND(100.0 * SUM(overall_non_compliant_flag) / COUNT(*), 2) AS non_compliance_pct
FROM site_visits
WHERE analytic_complete_flag = 1
GROUP BY budget_period
ORDER BY budget_period;

-- Domain-specific non-compliance, long format
SELECT budget_period, 'Training' AS domain, COUNT(*) AS visits,
       SUM(CASE WHEN training_compliant = 0 THEN 1 ELSE 0 END) AS non_compliant_n,
       ROUND(100.0 * SUM(CASE WHEN training_compliant = 0 THEN 1 ELSE 0 END) / COUNT(*), 2) AS non_compliance_pct
FROM site_visits WHERE analytic_complete_flag = 1 GROUP BY budget_period
UNION ALL
SELECT budget_period, 'Eligibility', COUNT(*),
       SUM(CASE WHEN eligibility_compliant = 0 THEN 1 ELSE 0 END),
       ROUND(100.0 * SUM(CASE WHEN eligibility_compliant = 0 THEN 1 ELSE 0 END) / COUNT(*), 2)
FROM site_visits WHERE analytic_complete_flag = 1 GROUP BY budget_period
UNION ALL
SELECT budget_period, 'Documentation', COUNT(*),
       SUM(CASE WHEN documentation_compliant = 0 THEN 1 ELSE 0 END),
       ROUND(100.0 * SUM(CASE WHEN documentation_compliant = 0 THEN 1 ELSE 0 END) / COUNT(*), 2)
FROM site_visits WHERE analytic_complete_flag = 1 GROUP BY budget_period
UNION ALL
SELECT budget_period, 'Inventory', COUNT(*),
       SUM(CASE WHEN inventory_compliant = 0 THEN 1 ELSE 0 END),
       ROUND(100.0 * SUM(CASE WHEN inventory_compliant = 0 THEN 1 ELSE 0 END) / COUNT(*), 2)
FROM site_visits WHERE analytic_complete_flag = 1 GROUP BY budget_period
UNION ALL
SELECT budget_period, 'Site Storage & Handling', COUNT(*),
       SUM(CASE WHEN site_storage_handling_compliant = 0 THEN 1 ELSE 0 END),
       ROUND(100.0 * SUM(CASE WHEN site_storage_handling_compliant = 0 THEN 1 ELSE 0 END) / COUNT(*), 2)
FROM site_visits WHERE analytic_complete_flag = 1 GROUP BY budget_period
UNION ALL
SELECT budget_period, 'Unit Storage & Handling', COUNT(*),
       SUM(CASE WHEN unit_storage_handling_compliant = 0 THEN 1 ELSE 0 END),
       ROUND(100.0 * SUM(CASE WHEN unit_storage_handling_compliant = 0 THEN 1 ELSE 0 END) / COUNT(*), 2)
FROM site_visits WHERE analytic_complete_flag = 1 GROUP BY budget_period
ORDER BY budget_period, domain;

-- Stratified non-compliance by HHS region
SELECT
    budget_period,
    region,
    COUNT(*) AS visits,
    SUM(overall_non_compliant_flag) AS non_compliant_n,
    ROUND(100.0 * SUM(overall_non_compliant_flag) / COUNT(*), 2) AS non_compliance_pct
FROM site_visits
WHERE analytic_complete_flag = 1
GROUP BY budget_period, region
ORDER BY budget_period, non_compliance_pct DESC;

-- Chi-square input table by time in program
SELECT
    time_in_program_category,
    overall_compliance_label,
    COUNT(*) AS visit_count
FROM site_visits
WHERE analytic_complete_flag = 1
GROUP BY time_in_program_category, overall_compliance_label
ORDER BY time_in_program_category, overall_compliance_label;
