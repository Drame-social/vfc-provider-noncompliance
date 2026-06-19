# Synthetic VFC Provider Non-Compliance Analytics

**Repository name:** `synthetic-vfc-provider-noncompliance-analytics`

This portfolio project demonstrates an end-to-end public health analytics workflow for monitoring provider non-compliance during VFC-style compliance site visits.

## Critical data notice

All row-level files in this repository are **synthetic**. They are not CDC data, PEAR data, provider data, patient data, or site-visit data. The uploaded SAS and Excel outputs that informed the analytic structure were treated as non-public working materials and are **not included** in this GitHub package.

## Public health question

Among synthetic VFC-style provider compliance site visits, how does overall provider non-compliance vary over budget periods, regions, provider categories, provider size, urbanicity, visit method, and time in program?

## Why this fits a CDC/public health analytics background

This project mirrors common public health analytics tasks: site-visit surveillance, complete-case cohort definition, domain-level compliance classification, missingness checks, trend reporting, stratified analysis, SQL validation, SAS analysis, Python data pipelines, and dashboard-ready outputs.

## Dataset strategy

A live public dataset search did not identify a current, downloadable, row-level public dataset for VFC provider compliance site visits or PEAR site-visit outputs. CDC guidance describes PEAR as an oversight system for awardees and CDC, and public oversight reports summarize site-visit findings without publishing provider-level records. For that reason, this project uses synthetic data.

## How to reproduce

```bash
pip install -r requirements.txt
python scripts/python/generate_synthetic_data.py
python scripts/python/validate_synthetic_data.py
python scripts/python/run_analysis.py
```

## Main files

- `data/raw_synthetic/providers_synthetic.csv`
- `data/raw_synthetic/site_visits_synthetic.csv`
- `data/processed/annual_synthetic_targets.csv`
- `outputs/annual_noncompliance_summary.csv`
- `outputs/domain_noncompliance_summary.csv`
- `outputs/validation_results.csv`

## Key validation results

- Providers: 62,000
- Raw synthetic site visits: 168,588
- Analytic complete site visits: 156,100
- All validation checks passed.
# vfc-provider-noncompliance
Synthetic VFC provider non-compliance analytics — Python, SQL, SAS, and Power BI portfolio project
