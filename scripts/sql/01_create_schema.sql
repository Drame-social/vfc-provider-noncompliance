-- 01_create_schema.sql
-- Synthetic VFC-style provider non-compliance portfolio project.
-- Tested with SQLite syntax. Data are synthetic and not real CDC/provider records.

DROP TABLE IF EXISTS providers;
DROP TABLE IF EXISTS site_visits;
DROP TABLE IF EXISTS annual_synthetic_targets;

CREATE TABLE providers (
    provider_id TEXT PRIMARY KEY,
    synthetic_awardee TEXT NOT NULL,
    region TEXT NOT NULL,
    urbanicity_category TEXT NOT NULL,
    provider_category TEXT NOT NULL,
    provider_size TEXT NOT NULL,
    synthetic_enrollment_date TEXT NOT NULL,
    data_source_label TEXT NOT NULL CHECK (data_source_label LIKE 'SYNTHETIC%')
);

CREATE TABLE site_visits (
    site_visit_id TEXT PRIMARY KEY,
    provider_id TEXT NOT NULL,
    budget_period TEXT NOT NULL,
    visit_start_date TEXT NOT NULL,
    visit_type TEXT,
    site_visit_status TEXT,
    vfc_function TEXT,
    current_provider_status TEXT,
    synthetic_awardee TEXT,
    region TEXT,
    urbanicity_category TEXT,
    provider_category TEXT,
    provider_size TEXT,
    overall_non_compliant_flag INTEGER CHECK (overall_non_compliant_flag IN (0, 1)),
    overall_compliance_code INTEGER CHECK (overall_compliance_code IN (1, 2)),
    overall_compliance_label TEXT CHECK (overall_compliance_label IN ('Compliant', 'Non-compliant')),
    analytic_complete_flag INTEGER CHECK (analytic_complete_flag IN (0, 1)),
    time_in_program_years REAL,
    time_in_program_category TEXT,
    visit_method TEXT,
    method_visit TEXT,
    training_compliant INTEGER CHECK (training_compliant IN (0, 1) OR training_compliant IS NULL),
    eligibility_compliant INTEGER CHECK (eligibility_compliant IN (0, 1) OR eligibility_compliant IS NULL),
    documentation_compliant INTEGER CHECK (documentation_compliant IN (0, 1) OR documentation_compliant IS NULL),
    inventory_compliant INTEGER CHECK (inventory_compliant IN (0, 1) OR inventory_compliant IS NULL),
    site_storage_handling_compliant INTEGER CHECK (site_storage_handling_compliant IN (0, 1) OR site_storage_handling_compliant IS NULL),
    unit_storage_handling_compliant INTEGER CHECK (unit_storage_handling_compliant IN (0, 1) OR unit_storage_handling_compliant IS NULL),
    data_source_label TEXT NOT NULL CHECK (data_source_label LIKE 'SYNTHETIC%'),
    FOREIGN KEY (provider_id) REFERENCES providers(provider_id)
);

CREATE TABLE annual_synthetic_targets (
    budget_period TEXT PRIMARY KEY,
    analytic_complete_n INTEGER NOT NULL,
    target_non_compliance_pct REAL NOT NULL,
    target_non_compliant_n INTEGER NOT NULL,
    target_compliant_n INTEGER NOT NULL,
    data_source_label TEXT NOT NULL CHECK (data_source_label LIKE 'SYNTHETIC%')
);

CREATE INDEX idx_site_visits_budget_period ON site_visits(budget_period);
CREATE INDEX idx_site_visits_provider_id ON site_visits(provider_id);
CREATE INDEX idx_site_visits_analytic ON site_visits(analytic_complete_flag);
