# Data Dictionary

## Data safety label

Every row-level dataset contains `data_source_label = SYNTHETIC_PORTFOLIO_DATA_NOT_REAL_CDC_PROVIDER_DATA`.

## File: `data/raw_synthetic/providers_synthetic.csv`

Table name: `providers`

| Column | Type | Definition | Expected values/categories | Missingness rule | Validation rule |
|---|---:|---|---|---|---|
| provider_id | string | Synthetic provider identifier. | `SYN-P000001` format | 0% | Primary key; unique; non-null |
| synthetic_awardee | string | Synthetic awardee/jurisdiction assignment. | State/city/territory-style public categories | 0% | Must map to one HHS-style region |
| region | string | HHS-style synthetic region. | Region 1–Region 10 | 0% | Non-null categorical |
| urbanicity_category | string | Collapsed urbanicity group. | URBAN, RURAL, NO DATA | 0% | Non-null categorical |
| provider_category | string | Collapsed provider type group. | Primary Care Providers; Public and Community Services; Hospital-Based Care; Educational and Youth Services; Specialty Health Services; Pharmacy and Vaccination Services; Indian Health Service or Tribal; Emergency or Immediate Care; Other; Uncategorized/Unavailable | 0% | Non-null categorical |
| provider_size | string | Synthetic provider size band. | Extra Small (XS), Small (S), Medium (M), Large (L), Extra Large (XL), No Size Data | 0% | Non-null categorical |
| synthetic_enrollment_date | date | Synthetic enrollment date used to calculate time in program. | YYYY-MM-DD | 0% | Must be on/before visit dates |
| data_source_label | string | Data safety marker. | `SYNTHETIC_PORTFOLIO_DATA_NOT_REAL_CDC_PROVIDER_DATA` | 0% | Must contain `SYNTHETIC` |

## File: `data/raw_synthetic/site_visits_synthetic.csv`

Table name: `site_visits`

