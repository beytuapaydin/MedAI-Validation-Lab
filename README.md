
# MedAI Validation Lab

### Risk-Based Medical AI Validation & Evidence Engineering

**Version 0.4 | AI-Assisted Engineering Portfolio | Synthetic Data Only**

> **A model can meet an overall performance criterion while failing critical subgroup or monitoring criteria.**

MedAI Validation Lab is a reproducible Python prototype demonstrating how medical AI evaluation can connect classification metrics, subgroup analysis, performance monitoring, risk-based requirements, automated verification, and reviewable evidence.

It uses entirely synthetic binary-classification records.

**This is a learning and engineering portfolio prototype, not a clinically validated medical device, SaMD product, or regulatory compliance demonstration.**

---

## 1. The Engineering Problem

Aggregate performance can hide important weaknesses.

A model may satisfy an illustrative overall sensitivity threshold while a defined subgroup performs below its acceptance criterion.

Likewise, changes in performance between evaluation periods may require investigation even when an aggregate metric appears acceptable.

The engineering challenge is not merely calculating metrics. It is making failures, evidence gaps, and limitations visible and traceable.

## 2. What the Prototype Demonstrates

- Binary classification evaluation using confusion-matrix metrics
- Sensitivity, specificity, false-negative rate, and predictive value
- Approximate 95% Wilson confidence intervals
- Subgroup-specific sensitivity assessment
- Period-specific performance comparison
- Cohort-by-period stratified analysis
- Detection of missing subgroup-period combinations
- Configurable illustrative acceptance checks
- Risk-to-requirement-to-test traceability
- Reproducible JSON and Markdown evidence reports
- A local, read-only dashboard with selectable datasets
- Automated verification through GitHub Actions

The implementation uses the Python standard library and requires no third-party packages.

## 3. Two Synthetic Evaluation Scenarios

### Scenario A — Original Dataset

**320 synthetic records**

The overall sensitivity criterion passes, while subgroup B and the period-change criterion fail.

| Metric | Result |
|---|---:|
| Overall sensitivity | 85.62% |
| Overall specificity | 92.50% |
| Subgroup A sensitivity | 92.50% |
| Subgroup B sensitivity | 78.75% |
| Period sensitivity change | -13.75 percentage points |
| Evidence review status | REVIEW_REQUIRED |

**Limitation:** Subgroup membership and evaluation period are completely confounded in this dataset. The observed period difference cannot be independently attributed to time.

### Scenario B — Balanced Dataset

**320 synthetic records; both subgroups represented in both periods**

| Subgroup | Baseline sensitivity | Current sensitivity | Change |
|---|---:|---:|---:|
| A | 95.0% | 90.0% | -5.0 percentage points |
| B | 85.0% | 70.0% | -15.0 percentage points |

Additional results:

| Metric | Result |
|---|---:|
| Overall sensitivity | 85.0% |
| Overall specificity | 92.5% |
| Subgroup A sensitivity | 92.5% |
| Subgroup B sensitivity | 77.5% |
| Overall period sensitivity change | -10.0 percentage points |
| Evidence review status | REVIEW_REQUIRED |

This second scenario allows descriptive within-cohort comparisons across periods.

It does not demonstrate causality, actual clinical model degradation, algorithmic discrimination, or data drift.

Both datasets contain fictional predictions constructed for demonstration purposes.

## 4. Risk-Based Validation and Traceability

The project contains two illustrative risk scenarios:

| Risk | Engineering concern | Requirement | Test |
|---|---|---|---|
| RISK-001 | Missed detection in a subgroup | REQ-001 | TEST-001 |
| RISK-002 | Performance deterioration across periods | REQ-002 | TEST-002 |

The repository provides:

- [Risk Register](docs/risk_register.md)
- [Validation Requirements](docs/validation_requirements.md)
- [Traceability Matrix](docs/traceability_matrix.md)
- [Validation Evidence Dossier](docs/VALIDATION_EVIDENCE_DOSSIER.md)

