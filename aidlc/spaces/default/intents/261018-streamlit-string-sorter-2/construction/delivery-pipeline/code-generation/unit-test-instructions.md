# Unit Test Instructions — delivery-pipeline (U3)

## Goal
Write the workflow structure tests after the workflow is implemented (test-after, team.md). The GitHub Actions run itself is the end-to-end test; these tests assert the committed YAML matches the design's fixed facts. Do not weaken the workflow's gates or the 80% coverage floor to make a step pass.

## Test Layout
- `tests/test_workflow.py` — parses the committed `.github/workflows/ci.yml` with PyYAML and asserts its structure. This is a packaging unit, so there is no component-under-test in the usual sense; the workflow file is the artifact.
- `pyyaml` is declared in `requirements.txt` as a test-only dependency so the parse step runs under the CI install step.

## Cases
1. YAML validity: `.github/workflows/ci.yml` parses as a top-level mapping.
2. Trigger: the workflow triggers on `push` to `main`, and has no `pull_request` trigger (SD-1, FR7.3).
3. Single serial job: exactly one job named `checks`, running on `ubuntu-latest` (nfr-design Q1 A; infrastructure-design Q1 A).
4. Install and setup: the step sequence contains `actions/setup-python` with `python-version: '3.12'` and `pip install -r requirements.txt` in order (SD-2, SD-7).
5. Gate steps: `black --check .`, `ruff check .`, and `pytest` appear in that order, and each carries `if: always()` (SD-2, SD-3; NFR4.1.1, NFR4.2.1).
6. Least privilege and no secrets: the top-level `permissions` is exactly `{contents: read}`; the file text contains no `secrets.` reference and no deploy step (SD-5, SD-6; NFR3.4.1).
7. Bare pytest command: the pytest step's `run` is exactly `pytest` with no extra arguments (SD-4, Contract 2).

## Running
Scope every run to this unit's test file only. Do not run a project-wide command for this unit.

```bash
pytest tests/test_workflow.py -q
```