| Column | Type | Definition | Expected values/categories | Missingness rule | Validation rule |
|---|---:|---|---|---|---|
| site_visit_id | string | Synthetic site visit identifier. | `SYN-SV000000001` format | 0% | Primary key; unique; non-null |
| provider_id | string | Synthetic provider identifier. | Must exist in `providers.provider_id` | 0% | Foreign key |
| budget_period | string | Synthetic cooperative agreement-style budget period. | 2013-14 through 2024-25 | 0% | Non-null categorical |
| visit_start_date | date | Synthetic visit date. | YYYY-MM-DD | 0% | Must fall within approximate budget-period year |
| visit_type | string | Site visit type. | VFC Compliance Visit, Enrollment Visit, Storage and Handling Visit | 0% | Analytic cohort keeps VFC Compliance Visit |
| site_visit_status | string | Visit completion status. | Completed, In Progress, Cancelled | 0% | Analytic cohort keeps Completed |
| vfc_function | string | Synthetic facility function. | Administers publicly funded vaccine, Only stores vaccine | 0% | Analytic cohort excludes Only stores vaccine |
| current_provider_status | string | Synthetic provider status at visit. | Enrolled, Unenrolled, Deactivated, Enrollment Pending, Enrollment Expired, Enrollment Denied | 0% in analytic cohort | Non-null in analytic cohort |
| synthetic_awardee | string | Synthetic awardee copied from provider table at visit. | State/city/territory-style categories | 0% in analytic cohort | Should be consistent with region |
| region | string | HHS-style region. | Region 1–Region 10 | 0% in analytic cohort | Non-null in analytic cohort |
| urbanicity_category | string | Collapsed urbanicity group. | URBAN, RURAL, NO DATA | 0% in analytic cohort; ~1–3% missing in raw incomplete rows | Non-null in analytic cohort |
| provider_category | string | Collapsed provider type group. | See providers table | 0% in analytic cohort | Non-null in analytic cohort |
| provider_size | string | Provider size band. | XS, S, M, L, XL, No Size Data | 0% in analytic cohort; ~2–4% missing in raw incomplete rows | Non-null in analytic cohort |
| overall_non_compliant_flag | integer | Outcome variable. | 1 = Non-compliant; 0 = Compliant | 0% in analytic cohort | Must be 0 or 1 |
| overall_compliance_code | integer | SAS-style compliance code. | 1 = Compliant; 2 = Non-compliant | 0% in analytic cohort | Must be 1 or 2 |
| overall_compliance_label | string | Human-readable outcome. | Compliant, Non-compliant | 0% in analytic cohort | Must agree with flag and code |
| analytic_complete_flag | integer | Complete-case analytic cohort indicator. | 1 = complete analytic record; 0 = raw/incomplete or ineligible record | 0% | Must be 0 or 1 |
| time_in_program_years | numeric | Years from synthetic enrollment to visit. | 0+ | 0% in analytic cohort; ~1–3% missing in raw incomplete rows | Must be >= 0 when present |
| time_in_program_category | string | Time-in-program band. | < 1 year; 1 to 3 years; 4 to 7 years; 8 to 10 years; 10+ years | 0% in analytic cohort; missing when time-in-program missing | Must match `time_in_program_years` |
| visit_method | string | Original visit method category. | Online, Paper, Virtual, Hybrid | 0% in analytic cohort; ~1–3% missing in raw incomplete rows | Non-null in analytic cohort |
| method_visit | string | Standardized visit method. | In-Person, Virtual, Other | 0% in analytic cohort | Online/Paper -> In-Person; Virtual/Hybrid -> Virtual |
| training_compliant | integer | Training domain compliance. | 1 = compliant; 0 = non-compliant | 0% in analytic cohort; realistic missingness in raw incomplete rows | Must be 0/1/non-missing in analytic cohort |
| eligibility_compliant | integer | Eligibility-screening domain compliance. | 1 = compliant; 0 = non-compliant | 0% in analytic cohort; realistic missingness in raw incomplete rows | Must be 0/1/non-missing in analytic cohort |
| documentation_compliant | integer | Documentation domain compliance. | 1 = compliant; 0 = non-compliant<| 0% in analytic cohort; realistic missingness in raw incomplete rows | Must be 0/1/non-missing in analytic cohort |
| inventory_compliant | integer | Inventory/accountability domain compliance. | 1 = compliant; 0 = non-compliant | 0% in analytic cohort; realistic missingness in raw incomplete rows | Must be 0/1/non-missing in analytic cohort |
| site_storage_handling_compliant | integer | Sitewide storage and handling compliance. | 1 = compliant; 0 = non-compliant | 0% in analytic cohort; realistic missingness in raw incomplete rows | Must be 0/1/non-missing in analytic cohort |
| unit_storage_handling_compliant | integer | Unit-level storage and handling roll-up. | 1 = compliant; 0 = non-compliant | 0% in analytic cohort; realistic missingness in raw incomplete rows | Must be 0/1/non-missing in analytic cohort |
| data_source_label | string | Data safety marker. | `SYNTHETIC_PORTFOLIO_DATA_NOT_REAL_CDC_PROVIDER_DATA` | 0% | Must contain `SYNTHETIC` |

## File: `data/processed/annual_synthetic_targets.csv`

Table name: `annual_synthetic_targets`

| Column | Type | Definition | Expected values | Missingness rule | Validation rule |
|---|---:|---|---|---|---|
| budget_period | string | Budget period. | 2013-14 through 2024-25 | 0% | Primary key |
| analytic_complete_n | integer | Synthetic complete analytic denominator. | Positive integer | 0% | Must equal analytic count in site visits |
| target_non_compliance_pct | numeric | Synthetic target non-compliance percentage. | 0–100 | 0% | Must match generated rate within 0.01 percentage points |
| target_non_compliant_n | integer | Synthetic target count. | Positive integer | 0% | Must equal generated non-compliant count |
| target_compliant_n | integer | Synthetic compliant count. | Positive integer | 0% | Must sum to analytic_complete_n |
| data_source_label | string | Data safety marker. | Synthetic label | 0% | Must contain `SYNTHETIC` |

## Logic checks

1. `site_visit_id` unique.
2. `provider_id` unique in providers.
3. Every `site_visits.provider_id` exists in `providers.provider_id`.
4. Analytic complete records must have no missing values in outcome, compliance domains, time, visit method, provider category, region, urbanicity, and size.
5. `overall_non_compliant_flag = 1` must map to `overall_compliance_code = 2` and `overall_compliance_label = Non-compliant`.
6. `overall_non_compliant_flag = 0` must map to `overall_compliance_code = 1` and `overall_compliance_label = Compliant`.
7. At least one domain should be non-compliant for non-compliant records.
8. `method_visit` must be derived from `visit_method`.
9. `time_in_program_category` must agree with `time_in_program_years`.
10. All public files must remain clearly labeled synthetic.
