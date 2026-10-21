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

The separate job chosen in Q2 (option B). It catches UI wiring errors that the core-only job would miss, and holds an 80% line-coverage floor for the UI's testable logic (NFR4.2). It runs the UI's own test path — `tests/ui/` — not the shared `tests/` root (which belongs to U1; see the test-path note below):

1. Checkout (`actions/checkout@v4`) and setup Python 3.12 (`actions/setup-python@v5`)
2. `pip install -r requirements.txt` — after U2 adds `streamlit>=1.40` to that file (Contract 2 obligation, see `infrastructure-specification.md`), so Streamlit is installed here
3. `black --check app.py tests/ui/`
4. `ruff check app.py tests/ui/`
5. **Import guard:** `PYTHONWARNINGS=error python -c "import app"` — imports the entry script so a top-level syntax error, a bad import, or a broken U1/U2 import-time wiring fails the job. Treating warnings as errors makes the guard deterministic (Streamlit's bare-mode `ScriptRunContext` warning becomes a failure rather than a silent pass). This guard catches **import-time and top-level script errors only**; anything that fails inside a widget handler at runtime is covered by step 6 (the UI's `AppTest`-driven tests), not by this step
6. `pytest tests/ui/ --cov=app --cov-report=term-missing --cov-fail-under=80`

## Stage → Gate Mapping

| Stage | Gate | Blocks merge |
|---|---|---|
| Style (`black --check`, `ruff check`) | Formatting and lint clean | Yes |
| No-I/O guard (`sorting_core/`) | No I/O/network/env imports in core | Yes |
| Unit tests (core) | Suite green + 80% coverage on `sorting_core` | Yes |
| Import guard (`import app`) | Entry script imports without error at import time | Yes |
| Unit tests (UI) | Suite green + 80% coverage on `app` | Yes |

## Deployment and Rollback

- **Strategy:** platform-managed rebuild on push to `main` (continuous deployment). There is no blue-green, canary, or rolling step to configure — the platform swaps the running app itself. The live app is replaced only when the rebuild succeeds; a failed build leaves the previously deployed app running, and the platform build status is the human-visible deploy signal.
- **Rollback:** revert the offending commit on `main`; the platform rebuilds from the reverted tree. Because `main` is trunk-based with squash merges (team.md), a single revert restores the prior state.
- **Environment promotion:** none. One environment (`main` → production); no staging tier (team.md).

## Test Paths and the UI Coverage Harness

- U1's suite lives at the shared repository `tests/` root (`tests/test_algorithms.py`, `tests/test_checker.py`, `tests/test_engine.py`, `tests/test_normalize.py`, `tests/test_runner.py`, `tests/test_types.py`, `tests/test_words.py`; `pyproject.toml` sets `testpaths = ["tests"]`). The `tests` job runs those.
- The UI's tests live under **`tests/ui/`**, which the `ui` job runs. Keeping them out of the shared root is what prevents the `ui` job from re-running U1's suite under `--cov=app` (which would score 0 UI coverage and fail a green `main`).
- `app.py`'s widget calls execute only under a runtime, so the `ui` job exercises them with **`streamlit.testing.v1.AppTest`** (bundled with `streamlit>=1.40`). Tests import `app` through `AppTest` and drive the widgets, so `--cov=app` measures executed lines rather than near-zero. Logic that is worth covering without a runtime (shared-list build, de-duplication, the 100-string cap) may be extracted into importable wiring helpers under test as well.

## Secrets Management

No secrets are required. The unit performs no I/O, no network access, and no authenticated calls (NFR3.2, SD-4), and the Streamlit deployment is public and unauthenticated (SD-5: no identity accepted, stored, or transmitted). No credentials are stored in the repository, in CI, or on the platform.

## Notes

- The `ui` job's `--cov=app` targets the entry script's file; UI tests drive it through `AppTest` and cover its extracted wiring helpers. The 80% floor is the team's coverage requirement (team.md) applied to the UI unit; it is measurable under the `AppTest` harness named above.
- **U2 must add `streamlit>=1.40` to the top-level `requirements.txt`** (currently `pytest`/`pytest-cov`/`black`/`ruff` only) for both the platform and this job's steps 5–6 to succeed. This is U2's Contract 2 obligation.
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
      - run: black --check app.py tests/ui/
      - run: ruff check app.py tests/ui/
      - run: PYTHONWARNINGS=error python -c "import app"
      - run: pytest tests/ui/ --cov=app --cov-report=term-missing --cov-fail-under=80
```
