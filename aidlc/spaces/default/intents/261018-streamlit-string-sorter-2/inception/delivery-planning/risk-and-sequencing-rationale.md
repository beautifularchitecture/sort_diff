# Risk and Sequencing Rationale

## Sequencing Heuristic

**Value-first, constrained by the dependency chain.** The Unit DAG is linear (U1 → U2 → U3), so sequencing is fixed by dependency. Value-first decides only emphasis within that order: U1 carries the core value (correct sorts and comparable counts), so it comes first.

WSJF scoring (Reinertsen / SAFe) was considered and not used, because a linear chain leaves no ordering choice for a score to change.

No walking skeleton (team.md). Bolt 1 is a complete, checkable domain slice, not a thin end-to-end skeleton. The end-to-end integration happens in Bolt 2.

## Risks and Mitigations

| # | Risk | Effect if it happens | Mitigation | Bolt |
|---|---|---|---|---|
| R1 | FR4.1 (loop iterations) and FR4.2 (element comparisons) are not reconciled, and quick sort's partition step is unclear | Counts are inconsistent across algorithms, undermining the app's main teaching point | Settle one definition in Functional Design for U1 before any counting code | Bolt 1 |
| R2 | FR1.3 wording says "only allows" ASCII, while the design passes non-ASCII through (D10) | Ambiguous acceptance criteria for normalization tests | Update FR1.3 wording to match D10 before Functional Design; contract 1 already encodes D10 | Bolt 1 |
| R3 | Target Python version and dependency pinning are undecided | CI configuration cannot be finalized | Decide during Bolt 3, before the CI workflow is written | Bolt 3 |
| R4 | US5.2 (Must, deploy on merge) depends on US5.1 (Should, local run) | If Should stories are descoped, the deploy story loses its prerequisite | Keep US5.1 in scope; it is needed for Bolt 2's demo anyway | Bolt 2 |
| R5 | The Streamlit Community Cloud account or deploy connection is not ready | Bolt 3 cannot be verified end to end | Set up the account early, while Bolts 1 and 2 run | Bolt 3 |
| R6 | The verification command is deferred until U1 exists | No automated check is recorded at the first checkpoint | Propose `pytest` at Bolt 1's checkpoint, for approval | Bolt 1 |

## Why This Order Is Safe

Each Bolt depends only on finished work from the previous Bolt. A failure in Bolt 1 (counts or accuracy) is caught before any UI exists, and the UI cannot hide a domain bug. Bolt 3 is last because it has nothing to deploy until the app runs.
