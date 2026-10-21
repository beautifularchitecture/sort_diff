# CI/CD Pipeline — playground-ui (U2)

Consumes U1's baseline (`sorting-core/infrastructure-design/cicd-pipeline.md`) and extends it for the UI unit. Platform: GitHub Actions. Deployment target: Streamlit Community Cloud (Q1 A). Deployment is continuous on merge to `main` (project.md, team.md).

## Pipeline Overview

- **Trigger:** push to `main`, pull request against `main`
- **Jobs:** `tests` and `ui` (the split chosen in Q2, option B)
- **Deploy:** Streamlit Community Cloud rebuilds from `main` automatically — no deploy step in the workflow

## Job: `tests`

Inherited from U1 unchanged. Runs the full suite and the repository-wide style and safety gates:

1. Checkout (`actions/checkout@v4`) and setup Python 3.12 (`actions/setup-python@v5`)
2. `pip install -r requirements.txt`
3. `black --check .`
4. `ruff check .`
5. No-I/O guard on `sorting_core/` (U1 SD-4)
6. `pytest --cov=sorting_core --cov-report=term-missing --cov-fail-under=80`

## Job: `ui`

The separate job chosen in Q2 (option B). It catches UI wiring errors that the core-only job would miss, and holds the 80% line-coverage floor for the UI unit (NFR4.2):

1. Checkout (`actions/checkout@v4`) and setup Python 3.12 (`actions/setup-python@v5`)
2. `pip install -r requirements.txt`
3. `black --check app.py tests/`
4. `ruff check app.py tests/`
5. **Import guard:** `python -c "import app"` — imports the entry script so a syntax error, a bad import, or a broken U1/U2 wiring fails the job
6. `pytest tests/ --cov=app --cov-report=term-missing --cov-fail-under=80`

## Stage → Gate Mapping

| Stage | Gate | Blocks merge |
|---|---|---|
| Style (`black --check`, `ruff check`) | Formatting and lint clean | Yes |
| No-I/O guard (`sorting_core/`) | No I/O/network/env imports in core | Yes |
| Unit tests (core) | Suite green + 80% coverage on `sorting_core` | Yes |
| Import guard (`import app`) | Entry script imports without error | Yes |
| Unit tests (UI) | Suite green + 80% coverage on `app` | Yes |

## Deployment and Rollback

- **Strategy:** platform-managed rebuild on push to `main` (continuous deployment). There is no blue-green, canary, or rolling step to configure — the platform swaps the running app itself.
- **Rollback:** revert the offending commit on `main`; the platform rebuilds from the reverted tree. Because `main` is trunk-based with squash merges (team.md), a single revert restores the prior state.
- **Environment promotion:** none. One environment (`main` → production); no staging tier (team.md).

## Secrets Management

No secrets are required. The unit performs no I/O, no network access, and no authenticated calls (NFR3.2, SD-4), and the Streamlit deployment is public and unauthenticated (SD-5: no identity accepted, stored, or transmitted). No credentials are stored in the repository, in CI, or on the platform.

## Notes

- The `ui` job's `--cov=app` targets the entry script's file; UI tests exercise its wiring helpers. The 80% floor is the team's coverage requirement (team.md) applied to the UI unit.
- Deployment target (Streamlit Community Cloud) is set here per Q1; U3 (delivery-pipeline) owns the corresponding operation-phase deployment stages.
- Failure of either job fails the pipeline and blocks the merge; a merge to `main` then deploys automatically with no further gate.

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

  ui:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: black --check app.py tests/
      - run: ruff check app.py tests/
      - run: python -c "import app"
      - run: pytest tests/ --cov=app --cov-report=term-missing --cov-fail-under=80
```
