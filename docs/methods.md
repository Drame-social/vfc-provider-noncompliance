# Methods

## Study design

Synthetic retrospective repeated cross-sectional analysis of VFC-style provider compliance site visits across 12 budget periods.

## Analytic cohort

The analytic cohort includes records with:

1. `analytic_complete_flag = 1`
2. Completed VFC-style compliance visit
3. Facility function not equal to storage-only
4. Non-missing outcome, domain compliance variables, time in program, visit method, region, urbanicity, provider category, and provider size

## Outcome

`overall_non_compliant_flag`

- `1`: provider/site visit classified as non-compliant
- `0`: provider/site visit classified as compliant

## Domain variables

- Training
- Eligibility
- Documentation
- Inventory
- Sitewide storage and handling
- Unit-level storage and handling roll-up

## Descriptive analysis

- Annual analytic denominator
- Annual non-compliant count
- Annual non-compliance percentage
- Domain-specific non-compliance percentages
- Stratification by region, provider category, provider size, urbanicity, time in program, and visit method

## Data-quality checks

- Unique provider IDs
- Unique site visit IDs
- Provider/site-visit referential integrity
- Complete-case validation
- Missingness profile
- Synthetic data safety label validation

## Statistical analysis

Recommended SAS analysis:

- `PROC FREQ` for domain frequencies
- `PROC FREQ / CHISQ` for association between compliance and covariates
- `PROC LOGISTIC` for adjusted odds of non-compliance

## Dashboard metrics

- Total analytic visits
- Non-compliant visits
- Non-compliance rate
- Domain non-compliance rates
- Year-over-year change
- Stratified non-compliance by region, provider type, urbanicity, provider size, time in program, and visit method

## Interpretation framework

Results should be interpreted as a portfolio demonstration of a public health compliance analytics workflow. No result should be interpreted as describing real CDC, PEAR, VFC, provider, jurisdiction, or patient performance.
