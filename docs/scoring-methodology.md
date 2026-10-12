# Scoring and risk methodology

## Weighting
Initial weighted score components:
- Academic 30%
- Attendance 20%
- LMS 15%
- Placement readiness 15%
- Skills 10%
- Engagement 10%

## Normalisation
Each component is normalised to a 0–100 scale using documented formulas. Weighted contribution = component_value * weight.

## Coverage and status
- Missing data is never silently converted to zero.
- Coverage is computed against the applicable weight total.
- If coverage is below 80%, display `Insufficient data`.
- If coverage is adequate but incomplete, the result is labelled `Provisional`.
- Score trends are only compared when scoring profiles are compatible.

## Risk rules
Academic risk and placement risk are computed independently. Thresholds are configurable and described as initial assumptions requiring institutional validation.

## Explainability
Each flag includes the observed evidence, threshold, reporting period, suggested intervention and last calculation timestamp.
