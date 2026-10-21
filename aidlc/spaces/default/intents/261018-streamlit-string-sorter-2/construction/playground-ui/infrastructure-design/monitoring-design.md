# Monitoring Design — playground-ui (U2)

This realizes the `observability-design` strategy inherited from NFR Design. That strategy is deliberately minimal: U2's NFR answers record no per-run logging beyond platform logs, no SLO, and no distributed tracing. This unit therefore configures monitoring rather than building it.

## Metrics & KPIs

| Metric | Source | Threshold | Why it matters |
|---|---|---|---|
| CI job result (pass/fail) | GitHub Actions `tests` and `ui` jobs | Fail blocks merge | The only automated correctness signal; NFR4.2 coverage floor and Black/Ruff gates ride here |
| Deployment status (build success) | Streamlit Community Cloud rebuild on push to `main` | Failure surfaces in the platform dashboard | Continuous deployment (team.md) has no manual gate, so the platform build result is the visible deploy signal |
| App availability (loads without error) | Streamlit platform uptime | None (best-effort; no SLO) | U2 NFR answers set best-effort reliability with no SLO; no alarm is configured |

No application custom metrics are emitted. There is no throughput or latency KPI because there is no numeric performance target (NFR1) and one interactive user per session (`performance-design.md`).

## Alerts

| Alert | Condition | Severity | Routes to |
|---|---|---|---|
| CI failure | A `tests` or `ui` job fails on a push or PR | Blocking (merge gate) | Pull-request author via GitHub's native CI status |
| Deploy build failure | Streamlit Community Cloud rebuild of `main` fails | Ad-hoc (platform dashboard) | Repository maintainers |

No paging, on-call rotation, or SLO-burn alarms are configured. U2 NFR answers record best-effort reliability with no SLO, so there is no threshold to burn.

## SLIs / SLOs

| SLI | SLO target | Measurement window |
|---|---|---|
| None defined | No SLO (best-effort reliability, per U2 NFR answers) | Not applicable |

This table is intentionally empty of targets, not an omission: the human answered that reliability is best-effort with no SLO. Defining one here would contradict that record.

## Logs & Tracing

- **Log aggregation:** Streamlit Community Cloud captures the process's stdout/stderr platform-side. The app writes no structured logs of its own (U2 NFR answers).
- **Tracing:** None. The unit is one process with no outbound calls, no queues, and no services to correlate (`logical-components.md`), so distributed tracing has nothing to trace.
- **Dashboards:** None beyond the platform's built-in app management view and GitHub Actions' job summaries.

## Rationale

Under NFR3.2 and SD-4 the UI performs no I/O, no network access, and no persistent storage. There is no external call, queue, or dependency whose health could be measured, and the reliability NFR is best-effort. The honest monitoring posture is therefore: CI results gate correctness before merge, the platform build result is the deploy signal, and nothing else is instrumented because there is nothing else to observe.
