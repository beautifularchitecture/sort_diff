# Unit Test Instructions — uvx-migration (stage-level)

No new tests are written for this refactor (refactor scope; minimal strategy; existing suite stays green).

## Test framework
- pytest, configured in `pyproject.toml` (`pythonpath = ["."]`, coverage gate 80% on `sorting_core`).
- Dependencies come from `requirements.txt` (`pytest`, `pytest-cov`, `pyyaml`, `streamlit`, `black`, `ruff`).

## Commands (run from the repo root)
- Full suite (CI order): `uvx black --check .`, then `uvx ruff check .`, then `uvx --with-requirements requirements.txt pytest`.
- Single test without the coverage gate: `uvx --with-requirements requirements.txt pytest tests/test_algorithms.py::test_name --no-cov`. Replace `test_name` with a real test in `tests/test_algorithms.py`.
- App: `uv run --with-requirements requirements.txt streamlit run app.py`.

## Coverage
- 80% line coverage on `sorting_core` (enforced by `pyproject.toml`); not weakened.

## Mocking and test data
- None required; the refactor does not change code under test.
