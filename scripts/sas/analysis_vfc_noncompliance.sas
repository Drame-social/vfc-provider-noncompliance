/* analysis_vfc_noncompliance.sas
   Synthetic VFC-style provider non-compliance portfolio analysis.
   Data are synthetic; not CDC, PEAR, patient, or provider records. */

%let project_root = /path/to/vfc-provider-noncompliance-analytics;

proc import datafile="&project_root./data/raw_synthetic/site_visits_synthetic.csv"
    out=site_visits
    dbms=csv
    replace;
    guessingrows=max;
run;

proc import datafile="&project_root./data/raw_synthetic/providers_synthetic.csv"
    out=providers
    dbms=csv
    replace;
    guessingrows=max;
run;

/* Analytic cohort mirrors the complete-case logic used in the portfolio spec. */
data analytic;
    set site_visits;
    where analytic_complete_flag = 1;
run;

/* Descriptive trend */
proc freq data=analytic;
    tables budget_period*overall_compliance_label / norow nocol nopercent;
run;

/* Domain compliance frequencies */
proc freq data=analytic;
    tables training_compliant eligibility_compliant documentation_compliant
           inventory_compliant site_storage_handling_compliant unit_storage_handling_compliant;
run;

/* Stratified analysis and chi-square examples */
proc freq data=analytic;
    tables overall_compliance_label*(region urbanicity_category provider_category provider_size
           time_in_program_category method_visit) / chisq expected;
run;

/* Logistic regression example: predictors of non-compliance */
proc logistic data=analytic descending;
    class region(ref='Region 1')
          urbanicity_category(ref='URBAN')
          provider_category(ref='Primary Care Providers')
          provider_size(ref='Medium (M)')
          time_in_program_category(ref='1 to 3 years')
          method_visit(ref='In-Person') / param=ref;
    model overall_non_compliant_flag =
          region urbanicity_category provider_category provider_size
          time_in_program_category method_visit;
run;
