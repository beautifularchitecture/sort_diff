# Code Generation Plan — playground-ui (U2)

## Summary

- Builds: the Streamlit single-page playground (`app.py`) that wires widgets to sorting-core, plus UI tests under `tests/ui/`.
- Touches: `app.py`, `requirements.txt` (add `streamlit>=1.40`), `tests/ui/` (new), and Step 5 artifacts under the unit record.
- Tests: standard strategy, test-after: UI wiring tests driven by `streamlit.testing.v1.AppTest`, about 12 tests, run with `pytest tests/ui/ -q`.

## Goals

- Implement `app.py` so it realizes the approved design: `functional-design/functional-spec.md` (Parts 2–6), `nfr-design/security-design.md` (SD-1..SD-6), `nfr-design/performance-design.md` (PD-1..PD-4), `nfr-design/logical-components.md`, and the `infrastructure-design/cicd-pipeline.md` `ui` job.
- Presentation and orchestration only (ADR-004): no sorting, normalization, or verification logic in this Unit. All of that is U1's `sorting_core`.
- Contract 2 (U2 → U3): entrypoint `app.py`, `requirements.txt` declares `streamlit`, local run `streamlit run app.py`.
- SD-2 plain-text rendering only (no `unsafe_allow_html`); SD-3 100-string cap before `normalize`; SD-4 no I/O/network/persistent storage; SD-5 no identity; SD-6 exceptions propagate.
- PD-1/PD-2 no caching, recompute from widgets each rerun; PD-3 three columns in one pass; PD-4 build and de-duplicate the shared list once per rerun.

## Traceability (plan step → design IDs)

| Plan step | Design IDs |
|---|---|
| 1 Module skeleton and entry point | Contract 2, logical-components.md (SortingPlaygroundApp) |
| 2 Bundled word list (WordListProvider) | FR1.5, AC1.2.1, AC1.2.3, SD-4, logical-components.md |
| 3 Shared list build + de-duplication | FR1.4, AC1.1.1, AC1.2.2, PD-4, functional-spec Part 3 |
| 4 100-string cap before normalize | NFR3.6, SD-3, functional-spec Part 3 |
| 5 Sort trigger + empty-input guard | FR6.1, AC4.1.1, AC4.1.2, functional-spec Part 4 |
| 6 Pipeline wiring (normalize, run_all, check) | Contract 1, AC1.2.1, ADR-004, functional-spec Part 7 |
| 7 Result rendering (echo + 3 columns, metrics, accuracy) | AC3.1.1–AC3.1.3, AC3.2.5, Q3 A, Q4 A, PD-3, SD-2 |
| 8 Error propagation (no catching) | NFR3.1, SD-6 |
| 9 UI tests (AppTest) | NFR4.2, all of the above |
| 10 Test configuration and coverage gate | NFR4.1, NFR4.2 |
| 11 Step 5 artifacts (summary, traceability, manifest) | Step 5 artifacts |

## Implementation Steps

