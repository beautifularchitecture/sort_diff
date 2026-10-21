# Unit Test Instructions — playground-ui (U2)

## Goal
Write UI tests after each implemented piece (test-after, team.md). Hold the 80% line-coverage floor on `app` (NFR4.2); never lower it to pass.

## Test Layout
- `tests/ui/test_app.py` — page wiring and rendering, driven through `streamlit.testing.v1.AppTest` (bundled with `streamlit>=1.40`) so widget calls execute and coverage is measurable.
- Keep any logic that cannot run without a full Streamlit runtime (for example the shared-list build and de-duplication) in importable helpers in `app.py` and test them directly.

The UI tests live under `tests/ui/`, separate from U1's suite at the shared `tests/` root, so the `ui` CI job does not re-run U1's tests under `--cov=app`.

## Cases
1. Happy path: typing `banana`, `apple`, `cherry` and pressing Sort renders three columns with the correct sorted order and `Accuracy: pass` for each.
2. De-duplication: a string typed and also picked from the bundled list sorts once (shared-list de-duplication, Q2 Option C).
3. Empty input: pressing Sort with nothing entered shows exactly `Enter or select at least one string` and renders no result columns (FR6.1).
4. Over-cap input: more than 100 de-duplicated strings shows a message stating the 100-string limit and runs no sorting (SD-3, NFR3.6).
5. Counts: each column shows `Comparisons: N` and `Swaps: N` as full integers with no truncation (AC3.2.5).
6. Words: the bundled word list is non-empty and read-only (FR1.5, AC1.2.3).
7. Safety: the source uses no `unsafe_allow_html` and no `eval`/`exec` on user input (SD-1, SD-2).

## Running
Scope every run to this unit's test files only. Do not run a project-wide command for this unit.

```bash
pytest tests/ui/ --cov=app --cov-report=term-missing --cov-fail-under=80 -q
```
