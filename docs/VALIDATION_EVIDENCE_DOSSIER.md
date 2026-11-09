
# Medical AI Validation Evidence Dossier

**Project:** MedAI Validation Lab  
**Version:** 0.4  
**Date:** November 2026  
**Development:** AI-assisted engineering portfolio  
**Scope:** Synthetic binary classification validation  
**Status:** Educational prototype — not for clinical use

---

## 1. Executive Summary

MedAI Validation Lab demonstrates a reproducible,
risk-based approach to medical AI performance evaluation.

The prototype examines aggregate performance, subgroup
sensitivity, period-specific sensitivity, and
cohort-by-period stratification.

It generates reviewable evidence through:

- Python validation logic
- Two synthetic evaluation datasets
- Automated acceptance checks
- JSON and Markdown reports
- A local read-only dashboard
- Risk and requirement traceability
- Automated verification using GitHub Actions

The central finding is that acceptable aggregate
sensitivity can coexist with failed subgroup and
performance-change criteria.

**Both synthetic scenarios return REVIEW_REQUIRED.**

This is an evidence-review result, not a clinical
release, regulatory, or deployment decision.

## 2. Intended Purpose

The prototype is intended to demonstrate engineering
methods for assessing fictional binary AI predictions.

It calculates classification metrics, evaluates
illustrative acceptance thresholds, and identifies
results requiring human investigation.

It does not diagnose patients, assess real clinical
performance, or authorize medical use.

## 3. Evaluation Scenarios

Two independent synthetic examples are provided.

### Scenario A — Original Dataset

Source: `data/synthetic_predictions.csv`

320 fictional records.

| Metric | Result |
|---|---:|
| Overall sensitivity | 85.62% |
| Overall specificity | 92.50% |
| Group A sensitivity | 92.50% |
| Group B sensitivity | 78.75% |
| Period sensitivity change | -13.75 percentage points |

**Finding A-001:** Group B fails the illustrative
80% minimum sensitivity criterion.

**Finding A-002:** The period sensitivity difference
exceeds the illustrative 8-percentage-point limit.

**Methodological limitation:** Group A corresponds
to the baseline period, and Group B corresponds
to the current period. These factors are completely
confounded.

Consequently, the observed period difference cannot
be independently attributed to time.

### Scenario B — Balanced Dataset

Source: `data/synthetic_predictions_balanced.csv`

320 fictional records.

Each subgroup is represented in both evaluation
periods, with 80 records in each combination.

| Cohort | Baseline | Current | Change |
|---|---:|---:|---:|
| A | 95.0% | 90.0% | -5.0 percentage points |
| B | 85.0% | 70.0% | -15.0 percentage points |

Aggregated results:

| Metric | Result |
|---|---:|
| Overall sensitivity | 85.0% |
| Overall specificity | 92.5% |
| Group A sensitivity | 92.5% |
| Group B sensitivity | 77.5% |
| Baseline sensitivity | 90.0% |
| Current sensitivity | 80.0% |
| Period sensitivity change | -10.0 percentage points |

**Finding B-001:** Group B fails the illustrative
80% sensitivity criterion.

**Finding B-002:** The overall period sensitivity
decrease exceeds the illustrative 8-percentage-point
limit.

**Finding B-003:** Within-cohort sensitivity changes
differ between groups: -5 points for A and -15
points for B.

The balanced dataset permits descriptive comparisons
within each subgroup.

These results do not establish the cause of the
observed differences or prove statistical significance,
algorithmic bias, clinical harm, or data drift.

## 4. Illustrative Acceptance Criteria

| Criterion | Threshold |
|---|---|
| Minimum overall sensitivity | 85% |
| Minimum overall specificity | 80% |
| Minimum subgroup sensitivity | 80% |
| Minimum reference-positive cases per subgroup | 15 |
| Maximum overall period sensitivity drop | 8 percentage points |

All thresholds are illustrative engineering inputs.

They have not been clinically justified or validated.

## 5. Risk-Based Traceability

