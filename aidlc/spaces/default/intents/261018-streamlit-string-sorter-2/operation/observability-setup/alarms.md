# Alarms — observability-setup

## Alarms

| Alarm | Condition | Severity | Route | Notes |
|---|---|---|---|---|
| CI failure | `tests` or `ui` job fails on push/PR to tracked branches | Blocking (merge gate) | PR author via GitHub native CI status checks | Enforced by CI workflow; blocks merge per repo policy |
| Deploy build failure | Streamlit Community Cloud rebuild of `main` fails | Ad-hoc | Repository maintainers (via Streamlit dashboard/email notifications from platform) | No manual approval gate; continuous deployment means build status is the deploy signal |

## Notes
- No paging/on-call rotation
- No SLO-burn alarms (no SLO defined)
- No application-level alarms (no custom metrics/alerts configured)
