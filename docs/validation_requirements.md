
# Medical AI Validation Requirements

**Project:** MedAI Validation Lab  
**Version:** 0.4  
**Date:** November 2026  
**Scope:** Synthetic binary-classification evaluation  
**Status:** Illustrative engineering requirements

> These requirements describe an educational,
> AI-assisted engineering prototype.
> Acceptance thresholds are illustrative and
> have not been clinically validated.

---

## 1. Purpose

The validation system evaluates fictional binary
AI predictions against configurable example criteria.

It is designed to make subgroup failures,
period-specific performance changes, and
unresolved evidence gaps visible.

The system does not diagnose patients,
authorize medical deployment, or establish
regulatory conformity.

## 2. REQ-001 — Subgroup Sensitivity

### Requirement

The validation system shall calculate sensitivity
separately for every defined subgroup.

The system shall evaluate each subgroup against
the configured illustrative minimum sensitivity.

A result below the threshold shall be reported
as FAIL.

### Related Risk

RISK-001 — Missed Detection in a Subgroup

### Acceptance Criteria

1. Every defined subgroup is evaluated.
2. Subgroup sensitivity is calculated from TP and FN.
3. The illustrative minimum is configurable.
4. A sensitivity equal to the threshold passes.
5. A sensitivity below the threshold fails.
6. A failed subgroup is identified in the report.
7. Undefined sensitivity is not classified as PASS.

### Verification Evidence

Primary reference: TEST-001

Executable tests:

- `tests/test_traceability.py`
- `tests/test_acceptance_criteria.py`
- `tests/test_report_evidence.py`

### Demonstration Results

| Scenario | Group A | Group B |
|---|---:|---:|
| Original | 92.50% | 78.75% |
| Balanced | 92.50% | 77.50% |

Illustrative threshold: 80%.

Group B fails the example criterion in both scenarios.

**Verification assessment:**
Selected requirement behaviors are covered by
automated tests.

**Clinical acceptability:** Not assessed.

---

## 3. REQ-002 — Performance Monitoring

### Requirement

The validation system shall calculate sensitivity
for defined evaluation periods.

It shall compare period sensitivities and flag
an observed decrease exceeding the configured
illustrative maximum.

The result shall be included in the evidence report.

### Related Risk

RISK-002 — Performance Deterioration Across Periods

### Acceptance Criteria

1. Sensitivity is calculated for each defined period.
2. Period comparisons are reproducible.
3. The example maximum allowed drop is configurable.
4. A drop equal to the threshold passes.
5. A drop exceeding the threshold fails.
6. Undefined sensitivity is not treated as PASS.
7. The result is available in the evidence report.

### Verification Evidence

Primary reference: TEST-002

Executable tests:

- `tests/test_traceability.py`
- `tests/test_acceptance_criteria.py`

Additional stratification tests:

- `tests/test_cohort_period.py`

### Demonstration Results

| Scenario | Observed sensitivity change |
|---|---:|
| Original | -13.75 percentage points |
| Balanced | -10.0 percentage points |

Illustrative maximum drop: 8 percentage points.

Both example scenarios fail this criterion.

The original scenario has complete confounding
between subgroup and period.

The balanced scenario allows descriptive
within-cohort comparisons but does not
demonstrate a causal time effect.

**Verification assessment:**
Selected period-comparison behaviors are
covered by automated tests.

**Clinical acceptability:** Not assessed.

---

## 4. Additional Implemented Engineering Capabilities

The prototype includes functionality supporting
the two primary requirements.

### REQ-SUP-001 — Input Integrity

The software checks required CSV fields,
duplicate or missing case identifiers,
binary prediction values, and empty datasets.

### REQ-SUP-002 — Classification Metrics

The software calculates:

- True positives
- False negatives
- True negatives
- False positives
- Sensitivity
- Specificity
- False-negative rate
- Positive predictive value
- Approximate Wilson confidence intervals

Undefined ratios are represented explicitly.

### REQ-SUP-003 — Cohort-Period Stratification

The software calculates separate metrics for
each observed cohort-period combination.

It also identifies missing combinations among
the defined cohorts and periods.

### REQ-SUP-004 — Evidence Reporting

The software generates JSON and Markdown
validation evidence reports.

Reports contain metric values, illustrative
acceptance checks, and evidence-review status.

### REQ-SUP-005 — Evidence Dashboard

A local read-only dashboard displays saved
validation results and permits selection
between original and balanced scenarios.

These supporting capabilities have selected
automated test coverage.

This document does not claim complete
requirements verification.

---

## 5. Evidence Review Logic

The validation report can return:

**CRITERIA_MET**

All evaluated illustrative criteria pass.

**REVIEW_REQUIRED**

At least one illustrative criterion fails.

**EVIDENCE_INCOMPLETE**

No criterion fails, but one or more results
have insufficient data.

These statuses are engineering evidence-review
outputs only.

They are not clinical release decisions.

---

## 6. Verification Evidence Summary

| Item | Evidence |
|---|---|
| Test framework | Python unittest |
| Automated tests | 19 |
| CI environments | Python 3.10 and 3.12 |
| Verification workflow | `.github/workflows/tests.yml` |
| Verified test execution | GitHub Actions #16 |
| Verified result | 19 tests passed |

The successful execution of software tests does
not prove that the evaluated synthetic predictions
meet every performance criterion.

Test coverage is limited to the implemented
assertions and input scenarios.

---

## 7. Requirements Traceability

| Risk | Requirement | Test reference |
|---|---|---|
| RISK-001 | REQ-001 | TEST-001 |
| RISK-002 | REQ-002 | TEST-002 |

Supporting documents:

- [Risk Register](risk_register.md)
- [Traceability Matrix](traceability_matrix.md)
- [Validation Evidence Dossier](VALIDATION_EVIDENCE_DOSSIER.md)
- [Engineering Case Study](ENGINEERING_CASE_STUDY.md)

---

## 8. Outstanding Requirements and Gaps

Before any real clinical application,
additional work would be necessary:

- Define a specific clinical intended purpose.
- Establish clinically justified thresholds.
- Evaluate representative authorized data.
- Verify ground-truth quality and provenance.
- Assess statistical uncertainty and sample sizes.
- Evaluate appropriate clinical performance metrics.
- Establish human review and escalation procedures.
- Perform formal risk management where applicable.
- Conduct independent verification and validation.
- Establish documented change-control procedures.

These activities are outside the demonstrated
scope of this portfolio prototype.

---

## Engineering Conclusion

REQ-001 and REQ-002 demonstrate selected
risk-based verification principles using
synthetic classification predictions.

The project distinguishes:

1. Correct operation of the validation software
2. Performance of the evaluated predictions
3. Evidence-review and clinical acceptability decisions

Passing an automated test does not establish
clinical safety or regulatory conformity.

**AI-assisted educational engineering prototype.**

**Synthetic data only. Not for clinical use.**
