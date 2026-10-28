# NFR Validation Matrix — performance-validation

| NFR | Target | Evidence | Status |
|---|---|---|---|
| NFR3.6 | Hard cap of 100 strings; 101 shows the limit message | CI `ui` job tests; manual PV-2 | Covered by tests; manual check pending |
| NFR3.6 (latency) | No numeric target; 100-string sort completes in a few seconds (Q2 A) | Manual PV-1 timing | Pending: not yet measured |
| NFR1.1 | Accuracy result shown exactly as computed | UI test (accuracy fail renders `Accuracy: fail`) | Covered by tests |
| NFR2.2 | Each column shows name, list, Comparisons, Swaps, Accuracy | UI test asserting all five elements | Covered by tests |
| Throughput | Not a requirement (Q3 A) | None | Not applicable |
