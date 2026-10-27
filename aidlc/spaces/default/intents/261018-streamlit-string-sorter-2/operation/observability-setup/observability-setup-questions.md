# Observability Setup Questions

## Q1: Golden signals
This project runs on Streamlit Community Cloud with GitHub Actions. The design records no custom metrics, no application logging, and no SLO. Which signals should be tracked?

A. Platform signals only — GitHub Actions run result, Streamlit build status, and the owner’s app-load/sort check (Recommended)
B. Add application-level metrics (requires code changes)
C. Add an external uptime or synthetic monitor (public access required)
X. Other (please specify)

[Answer]: A

## Q2: SLOs and SLIs
The NFR record says reliability is best-effort with no SLO, and the monitoring design intentionally defines no SLI. What should this stage record?

A. No SLO or SLI — keep the best-effort posture (Recommended)
B. Define an availability SLO (give the target and window)
C. Define a latency SLO (give the target, percentile, and window)
X. Other (please specify)

[Answer]: A

## Q3: Dashboards
There is no CloudWatch or Grafana in this project. What dashboard layout is needed?

A. Use GitHub Actions run summaries and the Streamlit app-management view only (Recommended)
B. Add an external dashboard (name the tool and hosting)
X. Other (please specify)

[Answer]: A

## Q4: Logs, retention, and aggregation
GitHub keeps Actions logs for 90 days by default; Streamlit captures the app’s stdout/stderr platform-side; the app writes no structured logs. What should the log policy be?

A. Platform defaults — GitHub 90-day retention and Streamlit platform logs, with no app-level logging (Recommended)
B. Add external log aggregation or a different retention period (name the tool and retention)
X. Other (please specify)

[Answer]: A

## Q5: Tracing and anomaly detection
The app is a single Streamlit process with no outbound calls, queues, or services to correlate. Should this stage add tracing or anomaly detection?

A. No distributed tracing and no anomaly detection — nothing to trace and no baseline metric (Recommended)
B. Add tracing or instrumentation (describe what)
C. Add anomaly detection (describe the signal and tool)
X. Other (please specify)

[Answer]: A

## Q6: Alerts and escalation
No paging, on-call rotation, or automated alerting exists today. How should failures reach a human?

A. No paging or on-call — the repository owner checks the CI run and Streamlit dashboard (Recommended)
B. Add notifications (email or Slack) — give the channel
C. Add paging or an on-call rotation — give the rotation
X. Other (please specify)

[Answer]: A

## Consolidated Summary Confirmation

- Q1 Golden signals: A — platform signals only: GitHub Actions run result, Streamlit build status, and the owner's app-load/sort check.
- Q2 SLO/SLI: A — no SLO or SLI; the best-effort posture is preserved.
- Q3 Dashboards: A — GitHub Actions run summaries and the Streamlit app-management view only.
- Q4 Logs: A — GitHub 90-day retention, Streamlit platform logs, no app-level logging.
- Q5 Tracing/anomaly: A — none; single process with no outbound calls.
- Q6 Alerts: A — no paging or on-call; the repository owner checks CI and the Streamlit dashboard.
- Upstream gap: no `reliability-design` artifact exists; the minimal surface is derived from `monitoring-design.md`, `infrastructure-specification.md`, and the no-SLO NFR record.
- Scope: no AWS, CloudWatch, or X-Ray resources; the observability surface is platform-native.

Does this all look correct before I generate the artifacts?
- Looks correct
- Request changes

[Answer]: Looks correct
