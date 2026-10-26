# Deployment Strategy — Streamlit String Sorter

## Sources

- `deployment-pipeline-questions.md` — Q1 D (recreate), Q2 A (direct to production), Q3 A (no approval), Q4 A (manual rollback via git revert), Q5 A (no feature flags).
- `construction/delivery-pipeline/infrastructure-design/infrastructure-specification.md` — one environment, platform-managed deployment, no infrastructure to orchestrate.
- `construction/delivery-pipeline/infrastructure-design/cicd-pipeline.md` — push-to-`main` checks and the platform rebuild path.
- `construction/delivery-pipeline/infrastructure-design/monitoring-design.md` — the two deploy signals (Actions run result, platform build status).
- `construction/ci-pipeline/ci-config.md` and `construction/ci-pipeline/quality-gates.md` — the checks that accompany each deploy.

## Chosen Strategy: Recreate

Each push to `main` produces a new build on Streamlit Community Cloud, which replaces the running app with the rebuilt version once the platform build succeeds. This is a recreate-style release: no traffic splitting, no parallel old/new versions, and no rolling batch. The previously deployed app stays live while a build is in progress; if the build fails, it keeps serving the last good build.

The confirmed choice is Q1 D (Recreate). It is the honest description of what the platform does, not an added orchestration layer.

## Why Not the Alternatives

| Alternative | Why rejected here |
|---|---|
| Blue/Green | Would require two maintained environments and a traffic switch. The platform offers no such control, and the app is a single-user demo with no zero-downtime requirement. |
| Canary | Would require traffic splitting and metric comparison automation. There is no traffic-splitting surface and no SLO/metric baseline beyond the platform build result. |
| Rolling | Would require multiple interchangeable instances and version-compatible state. The app is one process with no shared state, and the platform replaces it as a unit. |

The cost of recreate is a brief rebuild window. For a single interactive user per session and a demo-scale app, that window is acceptable and does not justify infrastructure the project does not otherwise need.

## Environment Promotion Matrix

| Environment | Purpose | Source | Promotion gate |
|---|---|---|---|
| Production | The only deployed instance | `main` | None; the platform rebuilds on every push |

There is no staging tier and no dev tier (team.md `## Deployment`: continuous deployment, no staging, no manual production approval). Q2 A confirms "direct to production (no staging)". Environment parity is therefore not a multi-tier concern: there is one topology, and it is the production topology.

## Release Flow

1. A change is squash-merged to `main` (trunk-based development, team.md).
2. GitHub Actions runs the `CI` checks job for that push.
3. Streamlit Community Cloud observes the new `main` commit and rebuilds the app.
4. When the rebuild succeeds, the new build replaces the running app.
5. The repository owner verifies the app URL loads and sorting works (see `rollback-runbook.md`).

The checks result and the platform build result are independent signals. Neither blocks the other: a failed check produces a failed Actions run, while the platform rebuild proceeds from the same commit.

## Approval and Promotion

No production approval is required (Q3 A). This matches `team.md` continuous deployment and the project-level mandate to deploy to production automatically whenever a change merges to `main`. There is no manual promotion step to perform, and no role-specific sign-off.

## Feature Flags

None (Q5 A). Nothing is gated behind a flag: there is no incomplete feature held back from production and no experiment to run. Trunk-based work lands directly, and the rollback path is `git revert`, not a flag flip.

## Observability of the Deploy

| Signal | Source | What it tells us |
|---|---|---|
| Check result | GitHub Actions `checks` job | Whether Black, Ruff, and the test/coverage gates passed for the pushed commit |
| Build result | Streamlit Community Cloud dashboard | Whether the new build is serving or the previous build remains live |
| App loads | Manual check of the deployed URL | Whether the new build is usable |

No pipeline-emitted metrics, dashboards, alerts, or SLOs are configured; the minimal posture is inherited from `monitoring-design.md` and was not expanded during this stage.

## Rollback Posture

Manual rollback via `git revert` on `main`, letting the platform rebuild from the reverted tree (Q4 A). Trunk-based squash merges mean one revert restores the previous state. Automated rollback is explicitly not used: there is no workflow deploy step to trigger one, and there is no health-check automation to feed it. The full procedure is in `rollback-runbook.md`.

## Trade-offs Recorded

- **Recreate over zero-downtime**: a brief rebuild window is accepted because the app has no availability SLO and one interactive user per session.
- **Direct-to-production over a staging tier**: faster feedback and less infrastructure, at the cost of the checks having no blocking role; accepted by the team's continuous-deployment choice and recorded in `nfr-requirements/security-requirements.md`.
- **Manual rollback over automated rollback**: fewer moving parts and no deploy credential; the cost is that detection and the revert are human-driven.
