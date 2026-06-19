# Interview Package

## 60-second explanation

I built a synthetic VFC-style provider non-compliance analytics project to show how I approach public health program monitoring from raw data through reporting. The project uses synthetic provider and site-visit tables, applies complete-case cohort logic, validates referential integrity and missingness, and produces annual and domain-level non-compliance summaries. I included Python for data generation and analysis, SQL for QA and querying, SAS for public health-style statistical analysis, and Power BI DAX measures for dashboarding. The important point is that the data are fully synthetic and safe for GitHub, but the workflow reflects the type of CDC-supported compliance and surveillance reporting work I have done.

## STAR answer

**Situation:** Public health programs need reliable ways to monitor provider compliance and identify where training or technical assistance may be needed.

**Task:** I wanted to build a public portfolio project that demonstrated this workflow without exposing confidential CDC, provider, patient, or restricted site-visit data.

**Action:** I created a fully synthetic VFC-style provider compliance dataset, documented every field in a data dictionary, built validation rules for uniqueness, referential integrity, missingness, and annual target matching, then developed Python, SQL, SAS, and Power BI-ready outputs.

**Result:** The final package includes validated synthetic data, reproducible code, dashboard-ready metrics, public health interpretation notes, and interview-ready documentation that demonstrates data quality, epidemiologic thinking, and public health informatics skills.

## Technical explanation

The pipeline generates provider-level and site-visit-level synthetic data with a reproducible random seed. The analytic cohort is restricted to complete VFC-style compliance visits using `analytic_complete_flag`. The primary outcome is `overall_non_compliant_flag`. Domain-level variables include training, eligibility, documentation, inventory, sitewide storage and handling, and unit-level storage and handling. The validation script checks primary keys, foreign keys, complete-case missingness, synthetic labels, and annual rates. SQL scripts support database implementation, QA checks, and stratified queries. The SAS script supports `PROC FREQ`, chi-square testing, and logistic regression.

## Public health interpretation

This type of analysis helps a public health program identify where non-compliance is concentrated, whether patterns are changing over time, and which domains may require training, follow-up, or technical assistance. In a real program setting, the findings would support quality improvement and oversight, not punitive interpretation without context.