1. [x] **Module skeleton and entry point (`app.py`).** Top-level Streamlit script at the repository root, entry point `app.py` (Contract 2). Page title and the single screen: input row (text area + word-list multiselect + Sort button), the empty-state hint, the FR6.1 warning area, the input echo, and three result columns. No custom CSS (design-system-mapping). Source: Contract 2, logical-components.md.
2. [x] **Bundled word list (`app.py`, WordListProvider).** A module-level constant `WORD_LIST: list[str]` — a fixed, non-empty list of common words, no I/O, no network, no file read (SD-4, FR1.5). Exposed read-only as the multiselect options. Source: FR1.5, AC1.2.1, AC1.2.3.
3. [x] **Shared list build and de-duplication (`build_shared_list`).** Combine the typed entries and the picked words in that order, then de-duplicate while preserving first-seen order, so a string entered twice sorts once (Q2 Option C). Typed entries are the raw text split the same way `normalize` will split them only for de-duplication purposes; the actual tokenization stays in U1's `normalize`. Source: FR1.4, AC1.1.1, AC1.2.2, PD-4.
4. [x] **100-string cap (`build_shared_list` / Sort handler).** On the de-duplicated shared list, immediately before `normalize`, if `len(shared_list) > 100` refuse to sort and show a message stating the limit (SD-3, NFR3.6). This also bounds quick-sort recursion depth (security-design.md Boundary Behaviour). Source: SD-3.
5. [x] **Sort trigger and empty-input guard.** On Sort press: build the shared list; if it is empty, render the exact message `Enter or select at least one string`, run no algorithm, produce no result panels, and hide the three columns (Q1 Option A, FR6.1, AC4.1.1, AC4.1.2). The empty-state hint shows only before the first Sort press. Source: functional-spec Part 4.
6. [x] **Pipeline wiring.** On a non-empty, within-cap list: `sort_input = normalize(shared_list)`, `results = run_all(sort_input)`, then `check(result, sort_input)` for each result in `[bubble, selection, quick]` order (Contract 1). No caching (PD-1); results recomputed from the current widget values every rerun (PD-2); no `st.session_state` for results. Source: Contract 1, ADR-004, functional-spec Part 7.
7. [x] **Result rendering (`render_results`).** Render the input echo, then `st.columns(3)` with one column per result in `[bubble, selection, quick]` order (PD-3). Each column shows the algorithm name, the sorted list, `Comparisons: N`, `Swaps: N`, and `Accuracy: pass`/`Accuracy: fail`, counts as full integers with no truncation. All text through Streamlit's default text/table APIs with plain strings; never `unsafe_allow_html=True` (SD-2). Source: AC3.1.1–AC3.1.3, AC3.2.5, Q3 A, Q4 A.
8. [x] **Error propagation.** Do not wrap the U1 calls in try/except; let `TypeError`/`ValueError`/`RecursionError` propagate so Streamlit shows the traceback (SD-6, NFR3.1). Errors are surfaced, never swallowed. Source: SD-6.
9. [x] **UI tests (`tests/ui/`).** Test-after (team posture). Drive the page through `streamlit.testing.v1.AppTest` (bundled with `streamlit>=1.40`) so widget calls execute and `--cov=app` is measurable. Cases:
   - happy path: typed input `["banana", "apple", "cherry"]` renders three columns with the correct sorted order and pass accuracy;
   - de-duplication: a string typed and picked once sorts once;
   - empty input: the exact message `Enter or select at least one string` appears and no columns render;
   - over-cap input: a message stating the 100-string limit appears and no sorting runs;
   - counts: `Comparisons: N` and `Swaps: N` render as full integers per algorithm;
   - words: the bundled list is non-empty and read-only;
   - plain-text safety: no `unsafe_allow_html` is used.
   Keep the patterns that cannot run without a full Streamlit runtime (if any) in importable helpers under test. Source: NFR4.2, all of the above.
10. [x] **Test configuration and the streamlit dependency.** Add `streamlit>=1.40` to the top-level `requirements.txt` (Contract 2 obligation; the file currently holds only `pytest`/`pytest-cov`/`black`/`ruff`). Use the existing `pyproject.toml` pytest configuration; the UI tests live under `tests/ui/` so the shared `tests/` root stays U1's. Do not lower the 80% coverage floor. Source: NFR4.1, NFR4.2, cicd-pipeline.md.
11. [x] **Step 5 artifacts.** Write `code-summary.md`, `traceability.json` (every assigned AC and NFR sub-ID; every OK target an existing file), and `source-manifest.json` listing every application-source path created or modified (`app.py`, `requirements.txt`, `tests/ui/`). Source: Step 5.

## Test Considerations (for code writer)

- Counts and sorted orders come from U1's `sorting_core`; do not change expected values to match the UI. The UI only displays what U1 returns.
- The exact empty-input string is `Enter or select at least one string` (FR6.1) — reproduce it character for character.
- Boundary: user strings are inert data (SD-1); no `eval`/`exec`; no `unsafe_allow_html`.
- Do not weaken the 80% coverage floor to make a step pass; surface the gap instead.

## Non-Functional Notes

- Presentation only: no sorting, normalization, or verification logic in this Unit (ADR-004).
- `app.py` and its tests follow Black, Ruff, snake_case (NFR4.1).
- No I/O, network, persistent storage, or identity (SD-4, SD-5).
- Local run: `streamlit run app.py` (Contract 2, US5.1).

## Testing Contract

