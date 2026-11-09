# MedAI Validation Lab

**Version 0.1 — medical AI validation evidence prototype (synthetic data only)**

> A high headline score does not prove safety for every patient subgroup.

This small, reproducible Python project evaluates *fictional binary AI predictions* with a standard-library implementation. It is intended as a medical AI safety/quality learning portfolio, not a clinical model, a SaMD, or regulatory-conformity evidence.

## Why this exists

AI-enabled medical software evaluation needs more than one aggregate metric. This example intentionally creates a situation where **overall sensitivity passes a chosen illustrative rule while a subgroup fails it**. The report flags this mismatch for further investigation.

## Run locally (Python 3.10+; no dependencies)

From the project directory:

```bash
python -m medai --output output/demo
python -m unittest discover -s tests -v
```

Review `output/demo/validation_report.md` and the machine-readable `validation_report.json`.

## Evidence produced

- Confusion-matrix counts: TP, FP, TN, FN
- Sensitivity, specificity, false-negative rate, positive predictive value
- 95% Wilson confidence intervals for sensitivity/specificity
- Metrics by predefined fictional cohort and time period
- Comparison of baseline/current sensitivity to flag **performance change** (not statistical evidence of dataset drift)
- Explicit illustrative criteria and `PASS` / `FAIL` / `INSUFFICIENT_DATA` evidence checks
- Report result `REVIEW_REQUIRED`, `EVIDENCE_INCOMPLETE`, or `CRITERIA_MET`

## Dataset

`data/synthetic_predictions.csv` has 320 fictional records. Groups `A` and `B` are **synthetic categories** and do not represent actual demographics. Periods `baseline` and `current` are synthetic windows. The predictions were hand-constructed to demonstrate a hidden failure mode; they are not trained-model outputs.

## Important limitations

- **No patients, real medical data, clinical validation, regulatory submission, or intended-use clearance.**
- Thresholds in `data/illustrative_criteria.json` are made-up teaching criteria, not sourced clinical acceptability requirements.
- The gate represents an **evidence-review flag**, not autonomous release authorization.
- The report does not address prevalence shift, site representativeness, confidence interval-based formal claims, calibration, operating-point selection, reader studies, prospective performance, or clinical utility.
- Sensitivity over time can degrade without feature drift; calling the change "dataset drift" would be inaccurate.
- The software is AI-assisted and requires human technical review.

## Next engineering milestones

1. Define a hypothetical intended use, clinical harm scenario, and stakeholder-approved acceptance criteria with rationale.
2. Add formal requirements / hazards / test traceability and boundary-condition test suite.
3. Demonstrate bootstrapped uncertainty, slice support thresholds, and false-negative investigation workflows.
4. Add interactive dashboard and a structured validation dossier with documented evidence limitations.
5. Optionally evaluate a public **nonclinical or properly licensed** dataset (subject to license/privacy review).

## Regulatory and quality references (context, not compliance claims)

- IMDRF / FDA Good Machine Learning Practice principles: https://www.fda.gov/medical-devices/artificial-intelligence-enabled-medical-devices/good-machine-learning-practice-medical-device-development-guiding-principles
- FDA transparency principles for ML medical devices: https://www.fda.gov/medical-devices/artificial-intelligence-enabled-medical-devices/transparency-machine-learning-enabled-medical-devices-guiding-principles
- ISO 14971 (risk management), IEC 62304 (medical software lifecycle), EU MDR 2017/745 (medical device framework): evaluate scope/applicability separately; this prototype does **not** implement these standards.
