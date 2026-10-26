# CD Configuration — Streamlit String Sorter

## Sources

- `construction/ci-pipeline/ci-config.md` — the `CI` workflow (trigger, permissions, steps).
- `construction/ci-pipeline/quality-gates.md` — Black, Ruff, and pytest/coverage gates.
- `construction/delivery-pipeline/infrastructure-design/infrastructure-specification.md` — one environment, no deploy step, platform-managed hosting.
- `construction/delivery-pipeline/infrastructure-design/cicd-pipeline.md` — push-to-`main` checks job and the platform rebuild path.
- `deployment-pipeline-questions.md` — the confirmed answers this configuration implements (Q1 D, Q2 A, Q3 A, Q4 A, Q5 A).

## Deployment Model

Continuous deployment from `main` to a single production environment. There is no deploy job, no deploy step, and no stored deploy credential: GitHub hosts the repository, GitHub Actions runs the checks, and Streamlit Community Cloud rebuilds the app from the pushed `main` commit.

| Facet | Configuration |
|---|---|
| Source of truth | `main` branch of the project repository |
| Application entry point | `app.py` (top-level) |
| Runtime dependencies | `requirements.txt` (`streamlit>=1.40`, Python >= 3.12) |
| Build/run platform | Streamlit Community Cloud, platform-managed |
| CI platform | GitHub Actions, `ubuntu-latest`, Python 3.12 |
| CI workflow | `.github/workflows/ci.yml` (`CI`) |
| Deploy trigger | Every push to `main`; the platform rebuilds from that commit |
| Deploy step in CI | None — the platform owns the rebuild |
| Production approval | None (continuous deployment, confirmed Q3 A) |
| Environment count | One (`main` → production); no staging or dev tier |

## Environment Promotion Matrix

| Stage | Trigger | Gate | Result |
|---|---|---|---|
| Checks | Push to `main` | Black, Ruff, and pytest with the 80% `sorting_core` coverage floor | A visibly passing or failing Actions run |
| Build | Platform observes the pushed `main` commit | Platform build succeeds | Previously deployed app stays live if the build fails |
| Production | Platform build succeeds | None | New build serves the app |

Because the trigger is push-to-`main` only (no pull-request trigger), no gate blocks a merge — the merge has already happened. A failed check therefore produces a failed run on `main` rather than a pre-merge block; the platform rebuild proceeds independently. This is the recorded deviation from the team's before-merge gate and is accepted in `nfr-requirements/security-requirements.md`.

## CI/CD Coupling

- The workflow is defined in `.github/workflows/ci.yml` exactly as recorded in `ci-config.md`: single serial `checks` job, `permissions: contents: read`, steps checkout → `actions/setup-python@v5` (3.12) → `pip install -r requirements.txt` → `black --check .` → `ruff check .` → `pytest`, with `if: always()` on the three gate steps.
- Quality gates and their enforcement are recorded in `quality-gates.md`; the coverage floor rides in `pyproject.toml`, not in the workflow command.
- CI and CD are deliberately decoupled: the checks job is a correctness/visibility signal, and the platform is the only deployment actor.

## Secrets and Configuration

- No `secrets.*` reference and no secret-sourced `env` value exists in the workflow or the repository.
- The automatic `GITHUB_TOKEN` is bounded by `permissions: contents: read` and is used only by `actions/checkout`.
- The Streamlit deployment is a platform repository connection with no committable credential, so there is no secret to rotate.
- Application configuration is limited to `requirements.txt`; no environment-specific variables are required.

## Feature Flags

None. The confirmed answer is "No feature flags needed" (Q5 A). This app has no progressive-delivery requirement and no incomplete feature gated in production; trunk-based work lands directly on `main`.

## Rollback

Manual rollback via `git revert` on `main`, followed by the platform's automatic rebuild from the reverted tree (confirmed Q4 A). Detailed steps, triggers, and verification live in `rollback-runbook.md`.

## Deployment Verification

No automated post-deploy smoke step exists in the workflow. Verification is manual and recorded in the runbook:

1. The Actions `checks` run for the pushed commit completes.
2. Streamlit Community Cloud reports a successful rebuild for that commit.
3. The deployed app URL loads, accepts a few strings, and returns an accuracy-checked sorted result.

## Accepted Risks

| Risk | Basis |
|---|---|
| Checks cannot block a merge or a deploy | Push-to-`main` trigger (NFR Q1 B); recorded in `nfr-requirements/security-requirements.md` |
| A broken runtime change reaches production before it is noticed | Continuous deployment with no staging tier (team.md); mitigated by the manual rollback runbook |
| Unpinned dependency install in CI and on the platform | Confirmed no-lockfile, minimum-version-range policy (NFR Q2 A) |
