# Infrastructure Specification — playground-ui (U2)

Consumes `nfr-design/performance-design.md`, `nfr-design/security-design.md`, `nfr-design/logical-components.md`, `inception/domain-design/components.md`, `functional-design/functional-spec.md`, and `inception/contract-design/contract-summary.md`.

## Deployment

The unit is a single Streamlit process. Hosting target per Q1 (option A): Streamlit Community Cloud, deploying directly from the GitHub repository. Deployment is continuous on merge to `main` (project.md, team.md).

| Facet | Choice | Rationale |
|---|---|---|
| Compute model | Managed platform process (Streamlit Community Cloud) — no container, no server we operate | Q1 A; logical-components.md records no infrastructure of its own; a free, zero-ops target fits a classroom demo |
| Networking topology | Public HTTPS endpoint provided by the platform; no VPC, subnet, load balancer, or ingress we configure | Platform-owned ingress; NFR3.4 rules out external APIs and any networking we design |
| Storage strategy | None — no database, bucket, or volume; the bundled word list is a module-level constant in source (SD-4) | logical-components.md: no shared resources; SD-4 forbids file I/O and persistent storage |
| Environments | Exactly one (`main` → production). No staging, no dev tier | team.md Deployment: continuous deployment, no staging tier and no manual production gate |
| IaC approach | None — the deployment is a repository connection and a selectable entry script, configured in the platform console | The only infrastructure is the platform's; there is nothing for CDK/Terraform to own |
| Resource sizing | Platform default; no sizing controls exposed or needed | NFR1 has no numeric target; a single interactive user per session |

## Infrastructure Services

This unit provisions no cloud services of its own. Everything it depends on is either in-process or supplied by the host platform or the CI runner.

| Service | Role | Configuration | Notes |
|---|---|---|---|
| Streamlit Community Cloud | Hosting runtime for `app.py` | Repo `main` branch, entry script `app.py`, `requirements.txt` for dependencies | Q1 A; Contract 2 names `app.py` and `requirements.txt` |
| GitHub Actions | CI execution (`tests` and `ui` jobs) | `ubuntu-latest` runner, Python 3.12 | See `cicd-pipeline.md`; inherited from U1's pipeline |
| Streamlit platform logs | Runtime log sink | Platform default capture of stdout/stderr | No app-level logging (U2 NFR answers: platform logs only) |

Deliberately absent: database, cache, queue, search, CDN, DNS, and load balancer. `logical-components.md` records no queues or external stores; adding any would be unused infrastructure.

## Shared Infrastructure

| Shared Resource | Owner Unit | Consumer Units | Access Boundary |
|---|---|---|---|
| GitHub repository + `main` branch | Shared (all units) | U1, U2, U3 | Each unit owns its own files; U2 owns `app.py` and `requirements.txt` (Contract 2) |
| `requirements.txt` | U2 (per Contract 2) | U3 (CI installs from it) | U2 owns the file; U3 consumes it read-only in the pipeline |
| GitHub Actions CI workflow | U1 established it; U3 owns deployment stages | U1, U2 | U2 adds UI checks to the shared workflow; U3 extends it with deployment (see `cicd-pipeline.md`) |

No runtime resources are shared: `logical-components.md` "Shared resources: None across units — no shared files, caches, connections, or counters."

## Rationale

The design deliberately provisions nothing the application does not use. The reliability NFR is best-effort with no SLO, observability is platform logs only, and there is no numeric performance target (U2 NFR answers), so multi-AZ, auto-scaling, caching, and dedicated monitoring infrastructure would all be cost without benefit. The entire infrastructure footprint is a repository connection to Streamlit Community Cloud plus CI jobs on GitHub Actions.
