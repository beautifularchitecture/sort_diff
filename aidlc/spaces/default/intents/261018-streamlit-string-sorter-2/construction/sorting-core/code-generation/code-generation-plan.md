# Code Generation Plan — sorting-core (U1)

## Summary

- Builds: the sorting-core package, aligned to the repaired functional and NFR design (bubble, selection, guarded Lomuto quick sort, per-algorithm counters).
- Touches: `sorting_core/algorithms.py`, `sorting_core/engine.py`, `sorting_core/normalize.py`, `sorting_core/__init__.py`, `tests/test_*.py`, `pyproject.toml` (test config only if missing).
- Tests: standard strategy, test-after: unit tests per component plus boundary tests for the counting rules, about 30 tests, run with `pytest tests/ -q`.

## Goals

- Implement the `sorting_core` package so it realizes the approved design: `functional-design/entities.md`, `rules.md` (BR1.1–BR5.3), `functional-spec.md`, `nfr-design/security-design.md`, `nfr-design/logical-components.md`.
- Counting follows BR2.1 (comparisons: bubble and selection exactly n(n-1)/2; quick sort counts every partition comparison) and BR2.2 (swaps: only real exchanges, positions and values both differ).
- Output equals `sorted(normalized_strings)` (BR2.5). Internal stability is not observable for strings, so no index-pair or stable-variant machinery is required.
- No HTML, no I/O, no network, no eval (SD-1, SD-3, SD-4). Standard library only (NFR3.4).

## Traceability (plan step → design rule)

| Plan step | Design IDs |
|---|---|
| 1 Bubble sort | BR2.1, BR2.2, BR2.3, BR2.5, AC2.1.2, AC3.2.1, AC3.2.2 |
| 2 Selection sort | BR2.1, BR2.2, BR2.3, BR2.5, AC3.2.1, AC3.2.2 |
| 3 Quick sort (guarded Lomuto) | BR2.1, BR2.2, BR5.2, BR5.3, AC4.2.1, AC4.2.2 |
| 4 Per-algorithm counters in engine | BR2.4, BR4.2, AC2.1.1, AC2.1.3 |
| 5 Normalization | BR1.1, BR1.2, BR1.3, AC1.1.2, AC1.1.4, AC4.2.3 |
| 6 Boundary type checks | SD-1, SD-2, BR3.1 (run_id mismatch), NFR2.1 |
| 7 Accuracy checker | BR3.1, BR3.2, AC3.2.3, AC3.2.4 |
| 8 Documentation and rule IDs | BR4.1, NFR2.2, NFR3.4 |
| 9 Tests | all of the above; NFR4.2 |
| 10 Test configuration and coverage gate | NFR4.1, NFR4.2 |
| 11 Code summary, traceability, source manifest | Step 5 artifacts |

## Implementation Steps

1. [ ] **Bubble sort (`algorithms.py`).** Remove the early-exit flag so the outer and inner loops always run; comparisons equal n(n-1)/2 for every input. Count a swap only when two adjacent positions hold different values and are out of order (BR2.2). Source: BR2.1, BR2.2.
2. [ ] **Selection sort (`algorithms.py`).** Replace the shift-based placement with one exchange per pass when the pass minimum is not already in place; comparisons equal n(n-1)/2; swaps count only real exchanges. Source: BR2.1, BR2.2.
3. [ ] **Quick sort, guarded Lomuto (`algorithms.py`).** Keep the recursive Lomuto partition with the last element as pivot (Q6). Count an inner exchange and the final pivot placement only when positions differ and values differ, so sorted and all-identical input yield 0 swaps (BR2.2, BR5.2, BR5.3). Comparisons count every partition comparison (BR2.1).
4. [ ] **Engine (`engine.py`).** `run_all` creates three fresh `Counter` objects per call, one per algorithm; each algorithm increments only its own counter (logical-components.md, Shared Counter). Source: BR2.4, BR4.2.
5. [ ] **Normalization (`normalize.py`).** Verify: split on `\n` and `,`, trim, drop empty tokens, lowercase ASCII A–Z only, duplicates kept, run_id generated once per SortInput (BR1.1–BR1.3). Adjust only if behavior differs from these rules.
6. [ ] **Boundary checks (`normalize.py`, `engine.py`, `checker.py`).** `TypeError` for wrong input types (SD-2); `ValueError` on `run_id` mismatch in the checker (BR3.1 and BR4.1). Verify against the existing code.
7. [ ] **Accuracy checker (`checker.py`).** `passed` is true only when `sorted_strings == sorted(normalized_strings)` position by position; each algorithm is checked independently (BR3.1, BR3.2).
8. [ ] **Documentation and rule IDs.** Replace legacy `BR-*` identifiers in docstrings and comments with the `BRx.y` IDs used by `rules.md`; remove any claim of a stable-variant selection sort. Source: BR4.1, NFR2.2, NFR3.4.
9. [ ] **Tests (`tests/`).** Add or update unit tests after each implemented piece (test-after, team posture):
   - bubble: `[3,1,2]` gives comparisons 3, swaps 2; sorted n=4 gives comparisons 6, swaps 0.
   - selection: `[3,1,2]` gives comparisons 3, swaps 2; reversed n=4 gives comparisons 6, swaps 2.
   - quick: `[3,1,2]` gives comparisons 2, swaps 2; sorted n=3 gives comparisons 3, swaps 0; all-identical n=3 gives comparisons 3, swaps 0.
   - single element and empty input give 0 comparisons and 0 swaps.
   - duplicates and non-ASCII input match `sorted()`.
   - engine: each algorithm's count comes from its own counter.
   - normalization and boundary cases (BR1.1–BR1.3, SD-2, BR3.1).
   - Coverage floor 80% on `sorting_core` (NFR4.2).
10. [ ] **Test configuration.** Use the existing `pyproject.toml` pytest configuration (`testpaths = ["tests"]`, `pythonpath = ["."]`). Add `pytest-cov` to the dev requirements only if it is missing; do not lower the 80% coverage floor.
11. [ ] **Step 5 artifacts.** Write `code-summary.md`, `traceability.json` (every assigned AC, NFR sub-ID, and BRx.y ID; every OK target an existing file), and `source-manifest.json` listing every application-source path created or modified.

## Test Considerations (for code writer)

- Counting examples above are taken from `functional-spec.md` and `rules.md`; do not change the expected numbers to match the code.
- Boundary: invalid types raise `TypeError`; `run_id` mismatch raises `ValueError`.
- Do not weaken the 80% coverage floor to make a step pass; surface the gap instead.

## Non-Functional Notes

- No third-party runtime deps; stdlib only.
- No I/O, network, eval, or HTML in `sorting_core/` (checked by the CI guard in infrastructure-design).
- 100-string maximum is the caller's obligation (security-design.md Caller Obligations); recursion depth stays bounded in practice.

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
