# Deployment Execution Log — Streamlit String Sorter

## Sources

- `operation/deployment-pipeline/cd-config.md` — push-to-`main` model, no deploy step, no stored credential.
- `operation/deployment-pipeline/deployment-strategy.md` — recreate strategy, direct to production, no approval gate.
- `operation/deployment-pipeline/rollback-runbook.md` — manual `git revert` rollback.
- `operation/environment-provisioning/environment-inventory.md` — one production environment; the app was recorded as created but not yet connected.
- `operation/environment-provisioning/validation-report.md` — static validation and the outstanding connection/build items.
- `construction/build-and-test/test-results.md` — 116 passing tests, 100% `sorting_core` coverage, clean Black and Ruff.
- `operation/deployment-execution/deployment-execution-questions.md` — confirmed answers Q1–Q7 and the recorded build evidence.
- Streamlit Community Cloud build log supplied by the app owner in this session.
- GitHub Actions run `40392449969` for commit `2952504` — `CI / checks` completed successfully.

## Deployment Summary

| Property | Value |
|---|---|
| Environment | Production (the only environment) |
| Strategy | Recreate — platform rebuild replaces the running app |
| Release commit | `2952504ea943ca0b2e944f7830417a4f8c387ca5` |
| Commit subject | `Added Dev Container Folder` |
| Branch | `main` |
| Entry point | `app.py` |
| Deployed at | 2026-10-26 20:04:57 UTC (platform `🔄 Updated app!`) |
| First build | 2026-10-26 09:37:15–09:37:33 UTC |
| Platform | Streamlit Community Cloud |
| Result | **Succeeded** — app server started and the app updated |
| Visibility | Private; unauthenticated requests redirect to Streamlit login |
| Rollback | Manual `git revert` on `main`, per `rollback-runbook.md` |

## Pre-Deployment Checks

| Check | Result | Evidence |
|---|---|---|
| Test suite | 116 passed | `construction/build-and-test/test-results.md` |
| Coverage | 100% `sorting_core` (floor 80%) | same |
| Format | `black --check .` clean, 18 files unchanged | same |
| Lint | `ruff check .` clean | same |
| Database migrations | None; confirmed by Q4 A | project has no database |
| Dependent services | GitHub, PyPI, Streamlit Community Cloud available | build and CI both completed |
| CI for the release commit | `CI / checks` success at 2026-10-26 20:05:35 UTC | GitHub Actions run `40392449969` |
| Deployment window | Now, confirmed by Q5 A | `deployment-execution-questions.md` |

## Execution Timeline

| Time (UTC) | Event | Evidence |
|---|---|---|
| 2026-10-26 09:37:15 | Platform started `sort_diff`, branch `main`, module `app.py`; cloned repository | Streamlit build log |
| 2026-10-26 09:37:28 | Dependencies installed from `requirements.txt` with `uv` | Streamlit build log |
| 2026-10-26 09:37:33 | Uvicorn started on port 8501 — first build succeeded | Streamlit build log |
| 2026-10-26 20:04:52 | Remote `main` commit `2952504` (`Added Dev Container Folder`) | GitHub API |
| 2026-10-26 20:04:55 | Platform pulled code changes and processed dependencies | Streamlit build log |
| 2026-10-26 20:04:56 | GitHub Actions `CI` run `40392449969` started for `2952504` | GitHub API |
| 2026-10-26 20:04:57 | Platform reported `🔄 Updated app!` | Streamlit build log |
| 2026-10-26 20:05:35 | `CI / checks` completed successfully | GitHub Actions API |

## Deployment Actions

- The app owner connected the Streamlit Community Cloud app to repository `welldesignedsystem/sort_diff`, branch `main`, entry point `app.py` (Q2 A).
- No commit or push was made by the orchestrator. Q1 A selected the committed `main` HEAD and left the AI-DLC workflow records uncommitted.
- The platform performed the build and rebuild itself; there is no deploy job or deploy step in `.github/workflows/ci.yml` (`cd-config.md`).
- No database migration was run; none exist.
- No feature flag was changed; none exist.

## Deviations and Observations

| Observation | Impact |
|---|---|
| Deployed commit is `2952504`, not the locally known `7e95813` | The remote `main` was one commit ahead. `git diff 7e95813..2952504` shows only `.devcontainer/devcontainer.json` added (33 lines); application code is unchanged. |
| Platform runtime is Python 3.14.9; CI pins Python 3.12 | The build succeeded and the local test run used Python 3.14.8. The runtime differs from the CI interpreter, so CI is not a byte-for-byte runtime guarantee. |
| Platform warned that more than one requirements file exists (`requirements.txt`, `pyproject.toml`) | It used `requirements.txt`, as intended; no action taken. |
| Platform replaced `pyarrow 26.0.0` with `24.0.0` due to a known segfault | Automatic platform mitigation; the app started successfully. |
| App is private; unauthenticated requests return `303` to `share.streamlit.io/-/auth/app` | Public access requested in Q7 is not yet effective. This is a sharing setting, not a deployment failure. |
| The app owner, not the orchestrator, performed the console steps | Execution evidence is the supplied build log plus the GitHub API checks; the orchestrator did not sign in to Streamlit. |

## Rollback Readiness

- The runbook is `operation/deployment-pipeline/rollback-runbook.md`.
- The rollback is `git revert --no-edit <commit-sha>` followed by `git push origin main`; the platform rebuilds from the reverted tree.
- No database or persistent state needs restoring, and no feature flag needs flipping.
- Rollback is manual; there is no automated health check or automated rollback trigger.

## Evidence

Key lines from the supplied Streamlit build log:

```text
[09:37:15] 🚀 Starting up repository: 'sort_diff', branch: 'main', main module: 'app.py'
[09:37:33] Uvicorn server started on :::8501
[20:04:55] 🐙 Pulling code changes from Github...
[20:04:57] 🔄 Updated app!
```

Additional evidence:

- GitHub Actions run: https://github.com/welldesignedsystem/sort_diff/actions/runs/40392449969
- Remote `main` at deployment: `2952504ea943ca0b2e944f7830417a4f8c387ca5`
- Public HTTP check on 2026-10-26 20:11 UTC: `HTTP/2 303` with `location: https://share.streamlit.io/-/auth/app?...`

## Outcome

The deployment succeeded. The platform built commit `2952504`, the app server started, a later rebuild completed, and CI passed for the same commit. The app owner confirmed the post-deployment smoke test. The only outstanding item is public visibility: the app still requires Streamlit authentication.

## Referenced Upstream

- `operation/deployment-pipeline/cd-config.md`
- `operation/deployment-pipeline/deployment-strategy.md`
- `operation/deployment-pipeline/rollback-runbook.md`
- `operation/environment-provisioning/environment-inventory.md`
- `operation/environment-provisioning/validation-report.md`
- `construction/build-and-test/test-results.md`
- `operation/deployment-execution/deployment-execution-questions.md`
