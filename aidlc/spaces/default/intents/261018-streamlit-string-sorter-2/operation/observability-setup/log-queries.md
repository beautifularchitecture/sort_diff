# Log Queries — observability-setup

## Log Sources
| Source | Retention | Notes |
|---|---|---|
| GitHub Actions logs | 90 days (default) | CI job stdout/stderr |
| Streamlit Community Cloud logs | Platform-managed (platform defaults) | App stdout/stderr from the running process |

## Saved Queries
None. No application-level structured logging is implemented; platform logs are inspected ad-hoc via the respective dashboards.

## Notes
- No log aggregation pipeline configured
- No log-based alerts
