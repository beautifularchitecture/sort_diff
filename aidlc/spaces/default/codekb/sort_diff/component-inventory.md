# Component Inventory — sort_diff

Headings below are the component names used by the Scope of Analysis block in `reverse-engineering-timestamp.md`; keep them verbatim.

## Components

### app
- **Path**: `app.py`
- **Type**: Streamlit entry script (UI)
- **Responsibility**: Render widgets, build the shared list, apply empty and limit checks, call `sorting_core`, render results.
- **Depends on**: `sorting_core` (`InputProcessor`, `SortingEngine`, `AccuracyChecker`, `WordListProvider`, types), `streamlit`, `re`.

### sorting_core
- **Path**: `sorting_core/__init__.py`
- **Type**: Package facade
- **Responsibility**: Re-export the 12 public names.
- **Depends on**: all `sorting_core` modules.

### sorting_core.types
- **Path**: `sorting_core/types.py`
- **Type**: Model
- **Responsibility**: `SortInput`, `AlgorithmResult`, `AccuracyCheck` (frozen), `Counter` (mutable).
- **Depends on**: stdlib `dataclasses`.

### sorting_core.normalize
- **Path**: `sorting_core/normalize.py`
- **Type**: Service (boundary validation and normalization)
- **Responsibility**: `InputProcessor.normalize` — split, trim, drop empties, ASCII-lowercase, keep duplicates, assign `run_id`.
- **Depends on**: `types`, `re`, `uuid`.

### sorting_core.algorithms
- **Path**: `sorting_core/algorithms.py`
- **Type**: Utility (algorithms)
- **Responsibility**: `bubble_sort`, `selection_sort` (stable shift variant), `quick_sort` (recursive Lomuto); count comparisons and swaps.
- **Depends on**: `types`.

### sorting_core.engine
- **Path**: `sorting_core/engine.py`
- **Type**: Service
- **Responsibility**: `SortingEngine.run_all` — run three algorithms in order with one shared, reset `Counter`.
- **Depends on**: `algorithms`, `types`.

### sorting_core.checker
- **Path**: `sorting_core/checker.py`
- **Type**: Service (verification)
- **Responsibility**: `AccuracyChecker.check` — compare each result to `sorted()`.
- **Depends on**: `types`.

### sorting_core.runner
- **Path**: `sorting_core/runner.py`
- **Type**: Service (convenience pipeline)
- **Responsibility**: `run_all` — normalize, run, check in one call. Exported but not used by `app.py`.
- **Depends on**: `checker`, `engine`, `normalize`, `types`.

### sorting_core.words
- **Path**: `sorting_core/words.py`
- **Type**: Static data
- **Responsibility**: Fixed immutable tuple of eight words; version `v1.0`.
- **Depends on**: none.

### tests
- **Path**: `tests/` (eight modules at top level) and `tests/ui/test_app.py`
- **Type**: Test suite
- **Responsibility**: Unit tests for `sorting_core`; `AppTest` UI tests; a structure test of the CI workflow (`tests/test_workflow.py`).
- **Depends on**: `sorting_core`, `app.py` (through AppTest), `streamlit`, `pytest`, `yaml`.

### ci-workflow
- **Path**: `.github/workflows/ci.yml`
- **Type**: CI pipeline
- **Responsibility**: One `checks` job on push to `main`: setup Python 3.12, install requirements, Black, Ruff, pytest.
- **Depends on**: `requirements.txt`, `pyproject.toml`.

### devcontainer
- **Path**: `.devcontainer/devcontainer.json`
- **Type**: Development environment
- **Responsibility**: Python 3.11 image; installs requirements with `pip3 --user`; starts Streamlit on attach; forwards port 8501.
- **Depends on**: `requirements.txt`, `app.py`.

### project-configuration
- **Path**: `requirements.txt`, `pyproject.toml`, `.gitignore` (project part), `opencode.json` (AI-DLC wiring; not analyzed)
- **Type**: Configuration
- **Responsibility**: Dependency list (runtime and dev in one file); Black, Ruff, and pytest settings; ignore rules.
