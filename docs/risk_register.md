
# Medical AI Risk Register

**Project:** MedAI Validation Lab  
**Version:** 0.4  
**Date:** November 2026  
**Scope:** Synthetic binary-classification evaluation  
**Status:** Preliminary engineering risk analysis

> This register illustrates risk-based medical AI
> engineering concepts. It is not a complete ISO 14971
> risk management file, a clinical safety assessment,
> or evidence of regulatory conformity.

---

## 1. Risk Register Summary

| Risk ID | Failure mode | Related requirement | Test reference | Evidence review |
|---|---|---|---|---|
| RISK-001 | Missed detection in a subgroup | REQ-001 | TEST-001 | REVIEW_REQUIRED |
| RISK-002 | Performance deterioration across periods | REQ-002 | TEST-002 | REVIEW_REQUIRED |

All evaluated records and model predictions are fictional.

The identified risks describe hypothetical clinical
use scenarios, not observed patient harm.

## 2. RISK-001 — Missed Detection in a Subgroup

### Failure Mode

A hypothetical medical AI classifier produces
false-negative predictions more frequently in
a defined subgroup.

### Hypothetical Hazardous Situation

A false-negative prediction is relied upon during
a clinical decision without appropriate independent
assessment or other safeguards.

### Potential Harm

Delayed clinical assessment, diagnosis, or treatment.

No actual patients or clinical decisions are
involved in this prototype.

### Synthetic Evidence

| Metric | Original scenario | Balanced scenario |
|---|---:|---:|
| Overall sensitivity | 85.62% | 85.0% |
| Subgroup A sensitivity | 92.50% | 92.5% |
| Subgroup B sensitivity | 78.75% | 77.5% |
| Illustrative subgroup threshold | 80% | 80% |
| Subgroup B criterion | FAIL | FAIL |

The subgroup B result fails the illustrative
sensitivity criterion in both scenarios.

### Related Engineering Evidence

- Requirement: `REQ-001`
- Test reference: `TEST-001`
- Source: `medai/validation.py`
- Automated tests: `tests/test_traceability.py`
- Boundary tests: `tests/test_acceptance_criteria.py`
- Reports: `output/demo/` and `output/balanced/`

### Demonstrated Engineering Controls

- Calculation of subgroup-specific sensitivity
- Evaluation against a configurable example criterion
- Identification of failed subgroup checks
- Generation of reviewable reports
- Display of failed results in the local dashboard

These are prototype evaluation features, not
validated clinical risk controls.

### Proposed Further Risk Controls

- Establish clinically justified sensitivity criteria
- Assess representativeness of relevant populations
- Investigate false-negative cases
- Evaluate uncertainty and sample size adequacy
- Define a documented human review procedure
- Establish requirements for escalation and follow-up

### Current Disposition

**REVIEW_REQUIRED**

The illustrative performance criterion is not met.

**Residual risk:** Not assessed.

**Clinical risk acceptability:** Not determined.

---

## 3. RISK-002 — Performance Deterioration Across Periods

### Failure Mode

The sensitivity of a hypothetical AI classifier
decreases between evaluation periods.

### Hypothetical Hazardous Situation

A change in predictive performance goes undetected
and predictions continue to be relied upon
without appropriate investigation.

### Potential Harm

Missed detection, delayed assessment, or
inappropriate clinical decision support.

No real clinical harm is observed in this project.

### Original Scenario Evidence

| Metric | Value |
|---|---:|
| Baseline sensitivity | 92.50% |
| Current sensitivity | 78.75% |
| Difference | -13.75 percentage points |
| Illustrative maximum decrease | 8 percentage points |
| Criterion | FAIL |

**Methodological limitation:**

In the original dataset, subgroup and period are
completely confounded.

The observed difference cannot establish
an independent temporal effect.

### Balanced Scenario Evidence

| Cohort | Baseline | Current | Change |
|---|---:|---:|---:|
| A | 95.0% | 90.0% | -5.0 percentage points |
| B | 85.0% | 70.0% | -15.0 percentage points |

The aggregate sensitivity decreases from 90.0%
to 80.0%, a difference of 10 percentage points.

This exceeds the illustrative maximum decrease
of 8 percentage points.

**Criterion: FAIL**

The balanced dataset permits descriptive
within-cohort comparisons.

It does not independently establish causality,
model drift, data drift, or clinical impact.

### Related Engineering Evidence

- Requirement: `REQ-002`
- Test reference: `TEST-002`
- Automated tests: `tests/test_traceability.py`
- Boundary tests: `tests/test_acceptance_criteria.py`
- Stratification tests: `tests/test_cohort_period.py`
- Generated reports: `output/balanced/`

### Demonstrated Engineering Controls

- Calculation of period-specific sensitivity
- Detection of performance differences
- Comparison against an illustrative threshold
- Cohort-by-period stratified analysis
- Identification of missing cohort-period combinations
- Evidence-review flag generation

### Proposed Further Risk Controls

- Establish clinically justified monitoring criteria
- Define monitoring frequency and data requirements
- Investigate possible sources of performance change
- Assess statistical uncertainty
- Evaluate subgroup-specific monitoring rules
- Document escalation and change-control procedures
- Perform independent review before clinical decisions

### Current Disposition

**REVIEW_REQUIRED**

The illustrative period-change criterion fails.

**Residual risk:** Not assessed.

**Clinical risk acceptability:** Not determined.

---

## 4. Verification Evidence

The repository includes 19 automated Python tests.

Verification covers selected functions including:

- Classification metric calculations
- Input integrity
- Subgroup sensitivity checks
- Illustrative acceptance boundaries
- Period performance comparisons
- Cohort-period stratification
- Report generation
- Selected dashboard content

The test suite has passed in GitHub Actions using
Python 3.10 and Python 3.12.

These passing tests support selected behaviors
of the validation software.

They do not demonstrate that the evaluated synthetic
predictions satisfy performance acceptance criteria.

## 5. Unresolved Risk Management Activities

The prototype does not include:

- Defined clinical intended use
- Formal hazard identification completeness review
- Severity and probability estimations
- Clinically justified risk acceptability criteria
- Validated clinical risk-control effectiveness
- Complete verification and validation coverage
- Formal residual-risk assessment
- Benefit-risk determination
- Real-world clinical evaluation
- Independent regulatory conformity assessment

Consequently, no risk is classified as clinically
acceptable or adequately controlled.

## 6. Engineering Interpretation

Three different outcomes must not be confused:

**Automated test result: PASS**

The software behaved as expected for defined tests.

**Illustrative performance criterion: FAIL**

The evaluated synthetic predictions did not satisfy
one or more configured example thresholds.

**Evidence-review decision: REVIEW_REQUIRED**

Further engineering investigation is indicated.

This decision is not a clinical release authorization
or a regulatory conformity determination.

## 7. Supporting Documents

- [Validation Requirements](validation_requirements.md)
- [Traceability Matrix](traceability_matrix.md)
- [Validation Evidence Dossier](VALIDATION_EVIDENCE_DOSSIER.md)
- [Engineering Case Study](ENGINEERING_CASE_STUDY.md)

---

## Conclusion

The prototype demonstrates how risk-based evaluation
can reveal subgroup and performance-monitoring
concerns that an aggregate metric may conceal.

It also illustrates the importance of documenting
dataset limitations, verification evidence, and
unresolved questions.

**AI-assisted educational engineering prototype.**

**Synthetic data only. Not for clinical use.
No ISO 14971, IEC 62304, or MDR conformity claim.**
