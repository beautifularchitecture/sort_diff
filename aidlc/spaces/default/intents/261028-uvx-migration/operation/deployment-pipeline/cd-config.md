# CD Configuration — uvx-migration

## Pipeline
No change (Q1 A). Deployment stays as it is today:

- Trigger: every push to `main`.
- Target: Streamlit Community Cloud, which rebuilds and redeploys the app from `main`.
- Gate: the existing CI `checks` job (`.github/workflows/ci.yml`), unchanged by this work (FR-9).
- Pre-deploy checks: black, ruff, and pytest, as CI runs them (Q3 A).

## Files changed by this work
`README.md`, `AGENTS.md`, `.gitignore`, `.devcontainer/devcontainer.json`. None of these alter the deploy path. `pyproject.toml`, `requirements.txt`, `app.py`, and `sorting_core/` are unchanged.

## Credentials
No credentials are stored in the repository. The Docker Hub secrets described in README are not used by this deploy path.
