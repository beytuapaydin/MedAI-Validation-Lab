
# Medical AI Validation Traceability Matrix

**Project:** MedAI Validation Lab  
**Version:** 0.2 (in development)  
**Scope:** Synthetic binary AI predictions

> This matrix tracks illustrative engineering evidence.
> It does not establish clinical safety or regulatory conformity.

## Risk-to-Verification Traceability

| Risk ID | Requirement ID | Test ID | Expected evidence | Verification status |
|---|---|---|---|---|
| RISK-001 | REQ-001 | TEST-001 | Subgroup sensitivity calculation and threshold flag | Mapping pending |
| RISK-002 | REQ-002 | TEST-002 | Period sensitivity comparison and degradation flag | Test mapping pending |

## Evidence Sources

- Source code: `medai/validation.py`
- Automated test module: `tests/test_validation.py`
- Synthetic dataset: `data/synthetic_predictions.csv`
- Illustrative thresholds: `data/illustrative_criteria.json`
- Example report: `output/demo/validation_report.json`
- CI workflow: `.github/workflows/tests.yml`

## Verification Rules

A requirement may be marked VERIFIED only when:

1. Its test is explicitly identified in the test code.
2. The test checks the intended acceptance criteria.
3. The test result is reproducible.
4. The resulting evidence is linked and reviewable.
5. Any limitations or unresolved failures are recorded.

## Open Actions

- Map TEST-001 to executable test assertions.
- Implement or map TEST-002 to executable assertions.
- Verify that both tests cover their stated acceptance criteria.
- Record reproducible test results and evidence references.
- Review failed subgroup performance separately from
  successful operation of the validation software.

## Important Distinction

A passing software test demonstrates that the validation
logic behaves as expected for the tested inputs.

It does not imply that the evaluated medical AI model
meets its performance acceptance criteria.
