# Dashboards — observability-setup

## Overview
This project has no self-hosted observability stack (no CloudWatch, Grafana, etc.). Observability is platform-native.

## Dashboards

| Dashboard | Location | Purpose |
|---|---|---|
| GitHub Actions run summaries | GitHub repo → Actions | CI correctness gates (Black, Ruff, pytest) for `tests` and `ui` jobs |
| Streamlit app management | Streamlit Community Cloud → app dashboard | Build/deploy status and app availability for the deployed app |

## Notes
- No application-level custom dashboards (no metrics to visualize)
- No SLO dashboards (best-effort posture, no SLO defined)
