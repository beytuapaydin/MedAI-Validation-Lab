# Engineering Case Study
## When Overall Medical AI Performance Hides Subgroup Failure

**Project:** MedAI Validation Lab  
**Version:** 0.4  
**Focus:** Medical AI Validation | Risk-Based Verification | Safety Evidence  
**Development:** AI-assisted engineering portfolio  
**Data:** Synthetic only

---

### 1. The Engineering Challenge

Medical AI evaluation cannot rely on a single aggregate performance metric.

A binary classification model might meet an overall sensitivity criterion while exhibiting unacceptable performance in a defined subgroup.

Similarly, performance differences across evaluation periods may remain hidden unless they are explicitly monitored.

This case study explores how to make these concerns visible, reproducible, and traceable.

**Engineering question:**

How can a validation workflow detect hidden performance failures and communicate the resulting evidence without presenting preliminary metrics as proof of clinical safety?

### 2. Prototype Design

MedAI Validation Lab implements a small, reproducible Python validation workflow.

The system:

- Loads and validates synthetic classification records.
- Calculates confusion-matrix metrics and approximate confidence intervals.
- Evaluates subgroup-specific sensitivity.
- Compares performance across defined periods.
- Analyzes subgroup-by-period combinations.
- Applies configurable illustrative acceptance criteria.
- Generates JSON and Markdown evidence reports.
- Presents results through a local read-only dashboard.
- Links selected findings to requirements, risks, and executable tests.

The implementation uses Python's standard library.

### 3. Initial Evaluation

The first dataset contains 320 synthetic predictions.

| Metric | Result |
|---|---:|
| Overall sensitivity | 85.62% |
| Overall specificity | 92.50% |
| Subgroup A sensitivity | 92.50% |
| Subgroup B sensitivity | 78.75% |

The overall sensitivity satisfies the illustrative 85% criterion.

However, subgroup B fails the illustrative 80% minimum.

**Finding 1:** Aggregate performance can conceal a failed subgroup acceptance criterion.

The validation system returns `REVIEW_REQUIRED` rather than presenting the overall PASS result as sufficient evidence.

### 4. Discovery of a Methodological Limitation

Review of the initial dataset identified a confounding problem.

All subgroup A observations belonged to the baseline period, while all subgroup B observations belonged to the current period.

Consequently, the dataset could not distinguish subgroup-associated differences from period-associated differences.

This was documented as a limitation rather than interpreted as independent evidence of temporal degradation.

### 5. Improved Evaluation Design

A second synthetic dataset was constructed with both subgroups represented in both evaluation periods.

The resulting stratified sensitivities were:

| Subgroup | Baseline | Current | Change |
|---|---:|---:|---:|
| A | 95.0% | 90.0% | −5.0 percentage points |
| B | 85.0% | 70.0% | −15.0 percentage points |

The balanced scenario permits separate descriptive comparisons within each subgroup.

Its aggregated sensitivity is 85.0%, meeting the illustrative overall threshold.

Nevertheless, subgroup B sensitivity is 77.5%, below its illustrative 80% minimum, and the overall period sensitivity decline is 10 percentage points, exceeding the illustrative 8-point limit.

**Finding 2:** The evaluation workflow detects failures that are not apparent from the headline aggregate score.

**Finding 3:** Dataset structure is itself an important validation consideration. Improved stratification supports more informative comparisons, without establishing causality.

### 6. Risk-Based Verification

Two illustrative risks were documented.

**RISK-001 — Missed Detection in a Subgroup**

Potential failure mode: Increased false-negative predictions in a defined subgroup.

Related requirement: `REQ-001`

Verification reference: `TEST-001`

**RISK-002 — Performance Degradation**

Potential failure mode: Reduced sensitivity between defined evaluation periods.

Related requirement: `REQ-002`

Verification reference: `TEST-002`

Supporting documentation includes a preliminary risk register, validation requirements, a traceability matrix, and an evidence dossier.

The risk assessment is illustrative. Formal clinical severity, risk acceptability, and residual-risk evaluations were not completed.

### 7. Automated Verification Evidence

The prototype includes 19 automated Python tests, covering calculation behavior, invalid inputs, subgroup checks, threshold boundaries, reporting, and cohort-period analysis.

The tests ran successfully under Python 3.10 and Python 3.12 in GitHub Actions.

Passing software tests support the tested behavior of the validation workflow.

They do not establish the clinical safety, effectiveness, or acceptability of a medical AI model.

### 8. Evidence Presentation

A local dashboard presents both synthetic evaluation scenarios.

Users can inspect:

- Overall sensitivity and specificity
- Subgroup performance
- Period-specific performance differences
- Cohort-by-period evidence
- Within-cohort sensitivity changes
- Illustrative acceptance-check failures
- Evidence-review status

Both scenarios produce `REVIEW_REQUIRED`.

This status indicates unresolved illustrative evaluation criteria requiring investigation. It is not a clinical release decision.

### 9. Key Engineering Lessons

**Aggregate performance is not sufficient.** Evaluation must consider relevant subgroups and predefined failure conditions.

**Dataset design affects interpretability.** Confounded variables can limit the conclusions that may be drawn.

**Verification and validation are distinct.** Correct operation of evaluation software does not establish clinical validity of the evaluated model.

**Traceability matters.** Engineering findings should connect to requirements, tests, and reviewable evidence.

**Limitations are part of the evidence.** Uncertainty and unresolved risks should be documented rather than hidden.

### 10. Limitations and Next Steps

This is an AI-assisted educational engineering prototype using fictional records and illustrative thresholds.

It has not been independently clinically validated and does not demonstrate compliance with ISO 14971, IEC 62304, or the EU MDR.

Potential future work includes clinical intended-use definition, independently justified acceptance criteria, stronger statistical uncertainty assessment, more comprehensive risk controls, and evaluation of appropriately authorized representative datasets.

### 11. Conclusion

MedAI Validation Lab illustrates an important principle for Medical AI Validation and Safety Assurance:

**A trustworthy evaluation workflow must expose subgroup failures, performance changes, methodological limitations, and unresolved evidence gaps—not merely report a successful aggregate score.**

---

**Repository:** https://github.com/beytuapaydin/MedAI-Validation-Lab

**Research and educational portfolio project. Not for clinical use.**
