
# Medical AI Validation Evidence Dossier

**Project:** MedAI Validation Lab  
**Version:** v0.4 — Portfolio Evidence Preparation  
**Date:** November 2026  
**Development approach:** AI-assisted engineering prototype  
**Data:** Fully synthetic binary classification records  
**Regulatory status:** Research and educational demonstration only

---

## 1. Executive Summary

MedAI Validation Lab demonstrates a reproducible
approach to evaluating medical AI classification
performance, subgroup disparities, and performance
changes across evaluation periods.

The prototype processes 320 synthetic records and
generates structured validation evidence, including
automated acceptance checks, JSON/Markdown reports,
and a read-only local dashboard.

The demonstration illustrates a critical principle:

**Acceptable aggregate performance does not guarantee
acceptable performance across individual subgroups.**

The system identifies two failed illustrative criteria
and returns REVIEW_REQUIRED.

No clinical safety, regulatory conformity, or
deployment authorization is claimed.

## 2. Intended Purpose and Scope

The validation software is designed to:

- Calculate binary classification performance metrics.
- Examine performance for defined subgroups.
- Compare sensitivity across evaluation periods.
- Evaluate configurable illustrative acceptance criteria.
- Generate reproducible machine-readable reports.
- Present results in a read-only dashboard.

The prototype does not provide a clinical diagnosis,
make patient-specific decisions, or authorize deployment.

## 3. Evaluation Dataset

| Attribute | Value |
|---|---|
| Total synthetic cases | 320 |
| Subgroup A | 160 |
| Subgroup B | 160 |
| Baseline period | 160 |
| Current period | 160 |
| Positive reference cases | 160 |
| Negative reference cases | 160 |

Source:
`data/synthetic_predictions.csv`

All records are fictional.

### Important Dataset Limitation

In the supplied example, subgroup A corresponds to
the baseline period and subgroup B corresponds to the
current period.

Therefore, subgroup effects and temporal effects
are confounded.

The demonstration can detect observed differences
but cannot establish whether they result from subgroup
membership, temporal degradation, or another cause.

A future validation dataset must separate these
dimensions to support independent conclusions.

## 4. Overall Performance Results

| Metric | Result |
|---|---:|
| True positives | 137 |
| False negatives | 23 |
| True negatives | 148 |
| False positives | 12 |
| Sensitivity | 85.62% |
| Specificity | 92.50% |
| False-negative rate | 14.37% |
| Positive predictive value | 91.95% |

Illustrative minimum overall sensitivity: 85%.

**Result: PASS**

This result alone is insufficient to establish
the acceptability of subgroup performance.

## 5. Subgroup Performance Assessment

| Metric | Subgroup A | Subgroup B |
|---|---:|---:|
| Cases | 160 | 160 |
| True positives | 74 | 63 |
| False negatives | 6 | 17 |
| Sensitivity | 92.50% | 78.75% |
| False-negative rate | 7.50% | 21.25% |
| Illustrative criterion | PASS | FAIL |

Illustrative minimum subgroup sensitivity: 80%.

### Finding F-001

Subgroup B sensitivity is below the predefined
illustrative criterion.

The validation system correctly records the failed
criterion and requires further investigation.

The observed difference does not independently
establish clinical harm or model bias.

## 6. Performance Change Assessment

| Evaluation period | Sensitivity |
|---|---:|
| Baseline | 92.50% |
| Current | 78.75% |

Observed sensitivity change: -13.75 percentage points.

Illustrative maximum allowed decrease:
8 percentage points.

**Result: FAIL**

### Finding F-002

The evaluation system detects a sensitivity difference
exceeding the configured illustrative limit.

Because subgroup and period are confounded in this
dataset, the observed change must not be presented as
independent proof of temporal model degradation.

It is also not proof of covariate drift or data drift.

## 7. Risk Analysis and Traceability

| Risk | Requirement | Test reference | Current position |
|---|---|---|---|
| RISK-001 | REQ-001 | TEST-001 | Failed subgroup criterion detected |
| RISK-002 | REQ-002 | TEST-002 | Performance difference detected |

Supporting documents:

- `docs/risk_register.md`
- `docs/validation_requirements.md`
- `docs/traceability_matrix.md`

The risk analysis is preliminary and inspired by
ISO 14971 principles.

Formal severity, probability, benefit-risk, and
residual-risk assessments have not been performed.

## 8. Automated Verification Evidence

The repository includes 15 automated Python tests.

The tests address:

- Confusion-matrix calculations
- Sensitivity and specificity
- Undefined metrics and insufficient data
- Synthetic input integrity
- Subgroup sensitivity checks
- Illustrative threshold boundaries
- Performance change detection
- JSON and Markdown report generation
- Dashboard evidence and disclaimers

Automated CI runs on:

- Python 3.10
- Python 3.12

Evidence:
`.github/workflows/tests.yml`

GitHub Actions run #12 completed successfully
on both configured Python environments.

Passing tests demonstrate expected software behavior
for covered inputs. They do not establish clinical
model validity.

## 9. Dashboard Evidence

The local dashboard presents:

1. Overall classification performance
2. Subgroup sensitivity comparison
3. Period-specific performance monitoring
4. Illustrative acceptance-criterion results
5. REVIEW_REQUIRED evidence status

Source:
`dashboard/app.py`

Input:
`output/demo/validation_report.json`

The dashboard is read-only and runs locally.

## 10. Evidence Review Decision

**Prototype evaluation status: REVIEW_REQUIRED**

Reasons:

- Subgroup B sensitivity fails its illustrative
  minimum criterion.
- The observed period difference exceeds its
  illustrative maximum.
- The synthetic dataset confounds subgroup and period.
- Clinical risk acceptability has not been assessed.

This status is an evidence review outcome, not a
clinical release or deployment decision.

## 11. Remaining Validation Gaps

The following work is necessary before making
stronger engineering or clinical claims:

- Separate subgroup and period effects using an
  appropriately structured evaluation dataset.
- Define the actual clinical intended purpose.
- Establish clinically justified acceptance criteria.
- Validate ground-truth labeling and data provenance.
- Evaluate representative clinical populations.
- Assess sample-size and confidence-interval adequacy.
- Perform formal hazard and residual-risk assessment.
- Evaluate model calibration and additional relevant
  performance metrics.
- Investigate observed subgroup differences.
- Establish monitoring and change-control procedures.
- Complete independent technical review.

## 12. Engineering Conclusion

The prototype demonstrates how aggregate medical AI
performance may conceal important evaluation failures.

The central engineering lesson is:

**A validation framework must make limitations,
subgroup failures, and unresolved risks visible
rather than reduce model safety to one headline metric.**

This project is an AI-assisted, synthetic engineering
portfolio demonstration.

It is not evidence of clinical validation,
ISO 14971 conformity, MDR compliance,
or authorization for medical use.
