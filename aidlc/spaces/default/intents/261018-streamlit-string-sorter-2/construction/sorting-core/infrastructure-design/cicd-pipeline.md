# CI/CD Pipeline — sorting-core (U1)

This unit's infrastructure consists of a single CI check in GitHub Actions. The app (U2) and this core (U1) will be tested in one job for simplicity and speed. Deployment is covered by the team's continuous deployment choice (project.md team section): auto-deploy to production on merge to `main`.

## Pipeline Overview

- **Platform:** GitHub Actions (FR7.3)
- **Trigger:** Push to `main`, pull request against `main`
- **Artifacts to check:** Code style, static checks, unit tests with coverage gate
- **Deployment:** Continuous deployment (project.md: deploy to production automatically on every merge to `main`)

## CI Job

Single job `tests` (simplest option per Q2):

1. **Checkout**: `actions/checkout@v4`
2. **Setup Python**: `actions/setup-python@v5` with Python `3.12` (tech-stack-decisions.md, Q6)
3. **Install dependencies**: `pip install -r requirements.txt` (minimum-version ranges per Q6)
4. **Format check**: `black --check .` (team code style)
5. **Lint**: `ruff check .` (team code style)
6. **No-I/O guard (SD-4, NFR3.2)**: fail the job if any module in `sorting_core/` imports an I/O, network, process, or environment module, or calls the builtin `open`. Command: `! grep -rEn "^\s*(import|from)\s+(socket|requests|urllib|http|subprocess|pathlib|shutil|os)\b|\bopen\(" sorting_core/`
7. **Unit tests + coverage**: `pytest --cov=sorting_core --cov-report=term-missing --cov-fail-under=80` covering the sorting logic (Q1, NFR4.2)
8. **Report**: Publish coverage summary in the job output

## Coverage Scope

The coverage floor applies to the `sorting_core` package (core sorting algorithms, accuracy checker, input processor, and counter types). Tests for the UI (U2) contribute to overall coverage but the gate focuses on the core logic per Q1.

## Notes

- The 80% line coverage floor is on the sorting logic (team.md, Q1). The gate is `--cov-fail-under=80`.
- No secrets are required for CI of this unit (no I/O, network, or credentials in core).
- Job runs on `ubuntu-latest`.
- If tests fail, the job fails and blocks the merge (Q1).
- Deployment target (Streamlit Cloud or otherwise) will be defined in the deployment-pipeline stage for U3, not in this unit's pipeline.
- This minimal single-job approach meets "easiest and simplest and faster" while still failing fast on core logic errors.

Example workflow (illustrative):

```yaml
name: ci
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: black --check .
      - run: ruff check .
      - run: '! grep -rEn "^\s*(import|from)\s+(socket|requests|urllib|http|subprocess|pathlib|shutil|os)\b|\bopen\(" sorting_core/'
      - run: pytest --cov=sorting_core --cov-report=term-missing --cov-fail-under=80
```