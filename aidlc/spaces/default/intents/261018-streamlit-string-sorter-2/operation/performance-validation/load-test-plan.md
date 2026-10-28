# Load Test Plan — performance-validation

## Scope
Single Streamlit app on Streamlit Community Cloud. One interactive user at a time, sequential runs (Q1 A). No throughput measurement (Q3 A).

## Objective
Confirm that the worst-case input (100 de-duplicated strings, the NFR3.6 cap) produces a result in a few seconds on the deployed app (Q2 A). No numeric p95 target is set.

## Test Cases
| ID | Scenario | Input | Expected |
|---|---|---|---|
| PV-1 | Cap boundary, accepted | 100 unique strings | Three result columns render; each shows Comparisons, Swaps, Accuracy |
| PV-2 | Cap boundary, refused | 101 strings | Limit message shown; no result columns |
| PV-3 | Typical input | 10 strings | Sorted output in all three columns, with accuracy pass |

## Method
1. Open the deployed app in a browser as the owner (the app is private; see the project's deployment notes).
2. Enter the PV-1 input and press Sort. Time from click to visible results with a stopwatch or browser timer.
3. Repeat PV-2 and PV-3.
4. Record the observed times and outcomes in `test-results.md`.

## Tooling
Manual browser run. No load generator, since concurrency is out of scope. The GitHub Actions `ui` job already exercises the 100-string cap in the test suite and is the automated evidence.

## Exit Criteria
PV-1 and PV-3 render correctly. PV-2 shows the limit message. PV-1 completes in a few seconds as judged by the owner.
