# Build Instructions

Project: Streamlit String Sorting Visualizer (bubble, selection, quick sort).

## Prerequisites

- Python 3.12 or newer. CI pins 3.12; the local verification environment ran 3.14.8.
- No environment variables, config files, databases, or local services are required.
- Dependencies are declared in `requirements.txt`: `streamlit`, `pytest`, `pytest-cov`, `black`, `ruff`, and `pyyaml` (test-only, parses the CI workflow).

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Local note: this workspace's `.venv` has no `pip` module, so the same install was performed with `uv pip install -r requirements.txt`. The canonical command above is what CI runs.

## Build / compile

```bash
python -m compileall -q app.py sorting_core
```

Expected: exit 0, no output.

## Import check

```bash
PYTHONWARNINGS=error python -c "import app; print('import_app_ok')"
```

Expected: `import_app_ok` and exit 0. Importing `app` does not start the server; `main()` runs only under `__name__ == "__main__"`.

## Run locally

```bash
streamlit run app.py
```

Expected: Streamlit prints a Local URL and the playground loads.

Headless build verification used:

```bash
timeout 20 streamlit run app.py --server.headless true --server.port 8599
```

Expected: a `Local URL: http://localhost:8599` line. A timeout exit (124) after the URL appears is a successful boot, not a failure.

## Verification steps

Run the same gates CI runs, in order:

```bash
black --check .
ruff check .
pytest
```

Expected:

- `black --check .` → all files unchanged.
- `ruff check .` → `All checks passed!`.
- `pytest` → full suite green with the `sorting_core` coverage floor met (see `test-results.md`).

## Troubleshooting

- **`No module named pip` inside `.venv`** — use `uv pip install -r requirements.txt` (as done locally), or recreate the venv with a Python that provides `ensurepip`.
- **`ModuleNotFoundError: yaml`** — `pyyaml` is a test-only dependency; re-run the dependency install.
- **Port already in use** — add `--server.port <free port>` to the Streamlit command.
- **`streamlit: command not found`** — the dependency install step has not run in the active environment.
