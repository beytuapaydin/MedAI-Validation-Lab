
# Medical AI Risk Register

**Project:** MedAI Validation Lab  
**Version:** 0.2 (in development)  
**Scope:** Synthetic binary medical AI predictions  
**Status:** Educational engineering prototype

> This register is an illustrative risk analysis inspired
> by ISO 14971 principles. It is not a complete clinical
> risk assessment or evidence of regulatory conformity.

## RISK-001 — Missed Detection in Subgroup B

**Failure mode:** The AI model produces false-negative
predictions for patients in subgroup B.

**Hazardous situation:** A false-negative result may
be relied upon during a clinical decision, potentially
delaying appropriate assessment or treatment.

**Potential harm:** Delayed diagnosis or treatment.

**Performance concern:** Subgroup B sensitivity is
approximately 78.8%, below the illustrative 80%
acceptance criterion.

**Related requirement:** REQ-001

**Verification evidence:** TEST-001

**Proposed risk controls:**
- Evaluate sensitivity separately by subgroup.
- Flag subgroup performance below the criterion.
- Require investigation before any simulated release.
- Document limitations and unresolved risks.

**Current disposition:** REVIEW_REQUIRED

**Residual risk:** Not evaluated.

## RISK-002 — Performance Degradation Over Time

**Failure mode:** Model sensitivity decreases between
evaluation periods.

**Hazardous situation:** A degrading model may continue
to produce predictions that are relied upon without
the deterioration being recognized.

**Potential harm:** Missed detection or delayed care.

**Related requirement:** REQ-002

**Verification evidence:** TEST-002 (planned)

**Proposed risk controls:**
- Compare performance across defined periods.
- Flag degradation beyond illustrative thresholds.
- Require investigation of significant changes.

**Current disposition:** ANALYSIS_REQUIRED

**Residual risk:** Not evaluated.

## Important Limitations

- All records and predictions are synthetic.
- Acceptance criteria are illustrative, not clinically
  validated.
- No real clinical deployment or patient impact exists.
- The risk register is preliminary and incomplete.
- Actual risk acceptability requires defined clinical
  context, severity and probability assessment,
  justified controls, and residual-risk evaluation.
