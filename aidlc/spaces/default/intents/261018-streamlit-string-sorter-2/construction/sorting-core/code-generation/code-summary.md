# Code Summary — sorting-core (U1)

## Files Created / Modified
Package modules (repo root `sorting_core/`):
- `types.py` — dataclasses `SortInput`, `AlgorithmResult`, `AccuracyCheck`, `Counter`.
- `normalize.py` — `InputProcessor`: split on `\n` and `,`, trim, drop empties, lowercase ASCII A–Z only, generate `uuid4` `run_id`.
- `algorithms.py` — bubble, selection, recursive Lomuto quick sort sharing one `Counter`; sorts `(value, index)` pairs for stable output matching `sorted()`.
- `engine.py` — `SortingEngine`: runs the three algorithms over one normalized input and returns exactly three `AlgorithmResult`s.
- `checker.py` — `AccuracyChecker`: exact element-wise match against `sorted()`, raises `ValueError` on `run_id` mismatch.
- `words.py` — `WordListProvider`: fixed, non-empty bundled tuple, no I/O.
- `runner.py` — `run_all` convenience combining processor, engine, and checker.
- `__init__.py` — public re-exports and `__all__`.

Tests (`tests/`): `test_types.py`, `test_normalize.py`, `test_algorithms.py`, `test_engine.py`, `test_checker.py`, `test_words.py`, `test_runner.py`.

Build configuration: `pyproject.toml` (Black + Ruff line-length 88 / py312, pytest `testpaths`, `pythonpath`), `requirements.txt` (pytest, pytest-cov, black, ruff).

## Key Implementation Decisions
- Single shared `Counter` per sort, incremented per the BR-SE-1 definition; comparison/swap counting matches the functional-spec worked examples.
- Stable ordering across all three algorithms via `(value, index)` keys, so each result equals `sorted()` exactly (BR-SE-5); bubble and selection also preserve equal-element order.
- Recursive Lomuto partitioning (NFR design Q2); depth is bounded well within Python's default recursion limit for the 100-string maximum.
- All public entry points and `normalize` validate types at the boundary and raise `TypeError` (SD-2); the package performs no I/O, network, `eval`, or process work (SD-1, SD-3, SD-4) and emits plain values only.
- `AccuracyChecker` performs independent per-algorithm checks and raises `ValueError` on a `run_id` mismatch (BR-INT-1).

## Test Coverage Summary
- Command: `pytest --cov=sorting_core --cov-report=term-missing --cov-fail-under=80`.
- Result: 97 passed, 0 failed; 100% line coverage on `sorting_core` (80% floor met).
- `black --check` and `ruff check` (E, F, I, W) are clean.

## Deviations from the Plan
- None from the approved plan. Where the `rules.md` example tables contained internally contradictory worked figures, the implementation follows the formal BR definitions and `entities.md` (the declared source of truth); the affected test docstrings record the specific discrepancy, and the plan's key notes already specified this behaviour.
