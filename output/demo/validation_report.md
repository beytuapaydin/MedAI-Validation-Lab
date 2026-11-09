# MedAI Validation Evidence Report

**Status:** `REVIEW_REQUIRED`

> Synthetic demonstration only. Not clinical validation, release approval, or regulatory conformity.

## Overall confusion matrix and metrics

```json
{
  "n": 320,
  "tp": 137,
  "fn": 23,
  "tn": 148,
  "fp": 12,
  "sensitivity": 0.8562,
  "specificity": 0.925,
  "false_negative_rate": 0.1437,
  "positive_predictive_value": 0.9195,
  "sensitivity_ci_95_wilson": [
    0.7935,
    0.9023
  ],
  "specificity_ci_95_wilson": [
    0.8735,
    0.9566
  ]
}
```

## Subgroup metrics

| Cohort | N | TP | FN | Sensitivity | 95% Wilson CI |
|---|---:|---:|---:|---:|---|
| A | 160 | 74 | 6 | 0.925 | [0.8459, 0.9652] |
| B | 160 | 63 | 17 | 0.7875 | [0.6858, 0.8629] |

## Predefined illustrative criteria

| Criterion | Observed | Rule | Result |
|---|---:|---|---|
| overall_sensitivity | 0.8562 | >= 0.85 | **PASS** |
| overall_specificity | 0.925 | >= 0.8 | **PASS** |
| cohort_A_sensitivity | 0.925 | >= 0.8 | **PASS** |
| cohort_A_minimum_positives | 80 | >= 15 | **PASS** |
| cohort_B_sensitivity | 0.7875 | >= 0.8 | **FAIL** |
| cohort_B_minimum_positives | 80 | >= 15 | **PASS** |
| period_sensitivity_drop | 0.1375 | <= 0.08 | **FAIL** |

## Interpretation and limits

- A failure triggers human investigation; it does not diagnose a patient or automatically authorize/block deployment.
- A change in sensitivity over time is **performance degradation**, not proof of feature/covariate drift.
- Small subgroup denominators create wide confidence intervals; illustrative cutoffs are not clinical requirements.
- No clinical data, patient identifiers, clinical validation, or formal standards compliance is claimed.
