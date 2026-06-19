-- 02_quality_checks.sql
-- Data-quality checks for synthetic VFC-style provider non-compliance data.

-- 1. Duplicate provider IDs
SELECT provider_id, COUNT(*) AS n
FROM providers
GROUP BY provider_id
HAVING COUNT(*) > 1;

-- 2. Duplicate site visit IDs
SELECT site_visit_id, COUNT(*) AS n
FROM site_visits
GROUP BY site_visit_id
HAVING COUNT(*) > 1;

-- 3. Referential integrity: site visits without provider rows
SELECT COUNT(*) AS missing_provider_links
FROM site_visits sv
LEFT JOIN providers p ON sv.provider_id = p.provider_id
WHERE p.provider_id IS NULL;

-- 4. Missing key fields in analytic complete cohort
SELECT
    SUM(CASE WHEN overall_non_compliant_flag IS NULL THEN 1 ELSE 0 END) AS missing_overall_non_compliant_flag,
    SUM(CASE WHEN training_compliant IS NULL THEN 1 ELSE 0 END) AS missing_training,
    SUM(CASE WHEN eligibility_compliant IS NULL THEN 1 ELSE 0 END) AS missing_eligibility,
    SUM(CASE WHEN documentation_compliant IS NULL THEN 1 ELSE 0 END) AS missing_documentation,
    SUM(CASE WHEN inventory_compliant IS NULL THEN 1 ELSE 0 END) AS missing_inventory,
    SUM(CASE WHEN site_storage_handling_compliant IS NULL THEN 1 ELSE 0 END) AS missing_site_storage_handling,
    SUM(CASE WHEN unit_storage_handling_compliant IS NULL THEN 1 ELSE 0 END) AS missing_unit_storage_handling,
    SUM(CASE WHEN time_in_program_years IS NULL THEN 1 ELSE 0 END) AS missing_time_in_program,
    SUM(CASE WHEN visit_method IS NULL THEN 1 ELSE 0 END) AS missing_visit_method,
    SUM(CASE WHEN provider_category IS NULL THEN 1 ELSE 0 END) AS missing_provider_category,
    SUM(CASE WHEN method_visit IS NULL THEN 1 ELSE 0 END) AS missing_method_visit,
    SUM(CASE WHEN region IS NULL THEN 1 ELSE 0 END) AS missing_region,
    SUM(CASE WHEN urbanicity_category IS NULL THEN 1 ELSE 0 END) AS missing_urbanicity_category,
    SUM(CASE WHEN time_in_program_category IS NULL THEN 1 ELSE 0 END) AS missing_time_in_program_category,
    SUM(CASE WHEN provider_size IS NULL THEN 1 ELSE 0 END) AS missing_provider_size,
    SUM(CASE WHEN current_provider_status IS NULL THEN 1 ELSE 0 END) AS missing_current_provider_status
FROM site_visits
WHERE analytic_complete_flag = 1;

-- 5. Annual validation against synthetic target table
SELECT
    sv.budget_period,
    COUNT(*) AS analytic_complete_n,
    SUM(overall_non_compliant_flag) AS non_compliant_n,
    ROUND(100.0 * SUM(overall_non_compliant_flag) / COUNT(*), 2) AS non_compliance_pct,
    t.analytic_complete_n AS target_n,
    t.target_non_compliant_n AS target_non_compliant_n,
    t.target_non_compliance_pct AS target_pct
FROM site_visits sv
JOIN annual_synthetic_targets t ON sv.budget_period = t.budget_period
WHERE sv.analytic_complete_flag = 1
GROUP BY sv.budget_period
ORDER BY sv.budget_period;
