# Performance Validation Questions

## Q1: Traffic pattern
The app is a single-user classroom tool: one run per Sort press, with input capped at 100 strings (NFR3.6). Which traffic pattern should validation cover?

A. Single user, sequential runs at the 100-string cap (Recommended)
B. Multiple concurrent users (describe the number)
X. Other (please specify)

[Answer]: A

## Q2: Latency targets
The NFR record sets no numeric latency target (NFR Q4 A). Which target should this stage record?

A. No numeric target; verify that a 100-string sort completes in a few seconds on the deployed app (Recommended)
B. Set a p95 target (give the value)
X. Other (please specify)

[Answer]: A

## Q3: Throughput
Throughput is not a requirement (one interactive user). Should it be measured?

A. No throughput measurement (Recommended)
B. Measure throughput (describe the load)
X. Other (please specify)

[Answer]: A

## Q4: Likely bottlenecks
Sorting is in-process and recomputed each rerun (PD-1, PD-2). Which area should the report examine?

A. Rendering and sorting at the 100-string cap; no external dependencies (Recommended)
B. Add another area (describe it)
X. Other (please specify)

[Answer]: A

## Consolidated Summary Confirmation

- Q1 Traffic pattern: A — single user, sequential runs at the 100-string cap.
- Q2 Latency target: A — no numeric target; a 100-string sort completes in a few seconds on the deployed app.
- Q3 Throughput: A — no throughput measurement.
- Q4 Bottlenecks: A — rendering and sorting at the 100-string cap; no external dependencies.

Does this all look correct before I generate the artifacts?
- Looks correct
- Request changes

[Answer]: Looks correct
