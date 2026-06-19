#!/usr/bin/env python3
"""
Analysis pipeline for the synthetic VFC-style provider non-compliance project.

Outputs:
- Annual non-compliance trend
- Domain non-compliance summary
- Stratified non-compliance summary
- Data-quality summary
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = PROJECT_ROOT / "data" / "raw_synthetic"
OUTPUTS = PROJECT_ROOT / "outputs"

DOMAIN_COLUMNS = {
    "training": "training_compliant",
    "eligibility": "eligibility_compliant",
    "documentation": "documentation_compliant",
    "inventory": "inventory_compliant",
    "site_storage_handling": "site_storage_handling_compliant",
    "unit_storage_handling": "unit_storage_handling_compliant",
}

def summarize_group(df: pd.DataFrame, group_cols: list[str]) -> pd.DataFrame:
    out = (
        df.groupby(group_cols, dropna=False, as_index=False)
        .agg(
            visits=("site_visit_id", "nunique"),
            non_compliant=("overall_non_compliant_flag", "sum"),
        )
    )
    out["non_compliance_pct"] = (out["non_compliant"] / out["visits"] * 100).round(2)
    return out

def main() -> None:
    visits = pd.read_csv(DATA_RAW / "site_visits_synthetic.csv", parse_dates=["visit_start_date"])
    analytic = visits[visits["analytic_complete_flag"] == 1].copy()

    annual = summarize_group(analytic, ["budget_period"])
    annual.to_csv(OUTPUTS / "annual_noncompliance_summary.csv", index=False)

    domain_summaries = []
    for domain, col in DOMAIN_COLUMNS.items():
        tmp = (
            analytic.assign(domain=domain, domain_non_compliant=1 - analytic[col])
            .groupby(["budget_period", "domain"], as_index=False)
            .agg(visits=("site_visit_id", "nunique"), non_compliant=("domain_non_compliant", "sum"))
        )
        tmp["non_compliance_pct"] = (tmp["non_compliant"] / tmp["visits"] * 100).round(2)
        domain_summaries.append(tmp)
    pd.concat(domain_summaries, ignore_index=True).to_csv(OUTPUTS / "domain_noncompliance_summary.csv", index=False)

    for col in ["region", "urbanicity_category", "provider_category", "provider_size", "time_in_program_category", "method_visit"]:
        summarize_group(analytic, ["budget_period", col]).to_csv(OUTPUTS / f"noncompliance_by_{col}.csv", index=False)

    quality = []
    for col in visits.columns:
        quality.append(
            {
                "column": col,
                "missing_n": int(visits[col].isna().sum()),
                "missing_pct": round(visits[col].isna().mean() * 100, 2),
                "distinct_values": int(visits[col].nunique(dropna=True)),
            }
        )
    pd.DataFrame(quality).to_csv(OUTPUTS / "data_quality_missingness_summary.csv", index=False)

    print("Analysis outputs written to outputs/")

if __name__ == "__main__":
    main()
