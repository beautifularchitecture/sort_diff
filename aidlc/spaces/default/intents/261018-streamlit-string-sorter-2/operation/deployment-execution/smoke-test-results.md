# Smoke Test Results — Streamlit String Sorter

## Sources

- `operation/deployment-execution/deployment-log.md` — deployed commit, build timeline, visibility state.
- `operation/deployment-execution/deployment-execution-questions.md` — Q6 smoke-test answer and the supplied build log.
- `construction/build-and-test/test-results.md` — pre-deployment functional coverage.
- `operation/deployment-pipeline/rollback-runbook.md` — the manual verification procedure this smoke test follows.

## Scope

Post-deployment smoke test of the production Streamlit app at
`https://sortdiff-nnthjumkztx7gfdla6vmlz.streamlit.app/`, deployed from commit
`2952504` on `main`.

The smoke test is the runbook's manual check: the app loads, accepts strings,
runs each of the three sorts, and returns an accuracy-checked sorted result with
the comparison, swap, and accuracy figures shown.

## Environment

| Property | Value |
|---|---|
| Deployed commit | `2952504ea943ca0b2e944f7830417a4f8c387ca5` |
| Deployment time | 2026-10-26 20:04:57 UTC |
| Tester | App owner, signed in to Streamlit Community Cloud |
| Access path | Authenticated browser session (the app is private) |
| Orchestrator access | Not available — unauthenticated requests redirect to Streamlit login |

## Procedure

1. Open the deployed app URL while signed in as the app owner.
2. Enter or select a set of strings.
3. Run bubble sort, selection sort, and quick sort.
4. Confirm each result is in sorted order.
5. Confirm each column shows the algorithm name, the sorted list, comparisons, swaps, and accuracy.
6. Confirm accuracy is checked against the expected sorted result.

## Results

| Check | Result | Detail |
|---|---|---|
| App loads | Pass | The deployed app opened in the owner's authenticated session. |
| Input accepted | Pass | The owner entered or selected strings and ran the sorts. |
| Bubble sort | Pass | Returned a sorted result. |
| Selection sort | Pass | Returned a sorted result. |
| Quick sort | Pass | Returned a sorted result. |
| Accuracy | Pass | Displayed accuracy matched the sorted result. |
| Comparisons | Pass | Counts were shown. |
| Swaps | Pass | Counts were shown. |
| **Overall** | **Pass** | App owner reported: “Smoke test passed.” |

## Limitations

- The smoke test was executed manually by the app owner, not by the orchestrator. The app is private, so an unauthenticated HTTP client cannot reach the application.
- No browser automation is configured in this project, so the interactive checks were not machine-executed.
- Public-access smoke testing remains pending until the app's sharing setting is changed to public.
- No automated post-deploy smoke step exists in CI; this manual check is the only post-deploy functional verification.

## Verdict

**Pass** based on the app owner's authenticated manual test of the deployed
commit. Independent public verification is pending the visibility change; it
does not change the functional result reported here.