These documents illustrate risk-based engineering practices.

They do not constitute a complete ISO 14971 risk management file, IEC 62304 lifecycle record, or MDR conformity assessment.

## 5. Automated Verification

The prototype includes **19 automated Python tests**, covering:

- Binary classification calculations
- Input integrity and duplicate-record rejection
- Undefined metrics and insufficient evidence
- Subgroup performance checks
- Acceptance-threshold boundary conditions
- Period sensitivity comparisons
- Cohort-by-period stratification
- Missing-combination detection
- JSON and Markdown evidence generation
- Dashboard content and safety disclaimers

The test suite runs through GitHub Actions on:

- Python 3.10
- Python 3.12

The 19-test suite passed in both configured environments during the verified development workflow.

[View GitHub Actions](../../actions)

**Important distinction:** Passing these tests supports the behavior of the validation software for covered cases. It does not demonstrate clinical acceptability of the evaluated AI predictions.

## 6. Run the Prototype Locally

Requirements:

- Python 3.10 or newer
- No external Python dependencies

Clone the repository:

```bash
git clone https://github.com/beytuapaydin/MedAI-Validation-Lab.git
cd MedAI-Validation-Lab
```

Run the original evaluation:

```bash
python -m medai --output output/demo
```

Generate the balanced synthetic dataset:

```bash
python tools/generate_balanced_dataset.py
```

Run the balanced evaluation:

```bash
python -m medai --data data/synthetic_predictions_balanced.csv --output output/balanced
```

Execute automated tests:

```bash
python -m unittest discover -s tests -v
```

Start the local dashboard:

```bash
python -m dashboard.app
```

Open:

http://127.0.0.1:8766

The dashboard includes an **Evaluation Scenario** selector for comparing the original and balanced datasets.

The application binds to the local loopback address and is not intended for public hosting.

## 7. Repository Structure

```text
MedAI-Validation-Lab/
├── .github/workflows/
│   └── tests.yml
├── dashboard/
│   └── app.py
├── data/
│   ├── synthetic_predictions.csv
│   ├── synthetic_predictions_balanced.csv
│   └── illustrative_criteria.json
├── docs/
│   ├── risk_register.md
│   ├── validation_requirements.md
│   ├── traceability_matrix.md
│   └── VALIDATION_EVIDENCE_DOSSIER.md
├── medai/
│   ├── __main__.py
│   └── validation.py
├── output/
│   ├── demo/
│   └── balanced/
├── tests/
└── tools/
    └── generate_balanced_dataset.py
```

## 8. Evidence Interpretation

An evidence review status such as `REVIEW_REQUIRED` is not an automated clinical approval or prohibition decision.

It indicates that illustrative criteria have not been met and further investigation is warranted.

The current evidence is limited by:

- Fully synthetic and deliberately constructed records
- Illustrative, non-clinical acceptance thresholds
- Small subgroup denominators
- Lack of clinical intended-use validation
- No independent clinical data or external validation
- No formal residual-risk or benefit-risk assessment
- No independent regulatory conformity assessment

The original dataset additionally confounds subgroup and period. The balanced dataset addresses missing combinations but does not resolve causal inference questions.

## 9. Engineering Approach

This project was developed using AI-assisted coding and iterative testing.

Its purpose is to explore practical engineering questions related to Medical AI Validation, Quality Assurance, Safety Evidence, and Risk-Based Verification.

The repository is intended to be reproducible, reviewable, and open to technical critique.

## 10. Key Takeaway

**Good medical AI validation does not stop at an aggregate performance score.**

It must identify subgroup failures, evaluate performance changes, connect findings to requirements and tests, and explicitly document unresolved limitations.

This prototype demonstrates those engineering principles using synthetic scenarios, without making clinical or regulatory compliance claims.

---

**Research and educational portfolio project — not for clinical use.**
