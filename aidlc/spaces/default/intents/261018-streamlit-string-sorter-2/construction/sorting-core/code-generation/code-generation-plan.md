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
