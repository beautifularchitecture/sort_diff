# Infrastructure Specification — delivery-pipeline (U3)

Consumes `nfr-design/security-design.md` (SD-1..SD-7), `inception/domain-design/components.md`, and `inception/contract-design/contract-summary.md` (Contract 2, the commands U3 invokes). This unit provisions the delivery pipeline itself: one GitHub Actions workflow on GitHub-hosted runners, plus the platform-side continuous-deployment path.

## Deployment

The unit is a CI/CD pipeline, not a running service. Its "deployment" is the continuous-deployment path from `main` to Streamlit Community Cloud, which is platform-managed (SD-5): there is no deploy step for the pipeline to run.

| Facet | Choice | Rationale |
|---|---|---|
| Compute model | GitHub-hosted `ubuntu-latest` runners for the checks; Streamlit Community Cloud for the app itself | Q4 A (`actions/setup-python` on a hosted runner); SD-5 leaves app hosting to the platform. Nothing self-hosted |
| Networking topology | Runner egress to PyPI for `pip install`; no VPC, subnet, load balancer, or inbound surface we configure | NFR3.4.2 permits only dependency installation as network access; the platform owns the app's public HTTPS endpoint |
| Storage strategy | None — no database, bucket, cache, or artifact store; run logs live in GitHub's own retention | Q5 A (GitHub default retention, no artifact upload); the pipeline persists no state of its own |
| Environments | Exactly one (`main` → production). No staging, no dev tier; the platform rebuilds on each push to `main` | team.md Deployment (continuous deployment, no staging tier, no manual production gate); SD-1 push-to-`main` only |
| IaC approach | None — the workflow is a committed YAML file; the deployment is a platform repository connection configured in the console | There is no cloud resource for CDK/Terraform to own; the only infrastructure is GitHub's and the platform's |
| Resource sizing | Runner defaults; platform defaults | No numeric performance target; a single interactive user per session and a demo-scale test suite |
| Environments (rollback) | Revert the offending commit on `main`; the platform rebuilds from the reverted tree | Q3 A; trunk-based squash merges (team.md) mean one revert restores the prior state — no automated rollback step |

## Infrastructure Services

This unit provisions no cloud services of its own. Everything it depends on is supplied by GitHub Actions or the hosting platform.

| Service | Role | Configuration | Notes |
|---|---|---|---|
| GitHub Actions | CI execution for the checks job | `ubuntu-latest` runner, Python 3.12 via `actions/setup-python`; one serial job | SD-2, SD-3; job structure per nfr-design Q1 A with Q3 B failure propagation (see `cicd-pipeline.md`) |
| PyPI | Dependency source | `pip install -r requirements.txt` with minimum-version ranges, no lockfile | SD-7; nfr-requirements Q2 A (accepted supply-chain risk) |
| Streamlit Community Cloud | Continuous-deployment target for `app.py` | Repo `main` branch, entry script `app.py`, top-level `requirements.txt` | SD-5; no deploy step, no stored credential (nfr-requirements Q3 B) |
| GitHub Actions log store | Run-log sink | GitHub default retention (90 days) | Q5 A; no artifact upload step |

Deliberately absent: database, cache, queue, search, CDN, DNS, load balancer, container registry, artifact store, and any deployment automation service. Adding any would be unused infrastructure; the checks job is stateless and the platform owns deployment.

## Shared Infrastructure

| Shared Resource | Owner Unit | Consumer Units | Access Boundary |
|---|---|---|---|
| GitHub repository + `main` branch | Shared (all units) | U1, U2, U3 | Each unit owns its own files; U3 owns the CI workflow and the deployment path |
| `requirements.txt` | U2 (per Contract 2) | U3 (CI installs from it) | U2 owns the file; U3 consumes it read-only. It already declares `streamlit>=1.40`, `pytest`, `pytest-cov`, `black`, `ruff` — so SD-2's single install step provisions every gate tool |
| GitHub Actions CI workflow | U3 (this unit) | U1, U2 (their tests run inside it) | **U3 owns the workflow end to end.** Per Q1 option 1, U3 supersedes U2's earlier two-job/PR-trigger draft with the U3-confirmed model: push to `main` only, one serial job covering the whole repository |
| Project pytest configuration (`pyproject.toml`) | U1 | U3 (relies on the coverage options) | U1 owns it; U3 invokes bare `pytest` per Contract 2 and does not alter the command (SD-4) |

## Cross-Unit Reconciliation (recorded)

Two earlier U2 design choices are superseded by this unit's confirmed answers, and the change is recorded here rather than left to inference:

| U2 infrastructure-design choice | U3 superseding decision | Why |
|---|---|---|
| Two-job workflow (`tests` + `ui`) | nfr-design Q1 A + infrastructure-design Q1 option 1: one serial job | U3 owns the workflow end to end (Contract 2 consumer); its confirmed answers settle the job structure for the shared pipeline |
| Pull-request trigger against `main` | nfr-requirements Q1 B: push to `main` only | The human confirmed push-only; no contributor branch code runs under the repository's context (closes the untrusted-PR threat) |
| 80% coverage floor on `app.py` (UI job) | infrastructure-design Q2 option 2: `sorting_core`-only coverage | The single `pytest` run measures `sorting_core`; no separate floor is declared for the `app.py` entry script. `app.py` is still exercised by the suite (its `AppTest` tests run under `tests/ui/`), but the coverage floor names `sorting_core` only |

## Rationale

The design deliberately provisions nothing the pipeline does not use. The project has no database, cache, queue, or external integration (NFR3.4, components.md "no shared resources"), no numeric performance target, and no staging tier (team.md). The entire infrastructure footprint is a GitHub Actions checks job plus the platform's own push-to-deploy path. The one authority this unit holds is over the shared workflow file, which is why the cross-unit reconciliations above are recorded explicitly.
