# Technology Stack — sort_diff

## Languages
- Python — `>=3.12` (`pyproject.toml` `requires-python`; CI `python-version: "3.12"`). The local `.venv` was created with Python 3.14.8 (`.venv/pyvenv.cfg`); the devcontainer image is 3.11, which is below the floor.

## Runtime Framework
- Streamlit — `>=1.40` (`requirements.txt`) — UI runtime and `streamlit.testing.v1.AppTest`.

## Libraries (stdlib)
- `dataclasses`, `re`, `uuid`, `random` (tests only). The `sorting_core` package uses no third-party code.

## Development and Test Tooling
| Tool | Declared | Config location | Used by |
|------|----------|-----------------|---------|
| pytest | `>=8.0` | `pyproject.toml` `[tool.pytest.ini_options]` | CI step `pytest` |
| pytest-cov | `>=5.0` | `addopts` (`--cov=sorting_core --cov-fail-under=80`) | pytest run |
| black | `>=24.0` | `pyproject.toml` `[tool.black]` (line-length 88, py312) | CI step `black --check .` |
| ruff | `>=0.4` | `pyproject.toml` `[tool.ruff]` (E, F, I, W) | CI step `ruff check .` |
| pyyaml | `>=6.0` | none | `tests/test_workflow.py` |

All versions are lower bounds. No resolved versions are recorded in the repository (no lock file).

## Build and Packaging
- pip with `requirements.txt`.
- `pyproject.toml` declares `[project]` name `sorting-core`, version `0.1.0`, `requires-python`, and no dependencies and no `[build-system]`.

## Infrastructure and Platform
- GitHub Actions, `ubuntu-latest`, actions `actions/checkout@v4` and `actions/setup-python@v5`.
- Dev container image `mcr.microsoft.com/devcontainers/python:1-3.11-bookworm`.
- No Dockerfile, no cloud IaC, no database.

## Runtime Port
- Streamlit default 8501 (`README.md`, `.devcontainer/devcontainer.json` `forwardPorts`).
