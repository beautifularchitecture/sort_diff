# String Sorting Visualizer

Python 3.12 / Streamlit app. `app.py` (UI only) → `sorting_core/` (pure-stdlib domain, re-exported from `__init__.py`). `tests/ui/test_app.py` uses `streamlit.testing.v1.AppTest`.

## Commands
- Setup: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
- Run: `streamlit run app.py`
- Full gate (CI order): `black --check .` → `ruff check .` → `pytest`
- Single test: `pytest tests/test_algorithms.py::test_name --no-cov`  
  (partial runs fail without `--no-cov` because `pyproject.toml` sets `--cov=sorting_core --cov-fail-under=80`; coverage only measures `sorting_core`)

## Critical constraints (tests enforce)
- **Algorithms**: only `bubble_sort`, `selection_sort`, `quick_sort` in `sorting_core/`. Every result must be accuracy-checked against `sorted()` with `Comparisons:`/`Swaps:`/`Accuracy:` reported.
- **UI (`app.py`)**: no `unsafe_allow_html`, no `eval`/`exec`/`compile`. Exceptions from `sorting_core` must propagate (no try/except). Results recompute fresh each rerun (no stored results). Exact strings: `"Enter or select at least one string"`, `"Input exceeds the 100-string limit."` Max 100 de-duplicated strings.
- **CI (`.github/workflows/ci.yml`)**: push to `main` only (**no PR checks**), single `checks` job, Python 3.12, gates in order with `if: always()`, `permissions: contents: read`, bare `pytest` step, **no `secrets.` or `deploy` (case-insensitive)**. Docker Hub README section is aspirational.
- **Style**: Black (88) + Ruff (`E,F,I,W`), import order enforced. Run linters before tests.

## Notes
- `opencode.json` loads AI-DLC rules from `aidlc/spaces/default/memory/**/*.md` and `.aidlc/onboarding.md`. Team/project rules live there (see `aidlc/spaces/default/memory/{org,team,project}.md`).
