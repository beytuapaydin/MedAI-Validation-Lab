
# Medical AI Validation Requirements

**Project:** MedAI Validation Lab
**Version:** 0.2 (in development)
**Scope:** Synthetic binary medical AI predictions

> These are illustrative engineering requirements.
> Thresholds are not clinically validated.

## REQ-001 — Subgroup Sensitivity

**Requirement:**
The validation system shall calculate sensitivity
separately for each defined subgroup.

The system shall flag any subgroup with sensitivity
below the illustrative threshold of 80%.

**Related risk:** RISK-001

**Verification method:** Automated calculation and
comparison against the configured threshold.

**Test reference:** TEST-001

**Acceptance criteria:**
- Sensitivity calculated for every defined subgroup.
- Subgroup B result correctly identified as below 80%.
- Validation report flags the failed criterion.

## REQ-002 — Performance Degradation

**Requirement:**
The validation system shall calculate sensitivity
for each defined evaluation period.

The system shall identify performance deterioration
exceeding a configurable illustrative threshold.

**Related risk:** RISK-002

**Verification method:** Comparison of sensitivity
between evaluation periods.

**Test reference:** TEST-002 (planned)

**Acceptance criteria:**
- Period-specific sensitivities are calculated.
- Defined performance deterioration is identified.
- The report flags the result for investigation.

## Limitations

Passing these requirements does not demonstrate
clinical safety, diagnostic effectiveness, or
regulatory compliance.