| Risk | Requirement | Verification |
|---|---|---|
| RISK-001: Missed subgroup detection | REQ-001 | TEST-001 |
| RISK-002: Performance degradation | REQ-002 | TEST-002 |

Supporting documents:

- [Risk Register](risk_register.md)
- [Validation Requirements](validation_requirements.md)
- [Traceability Matrix](traceability_matrix.md)

The project illustrates traceability concepts
associated with risk-based medical software engineering.

It is not a complete ISO 14971 risk management file.

## 6. Automated Verification

The repository includes **19 automated Python tests**.

Verification coverage includes:

- Confusion-matrix metrics
- Sensitivity and specificity calculations
- Confidence intervals
- Invalid and duplicate inputs
- Insufficient-data handling
- Subgroup-specific evaluations
- Illustrative threshold boundaries
- Period performance comparisons
- JSON and Markdown report evidence
- Dashboard content and safety disclaimers
- Cohort-by-period combination coverage
- Expected stratified sensitivity values
- Within-cohort sensitivity changes

GitHub Actions runs the test suite on Python 3.10
and Python 3.12.

**Evidence:** GitHub Actions workflow #16 verified
19 passing tests following the cohort-period
verification update.

Subsequent workflow executions also completed
successfully after the balanced dataset and
dashboard changes.

[GitHub Actions](../../actions)

A successful software test demonstrates expected
behavior for the tested inputs. It does not establish
the clinical performance or safety of a medical AI
model.

## 7. Dashboard Evidence

The application provides:

- Selection between the original and balanced datasets
- Aggregate sensitivity and specificity
- Subgroup sensitivity visualization
- Performance comparison across periods
- Acceptance-check results
- Cohort-by-period stratified metrics
- Within-cohort sensitivity changes
- Data coverage information
- Evidence-review status

Implementation: `dashboard/app.py`

Report inputs:

- `output/demo/validation_report.json`
- `output/balanced/validation_report.json`

The dashboard operates locally at:

`http://127.0.0.1:8766`

It reads saved evaluation reports and does not
perform clinical actions.

## 8. Evidence Review Decision

**Scenario A: REVIEW_REQUIRED**

Reasons:
- Failed subgroup sensitivity criterion
- Failed period-change criterion
- Completely confounded subgroup and period factors

**Scenario B: REVIEW_REQUIRED**

Reasons:
- Failed subgroup sensitivity criterion
- Failed period-change criterion
- Unequal within-cohort sensitivity changes

The results are illustrative evidence-review flags,
not legally or clinically meaningful release decisions.

## 9. Remaining Engineering Gaps

The following gaps remain unresolved:

1. Define a hypothetical clinical intended purpose
   and use environment.
2. Establish clinically justified acceptance criteria.
3. Validate ground-truth labeling and data provenance.
4. Evaluate representative real-world populations
   using appropriately authorized data.
5. Assess uncertainty, sample-size adequacy, and
   clinically meaningful subgroup differences.
6. Establish independent verification and review.
7. Investigate potential sources of performance change.
8. Evaluate calibration and other relevant metrics.
9. Complete formal severity, probability, risk-control,
   and residual-risk assessments where applicable.
10. Establish change management, monitoring, and
    documented investigation procedures.

The available tests provide partial verification
evidence for selected requirements. They do not
justify a blanket claim of full validation.

## 10. Engineering Conclusion

This prototype demonstrates an evidence-oriented
approach to AI performance evaluation.

The main lessons are:

- Aggregate metrics alone are insufficient.
- Subgroup performance deserves separate evaluation.
- Period comparisons need careful interpretation.
- Dataset structure can introduce confounding.
- Risk, requirements, tests, and evidence should be
  traceable.
- Unresolved failures must remain visible.

**Engineering principle:**

A credible validation process should expose
uncertainty and unresolved risks rather than hide
them behind a successful aggregate metric.

---

**AI-assisted educational portfolio prototype.**

**No real clinical data. No clinical validation.
No ISO 14971, IEC 62304, or MDR conformity claim.
Not authorized for medical use.**
