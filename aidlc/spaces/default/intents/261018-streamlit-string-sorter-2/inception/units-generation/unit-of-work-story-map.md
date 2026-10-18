# Unit of Work — Story Map

Every upstream story is assigned to one primary Unit. Cross-cutting rows note supporting Units.

## Story to Unit

| Story | Unit ID | Directory | Summary |
|---|---|---|---|
| US1.1 | U2 | `u2-playground-ui` | Manual entry in the text area; normalization applied by U1 |
| US1.2 | U2 | `u2-playground-ui` | Word-list picker; list owned by U2 |
| US2.1 | U1 | `u1-sorting-core` | Three algorithms run on one input; Sort button wiring in U2 |
| US3.1 | U2 | `u2-playground-ui` | Side-by-side display of U1 results |
| US3.2 | U1 | `u1-sorting-core` | Comparisons, swaps, accuracy computed in U1; displayed in U2 |
| US4.1 | U2 | `u2-playground-ui` | Exact FR6.1 warning on empty shared list |
| US4.2 | U1 | `u1-sorting-core` | Single, identical, and empty-token edge cases |
| US5.1 | U2 | `u2-playground-ui` | Local run via `streamlit run` |
| US5.2 | U3 | `u3-delivery-pipeline` | Auto-deploy to Streamlit Community Cloud on merge to `main` |

## Rows Spanning Multiple Units

| Concern | Units | Notes |
|---|---|---|
| Normalization rule (FR1.3) | U1 (rule), U2 (display of normalized echo) | The echo in U2 shows U1's output |
| Accuracy and step counts | U1 (compute), U2 (display) | Same metric definition in both |
| Test coverage floor (~80%) | U1 (sorting logic), U2 (UI wiring smoke), U3 (CI enforcement) | U3 enforces the floor in CI |

## Implementation Order Within Each Unit

Recorded for orientation only. Economic sequencing belongs to Delivery Planning.

- **U1**: InputProcessor, then SortingEngine (the three algorithms), then AccuracyChecker. Test-after each piece.
- **U2**: WordListProvider, then SortingPlaygroundApp wiring, then empty-state and warning paths. Test-after each piece.
- **U3**: CI workflow (install, lint, format, test), then deploy step on merge to `main`.

## Coverage Verification

- Every story ID (US1.1 to US5.2) appears exactly once as a primary assignment.
- Every Unit has at least one story row: U1 (US2.1, US3.2, US4.2), U2 (US1.1, US1.2, US3.1, US4.1, US5.1), U3 (US5.2).
- No story is unassigned.
