#!/usr/bin/env python3
"""
Generate synthetic VFC-style provider non-compliance portfolio data.

IMPORTANT:
- This script creates SYNTHETIC data only.
- It does not read, copy, transform, or publish any real CDC, PEAR, provider,
  patient, or site-visit data.
- Annual targets are synthetic, scaled, and intentionally perturbed for a
  public GitHub/LinkedIn portfolio demonstration.
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

SEED = 20260618
rng = np.random.default_rng(SEED)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = PROJECT_ROOT / "data" / "raw_synthetic"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
OUTPUTS = PROJECT_ROOT / "outputs"

SYN_LABEL = "SYNTHETIC_PORTFOLIO_DATA_NOT_REAL_CDC_PROVIDER_DATA"

BUDGET_TARGETS = pd.DataFrame(
    [
        # budget_period, analytic_complete_n, synthetic non-compliance percent
        ("2013-14", 9300, 51.8),
        ("2014-15", 15400, 38.7),
        ("2015-16", 15100, 55.2),
        ("2016-17", 4200, 50.6),   # shortened-period style synthetic year
        ("2017-18", 17400, 57.9),
        ("2018-19", 15800, 64.2),
        ("2019-20", 10200, 52.8),
        ("2020-21", 10150, 54.7),
        ("2021-22", 14100, 55.8),
        ("2022-23", 14800, 58.4),
        ("2023-24", 15600, 60.1),
        ("2024-25", 14050, 62.5),
    ],
    columns=["budget_period", "analytic_complete_n", "target_non_compliance_pct"],
)
BUDGET_TARGETS["target_non_compliant_n"] = (
    BUDGET_TARGETS["analytic_complete_n"] * BUDGET_TARGETS["target_non_compliance_pct"] / 100
).round().astype(int)
BUDGET_TARGETS["target_compliant_n"] = (
    BUDGET_TARGETS["analytic_complete_n"] - BUDGET_TARGETS["target_non_compliant_n"]
)
BUDGET_TARGETS["data_source_label"] = SYN_LABEL

REGION_AWARDEES = {
    "Region 1": ["Connecticut", "Maine", "Massachusetts", "New Hampshire", "Rhode Island", "Vermont"],
    "Region 2": ["New Jersey", "New York", "New York City", "Puerto Rico", "Virgin Islands"],
    "Region 3": ["Delaware", "District of Columbia", "Maryland", "Pennsylvania", "Philadelphia", "Virginia", "West Virginia"],
    "Region 4": ["Alabama", "Florida", "Georgia", "Kentucky", "Mississippi", "North Carolina", "South Carolina", "Tennessee"],
    "Region 5": ["Chicago", "Illinois", "Indiana", "Michigan", "Minnesota", "Ohio", "Wisconsin"],
    "Region 6": ["Arkansas", "Louisiana", "New Mexico", "Oklahoma", "Texas", "Houston", "San Antonio"],
    "Region 7": ["Iowa", "Kansas", "Missouri", "Nebraska"],
    "Region 8": ["Colorado", "Montana", "North Dakota", "South Dakota", "Utah", "Wyoming"],
    "Region 9": ["Arizona", "California", "Hawaii", "Nevada", "American Samoa", "Guam", "Northern Mariana Islands"],
    "Region 10": ["Alaska", "Idaho", "Oregon", "Washington"],
}

PROVIDER_CATEGORIES = [
    "Primary Care Providers",
    "Public and Community Services",
    "Hospital-Based Care",
    "Educational and Youth Services",
    "Specialty Health Services",
    "Pharmacy and Vaccination Services",
    "Indian Health Service or Tribal",
    "Emergency or Immediate Care",
    "Other",
    "Uncategorized/Unavailable",
]
PROVIDER_CATEGORY_PROBS = np.array([0.50, 0.23, 0.05, 0.04, 0.04, 0.03, 0.025, 0.015, 0.035, 0.035])
PROVIDER_CATEGORY_PROBS = PROVIDER_CATEGORY_PROBS / PROVIDER_CATEGORY_PROBS.sum()

PROVIDER_SIZES = ["Extra Small (XS)", "Small (S)", "Medium (M)", "Large (L)", "Extra Large (XL)", "No Size Data"]
PROVIDER_SIZE_PROBS = [0.08, 0.16, 0.24, 0.25, 0.18, 0.09]

URBANICITY = ["URBAN", "RURAL", "NO DATA"]
URBANICITY_PROBS = [0.72, 0.25, 0.03]

STATUS = ["Enrolled", "Unenrolled", "Deactivated", "Enrollment Pending", "Enrollment Expired", "Enrollment Denied"]
STATUS_PROBS = [0.72, 0.20, 0.045, 0.015, 0.015, 0.005]

VISIT_METHODS = ["Online", "Paper", "Virtual", "Hybrid"]
VISIT_METHOD_PROBS_BY_PERIOD = {
    "pre_2020": [0.47, 0.48, 0.03, 0.02],
    "pandemic": [0.32, 0.18, 0.35, 0.15],
    "post_2021": [0.46, 0.25, 0.18, 0.11],
}

DOMAIN_NAMES = [
    "training_compliant",
    "eligibility_compliant",
    "documentation_compliant",
    "inventory_compliant",
    "site_storage_handling_compliant",
    "unit_storage_handling_compliant",
]
DOMAIN_FAILURE_WEIGHTS = np.array([0.22, 0.13, 0.10, 0.28, 0.42, 0.56])
DOMAIN_FAILURE_WEIGHTS = DOMAIN_FAILURE_WEIGHTS / DOMAIN_FAILURE_WEIGHTS.sum()

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

def choose_awardee_by_region(region: str) -> str:
    return rng.choice(REGION_AWARDEES[region])

def method_visit(visit_method: str) -> str:
    if visit_method in ["Virtual", "Hybrid"]:
        return "Virtual"
    if visit_method in ["Paper", "Online"]:
        return "In-Person"
    return "Other"

def time_category(years: float | None) -> str | None:
    if years is None or pd.isna(years):
        return None
    if years < 1:
        return "< 1 year"
    if years <= 3:
        return "1 to 3 years"
    if years <= 7:
        return "4 to 7 years"
    if years <= 10:
        return "8 to 10 years"
    return "10+ years"

def budget_period_mid_date(bp: str) -> pd.Timestamp:
    start_year = 2000 + int(bp.split("-")[0])
    end_year = 2000 + int(bp.split("-")[1])
    # CDC-style cooperative agreement budget period usually spans July-June.
    return pd.Timestamp(year=start_year, month=7, day=1) + pd.Timedelta(days=int(rng.integers(0, 365)))

def build_providers(n: int = 62000) -> pd.DataFrame:
    regions = list(REGION_AWARDEES.keys())
    region_probs = np.array([0.05, 0.06, 0.08, 0.14, 0.15, 0.13, 0.06, 0.05, 0.18, 0.10])
    region_probs = region_probs / region_probs.sum()
    provider_region = rng.choice(regions, size=n, p=region_probs)
    awardees = [choose_awardee_by_region(r) for r in provider_region]
    provider_category = rng.choice(PROVIDER_CATEGORIES, size=n, p=PROVIDER_CATEGORY_PROBS)
    provider_size = rng.choice(PROVIDER_SIZES, size=n, p=PROVIDER_SIZE_PROBS)
    urban = rng.choice(URBANICITY, size=n, p=URBANICITY_PROBS)

    enrollment_years = rng.integers(1998, 2025, size=n)
    enrollment_dates = [
        pd.Timestamp(year=int(y), month=int(rng.integers(1, 13)), day=int(rng.integers(1, 28)))
        for y in enrollment_years
    ]

    providers = pd.DataFrame(
        {
            "provider_id": [f"SYN-P{idx:06d}" for idx in range(1, n + 1)],
            "synthetic_awardee": awardees,
            "region": provider_region,
            "urbanicity_category": urban,
            "provider_category": provider_category,
            "provider_size": provider_size,
            "synthetic_enrollment_date": enrollment_dates,
            "data_source_label": SYN_LABEL,
        }
    )
    return providers

def choose_visit_method(bp: str, n: int) -> np.ndarray:
    end_year = 2000 + int(bp.split("-")[1])
    if end_year in [2020, 2021]:
        probs = VISIT_METHOD_PROBS_BY_PERIOD["pandemic"]
    elif end_year >= 2022:
        probs = VISIT_METHOD_PROBS_BY_PERIOD["post_2021"]
    else:
        probs = VISIT_METHOD_PROBS_BY_PERIOD["pre_2020"]
    return rng.choice(VISIT_METHODS, size=n, p=probs)

def build_complete_visits(providers: pd.DataFrame) -> pd.DataFrame:
    all_rows = []
    total_seq = 1
    for _, target in BUDGET_TARGETS.iterrows():
        bp = target["budget_period"]
        n = int(target["analytic_complete_n"])
        non_n = int(target["target_non_compliant_n"])
        compliant_n = n - non_n

        sampled_provider_idx = rng.choice(providers.index, size=n, replace=True)
        p = providers.loc[sampled_provider_idx].reset_index(drop=True).copy()

        y_end = 2000 + int(bp.split("-")[1])
        visit_dates = [
            pd.Timestamp(year=y_end, month=1, day=1) + pd.Timedelta(days=int(rng.integers(0, 180)))
            for _ in range(n)
        ]

        non_flags = np.array([1] * non_n + [0] * compliant_n, dtype=int)
        rng.shuffle(non_flags)

        visits = pd.DataFrame(
            {
                "site_visit_id": [f"SYN-SV{idx:09d}" for idx in range(total_seq, total_seq + n)],
                "provider_id": p["provider_id"].values,
                "budget_period": bp,
                "visit_start_date": visit_dates,
                "visit_type": "VFC Compliance Visit",
                "site_visit_status": "Completed",
                "vfc_function": "Administers publicly funded vaccine",
                "current_provider_status": rng.choice(STATUS, size=n, p=STATUS_PROBS),
                "synthetic_awardee": p["synthetic_awardee"].values,
                "region": p["region"].values,
                "urbanicity_category": p["urbanicity_category"].values,
                "provider_category": p["provider_category"].values,
                "provider_size": p["provider_size"].values,
                "overall_non_compliant_flag": non_flags,
                "overall_compliance_code": np.where(non_flags == 1, 2, 1),
                "overall_compliance_label": np.where(non_flags == 1, "Non-compliant", "Compliant"),
                "analytic_complete_flag": 1,
                "data_source_label": SYN_LABEL,
            }
        )

        years_in_program = []
        for vdate, edate in zip(visits["visit_start_date"], p["synthetic_enrollment_date"]):
            years = max(0, (vdate - edate).days / 365.25)
            years_in_program.append(round(years, 2))
        visits["time_in_program_years"] = years_in_program
        visits["time_in_program_category"] = visits["time_in_program_years"].apply(time_category)
        visits["visit_method"] = choose_visit_method(bp, n)
        visits["method_visit"] = visits["visit_method"].map(method_visit)

        # Domain compliance logic: compliant visits pass every domain.
        for col in DOMAIN_NAMES:
            visits[col] = 1

        non_idx = np.flatnonzero(non_flags == 1)
        for i in non_idx:
            # Each non-compliant visit has at least one failed domain; storage/handling has higher probability.
            failure_count = int(rng.choice([1, 2, 3, 4], p=[0.45, 0.32, 0.17, 0.06]))
            failures = rng.choice(DOMAIN_NAMES, size=failure_count, replace=False, p=DOMAIN_FAILURE_WEIGHTS)
            for col in failures:
                visits.at[i, col] = 0

        all_rows.append(visits)
        total_seq += n
    return pd.concat(all_rows, ignore_index=True)

def add_incomplete_raw_visits(complete_visits: pd.DataFrame, providers: pd.DataFrame) -> pd.DataFrame:
    raw_extra = []
    total_seq = complete_visits["site_visit_id"].str.extract(r"(\d+)").astype(int)[0].max() + 1
    for _, target in BUDGET_TARGETS.iterrows():
        bp = target["budget_period"]
        n_complete = int(target["analytic_complete_n"])
        n_extra = max(75, int(round(n_complete * 0.08)))
        sampled_provider_idx = rng.choice(providers.index, size=n_extra, replace=True)
        p = providers.loc[sampled_provider_idx].reset_index(drop=True).copy()
        y_end = 2000 + int(bp.split("-")[1])
        visit_dates = [
            pd.Timestamp(year=y_end, month=1, day=1) + pd.Timedelta(days=int(rng.integers(0, 180)))
            for _ in range(n_extra)
        ]
        non_flags = rng.binomial(1, 0.55, size=n_extra)

        visits = pd.DataFrame(
            {
                "site_visit_id": [f"SYN-SV{idx:09d}" for idx in range(total_seq, total_seq + n_extra)],
                "provider_id": p["provider_id"].values,
                "budget_period": bp,
                "visit_start_date": visit_dates,
                "visit_type": rng.choice(["VFC Compliance Visit", "Enrollment Visit", "Storage and Handling Visit"], size=n_extra, p=[0.84, 0.08, 0.08]),
                "site_visit_status": rng.choice(["Completed", "In Progress", "Cancelled"], size=n_extra, p=[0.88, 0.09, 0.03]),
                "vfc_function": rng.choice(["Administers publicly funded vaccine", "Only stores vaccine"], size=n_extra, p=[0.92, 0.08]),
                "current_provider_status": rng.choice(STATUS, size=n_extra, p=STATUS_PROBS),
                "synthetic_awardee": p["synthetic_awardee"].values,
                "region": p["region"].values,
                "urbanicity_category": p["urbanicity_category"].values,
                "provider_category": p["provider_category"].values,
                "provider_size": p["provider_size"].values,
                "overall_non_compliant_flag": non_flags,
                "overall_compliance_code": np.where(non_flags == 1, 2, 1),
                "overall_compliance_label": np.where(non_flags == 1, "Non-compliant", "Compliant"),
                "analytic_complete_flag": 0,
                "data_source_label": SYN_LABEL,
            }
        )
        visits["time_in_program_years"] = [
            round(max(0, (vdate - edate).days / 365.25), 2)
            for vdate, edate in zip(visits["visit_start_date"], p["synthetic_enrollment_date"])
        ]
        visits["time_in_program_category"] = visits["time_in_program_years"].apply(time_category)
        visits["visit_method"] = choose_visit_method(bp, n_extra)
        visits["method_visit"] = visits["visit_method"].map(method_visit)

        for col in DOMAIN_NAMES:
            visits[col] = np.where(non_flags == 1, rng.binomial(1, 0.78, size=n_extra), 1)

        # Apply realistic missingness to incomplete rows. Each row gets at least one missing analytic field.
        missable = [
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
            "urbanicity_category",
            "provider_size",
        ]
        for i in range(n_extra):
            k = int(rng.choice([1, 2, 3], p=[0.72, 0.22, 0.06]))
            cols = rng.choice(missable, size=k, replace=False)
            for col in cols:
                visits.at[i, col] = np.nan

        raw_extra.append(visits)
        total_seq += n_extra
    return pd.concat([complete_visits] + raw_extra, ignore_index=True)

def make_outputs(site_visits: pd.DataFrame) -> None:
    analytic = site_visits.query("analytic_complete_flag == 1").copy()

    annual = (
        analytic.groupby("budget_period", as_index=False)
        .agg(
            analytic_complete_n=("site_visit_id", "nunique"),
            non_compliant_n=("overall_non_compliant_flag", "sum"),
            compliant_n=("overall_non_compliant_flag", lambda s: int((s == 0).sum())),
        )
    )
    annual["non_compliance_pct"] = (annual["non_compliant_n"] / annual["analytic_complete_n"] * 100).round(2)
    annual = annual.merge(BUDGET_TARGETS[["budget_period", "target_non_compliance_pct", "target_non_compliant_n"]], on="budget_period", how="left")
    annual["pct_difference_from_synthetic_target"] = (annual["non_compliance_pct"] - annual["target_non_compliance_pct"]).round(2)
    annual["data_source_label"] = SYN_LABEL

    domain_rows = []
    for col in DOMAIN_NAMES:
        tmp = (
            analytic.groupby("budget_period")
            .agg(total=("site_visit_id", "count"), compliant=(col, "sum"))
            .reset_index()
        )
        tmp["domain"] = col.replace("_compliant", "")
        tmp["non_compliant_n"] = tmp["total"] - tmp["compliant"]
        tmp["non_compliance_pct"] = (tmp["non_compliant_n"] / tmp["total"] * 100).round(2)
        domain_rows.append(tmp[["budget_period", "domain", "total", "non_compliant_n", "non_compliance_pct"]])
    domain = pd.concat(domain_rows, ignore_index=True)
    domain["data_source_label"] = SYN_LABEL

    provider_cat = (
        analytic.groupby(["budget_period", "provider_category"], as_index=False)
        .agg(
            analytic_complete_n=("site_visit_id", "count"),
            non_compliant_n=("overall_non_compliant_flag", "sum"),
        )
    )
    provider_cat["non_compliance_pct"] = (provider_cat["non_compliant_n"] / provider_cat["analytic_complete_n"] * 100).round(2)
    provider_cat["data_source_label"] = SYN_LABEL

    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    OUTPUTS.mkdir(parents=True, exist_ok=True)

    BUDGET_TARGETS.to_csv(DATA_PROCESSED / "annual_synthetic_targets.csv", index=False)
    annual.to_csv(OUTPUTS / "annual_noncompliance_summary.csv", index=False)
    domain.to_csv(OUTPUTS / "domain_noncompliance_summary.csv", index=False)
    provider_cat.to_csv(OUTPUTS / "provider_category_noncompliance_summary.csv", index=False)

def main() -> None:
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    OUTPUTS.mkdir(parents=True, exist_ok=True)

    providers = build_providers()
    complete_visits = build_complete_visits(providers)
    site_visits = add_incomplete_raw_visits(complete_visits, providers)

    providers.to_csv(DATA_RAW / "providers_synthetic.csv", index=False)
    site_visits.to_csv(DATA_RAW / "site_visits_synthetic.csv", index=False)
    make_outputs(site_visits)

    print("Synthetic dataset generated.")
    print(f"Providers: {len(providers):,}")
    print(f"Raw site visits: {len(site_visits):,}")
    print(f"Analytic complete site visits: {int(site_visits['analytic_complete_flag'].sum()):,}")
    print(f"Files saved under: {PROJECT_ROOT}")

if __name__ == "__main__":
    main()
