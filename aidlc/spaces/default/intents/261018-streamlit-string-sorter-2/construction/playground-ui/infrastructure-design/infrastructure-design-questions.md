# Infrastructure Design Questions — playground-ui (U2)

Settled earlier and not repeated here: Python 3.12, `streamlit>=1.40` minimum-version range, Black/Ruff/pytest, no secrets required (no external services, no I/O), best-effort reliability, no observability beyond platform logs, continuous deployment to production on merge to `main` (project.md). U1's CI job (`tests`, GitHub Actions, `ubuntu-latest`) is inherited as the baseline.

## Q1: Hosting target for the Streamlit app

The deployment target was left open at Requirements Analysis. Where should the app run?

A. Streamlit Community Cloud (free, deploys directly from the GitHub repository and `app.py`)
B. A container image on a general-purpose PaaS (for example Render, Fly.io, or Cloud Run)
C. Local only for now; no hosted deployment in this unit
X. Other (please specify)

[Answer]: A

## Q2: CI job structure for the UI

U1's CI runs one `tests` job covering the whole repository. How should U2's checks run?

A. Reuse U1's single `tests` job; U2's tests and the Streamlit import check run in that job
B. Add a separate `ui` job that installs dependencies, runs `pytest tests/`, and imports `app.py` to catch wiring errors
X. Other (please specify)

[Answer]: B

## Consolidated Summary Confirmation

- Q1: Hosting target — Streamlit Community Cloud, deploying directly from the GitHub repository and `app.py`
- Q2: CI job structure — a separate `ui` job that installs dependencies, runs `pytest tests/`, and imports `app.py` to catch wiring errors
- Inherited, unchanged: Python 3.12 and `streamlit>=1.40`; Black/Ruff/pytest; no secrets; best-effort reliability with no SLO; platform logs only; continuous deployment to production on merge to `main`; U1's `tests` job kept as the baseline
- Artifacts to generate: `infrastructure-specification.md`, `monitoring-design.md`, `cicd-pipeline.md`, `traceability.json`

- Looks correct
- Request changes

[Answer]: Looks correct
