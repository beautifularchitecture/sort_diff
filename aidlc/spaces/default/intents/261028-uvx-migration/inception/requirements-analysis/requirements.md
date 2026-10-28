# Requirements — uvx-migration

## Intent
Remove the project's local virtual environment setup (`python3 -m venv .venv`, `source .venv/bin/activate`) and run the project's tools and app through `uv`. Source: `project-description.json` ("remove venv and convert it to only use uvx").

## Answers Applied
- Q1 A: remove the local `.venv/` directory; rewrite README and AGENTS.md to use uv/uvx only.
- Q2 A: `uvx` for tools (black, ruff, pytest); `uv run` for the app.
- Q3 A: `requirements.txt` stays the source of truth.
- Q4 B: devcontainer moves to Python 3.12 in this work.
- Gate feedback (Request Changes, 2): keep `uv run` for the app and add `.venv/` to `.gitignore` (Q1 option B).

## Functional Requirements

| ID | Requirement | Acceptance criterion (pass/fail) |
|---|---|---|
| FR-1 | The existing `.venv/` directory is deleted from the working copy. | `test ! -d .venv` exits 0 before the work is finished. |
| FR-2 | README setup and run sections no longer contain the strings `python3 -m venv`, `source .venv/bin/activate`, or `pip install -r`. | `grep -cE "python3 -m venv|source .venv/bin/activate|pip install" README.md` prints `0`. |
| FR-3 | README documents the app run command `uv run --with-requirements requirements.txt streamlit run app.py`. | The exact string appears in README; running it starts the app (Streamlit serves on port 8501). |
| FR-4 | README check section lists, in CI order, `uvx black --check .`, `uvx ruff check .`, and `uvx --with-requirements requirements.txt pytest`. | Each listed command, run in order from the repo root with `uv` installed, exits 0. |
| FR-5 | README documents the single-test command `uvx --with-requirements requirements.txt pytest tests/test_algorithms.py::test_name --no-cov`. | The command, with a real test name, exits 0. |
| FR-6 | AGENTS.md setup and command sections use the same uv commands as FR-3 to FR-5 and contain no venv instructions. | `grep -cE "venv|source .venv" AGENTS.md` prints `0`. |
| FR-7 | `.venv/` is listed in `.gitignore` as a project entry. | `grep -nx ".venv/" .gitignore` prints one matching line. |
| FR-8 | The devcontainer image uses Python 3.12. | `.devcontainer/devcontainer.json` `image` value contains `3.12`. |
| FR-9 | `.github/workflows/ci.yml` is not changed. | `git diff -- .github/workflows/ci.yml` is empty. |
| FR-10 | `pyproject.toml`, `requirements.txt`, `app.py`, and `sorting_core/` are not changed. | `git diff -- pyproject.toml requirements.txt app.py sorting_core` is empty. |

## Non-Functional Requirements
- NFR-1: Commands run on Linux with only `uv` installed; Python 3.12 is provisioned by uv.
- NFR-2: The 80% line-coverage gate on `sorting_core` (in `pyproject.toml`) remains enforced; the pytest commands in FR-4 and FR-5 must not disable it except where `--no-cov` is stated.

## Constraints
- `uv run` creates `.venv/` in the project directory. The directory is still created on disk when the app or tests are run; it is git-ignored by FR-7, not absent. Acceptance of this is the human's Q1 B / gate choice.
- `pyproject.toml` declares no runtime dependencies (Q3 A), so `uv run` alone cannot find `streamlit`; `--with-requirements` supplies them.

## Assumptions
- `uv` is installed on the developer machine. Installing it is not part of this work.
- The CI workflow keeps its existing pip-based install; this work does not change CI.

## Out of Scope
- Moving dependencies into `pyproject.toml` (Q3 option B).
- Removing venv setup from CI (Q1 option C).
- `uvx --from streamlit streamlit run app.py` (Q2 option B).
- Changing the devcontainer's pip install steps beyond the Python version (Q4 option B only).

## Open Questions
- None. Items that need verification (the exact commands in FR-3 to FR-5) are checked at Code Generation and Build and Test, not here.
