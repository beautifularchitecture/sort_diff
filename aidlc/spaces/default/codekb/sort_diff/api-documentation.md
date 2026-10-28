# API Documentation — sort_diff

This repository exposes no HTTP, GraphQL, RPC, or message API. Its interfaces are the Streamlit UI and an in-process Python package.

## 1. Streamlit UI (`app.py`)

Single page, run with `streamlit run app.py`.

| Element | Type | Key | Label / text |
|---------|------|-----|--------------|
| Text area | `st.text_area` | `strings_text_area` | "Strings to sort" |
| Word picker | `st.multiselect` | `word_picks` | "Pick from the bundled word list" (options: `WORD_LIST`) |
| Sort button | `st.button` | `sort_button` | "Sort" |

Outputs:

| Condition | Rendered |
|-----------|----------|
| Before first Sort press | Info hint (`_EMPTY_STATE_HINT`) |
| Zero strings after normalization | Warning `Enter or select at least one string` |
| More than 100 de-duplicated strings | Error `Input exceeds the 100-string limit.` |
| Otherwise | Input echo, then three columns (bubble, selection, quick) with sorted strings, `Comparisons:`, `Swaps:`, `Accuracy: pass|fail` |

Error behaviour: exceptions from `sorting_core` propagate and are not caught (no `try`/`except` in `app.py`).

## 2. Python public API (`sorting_core/__init__.py`)

All exports are listed in `__all__`. The package has no version constant beyond `WordListProvider.get_version()` (returns `"v1.0"`).

| Name | Signature (as implemented) | Notes |
|------|----------------------------|-------|
| `InputProcessor.normalize` | `(raw_entries: list[str]) -> SortInput` | `TypeError` unless a list of strings; fresh UUID4 `run_id` |
| `SortingEngine.run_all` | `(sort_input: SortInput) -> list[AlgorithmResult]` | Three results in order bubble, selection, quick; `TypeError` on wrong type |
| `AccuracyChecker.check` | `(algorithm_result, sort_input) -> AccuracyCheck` | `TypeError` on wrong types; `ValueError` on `run_id` mismatch |
| `run_all` | `(raw_entries: list[str]) -> (SortInput, list[AlgorithmResult], list[AccuracyCheck])` | Full pipeline; not used by `app.py` |
| `bubble_sort`, `selection_sort`, `quick_sort` | `(strings: list[str], counter: Counter) -> list[str]` | Do not mutate input; increment `counter` |
| `WordListProvider.get_words` | `() -> tuple[str, ...]` | Eight fixed words |
| `WordListProvider.get_version` | `() -> str` | `"v1.0"` |
| Data types | `SortInput`, `AlgorithmResult`, `AccuracyCheck` (frozen dataclasses); `Counter` (mutable dataclass with `reset()`) | See `sorting_core/types.py` |

## 3. Error Contract

| Source | Exception | Trigger |
|--------|-----------|---------|
| `normalize` | `TypeError` | Non-list input or non-string item |
| `SortingEngine.run_all` | `TypeError` | Argument not a `SortInput` |
| `AccuracyChecker.check` | `TypeError` | Argument types wrong |
| `AccuracyChecker.check` | `ValueError` | `run_id` mismatch between result and input |

## 4. Authentication and Authorization
None. The app has no users, sessions, or identity (`app.py` SD-5 comment; `sorting_core/__init__.py`).
