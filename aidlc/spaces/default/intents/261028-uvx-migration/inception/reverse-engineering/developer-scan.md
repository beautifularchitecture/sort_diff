# Developer Scan — sort_diff (intent uvx-migration)

## Developer Code Scan Results

### Scan Coverage
- **Analyzed deeply**:
  - `app.py`
  - `sorting_core/` (`__init__.py`, `types.py`, `normalize.py`, `algorithms.py`, `engine.py`, `checker.py`, `runner.py`, `words.py`)
  - `tests/` (`test_algorithms.py`, `test_checker.py`, `test_engine.py`, `test_normalize.py`, `test_runner.py`, `test_types.py`, `test_words.py`, `test_workflow.py`)
  - `tests/ui/test_app.py`
  - `requirements.txt`, `pyproject.toml`
  - `README.md` (working-tree copy, which includes an uncommitted Setup/Run/Checks section)
  - `AGENTS.md`
  - `.github/workflows/ci.yml`
  - `.devcontainer/devcontainer.json`
  - `.gitignore` (project part, below the AI-DLC marker block)
  - `opencode.json` (read for setup-relevant keys only; it is AI-DLC wiring and was not analyzed further)
- **Skimmed only**: none. Every hand-written project file was read in full.
- **Left out**:
  - `.aidlc/`, `.opencode/`, `aidlc/` (AI-DLC install and workspace; excluded by rule)
  - `.venv/` (local virtualenv, built with Python 3.14.8; this is the directory the intent removes)
  - `__pycache__/`, `.pytest_cache/`, `.ruff_cache/` (tool caches)
  - `.git/`

### Packages Found
- `sorting_core` — library package (pure stdlib, in-tree, not installed; no build-system table) — Python — bubble/selection/quick sort, normalization, accuracy check
- `app` (`app.py`) — Streamlit entry script — Python — single-page UI, presentation only
- `tests` — pytest suite (unit tests plus `streamlit.testing.v1.AppTest` UI tests) — Python

### Build System
- **Type**: pip with a plain `requirements.txt`; `pyproject.toml` holds tool config and project metadata only (no `[build-system]`, no `dependencies`)
- **Config Files**: `requirements.txt`, `pyproject.toml`, `.github/workflows/ci.yml`, `.devcontainer/devcontainer.json`
- **Build Dependencies**: `app` → `sorting_core`; `tests` → `sorting_core`, `streamlit`, `yaml` (PyYAML, used by `tests/test_workflow.py`)

### APIs Discovered
- Streamlit UI — `app.py` `main()` — 3 input widgets (text area, multiselect, Sort button), 0 HTTP endpoints
- Python public API — `sorting_core/__init__.py` — 12 exported names
- No network, HTTP, or RPC API exists in the repository

### Frameworks & Libraries
- streamlit — `>=1.40` (lower bound only) — UI runtime
- pytest — `>=8.0` — test runner
- pytest-cov — `>=5.0` — coverage plugin
- black — `>=24.0` — formatter
- ruff — `>=0.4` — linter
- pyyaml — `>=6.0` — parses the CI workflow in tests
- Python — `>=3.12` (pyproject and CI); devcontainer image is 3.11

### Test Coverage
- **Test Directories**: `tests/`, `tests/ui/`
- **Test Frameworks**: pytest, streamlit `AppTest`
- **Coverage Config**: present — `pyproject.toml` `addopts = --cov=sorting_core --cov-fail-under=80`

### Code Quality Indicators
- **Linting**: Ruff, `pyproject.toml` `[tool.ruff.lint] select = ["E","F","I","W"]`; Black, `pyproject.toml` `[tool.black]` line-length 88
- **CI/CD**: `.github/workflows/ci.yml` — one `checks` job on push to `main`: setup-python 3.12, `pip install -r requirements.txt`, `black --check .`, `ruff check .`, `pytest`
- **Documentation**: `README.md` and `AGENTS.md` both carry the venv setup commands; module docstrings are present across `sorting_core/` and `app.py`

### Technical Debt Signals
- `requirements.txt` lines 4–9: lower-bound ranges only, no lock file, runtime and dev/test tools in one list
- `.devcontainer/devcontainer.json` `image`: Python 3.11 image; CI and `pyproject.toml` require 3.12
- `.devcontainer/devcontainer.json` `updateContentCommand`: installs with `pip3 install --user` and installs `streamlit` a second time
- `.devcontainer/devcontainer.json` `postAttachCommand`: runs Streamlit with `--server.enableXsrfProtection false`
- `README.md` Setup section and `AGENTS.md` line 6: both hard-code `python3 -m venv .venv`
- `.gitignore` project part: no `.venv/` entry; the venv is ignored only by the `.gitignore` its own tool writes inside it
- `README.md` "Docker Hub credentials" section: describes secrets and Docker publishing that `ci.yml` does not implement
- `app.py` `_SPLIT_PATTERN` / `split_typed_entries`: duplicates the split rule in `sorting_core/normalize.py`; `app.py` also re-implements the `run_all` pipeline instead of calling `sorting_core.run_all`
- `sorting_core/algorithms.py` `quick_sort`: recursive, last-element pivot; worst case is O(n²) comparisons and O(n) recursion depth. The 100-string cap is enforced only in `app.py`, not in the core
- `sorting_core/types.py` `class Counter`: name shadows `collections.Counter`
- `tests/ui/test_app.py` module docstring says `--cov=app`; coverage actually measures only `sorting_core`
- `.github/workflows/ci.yml`: actions pinned by tag (`@v4`, `@v5`), not by SHA; no pip cache; installs unpinned
- Gate status not executed in this scan: Black and Ruff exist only inside `.venv`, and `pytest` was not run

## Handoff Summary
- **Intent-relevant finding**: The venv is referenced in exactly two places: `README.md` Setup (lines 17–21 of the working-tree file) and `AGENTS.md` Commands line 6. CI (`ci.yml`) installs straight onto the runner with no venv, and the devcontainer uses `pip3 --user`, so neither depends on `.venv`. `pyproject.toml` has no `[project] dependencies`, so `requirements.txt` is the only dependency declaration; a `uvx`-only setup has to carry it forward. `tests/test_workflow.py` reads `pyyaml` from the same file.
- **Risks / follow-up**:
  - `uvx` runs each tool in its own isolated environment. `pytest` needs `pytest-cov` and `streamlit` (for `AppTest`) and `pyyaml` in that same environment, so they must be injected together (for example `uvx --with pytest-cov --with streamlit --with pyyaml pytest`). The architect should choose how to express this.
  - `pytest` config `pythonpath = ["."]` lets `sorting_core` import from the repo root without installation. Keep that property, or the tests need an install step.
  - Dependencies have no lock file. A uvx-only setup that pins by tool version or by a lock file is a decision for the architect.
  - `.devcontainer` Python 3.11 versus the 3.12 requirement is a pre-existing mismatch; the migration touches the devcontainer's install command, so the image version is in scope to be aligned or deliberately left.
  - Uncommitted changes in the working tree: `README.md` (Setup section added) and `aidlc/spaces/default/intents/intents.json`. The README analysis above is of the working-tree copy.
  - The requested run commit `745cec4` is not present in this repository; HEAD is `df37765`. See the Run Record.
