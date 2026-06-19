# Results Summary

## Synthetic dataset generated

- Providers: 62,000
- Raw synthetic site visits: 168,588
- Analytic complete site visits: 156,100

## Annual non-compliance summary

| Budget period | Analytic visits | Non-compliant visits | Non-compliance % |
|---|---:|---:|---:|
| 2013-14 | 9,300 | 4,817 | 51.80 |
| 2014-15 | 15,400 | 5,960 | 38.70 |
| 2015-16 | 15,100 | 8,335 | 55.20 |
| 2016-17 | 4,200 | 2,125 | 50.60 |
| 2017-18 | 17,400 | 10,075 | 57.90 |
| 2018-19 | 15,800 | 10,144 | 64.20 |
| 2019-20 | 10,200 | 5,386 | 52.80 |
| 2020-21 | 10,150 | 5,552 | 54.70 |
| 2021-22 | 14,100 | 7,868 | 55.80 |
| 2022-23 | 14,800 | 8,643 | 58.40 |
| 2023-24 | 15,600 | 9,376 | 60.10 |
| 2024-25 | 14,050 | 8,781 | 62.50 |

## Validation results

All checks passed:

- Provider IDs unique
- Site visit IDs unique
- Provider/site-visit referential integrity valid
- No missing key fields in analytic complete cohort
- Annual rates match synthetic targets
- Raw incomplete records include realistic missingness
- Synthetic label present in all row-level files

## Public health interpretation

The synthetic trend demonstrates how a public health analyst can monitor provider non-compliance over time and identify domains requiring training, technical assistance, or follow-up. The dashboard is designed to support program monitoring, not individual provider judgment.

## Important limitation

These results are synthetic and should never be represented as actual CDC, PEAR, VFC, provider, patient, jurisdiction, or site-visit findings.
