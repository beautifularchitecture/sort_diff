# Unit Test Instructions — sorting-core (U1)

## Goal
Write unit tests after code (test-after, team.md). Target ~80% coverage on sorting logic; tests must be runnable with `pytest`.

## Test Layout
- `tests/test_normalize.py` — InputProcessor normalization, empty token dropping, ASCII lowercase only, duplicates preserved, run_id generation.
- `tests/test_algorithms.py` — comparison/swap counts for each algorithm; edge cases (empty, single, all identical); lexicographic ordering; stability.
- `tests/test_engine.py` — `run_all` returns exactly three results, same run_id, identical input.
- `tests/test_checker.py` — exact-match accuracy; independent checks; run_id mismatch raises ValueError.
- `tests/test_words.py` — WordListProvider non-empty, fixed, no I/O.
- `tests/test_runner.py` (optional) — convenience `run_all` behavior.

## Cases
1. Normalization: `["Alice", "bob", "", "Alice", "cäfe"]` → `["alice", "bob", "alice", "café"]`. Split `["HELLO,world\nnew line"]` → `["hello", "world", "new", "line"]`.
2. Counting examples from BR-SE-1: bubble on `[3,1,2]` gives 5 comparisons; selection gives 3; quick Lomuto on `[3,1,2]` (pivot 2) gives 2. Verify swaps as in BR-SE-2.
3. Empty/single/all-identical per BR-EDGE-1–BR-EDGE-3.
4. Accuracy: `sorted_strings == sorted(normalized_strings)`.
5. Boundary: non-list or non-string item raises `TypeError` (SD-2); checker raises `ValueError` on run_id mismatch.
6. Stability: duplicates preserve input order (e.g. `['apple','apple']` stays in order).

## Running
```bash
pytest --cov=sorting_core --cov-report=term-missing --cov-fail-under=80
```