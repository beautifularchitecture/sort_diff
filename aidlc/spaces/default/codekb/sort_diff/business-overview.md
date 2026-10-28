# Business Overview — sort_diff

## Purpose
An educational Streamlit app for showing how different sorting algorithms order strings. It runs bubble sort, selection sort, and quick sort on the same input and reports, per algorithm, the sorted output, comparison count, swap count, and an accuracy check against Python's built-in `sorted()` (source: `README.md`, `app.py` module docstring).

## Users
- Learners and educators exploring sorting behaviour (source: `README.md` opening paragraph).

## Key Functionality
- Enter strings in a text area (newline or comma separated) and/or pick from a bundled word list of eight words (`sorting_core/words.py`).
- Press Sort to render the input echo and three result columns in the fixed order bubble, selection, quick (`app.py` `render_results`).
- Each column shows sorted strings, `Comparisons:`, `Swaps:`, and `Accuracy: pass|fail`.

## Business Rules
- Strings are normalized: split on newline and comma, trimmed, empty tokens dropped, ASCII capitals lowercased, duplicates kept by the core and de-duplicated by the UI (`sorting_core/normalize.py`, `app.py` `build_shared_list`).
- At most 100 de-duplicated strings may be sorted; above that the UI shows `Input exceeds the 100-string limit.` (`app.py` `MAX_SORT_STRINGS`, `LIMIT_MESSAGE`).
- Empty input shows `Enter or select at least one string` (`app.py` `EMPTY_INPUT_MESSAGE`).
- Every result is accuracy-checked against `sorted()` (`sorting_core/checker.py`).

## Scope Note
This repository has no commercial domain. The current intent (`uvx-migration`) concerns developer setup and tooling, not business behaviour.
