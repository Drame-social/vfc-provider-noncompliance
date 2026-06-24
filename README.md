# VFC Provider Non-Compliance Analytics

**Author:** Aly Drame, MD, MPH, MBA  
**Languages:** Python · SQL · SAS · Power BI  
**Domain:** Immunization program compliance, public health surveillance  
**Data:** Fully synthetic — generated for portfolio demonstration

---

## Public Health Question

Among VFC-style provider compliance site visits, how does overall provider non-compliance vary across budget periods, regions, provider categories, provider size, urbanicity, visit method, and time in program?

---

## Project Overview

This portfolio project demonstrates an end-to-end public health analytics workflow for monitoring provider non-compliance during VFC-style compliance site visits. It mirrors common CDC/state immunization program analytics tasks: site-visit surveillance, non-compliance pattern detection, trend analysis by region and provider type, and predictive flagging of high-risk providers.

The analytic pipeline is implemented in Python (data generation, cleaning, analysis), SQL (schema and reporting queries), SAS (descriptive and inferential analysis), and Power BI (dashboard outputs).

---

## Data

All row-level files in this repository are **synthetic**. They are not CDC data, PEAR data, provider data, patient data, or site-visit data of any kind. No non-public working materials are included in this repository.

| Dataset | Records | Notes |
|---------|---------|-------|
| Providers | 62,000 | Synthetic provider registry |
| Raw site visits | 168,588 | Synthetic compliance visit records |
| Analytic complete visits | 156,100 | After cleaning and exclusions |

---

## Analytic Dimensions

Non-compliance is examined across the following dimensions:

- Budget period
- Region
- Provider category (physician practice, clinic, pharmacy, etc.)
- Provider size (number of enrolled patients)
- Urbanicity (urban, suburban, rural)
- Visit method (in-person vs. remote)
- Time in program (tenure cohorts)

---

## Repository Structure

```
vfc-provider-noncompliance/
├── README.md
├── scripts/
│   ├── python/      # Data generation, cleaning, analysis
│   ├── sql/         # Schema, validation, reporting queries
│   └── sas/         # Descriptive stats, logistic regression
├── outputs/         # Summary tables, figures
├── portfolio_assets/ # Portfolio documentation
└── docs/            # Data dictionary, methods, limitations
```

---

## Key Validation Results

- Providers: 62,000
- Raw synthetic site visits: 168,588
- Analytic complete site visits: 156,100
- All validation checks passed

---

## How to Run

```bash
# Python pipeline
python scripts/python/01_generate_synthetic_data.py
python scripts/python/02_clean_and_validate.py
python scripts/python/03_noncompliance_analysis.py
```

SAS scripts: update `%let root = ...` to your project path, then submit in order from SAS 9.4.

---

*All data in this project are synthetic and were generated solely for portfolio demonstration. No real CDC records, provider data, patient data, or site-visit records are included.*
