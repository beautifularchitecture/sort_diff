# Drift Report — feedback-optimization

Check (Q3 A): compare the deployed commit with `main` HEAD and the dependency pins in `requirements.txt`.

## Deployed commit vs `main`
| Item | Value |
|---|---|
| Deployed commit | `2952504` (`Added Dev Container Folder`) |
| `origin/main` HEAD | `2952504` |
| Match | Yes: deployed code equals `origin/main` |

## Local branch vs `main`
The local branch has diverged from `origin/main`: 3 commits are local only, and 1 commit is on `origin/main` only. These local commits (the Observability Setup, Incident Response, and later stage artifacts) are not on `main`, so they are not deployed.

The uncommitted changes are `aidlc-state.md`, an audit file, and the new `feedback-optimization/` and `performance-validation/` directories.

Action for the owner: reconcile the local branch with `origin/main` before the next push to `main`. Pushing to `main` deploys automatically (team policy), so unreviewed local commits would reach production.

## Dependency pins
`requirements.txt` uses minimum-version ranges (`streamlit>=1.40`, `pytest>=8.0`, `pytest-cov>=5.0`, `black>=24.0`, `ruff>=0.4`, `pyyaml>=6.0`). These are not exact pins, so the resolved versions can change at each build. No drift was measured against a resolved lock file, because none exists in the repository.
