# Unit Test Instructions — sorting-core (U1)

## Goal
Write unit tests after each implemented piece (test-after, team.md). Hold the 80% line-coverage floor on `sorting_core` (NFR4.2); never lower it to pass.

## Test Layout
- `tests/test_normalize.py` — InputProcessor normalization (BR1.1), empty token dropping (BR1.2), run_id generation (BR1.3), boundary `TypeError` (SD-2).
- `tests/test_algorithms.py` — comparison and swap counts for each algorithm (BR2.1, BR2.2); edge cases empty, single, sorted, all-identical (BR5.1–BR5.3); lexicographic order (BR2.3).
- `tests/test_engine.py` — `run_all` returns exactly three results (BR2.4), same run_id (BR4.1), identical normalized input (BR4.2), each algorithm's count from its own counter.
- `tests/test_checker.py` — exact-match accuracy (BR3.1), independent checks (BR3.2), run_id mismatch raises `ValueError`.
- `tests/test_types.py`, `tests/test_words.py`, `tests/test_runner.py` — dataclass and helper behavior as they exist in the package.

## Cases
1. Normalization: `["Alice", "bob", "", "Alice", "cäfe"]` gives `["alice", "bob", "alice", "cäfe"]` (non-ASCII passes through). `["HELLO,world\nnew line"]` gives `["hello", "world", "new line"]` (three tokens).
2. Counting (from functional-spec.md and rules.md):
   - bubble `[3,1,2]`: comparisons 3, swaps 2; sorted n=4: comparisons 6, swaps 0.
   - selection `[3,1,2]`: comparisons 3, swaps 2; reversed n=4: comparisons 6, swaps 2.
   - quick (guarded Lomuto) `[3,1,2]`: comparisons 2, swaps 2; sorted n=3: comparisons 3, swaps 0; all-identical n=3: comparisons 3, swaps 0.
3. Empty and single-element input: 0 comparisons, 0 swaps for every algorithm.
4. Accuracy: `passed` is true iff `sorted_strings == sorted(normalized_strings)`; duplicates and non-ASCII inputs match `sorted()`.
5. Boundary: non-list input or a non-string item raises `TypeError`; checker raises `ValueError` on run_id mismatch.

## Running
Scope every run to this unit's test files only. Do not run a project-wide command for this unit.

```bash
pytest tests/test_normalize.py tests/test_algorithms.py tests/test_engine.py tests/test_checker.py tests/test_types.py tests/test_words.py tests/test_runner.py --cov=sorting_core --cov-report=term-missing --cov-fail-under=80 -q
```
