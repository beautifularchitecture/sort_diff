# Code Summary — playground-ui (U2)

## Sources

This unit was generated from the consumed upstream artifacts: `functional-spec` (Parts 2–6 build contract), `contract-summary` (Contract 1 sorting-core API, Contract 2 app packaging), `performance-design` (PD-1..PD-4), `security-design` (SD-1..SD-6), `infrastructure-specification`, `unit-of-work` (U2 playground-ui, ADR-004), and `requirements` (FR1–FR7, NFR1–NFR4 and their acceptance criteria).

## Files Created / Modified
Entry point (repo root):
- `app.py` — Streamlit single-page playground. Module-level `WORD_LIST: tuple[str, ...]` (bundled list from U1's `WordListProvider`, read-only), `MAX_SORT_STRINGS = 100`, exact `EMPTY_INPUT_MESSAGE = "Enter or select at least one string"`, helpers `split_typed_entries` and `build_shared_list` (de-duplication, Q2 Option C), `render_results` (input echo + `st.columns(3)`), and `main()` wiring the text area, word-list multiselect, and Sort button to `sorting_core`.

Tests (`tests/ui/`):
- `test_app.py` — 12 `AppTest`-driven UI tests (happy path, U1-matching untruncated counts, de-duplication, exact empty message with no columns, over-cap refusal with proof `normalize` never ran, bundled list non-empty/read-only, multiselect options, AST plain-text-safety scan, single-string and all-identical edges, SD-6 exception propagation, PD-2 recompute-on-rerun).

Configuration:
- `requirements.txt` — added `streamlit>=1.40` (Contract 2 obligation).

## Key Implementation Decisions
- Presentation and orchestration only (ADR-004): `app.py` performs no sorting, normalization, or verification; it delegates to U1's `InputProcessor.normalize`, `SortingEngine.run_all`, and `AccuracyChecker.check` in `[bubble, selection, quick]` order (Contract 1).
- The bundled list reuses U1's `WordListProvider().get_words()` as a `tuple`, so it is genuinely read-only (AC1.2.3) with no second divergent copy (SD-4, FR1.5).
- `build_shared_list` combines typed entries then picked words and de-duplicates preserving first-seen order, so a string typed and picked sorts once (FR1.4, AC1.1.1, AC1.1.2).
- The 100-string cap is checked on the de-duplicated list immediately before `normalize`; above it the app refuses to sort and shows a limit message (SD-3, NFR3.6).
- The empty-input guard shows exactly `Enter or select at least one string` and renders no result columns (FR6.1, AC4.1.1, AC4.1.2).
- No caching and no stored results (PD-1, PD-2): a `sort_attempted` boolean marker (not result state) lets the empty-state hint show only before the first Sort press, while every rerun recomputes fresh from the current widget values.
- Plain-text rendering only, never `unsafe_allow_html` (SD-2); counts shown as full integers (AC3.2.5).
- U1 exceptions are not caught, so `TypeError`/`ValueError`/`RecursionError` propagate (SD-6, NFR3.1).

## Test Coverage Summary
- Command: `pytest tests/ui/ --cov=app --cov-report=term-missing --cov-fail-under=80 -q`.
- Result: 12 passed, 0 failed; 100% line coverage on `app.py` (80% floor met, not lowered).
- `black --check app.py tests/ui/` and `ruff check app.py tests/ui/` clean; `PYTHONWARNINGS=error python -c "import app"` clean.

## Deviations from the Plan
- U1's public API exposes `InputProcessor`/`SortingEngine`/`AccuracyChecker`/`run_all` classes rather than module-level `normalize`/`check`; the plan's three-operation sequence is implemented through those classes (Contract 1 semantics preserved).
- Streamlit widget commands do not accept `data-testid`; automation handles are supplied through each widget's `key=` (`strings_text_area`, `word_picks`, `sort_button`).
- No other deviations from the approved plan.