```json
{
  "version": 1,
  "methodology": "test-after",
  "source": "team",
  "ordering": "Implement each testable piece — each sorting algorithm, then the UI wiring — and then write and run that piece's tests before moving on to the next piece.",
  "scope": "feature",
  "test_strategy": "standard",
  "project_type": "greenfield",
  "applicable_notes": [
    {
      "layer": "org",
      "text": "We treat tests as a first-class deliverable in every Bolt. The specific\nmethodology (TDD, BDD, ATDD, or classic test-after) is affirmed at\npractices-discovery and recorded in `team.md` under this heading with explicit\n`Methodology` and `Ordering` fields; Code Generation resolves those fields\nindependently from coverage, tooling, and scope notes.\n\nWhen no posture has been affirmed, our default per scope is:\n- **Methodology**: test-after\n- **Ordering**: implement each applicable testable layer, then write and run\n  that layer's tests.\n- `mvp`, `enterprise`, `feature`, `infra`, `classic` add an 80% line-coverage\n  floor and CI execution before merge.\n- `bugfix`, `security-patch` add a targeted regression for the specific\n  bug/vulnerability and require the existing suite to remain green.\n- `express` uses the Minimal strategy: requirement-driven unit tests (one per\n  requirement, with a happy-path floor per component); existing tests remain\n  green.\n- `poc`, `refactor`, `workshop` add no extra new-test floor and require the\n  existing suite to remain green.\n\nThe active `Test Strategy` still applies in every scope and determines test\nvolume/types. Scope floors are additive; they never reduce or replace the\nselected strategy.\n\nBuild and Test verifies defined coverage floors and affirmed quality targets;\nthey may not be weakened to make a step pass.\n\nAffirm a stricter posture in `team.md` if the team commits to one."
    },
    {
      "layer": "team",
      "text": "- **Methodology**: test-after\n- **Methodology evidence**: The human chose \"tests after each piece is implemented\" in the interview (Q3, answer A — the org default for this scope), so tests are written after each piece of code rather than first.\n- **Ordering**: Implement each testable piece — each sorting algorithm, then the UI wiring — and then write and run that piece's tests before moving on to the next piece.\n- **Tooling**: pytest for unit tests; the test suite runs in CI before merge.\n- **Coverage**: roughly 80% line coverage on the sorting logic (the three algorithms), held as a floor in Build and Test and never weakened to make a step pass.\n- **Scope notes**: focus on correctness and step-count accuracy for bubble sort, selection sort, and quick sort; no BDD feature files unless a later stage introduces them."
    }
  ],
  "obligations": {
    "strategy": "standard",
    "strategy_volume": [
      "Five to eight tests per component.",
      "Unit tests plus integration tests for key boundaries.",
      "Add E2E, performance, or security tests when requirements demand them."
    ],
    "scope_floor": [
      "Meet an 80% line-coverage floor.",
      "Run the selected tests in CI before merge."
    ],
    "combination_rule": "Apply every selected-strategy obligation and every scope-floor obligation; neither replaces the other, and a targeted scope regression may add the narrowest necessary test type beyond the strategy default."
  },
  "plan_profile": {
    "methodology": "test-after",
    "runner_step": "Bootstrap the minimal test runner/configuration and record the exact unit-scoped command.",
    "runner_ready_before_first_test": true,
    "testable_layers": [
      "Data model / database behavior",
      "Repository / data access",
      "Business logic",
      "API / endpoint",
      "Frontend behavior"
    ],
    "steps": [
      "Project structure and production configuration skeleton.",
      "Bootstrap the minimal test runner/configuration and record the exact unit-scoped command.",
      "Data model / database behavior - implement.",
      "Data model / database behavior - write and run its tests after implementation.",
      "Repository / data access - implement.",
      "Repository / data access - write and run its tests after implementation.",
      "Business logic - implement.",
      "Business logic - write and run its tests after implementation.",
      "API / endpoint - implement.",
      "API / endpoint - write and run its tests after implementation.",
      "Frontend behavior - implement.",
      "Frontend behavior - write and run its tests after implementation.",
      "Environment/build configuration.",
      "Documentation and traceability."
    ]
  },
  "input_sha256": "sha256:43e2ce67a9fc94f414b7e3f4a8779aa72dec0d741bec78b6fadea13a42ddfdad",
  "contract_sha256": "sha256:e154f7554fa204574257c53f960d41fc0ea68813e93b20163f448966f784149e"
}
```
