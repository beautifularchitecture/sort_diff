# Deployment Strategy — uvx-migration

## Strategy
Recreate, direct to production. Streamlit Community Cloud rebuilds the app from `main` and replaces the running instance. There is no staging environment and no manual approval gate (team.md and project.md: continuous deployment on merge to `main`).

## Promotion
None. One environment: production.

## Approval
None, by affirmed team choice. The CI `checks` job must be green before the commit lands on `main`; a failing push is a failing deploy.

## Risk for this change
Low. The change touches documentation, `.gitignore`, and the devcontainer image. It does not change application code, `pyproject.toml`, or `requirements.txt`, so the runtime deploy artifact is the same.
