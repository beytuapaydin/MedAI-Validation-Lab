# MedAI Validation Evidence Report

**Status:** `REVIEW_REQUIRED`

> Synthetic demonstration only. Not clinical validation, release approval, or regulatory conformity.

## Overall confusion matrix and metrics

```json
{
  "n": 320,
  "tp": 136,
  "fn": 24,
  "tn": 148,
  "fp": 12,
  "sensitivity": 0.85,
  "specificity": 0.925,
  "false_negative_rate": 0.15,
  "positive_predictive_value": 0.9189,
  "sensitivity_ci_95_wilson": [
    0.7865,
    0.8971
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
| B | 160 | 62 | 18 | 0.775 | [0.6721, 0.8527] |

## Cohort x Period Analysis

| Cohort | Period | N | TP | FN | Sensitivity |
|---|---|---:|---:|---:|---:|
| A | baseline | 80 | 38 | 2 | 0.95 |
| A | current | 80 | 36 | 4 | 0.9 |
| B | baseline | 80 | 34 | 6 | 0.85 |
| B | current | 80 | 28 | 12 | 0.7 |

## Within-Cohort Sensitivity Changes

| Cohort | Sensitivity change |
|---|---:|
| A | -5.00 percentage points |
| B | -15.00 percentage points |

## Cohort-Period Coverage

Every defined cohort is represented in every defined evaluation period.

## Predefined illustrative criteria

| Criterion | Observed | Rule | Result |
|---|---:|---|---|
| overall_sensitivity | 0.85 | >= 0.85 | **PASS** |
| overall_specificity | 0.925 | >= 0.8 | **PASS** |
| cohort_A_sensitivity | 0.925 | >= 0.8 | **PASS** |
| cohort_A_minimum_positives | 80 | >= 15 | **PASS** |
| cohort_B_sensitivity | 0.775 | >= 0.8 | **FAIL** |
| cohort_B_minimum_positives | 80 | >= 15 | **PASS** |
| period_sensitivity_drop | 0.1 | <= 0.08 | **FAIL** |

## Interpretation and limits

- A failure triggers human investigation; it does not diagnose a patient or authorize deployment.
- A change in sensitivity is not proof of feature or covariate drift.
- Complete cohort-period coverage does not establish causal independence.
- Small subgroup denominators can produce wide confidence intervals.
- Acceptance thresholds are illustrative.
- No clinical data, clinical validation, or formal standards compliance is claimed.
