
# Medical AI Validation Traceability Matrix

**Project:** MedAI Validation Lab  
**Version:** 0.4  
**Date:** November 2026  
**Scope:** Synthetic binary-classification evaluation  
**Status:** Partial engineering verification evidence

> This matrix documents illustrative software verification
> evidence. It does not establish clinical safety, regulatory
> conformity, or authorization for medical use.

---

## 1. Risk-to-Requirement-to-Test Traceability

| Risk ID | Requirement | Test ID | Executable evidence | Verification assessment |
|---|---|---|---|---|
| RISK-001 | REQ-001: Subgroup sensitivity | TEST-001 | `tests/test_traceability.py::TraceabilityTests::test_TEST_001_subgroup_sensitivity` | Covered by automated assertions |
| RISK-002 | REQ-002: Performance degradation | TEST-002 | `tests/test_traceability.py::TraceabilityTests::test_TEST_002_performance_degradation` | Covered by automated assertions |

Both tests verify selected behaviors of the validation
software using synthetic inputs.

The evaluated predictions may still fail the
illustrative performance criteria.

## 2. Additional Verification Coverage

### REQ-001 — Subgroup Sensitivity

Additional executable tests:

- `tests/test_acceptance_criteria.py::AcceptanceCriteriaTests::test_REQ_001_all_subgroups_checked`
- `tests/test_acceptance_criteria.py::AcceptanceCriteriaTests::test_REQ_001_threshold_boundary`
- `tests/test_report_evidence.py::ReportEvidenceTests::test_failed_subgroup_is_reported`

These tests check:

- Evaluation of every defined subgroup
- Correct detection of a subgroup sensitivity failure
- The illustrative 80% threshold boundary
- Reporting of a failed subgroup criterion

**Engineering verification assessment:**
Selected requirements and boundaries are covered
by reproducible automated tests.

**Clinical acceptability:** Not assessed.

### REQ-002 — Performance Degradation

Additional executable test:

- `tests/test_acceptance_criteria.py::AcceptanceCriteriaTests::test_REQ_002_degradation_boundary`

Related stratification tests:

- `tests/test_cohort_period.py::CohortPeriodTests::test_all_four_combinations_exist`
- `tests/test_cohort_period.py::CohortPeriodTests::test_expected_cell_sensitivities`
- `tests/test_cohort_period.py::CohortPeriodTests::test_within_cohort_changes`
- `tests/test_cohort_period.py::CohortPeriodTests::test_complete_cohort_period_coverage`

These tests check:

- Detection of an illustrative period sensitivity decline
- The 8-percentage-point threshold boundary
- Presence of four subgroup-period combinations
- Expected stratified sensitivities
- Within-cohort sensitivity changes
- Completeness of subgroup-period coverage

**Engineering verification assessment:**
Selected period-comparison and stratification behaviors
are covered by reproducible automated tests.

**Clinical acceptability:** Not assessed.

## 3. Automated Verification Evidence

| Attribute | Evidence |
|---|---|
| Test framework | Python unittest |
| Total automated tests | 19 |
| CI workflow | `.github/workflows/tests.yml` |
| Python environments | 3.10 and 3.12 |
| Verified test run | GitHub Actions #16 |
| Result | 19 tests passed |
| Later integration runs | Completed successfully |

[GitHub Actions Evidence](../../actions)

Passing tests support the correct behavior of
the tested software functions.

They do not demonstrate that the evaluated medical
AI predictions meet all acceptance criteria.

## 4. Dataset and Report Evidence

### Scenario A — Original Synthetic Dataset

Source:
`data/synthetic_predictions.csv`

Report:
`output/demo/validation_report.json`

Observed findings:

- Overall sensitivity: 85.62% — PASS
- Subgroup B sensitivity: 78.75% — FAIL
- Illustrative period decline: 13.75 percentage points — FAIL

Evidence review status: `REVIEW_REQUIRED`

Important limitation: subgroup and period variables
are completely confounded in this example.

### Scenario B — Balanced Synthetic Dataset

Source:
`data/synthetic_predictions_balanced.csv`

Report:
`output/balanced/validation_report.json`

Observed findings:

- Overall sensitivity: 85.0% — PASS
- Subgroup B sensitivity: 77.5% — FAIL
- Illustrative overall period decline: 10 percentage points — FAIL

Additional cohort-period sensitivities:

| Cohort | Baseline | Current |
|---|---:|---:|
| A | 95.0% | 90.0% |
| B | 85.0% | 70.0% |

Evidence review status: `REVIEW_REQUIRED`

The results are descriptive and entirely synthetic.

## 5. Dashboard Evidence

Implementation:
`dashboard/app.py`

Verification module:
`tests/test_dashboard.py`

The dashboard provides:

- Overall classification metrics
- Subgroup sensitivity comparisons
- Performance monitoring across periods
- Cohort-period stratification
- Evidence-review status
- Safety disclaimers
- Selection between two synthetic scenarios

Dashboard tests verify selected displayed content
and disclaimers.

The complete interactive user workflow has also
been manually demonstrated locally, but is not fully
covered by browser-level automated tests.

## 6. Verification Status Interpretation

Three different concepts must remain separate.

**Software test status: PASS**

The relevant executable test completed successfully
for its defined inputs and assertions.

**Illustrative performance criterion: PASS or FAIL**

The evaluated synthetic prediction results either
satisfy or fail a configurable example threshold.

**Evidence review status: REVIEW_REQUIRED**

One or more illustrative acceptance criteria have
failed and further investigation is required.

None of these statuses constitutes clinical approval
or a regulatory conformity decision.

## 7. Remaining Verification Gaps

- Independent review of requirement completeness
- Additional negative and edge-case testing
- Automated verification of missing-combination behavior
- More comprehensive dashboard interaction tests
- Independently justified clinical acceptance criteria
- Statistical uncertainty and sample-size adequacy
- Clinical intended-use validation
- Realistic data provenance and representativeness
- Formal risk-control effectiveness assessment
- Residual-risk and benefit-risk evaluation

The current evidence supports partial software
verification for selected engineering requirements.

It does not justify claiming complete verification
of all possible behaviors.

## 8. Evidence References

- [Risk Register](risk_register.md)
- [Validation Requirements](validation_requirements.md)
- [Validation Evidence Dossier](VALIDATION_EVIDENCE_DOSSIER.md)
- [Engineering Case Study](ENGINEERING_CASE_STUDY.md)
- `medai/validation.py`
- `tests/test_traceability.py`
- `tests/test_acceptance_criteria.py`
- `tests/test_cohort_period.py`
- `tests/test_report_evidence.py`
- `tests/test_dashboard.py`
- `.github/workflows/tests.yml`

---

## Engineering Conclusion

The traceability chain connects illustrative risks,
requirements, executable tests, and reviewable evidence.

**Passing verification tests does not imply that the
evaluated AI predictions are clinically acceptable.**

This is an AI-assisted educational engineering
prototype using entirely synthetic data.

Not for clinical use.
