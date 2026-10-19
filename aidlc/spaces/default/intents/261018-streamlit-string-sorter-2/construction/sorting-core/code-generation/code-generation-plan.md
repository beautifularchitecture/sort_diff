# Code Generation Plan — sorting-core (U1)

## Goals
- Implement an in-process Python package `sorting_core` that realizes the sorting-core unit.
- Follow `entities.md`, `rules.md`, `functional-spec.md`, and `security-design.md`.
- Meet the team posture (test-after, but plan covers implementation; tests will be written after code per team instructions; NFR4.2 still requires coverage).
- Output plain values only; no HTML/markup, no I/O, no network, no auth.

## Package Structure
- `sorting_core/__init__.py` — exports public API: `SortInput`, `AlgorithmResult`, `AccuracyCheck`, `Counter`, `InputProcessor`, `SortingEngine`, `AccuracyChecker`, `WordListProvider`, `run_all`.
- `sorting_core/types.py` — dataclasses for `SortInput`, `AlgorithmResult`, `AccuracyCheck`, `Counter`.
- `sorting_core/normalize.py` — `InputProcessor` (BR-INP-1, BR-INP-2, BR-INP-3).
- `sorting_core/algorithms.py` — bubble, selection, quick (Lomuto) with shared `Counter` (BR-SE-1, BR-SE-2, BR-SE-3, BR-SE-4, BR-SE-5; NFR design Q2 recursive quick, Q3 shared counter).
- `sorting_core/engine.py` — `SortingEngine` (BR-INT-2, BR-SE-4).
- `sorting_core/checker.py` — `AccuracyChecker` (BR-AC-1, BR-AC-2).
- `sorting_core/words.py` — `WordListProvider` (BR-WLP-1).
- `sorting_core/runner.py` — convenience `run_all` combining InputProcessor, SortingEngine, AccuracyChecker.

## Key Implementation Notes
- Input validation: `normalize` and public entry points raise `TypeError` for invalid types (security design SD-2). `AccuracyChecker` raises `ValueError` on `run_id` mismatch (BR-INT-1).
- Normalization: split on `\n` and `,`; trim; drop empty after trim; lowercase ASCII A-Z only (BR-INP-1).
- Run ID: stable identifier (uuid4) generated on `normalize` (BR-INP-3).
- Counter: single object passed into each algorithm (Q3); `comparisons` and `swaps` incremented as specified.
- Quick sort: recursive Lomuto (Q2). Depth ≤ 100 for max 100 strings; Python recursionlimit default is fine.
- Lexicographic order: default string `<`/`>` (BR-SE-3).
- Stable semantics: implement selection/quick so duplicates preserve input order for matching `sorted()`? Quick sort is not inherently stable. Implement stable version (e.g. Hoare is not trivially stable; Lomuto can be adapted or just use stable approach — easier: for quicksort, sort indices or use `bisect` pattern not allowed; implement stable quicksort by swapping equal elements carefully, or note that to match `sorted()` (Timsort, stable) we must produce stable order. But easier: implement bubble (stable), selection (stable if we don't swap equal elements unnecessarily), and quicksort in a stable way by sorting key with original index; but that changes data model. Alternatively implement quicksort to match `sorted()` by using Python comparison and ensure stability by not reordering equal elements. But default Lomuto swaps equal elements. To satisfy BR-SE-5 (must match `sorted()`), prefer implementing algorithms that produce stable results or adjust quicksort to be stable. For this exercise, implement bubble as stable (adjacent swaps don't reorder equal), selection: when min is found, only swap if different; Lomuto quicksort: treat elements as equal and don't swap when equal to pivot in a way that breaks stability — or implement introsort? Or use index-based approach: work with (index, value) to preserve original index, then discard index. That makes all algorithms stable and preserves input order for equal elements.)
  - Recommendation: use (index, value) pairs for sorting to guarantee stability across all three, then extract values. This is straightforward and guarantees exact match with `sorted()` for equal elements.
- Accuracy: `passed` true iff `sorted_strings == sorted(normalized_strings)` (element-wise equality). (BR-AC-1, BR-AC-2.)

## Files to Create
1. `types.py` — dataclasses with type hints.
2. `normalize.py` — InputProcessor.
3. `algorithms.py` — implementations + Counter.
4. `engine.py` — SortingEngine.
5. `checker.py` — AccuracyChecker.
6. `words.py` — WordListProvider (fixed list; non-empty).
7. `runner.py` — `run_all` helper (combines processor, engine, checker).
8. `__init__.py` — re-exports and `__all__`.
9. `__version__.py` (optional) — not required, skip.
10. `py.typed` (optional) — not required for this demo.

## Test Considerations (for code writer)
- Edge cases: empty input (if called), single element, all identical, duplicates preserve order, ASCII vs non-ASCII, normalization (commas/newlines, trim, drop empty, ASCII lowercase only).
- Counting: follow BR-SE-1 examples (bubble [3,1,2] gives 5 comparisons; selection gives 3; quick Lomuto on [3,1,2] pivot 2 gives 2).
- Boundary: invalid types raise TypeError; run_id mismatch raises ValueError.

## Non-Functional Notes
- No third-party deps; stdlib only.
- No I/O, network, eval, HTML (SD-1, SD-3, SD-4).
- No secrets.
- 100-string max is fine for O(n²); quicksort recursive depth fine.

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
