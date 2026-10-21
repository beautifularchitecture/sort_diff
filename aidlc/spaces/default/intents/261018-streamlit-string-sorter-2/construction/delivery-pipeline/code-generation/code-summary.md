# Code Summary — delivery-pipeline (U3)

## Sources

This unit was generated from the consumed upstream artifacts: `cicd-pipeline` (workflow structure, trigger, job, gate order), `infrastructure-specification` (deployment facets, services, Cross-Unit Reconciliation), `monitoring-design`, `security-design` (SD-1..SD-7), `security-requirements` (NFR3.4.1, NFR3.4.2, NFR2.3.1, NFR4.1.1, NFR4.2.1), `contract-summary` (Contract 2 app-packaging-interface, commands U3 invokes), `unit-of-work` (U3 delivery-pipeline, kind packaging, US5.2), and `requirements` (FR7.1–FR7.3, NFR1–NFR4).

## Files Created / Modified

Workflow (production artifact):
- `.github/workflows/ci.yml` — one serial `checks` job on `ubuntu-latest`: `actions/checkout@v4`, `actions/setup-python@v5` with `python-version: "3.12"`, `pip install -r requirements.txt`, then `black --check .`, `ruff check .`, and bare `pytest`, each gate step carrying `if: always()`. Trigger is `push` on `main` only (no `pull_request`). Top-level `permissions: contents: read`. No deploy step, no `secrets.*` reference.

Tests (`tests/`):
- `test_workflow.py` — 7 structure tests over the committed YAML (PyYAML): YAML mapping validity; push-to-`main`-only trigger; exactly one `checks` job on `ubuntu-latest`; setup-python 3.12 before the install step; install < Black < Ruff < pytest order with `if: always()` on the three gates; `permissions == {contents: read}` plus no `secrets.`/`deploy` in the file text; pytest step `run` exactly `pytest`.

Configuration:
- `requirements.txt` — added `pyyaml>=6.0` as a test-only dependency so `tests/test_workflow.py` can parse the workflow under the CI install step (U2-owned file, read-only otherwise; the workflow consumes it unchanged).

## Key Implementation Decisions

- Plain `pytest` in the workflow (Contract 2, SD-4): the 80% `sorting_core` coverage floor rides in `pyproject.toml` `addopts` (U1-owned) and is not restated or altered by the workflow command.
- `if: always()` on exactly the three gate steps (SD-3): a failing Black or Ruff gate does not skip Ruff or pytest, and the job still fails overall at the end.
- Push-to-`main` only (SD-1): no `pull_request` trigger, so no untrusted PR context runs under the repository's token.
- Read-only token (SD-6): top-level `permissions: contents: read`; no `secrets.*` and no secret-sourced `env` anywhere.
- No deploy step (SD-5): the workflow ends at `pytest`; Streamlit Community Cloud rebuilds from the pushed `main` commit, so the workflow carries no deploy credential.
- The tests read the committed YAML rather than duplicating its facts in Python; PyYAML parses the bare `on:` key as boolean `True` under YAML 1.1, which the test helper handles explicitly.

## Test Coverage Summary

- Command: `pytest tests/test_workflow.py -q`.
- Result: **7 passed, 0 failed.** The pytest process exits non-zero for a coverage reason only — see "Surfaced gap" below.
- `black --check .` — clean (18 files unchanged); `ruff check .` — all checks passed.

### Surfaced gap (not worked around)

The scoped run exits non-zero solely because the U1-owned project-wide pytest `addopts` (`--cov=sorting_core --cov-report=term-missing --cov-fail-under=80`) applies to every run, and this unit-scoped run imports no application code: `sorting_core` is reported at 0.00% (all 8 modules, 0/166 statements) and the floor check reports `FAIL Required test coverage of 80% not reached`.

Per the plan and the hard rule, the floor was **not** lowered, disabled, or bypassed (no config edit, no `--no-cov`, no `--cov-fail-under` override). The floor is meaningful where it is measured: the workflow's bare `pytest` in CI runs the full suite, where U1's algorithm tests exercise `sorting_core`. Build and Test should verify the floor on the full suite; this unit-scoped run cannot demonstrate it.

## Deviations from the Plan

- Local dependency provisioning used `uv pip install -r requirements.txt` because this environment's virtualenv has neither `pip` nor `ensurepip` on PATH; the plan's install command inside the workflow remains exactly `pip install -r requirements.txt` and CI itself is unaffected.
- The scoped-run coverage-floor interaction above is surfaced rather than worked around (the plan's Test Considerations direct this).
- No other deviations from the approved plan.
