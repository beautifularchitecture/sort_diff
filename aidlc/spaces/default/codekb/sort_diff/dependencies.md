# Dependencies — sort_diff

## External Dependencies (declared in `requirements.txt`)
| Package | Constraint | Group | Used in |
|---------|-----------|-------|---------|
| streamlit | `>=1.40` | runtime | `app.py`, `tests/ui/test_app.py` |
| pytest | `>=8.0` | dev/test | `tests/` |
| pytest-cov | `>=5.0` | dev/test | `pyproject.toml` addopts |
| black | `>=24.0` | dev/lint | CI, local |
| ruff | `>=0.4` | dev/lint | CI, local |
| pyyaml | `>=6.0` | test-only | `tests/test_workflow.py` |

`requirements.txt` mixes the runtime dependency and the development toolchain in one list. `pyproject.toml` has no `dependencies`, `optional-dependencies`, or `dependency-groups`.

Dependency source of truth as the repository stands: `requirements.txt` only. Nothing lists these packages in `pyproject.toml`.

## Internal Dependencies
- `app.py` → `sorting_core` (package-level import)
- `sorting_core/__init__.py` → every `sorting_core` module
- `sorting_core/engine.py` → `algorithms`, `types`
- `sorting_core/runner.py` → `checker`, `engine`, `normalize`, `types`
- `sorting_core/checker.py`, `sorting_core/normalize.py`, `sorting_core/algorithms.py` → `types`
- `tests/*` → `sorting_core`; `tests/ui/test_app.py` → `app.py` (via AppTest)
- No cycles.

## Import Resolution
- `sorting_core` is not installed. Tests import it because `pyproject.toml` sets `pythonpath = ["."]`; `app.py` resolves it when `streamlit run app.py` runs from the repo root.
- No `sys.path` manipulation exists outside that config.

## Tool Dependencies (outside Python packages)
- `python3` (>=3.12), `pip`, `git`.
- `.devcontainer` installs `pip3 install --user -r requirements.txt` and `pip3 install --user streamlit` (streamlit appears twice).

## Version Conflicts and Advisories
- No conflicts detectable from declarations alone (only lower bounds).
- Advisory check not performed in this scan (no network audit run).
- Outdated-by-major: not assessable without resolved versions.
