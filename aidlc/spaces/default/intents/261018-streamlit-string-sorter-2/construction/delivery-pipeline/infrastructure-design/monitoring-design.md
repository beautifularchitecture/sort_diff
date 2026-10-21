# Monitoring Design — delivery-pipeline (U3)

The pipeline configures no monitoring of its own; it relies entirely on the two signals GitHub Actions and Streamlit Community Cloud already produce. This realizes the minimal observability posture inherited from NFR Design (U3's NFR answers record no custom metrics, no dashboards, and no alerts beyond the platform signals). Per infrastructure-design Q4 option 1, no scheduled health check or pipeline-emitted metric is added.

## Metrics & KPIs

| Metric | Source | Threshold | Why it matters |
|---|---|---|---|
| CI run result (pass/fail) | GitHub Actions `checks` job | Any failed gate fails the run | The only automated correctness signal; the Black, Ruff, and pytest-with-coverage gates all ride here (NFR4.1.1, NFR4.2.1) |
| Deployment status (build success) | Streamlit Community Cloud rebuild on push to `main` | Failure surfaces in the platform dashboard | Continuous deployment (team.md) has no manual gate, so the platform build result is the visible deploy signal (SD-5) |
| App availability (loads without error) | Streamlit platform uptime | None (best-effort; no SLO) | No reliability SLO was set; no alarm is configured |

No pipeline-emitted metrics exist. There is no throughput or latency KPI: the pipeline runs once per push, and the app has one interactive user per session.

## Alerts

| Alert | Condition | Severity | Routes to |
|---|---|---|---|
| CI failure | The `checks` job fails on a push to `main` | Ad-hoc (not blocking, since the push already landed) | Repository owner via GitHub's native run status |
| Deploy build failure | Streamlit Community Cloud rebuild of `main` fails | Ad-hoc (platform dashboard) | Repository owner |

No paging, on-call rotation, or SLO-burn alarms are configured. Because the trigger is push-to-`main` (SD-1), a CI failure cannot block the merge that already landed; its effect is a visibly failed run. This is the recorded deviation from the team's before-merge gate (see `nfr-requirements/security-requirements.md` Accepted Risks).

## SLIs / SLOs

| SLI | SLO target | Measurement window |
|---|---|---|
| None defined | No SLO (best-effort) | Not applicable |

This table is intentionally empty of targets, not an omission: no reliability SLO was set for the pipeline or the app, so defining one here would contradict the record.

## Logs & Tracing

- **Log aggregation:** GitHub Actions retains run logs under GitHub's default retention (90 days; Q5 A). No artifact upload or failure-archiving step exists, so a failed run's evidence lives in the Actions history until GitHub expires it. For the app, Streamlit Community Cloud captures stdout/stderr platform-side.
- **Tracing:** None. The pipeline is a single stateless job with no services to correlate; the app is one process with no outbound calls (components.md), so distributed tracing has nothing to trace.
- **Dashboards:** None beyond GitHub Actions' run summaries and the Streamlit platform's app-management view.

## Rationale

The pipeline performs checks only (SD-2, SD-3) and owns no running service; deployment is platform-managed (SD-5). There is no resource whose health could be measured beyond the run result and the platform build status, and no SLO was set. The honest monitoring posture is therefore: the Actions run result is the correctness signal, the platform build status is the deploy signal, and nothing else is instrumented because there is nothing else to observe.
