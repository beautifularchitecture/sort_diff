# Environment Validation Report — Streamlit String Sorter

## Sources

- `construction/playground-ui/infrastructure-design/infrastructure-specification.md`
- `construction/delivery-pipeline/infrastructure-design/infrastructure-specification.md`
- `operation/deployment-pipeline/cd-config.md`
- `operation/environment-provisioning/environment-inventory.md`
- `operation/environment-provisioning/environment-provisioning-questions.md` — Q1 B, Q2 URL, Q3 static validation only, Q4 absent infrastructure.

## Validation Approach

Validation is **static only**, per Q3 A. I inspected the repository, the workflow, the dependency declaration, the pytest configuration, and the recorded platform design. I did not sign in to Streamlit Community Cloud and did not send a live request to the app URL. No AWS CLI, cloud account, or infrastructure stack was involved, because this project provisions no AWS resources.

## Checks

| ID | Area | Check | Method | Result | Evidence |
|---|---|---|---|---|---|
| V-01 | Source control | Deploy branch is `main` | `git branch --show-current` | PASS | Returns `main` |
| V-02 | Application | Entry script exists at repository root | File inspection | PASS | `app.py` present |
| V-03 | Dependencies | `requirements.txt` declares the Streamlit runtime and gate tooling | File inspection | PASS | `streamlit>=1.40`, `pytest>=8.0`, `pytest-cov>=5.0`, `black>=24.0`, `ruff>=0.4`, `pyyaml>=6.0` |
| V-04 | CI trigger | Workflow runs on push to `main` only | Workflow inspection | PASS | `on.push.branches: [main]`; no `pull_request` trigger |
| V-05 | CI permissions | Token is least privilege | Workflow inspection | PASS | `permissions: contents: read` |
| V-06 | CI job shape | One serial `checks` job with the recorded steps | Workflow inspection | PASS | Checkout → Python 3.12 → install → Black → Ruff → pytest |
| V-07 | CI failure visibility | All gate steps run even after an earlier failure | Workflow inspection | PASS | `if: always()` on Black, Ruff, and pytest |
| V-08 | Format gate | Black check present | Workflow inspection | PASS | `black --check .` |
| V-09 | Lint gate | Ruff check present | Workflow inspection | PASS | `ruff check .` |
| V-10 | Test/coverage gate | pytest runs and the 80% `sorting_core` floor is configured | Workflow and `pyproject.toml` inspection | PASS | `pytest` step; `addopts = "--cov=sorting_core ... --cov-fail-under=80"` |
| V-11 | Credentials | No stored deploy credential in the workflow or repository | Workflow inspection | PASS | No `secrets.*`, no secret-sourced `env`, no deploy step |
| V-12 | Environment count | Exactly one production environment, no staging/dev | Design inspection | PASS | Both infrastructure specifications and `cd-config.md` |
| V-13 | Absent cloud resources | No VPC, subnets, security groups, NACLs, database, bucket, cache, queue, CDN, DNS, load balancer, registry, or artifact store | Design inspection | PASS | Explicitly recorded as absent in both infrastructure specifications |
| V-14 | Secret infrastructure | No Secrets Manager / Parameter Store dependency | Design inspection | PASS | No secret exists to store or inject |
| V-15 | Cross-account / cross-VPC | No cross-account or cross-VPC connectivity | Design inspection | PASS (N/A) | Confirmed by Q4 A |
| V-16 | Platform connection | Streamlit Community Cloud app is connected to this repository | Human answer + console action | PENDING | Q1 B: created but not yet connected |
| V-17 | Production endpoint | Recorded URL serves the app | Live HTTP request | NOT RUN | Static-only validation chosen (Q3 A); URL recorded but not exercised |
| V-18 | Platform build | Current `main` build succeeds on the platform | Platform dashboard | PENDING | Not observable without platform access |
| V-19 | Drift detection | Platform configuration matches the recorded design | Console inspection | LIMITED | Console-managed; no automated drift signal |

## Results Summary

| Result | Count | Checks |
|---|---|---|
| PASS | 14 | V-01 through V-14 |
| N/A | 1 | V-15 |
| PENDING | 2 | V-16, V-18 |
| NOT RUN | 1 | V-17 |
| LIMITED | 1 | V-19 |
| FAIL | 0 | — |

## Findings

1. **F1 — Platform connection incomplete.** The app exists but is not yet connected to this repository (Q1 B). Until it is connected, pushes to `main` cannot trigger a platform rebuild. This is a manual console action, not something this run can perform.
2. **F2 — Endpoint liveness unverified.** A production URL was supplied, but static-only validation means it was not requested. Because Q1 says the app is not yet connected, the URL may be an assigned endpoint rather than a serving one. Confirm it after the connection and first successful build.
3. **F3 — No AWS resources to validate.** Every VPC, subnet, security-group, NACL, secret-store, and cross-account check in the stage template is not applicable and is recorded as such under Q4 A.
4. **F4 — No automated drift or health signal.** Platform settings are console-managed and CI has no deploy or smoke step. Drift and deploy health are manual observations, consistent with `cd-config.md` and `rollback-runbook.md`.
5. **F5 — No automated provisioning authority.** The orchestrator has no platform credential and no cloud account. Provisioning is limited to recording the target state and the manual connection step.

## Security Posture

- No long-lived credential exists in the repository or workflow.
- The CI token is read-only and used only by checkout.
- No secret store, no secret injection, and no cross-account trust are configured.
- No inbound network surface is configured by this project; the platform owns the public HTTPS endpoint.
- The recorded accepted risks are unchanged: unpinned dependency installation and a push-to-`main` check that cannot block a merge or deploy.

## Drift Detection

The repository state can be compared to the recorded design at any time (workflow, `requirements.txt`, `pyproject.toml`). The platform-side configuration — repository connection, branch, entry script, and build result — is visible only in the platform console and has no automated drift check. Treat a console change as drift until it is reconciled with `cd-config.md` and this inventory.

## Readiness Decision

**Not yet fully provisioned.** The static configuration is consistent and no check failed, but two actions remain before the environment is operational:

1. Connect the Streamlit Community Cloud app to this repository, select `main`, and set `app.py` as the entry script.
2. Confirm the first platform build succeeds and the recorded URL serves the app; perform the manual smoke check from `rollback-runbook.md`.

No AWS provisioning, VPC validation, secret injection, or cross-account validation applies to this project.

## Referenced Upstream

- `construction/playground-ui/infrastructure-design/infrastructure-specification.md`
- `construction/delivery-pipeline/infrastructure-design/infrastructure-specification.md`
- `operation/deployment-pipeline/cd-config.md`
- `operation/environment-provisioning/environment-inventory.md`
- `operation/environment-provisioning/environment-provisioning-questions.md`
