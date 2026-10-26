# Environment Inventory — Streamlit String Sorter

## Sources

- `construction/playground-ui/infrastructure-design/infrastructure-specification.md` — one production environment, Streamlit Community Cloud, no infrastructure of our own.
- `construction/delivery-pipeline/infrastructure-design/infrastructure-specification.md` — GitHub Actions checks, platform-owned deployment, no cloud services.
- `operation/deployment-pipeline/cd-config.md` — push-to-`main` deployment model, no deploy step, no stored credential.
- `operation/environment-provisioning/environment-provisioning-questions.md` — confirmed answers (Q1 B, Q2 URL, Q3 static, Q4 absent infrastructure).

## Environment Summary

| Property | Value |
|---|---|
| Environment count | One: production |
| Hosting platform | Streamlit Community Cloud (platform-managed) |
| Source repository | GitHub repository, `main` branch |
| Recorded production URL | https://sortdiff-nnthjumkztx7gfdla6vmlz.streamlit.app/ |
| Platform connection state | Created but not yet connected to this repository (Q1 B) |
| CI platform | GitHub Actions (`CI`, `.github/workflows/ci.yml`) |
| CI trigger | Push to `main` only |
| AWS account / region | None — this project provisions no AWS resources |
| Staging / dev environments | None (confirmed by both infrastructure specifications and `cd-config.md`) |

## Resource Inventory

| ID | Resource | Provider | Configuration | State | Notes |
|---|---|---|---|---|---|
| ENV-1 | Production app runtime | Streamlit Community Cloud | Repository `main`, entry script `app.py`, top-level `requirements.txt` | Created, not yet connected (Q1 B) | Platform owns the process and public HTTPS endpoint |
| ENV-2 | Application endpoint | Streamlit Community Cloud | `https://sortdiff-nnthjumkztx7gfdla6vmlz.streamlit.app/` | URL recorded; liveness not verified | Static-only validation was chosen (Q3 A) |
| ENV-3 | Source repository and `main` branch | GitHub | Current branch is `main` | Present | Shared by all units; each unit owns its files |
| ENV-4 | CI checks job | GitHub Actions | `ubuntu-latest`, Python 3.12, single serial `checks` job | Present and statically verified | Push to `main`; `permissions: contents: read` |
| ENV-5 | Dependency source | PyPI | `pip install -r requirements.txt`, minimum-version ranges, no lockfile | Available | `requirements.txt` declares `streamlit>=1.40` plus test/format/lint tooling |
| ENV-6 | CI run-log store | GitHub Actions | GitHub default retention (90 days) | Platform-managed | No artifact upload step |
| ENV-7 | Runtime log sink | Streamlit Community Cloud | Platform default capture of stdout/stderr | Platform-managed | No application-level logging |

## Provisioning State

- No provisioning action was executed in this stage. The project has no AWS account, no cloud resource for an IaC tool to own, and no platform credential available to the orchestrator.
- ENV-1 is recorded as **created but not yet connected** to this repository. Connecting it is a manual action in the Streamlit Community Cloud console; it is not performed by this run.
- ENV-2 is recorded as supplied by the human. Its liveness was not tested because Q3 selected static validation only.
- ENV-3, ENV-4, ENV-5, and ENV-6 are platform-provided and already present; they need no provisioning.
- ENV-7 is provisioned implicitly by the hosting platform.

## Secrets and Parameter Store Audit

- No secret store is configured and none is required.
- The repository and workflow contain no `secrets.*` reference and no secret-sourced environment variable.
- The only token present in CI is the automatic `GITHUB_TOKEN`, bounded by `permissions: contents: read` and used only by `actions/checkout`.
- There is no deployment credential to store, inject, rotate, or audit; the platform connection carries no committable secret.

## Stack Deployment Logs

Not applicable. There is no infrastructure stack (no CDK, CloudFormation, Terraform, or Pulumi), so no stack deployment was run and no stack log exists. The deployment path is the platform's own rebuild on push to `main`.

## Health Checks

- No health-check endpoint exists; the app is a single Streamlit process with no separate health route.
- No post-deploy smoke step exists in CI.
- The operational verification is the manual check in `rollback-runbook.md`: the app URL loads, accepts strings, and returns an accuracy-checked sorted result.
- The only automated signal is the Actions `checks` run; the platform build status is visible on the platform dashboard.

## Confirmed Absent Infrastructure

Confirmed by Q4 A; these are recorded as not applicable rather than assumed:

- VPC, subnets, route tables, NAT gateways, internet gateways
- Security groups and network ACLs
- Load balancer, ingress controller, or DNS record that we configure
- Database, object store, cache, queue, search index, or volume
- Container registry or artifact store
- Secrets Manager or SSM Parameter Store entries
- Cross-account or cross-VPC connectivity, peering, or transit gateway
- IAM roles or policies beyond the automatic GitHub Actions token

## Ownership and Access

| Concern | Owner | Access boundary |
|---|---|---|
| GitHub repository, `main`, and Actions | Repository owner | Repository permissions; CI token is read-only |
| Streamlit Community Cloud app | Platform account owner | Console-managed repository connection; no credential in the repo |
| `requirements.txt` | U2 (playground-ui) | U3 installs from it read-only in CI |
| CI workflow | U3 (delivery-pipeline) | Runs on push to `main` |

## Cost and Lifecycle

- Cost posture: no separately billed infrastructure that this project manages; GitHub-hosted runners and the platform account's plan/tier apply.
- Creation: connect the repository and select `app.py` in the Streamlit Community Cloud console.
- Refresh: every push to `main` triggers a platform rebuild; a failed build leaves the previous build live.
- Teardown: disconnect or delete the platform app; the repository and workflow remain until deleted separately.

## Open Items

1. **ENV-1 connection** — The app is created but not connected to this repository. Connecting it and confirming the first successful build are outstanding manual actions.
2. **ENV-2 liveness** — The URL is recorded but was not exercised, because static-only validation was chosen. Its relationship to the unconnected app must be confirmed manually.
3. **Platform drift** — The repository connection and build settings are console-managed, so drift is not observable from the repository; confirm them manually after any platform change.

## Referenced Upstream

- `construction/playground-ui/infrastructure-design/infrastructure-specification.md`
- `construction/delivery-pipeline/infrastructure-design/infrastructure-specification.md`
- `operation/deployment-pipeline/cd-config.md`
- `operation/environment-provisioning/environment-provisioning-questions.md`
