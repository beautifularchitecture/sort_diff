# Deployment Pipeline Questions

Context: this project deploys to Streamlit Community Cloud on every push to `main` (project.md, affirmed). This change touches setup docs, `.gitignore`, and the devcontainer image only; CI and `pyproject.toml` are unchanged.

## Q1: Deployment model for this change
Should this change keep the existing push-to-`main` deployment unchanged?

A. Yes, no pipeline change; the existing auto-deploy continues (Recommended)
B. Add a manual gate before deploy (describe it)
X. Other (please specify)

[Answer]: A

## Q2: Rollback
What rollback should the runbook document?

A. Revert the commit on `main` and push; Streamlit redeploys (Recommended)
B. Another procedure (describe it)
X. Other (please specify)

[Answer]: X. Fix forward or revert: push a new commit on top of `main`. Never rewrite or force-push `main`.

## Q3: Pre-deploy checks
Which checks must pass before a push to `main` deploys?

A. The existing CI `checks` job only (black, ruff, pytest) (Recommended)
B. Add a deployment smoke step (describe it)
X. Other (please specify)

[Answer]: A

## Consolidated Summary Confirmation

- Q1 Deployment model: A — no pipeline change; push-to-`main` auto-deploy continues.
- Q2 Rollback: X — fix forward or revert: push a new commit on top of `main`; never rewrite or force-push `main`.
- Q3 Pre-deploy checks: A — the existing CI `checks` job only (black, ruff, pytest).

Does this all look correct before I generate the artifacts?
- Looks correct
- Request changes

[Answer]: Looks correct
