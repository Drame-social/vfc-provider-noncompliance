#!/usr/bin/env python3
"""
Validate synthetic VFC-style provider non-compliance portfolio data.

This validates reproducibility and GitHub readiness:
- Unique IDs
- Provider/site-visit referential integrity
- Synthetic annual target counts and rates
- No missing analytic fields in the complete cohort
- Expected missingness in raw/incomplete records
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = PROJECT_ROOT / "data" / "raw_synthetic"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
OUTPUTS = PROJECT_ROOT / "outputs"

KEY_FIELDS = [
    "overall_non_compliant_flag",
    "training_compliant",
    "eligibility_compliant",
    "documentation_compliant",
    "inventory_compliant",
    "site_storage_handling_compliant",
    "unit_storage_handling_compliant",
    "time_in_program_years",
    "time_in_program_category",
    "visit_method",
    "method_visit",
    "current_provider_status",
    "region",
    "urbanicity_category",
    "provider_category",
    "provider_size",
]

def check(condition: bool, name: str, details: str = "") -> dict:
    return {"check_name": name, "passed": bool(condition), "details": details}

def main() -> None:
    providers = pd.read_csv(DATA_RAW / "providers_synthetic.csv")
    visits = pd.read_csv(DATA_RAW / "site_visits_synthetic.csv")
    targets = pd.read_csv(DATA_PROCESSED / "annual_synthetic_targets.csv")

    results = []

    results.append(check(
        providers["provider_id"].is_unique,
        "provider_id uniqueness",
        f"{providers['provider_id'].nunique():,} unique / {len(providers):,} rows"
    ))
    results.append(check(
        visits["site_visit_id"].is_unique,
        "site_visit_id uniqueness",
        f"{visits['site_visit_id'].nunique():,} unique / {len(visits):,} rows"
    ))
    missing_provider_links = (~visits["provider_id"].isin(providers["provider_id"])).sum()
    results.append(check(
        missing_provider_links == 0,
        "referential integrity: site_visits.provider_id -> providers.provider_id",
        f"{missing_provider_links:,} missing provider links"
    ))

    analytic = visits[visits["analytic_complete_flag"] == 1].copy()
    missing_analytic_key_values = analytic[KEY_FIELDS].isna().sum().sum()
    results.append(check(
        missing_analytic_key_values == 0,
        "no missing key fields in analytic complete cohort",
        f"{int(missing_analytic_key_values):,} missing key values"
    ))

    annual = (
        analytic.groupby("budget_period", as_index=False)
        .agg(
            analytic_complete_n=("site_visit_id", "nunique"),
            non_compliant_n=("overall_non_compliant_flag", "sum"),
        )
    )
    annual["non_compliance_pct"] = (annual["non_compliant_n"] / annual["analytic_complete_n"] * 100).round(2)
    merged = annual.merge(targets, on="budget_period", how="outer", indicator=True)
    merged["count_match"] = merged["analytic_complete_n_x"].fillna(-1).astype(int) == merged["analytic_complete_n_y"].fillna(-2).astype(int)
    merged["non_compliant_count_match"] = merged["non_compliant_n"].fillna(-1).astype(int) == merged["target_non_compliant_n"].fillna(-2).astype(int)
    merged["pct_diff"] = (merged["non_compliance_pct"] - merged["target_non_compliance_pct"]).abs().round(2)
    annual_pass = (
        (merged["_merge"] == "both").all()
        and merged["count_match"].all()
        and merged["non_compliant_count_match"].all()
        and (merged["pct_diff"] <= 0.01).all()
    )
    results.append(check(
        annual_pass,
        "annual counts and non-compliance rates match synthetic targets",
        f"max pct diff={merged['pct_diff'].max()}"
    ))

    incomplete = visits[visits["analytic_complete_flag"] == 0].copy()
    incomplete_missing_key_values = incomplete[KEY_FIELDS].isna().sum().sum()
    results.append(check(
        incomplete_missing_key_values > 0,
        "raw incomplete records include realistic missingness",
        f"{int(incomplete_missing_key_values):,} missing key values in incomplete records"
    ))

    label_ok = providers["data_source_label"].str.contains("SYNTHETIC", na=False).all() and visits["data_source_label"].str.contains("SYNTHETIC", na=False).all()
    results.append(check(
        label_ok,
        "synthetic label present in all row-level data files",
        "All row-level records must be clearly marked synthetic."
    ))

    results_df = pd.DataFrame(results)
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(OUTPUTS / "validation_results.csv", index=False)
    merged.to_csv(OUTPUTS / "annual_target_validation_detail.csv", index=False)

    failed = results_df[~results_df["passed"]]
    print(results_df.to_string(index=False))
    if not failed.empty:
        raise SystemExit("Validation failed. See outputs/validation_results.csv")
    print("All validation checks passed.")

if __name__ == "__main__":
    main()
