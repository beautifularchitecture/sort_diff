# CI/CD Pipeline — delivery-pipeline (U3)

The delivery pipeline: the GitHub Actions checks job and the continuous-deployment path to Streamlit Community Cloud. Consumes `nfr-design/security-design.md` (SD-1..SD-7), `inception/contract-design/contract-summary.md` (Contract 2, the commands U3 invokes), and `inception/domain-design/components.md` (the component topology, which confirms the pipeline owns no runtime service). Because this is a packaging-kind unit, the stage's other declared upstream artifacts — `performance-design`, `scalability-design`, `reliability-design`, `observability-design`, `logical-components`, and `functional-spec` — were not produced for this unit; no performance target, scalability, reliability, or observability design applies to a stateless checks job, and the pipeline has no functional spec of its own. Platform: GitHub Actions. Deployment target: Streamlit Community Cloud, platform-managed (SD-5).

## Pipeline Overview

- **Trigger:** push to `main` only (SD-1; nfr-requirements Q1 B). No pull-request trigger — this is the U3-confirmed model that supersedes U2's earlier PR-trigger draft (see `infrastructure-specification.md` Cross-Unit Reconciliation).
- **Jobs:** one serial `checks` job (nfr-design Q1 A; infrastructure-design Q1 option 1).
- **Deploy:** Streamlit Community Cloud rebuilds from `main` automatically on push — no deploy step in the workflow, no stored credential (SD-5; nfr-requirements Q3 B).

## Job: `checks`

One serial job. Steps run in order; the gate steps run even after an earlier failure, and the job fails at the end if any step failed (SD-3; nfr-design Q3 B):

1. Checkout (`actions/checkout@v4`)
2. Setup Python 3.12 (`actions/setup-python@v5`, `python-version: "3.12"`; nfr-design Q4 A)
3. `pip install -r requirements.txt` — the U2-owned file already declares `streamlit>=1.40`, `pytest>=8.0`, `pytest-cov>=5.0`, `black>=24.0`, `ruff>=0.4`, so this single step provisions every gate tool (SD-2, SD-7)
4. `black --check .` (`if: always()`)
5. `ruff check .` (`if: always()`)
6. `pytest` (`if: always()`) — invoked exactly as Contract 2 states; the coverage floor rides in the project pytest configuration, not in this command (SD-4)

Per SD-3, steps 4–6 carry `if: always()` so a failing Black or Ruff step does not skip pytest; the job's overall result is failure if any step failed. The workflow sets `permissions: contents: read` so the automatic `GITHUB_TOKEN` cannot write (SD-6).

## Stage → Gate Mapping

| Stage | Gate | Effect of failure |
|---|---|---|
| Install (`pip install -r requirements.txt`) | Dependencies resolve | Run fails; the gate steps that follow still run under `if: always()` and fail too (their commands are missing), so the run shows both the install error and the downstream command-not-found |
| Format (`black --check .`) | Formatting clean | Fails the run; deploy still proceeds (push-to-`main` model) |
| Lint (`ruff check .`) | Lint clean | Fails the run; deploy still proceeds |
| Test (`pytest`) | Suite green + coverage floor met | Fails the run; deploy still proceeds |

Because the trigger is push-to-`main` only (SD-1), no gate blocks the merge — the merge already happened. A failed gate's practical effect is a visibly failed run on `main`, the recorded deviation from the team's before-merge gate. Deployment is platform-managed and proceeds from the pushed commit regardless (SD-5). See `nfr-requirements/security-requirements.md` Accepted Risks.

## Deployment and Rollback

- **Strategy:** platform-managed rebuild on push to `main` (continuous deployment; team.md). There is no blue-green, canary, or rolling step for the pipeline to configure — the platform swaps the running app itself. The live app is replaced only when the rebuild succeeds; a failed build leaves the previously deployed app running, and the platform build status is the human-visible deploy signal.
- **Rollback:** revert the offending commit on `main`; the platform rebuilds from the reverted tree (Q3 A). Because `main` is trunk-based with squash merges (team.md), a single revert restores the prior state. No automated rollback step exists in the workflow.
- **Environment promotion:** none. One environment (`main` → production); no staging tier (team.md).

## Secrets Management

No secrets are required, and none are used (SD-6). The workflow references no `secrets.*` and sources no `env` value from a secret. The automatic `GITHUB_TOKEN` that Actions provides is used only read-only by `actions/checkout`, and the workflow sets `permissions: contents: read` so it cannot write (SD-6). No step reads a deploy credential. The Streamlit deployment is a platform repository connection with no committable credential (SD-5; nfr-requirements Q3 B). Because no secret is stored, there is no rotation policy to define.

## Test Paths and Coverage

- The suite lives under `tests/` (U1's tests at the root, U2's UI tests under `tests/ui/`); `pyproject.toml` sets `testpaths = ["tests"]`, so the bare `pytest` step runs everything.
- The coverage floor names `sorting_core` only (infrastructure-design Q2 option 2): `pyproject.toml` `[tool.pytest.ini_options]` `addopts` carries `--cov=sorting_core --cov-report=term-missing --cov-fail-under=80` (U1-owned, verified on disk). No separate floor is declared for `app.py`; the UI entry script is still exercised by its `tests/ui/` `AppTest` tests, but the measured floor is on `sorting_core`. U1 owns the configuration, and U3 invokes bare `pytest` per Contract 2 (SD-4).

Example workflow (illustrative, interface-level, abbreviated):

```yaml
on: { push: { branches: [main] } }
permissions: { contents: read }
jobs:
  checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install -r requirements.txt
      - { if: always(), run: black --check . }
      - { if: always(), run: ruff check . }
      - { if: always(), run: pytest }
```

## Notes

- The workflow is U3's to own end to end (Contract 2 consumer). Its confirmed answers supersede U2's earlier two-job/PR-trigger draft; the reconciliation is recorded in `infrastructure-specification.md`.
- `linter` and `type-check` sensors target TypeScript/JavaScript snippets; this unit has none, so they are inert here.
- No artifact upload and no failure-archiving step: GitHub's default retention (90 days) holds the run logs (Q5 A).
