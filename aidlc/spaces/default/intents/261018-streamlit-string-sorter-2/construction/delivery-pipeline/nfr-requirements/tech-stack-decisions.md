# Tech Stack Decisions — delivery-pipeline (U3)

## Decisions

| Area | Decision | Rationale | Source |
|---|---|---|---|
| CI platform | GitHub Actions | Contract-summary names GitHub Actions; team practice (FR7.3) | contract-summary, FR7.3 |
| Hosting | Streamlit Community Cloud | Settled for the app in U2 infrastructure-design; no-secret push deployment | U2 infrastructure-design, NFR Q3 (B) |
| Language runtime | Python 3.12 | Project-wide choice (inherited from U1/U2) | NFR Q6 (C), U1 tech-stack-decisions |
| Dependency install | `pip install -r requirements.txt` with minimum-version ranges | Confirmed in NFR Q2 (A); matches the project pin strategy | NFR Q2 (A), NFR Q6 (C) |
| Test framework | pytest (run in CI) | Team testing posture; enforces the 80% coverage floor | team.md, NFR4.2 |
| Formatter and linter | Black and Ruff (run as `--check` in CI) | Team code style; failure blocks merge | team.md Code Style, NFR4.1 |
| Deployment trigger | Automatic on push/merge to `main` (continuous deployment) | Team's affirmed practice; FR7.3 | team.md Deployment, FR7.3 |
| Deploy credential | None stored; platform push integration | Confirmed in NFR Q3 (B) | NFR Q3 (B) |
| Deployment failure handling | Fail the run, no automatic retry | Confirmed in NFR Q5 (A) | NFR Q5 (A) |
| CI trigger | Push to `main` only | Confirmed in NFR Q1 (B) | NFR Q1 (B) |

## Notes

- This unit adds no application runtime dependency. It consumes Contract 2 (`app.py` entry point, `streamlit run app.py`, `pytest`, `ruff check .`, `black --check .`) exactly as written; it does not reach into U2 source.
- The pipeline installs `requirements.txt` (which U2 updated to declare `streamlit>=1.40`), so the same dependency set is used locally, in CI, and on the hosting platform.
- Python 3.12 is the runner version, consistent with the resolution recorded in U1's tech-stack-decisions.
