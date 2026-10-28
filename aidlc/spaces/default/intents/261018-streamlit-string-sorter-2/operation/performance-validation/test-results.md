# Test Results — performance-validation

## Status
Not executed. No browser timing or load measurement has been recorded yet. The cases in `load-test-plan.md` (PV-1, PV-2, PV-3) are the manual checks the owner runs against the deployed app.

## Automated evidence (existing)
- The CI `ui` job covers the 100-string cap (NFR3.6): 101 strings shows the limit message with no result columns; 100 strings sorts normally.
- Sorting correctness and step counts are checked against `sorted()` in the algorithm tests.

## Results Log
| Case | Date | Observed time to results | Outcome | Notes |
|---|---|---|---|---|
| PV-1 | (pending) | | | |
| PV-2 | (pending) | | | |
| PV-3 | (pending) | | | |
