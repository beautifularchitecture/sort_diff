# Build Instructions — uvx-migration

## Prerequisites
- `uv` installed. Python 3.12 is provided by uv (CI and the devcontainer pin 3.12; a local machine without a `.python-version` file may use another interpreter).

## Build
This project has no compile step. The build is dependency resolution and an import check:

```
uvx --with-requirements requirements.txt pytest --collect-only -q
```

## Verification commands
- Format: `uvx black --check .`
- Lint: `uvx ruff check .`
- Tests with coverage gate: `uvx --with-requirements requirements.txt pytest`
- App start: `uv run --with-requirements requirements.txt streamlit run app.py`

## Troubleshooting
- `uv run` creates `.venv/` in the project directory; it is git-ignored.
- `uv run` writes `uv.lock`, which is not git-ignored (open item from review).
