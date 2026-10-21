# Tech Stack Decisions — delivery-pipeline (U3)

## Decisions

| Area | Decision | Rationale | Source |
|---|---|---|---|
| CI platform | GitHub Actions | Contract-summary names GitHub Actions; team practice (FR7.3) | contract-summary, FR7.3 |
| Hosting | Streamlit Community Cloud | Settled for the app in U2 infrastructure-design; no-secret push deployment | U2 infrastructure-design, NFR Q3 (B) |
| Language runtime | Python 3.12 | Project-wide choice (inherited from U1/U2) | NFR Q6 (C), U1 tech-stack-decisions |
| Dependency install | `pip install -r requirements.txt` with minimum-version ranges | Confirmed in NFR Q2 (A); matches the project pin strategy | NFR Q2 (A), NFR Q6 (C) |
| Test framework | pytest (run in CI as `pytest`, exactly per Contract 2) | Team testing posture; NFR4.2.1 coverage gate via the project pytest config | team.md, NFR4.2, contract-summary |
| Coverage gate | 80% sorting-logic floor enforced by the project-owned pytest configuration (`--cov-fail-under=80` in `pyproject.toml`/`pytest.ini`, owned by U1), not by changing Contract 2's `pytest` command | Confirmed in NFR Q4 (A); keeps Contract 2's exact-command rule intact | NFR Q4 (A), NFR4.2.1, contract-summary |
| Formatter and linter | Black and Ruff (run as `--check` in CI) | Team code style; failure fails the Actions run (blocks deploy, not merge — see deviation below) | team.md Code Style, NFR4.1.1 |
| CI trigger | Push/merge to `main` only, no pull-request gate | Confirmed in NFR Q1 (B) | NFR Q1 (B) |
| Deployment model | Automatic rebuild on push to `main` via the platform's no-secret push integration; no deploy step in the Actions workflow | Confirmed in NFR Q3 (B); team's affirmed practice (FR7.3) | NFR Q3 (B), team.md Deployment, FR7.3 |
| Deployment failure handling | The Actions run covers the checks only; a platform deploy failure surfaces out-of-band (platform dashboard), previous deployment stays live, and the fix is a new commit — no automatic retry | Confirmed in NFR Q5 (A), reconciled with the Q3 (B) no-deploy-step model | NFR Q5 (A), NFR3.4.1 |

## Accepted Deviations

- **"Lint/format failure blocks merge"**: the team Code Style rule assumes a pre-merge CI gate. The confirmed trigger is push-to-`main` only (NFR Q1 B), so checks run after the merge lands and a failure fails the Actions run rather than blocking the merge. This deviation is accepted on the basis of the confirmed Q1 answer and is recorded in security-requirements.md (NFR4.1.1, Accepted Risks).

## Notes

- This unit adds no application runtime dependency. It consumes Contract 2 (`app.py` entry point, `streamlit run app.py`, `pytest`, `ruff check .`, `black --check .`) exactly as written; it does not reach into U2 source.
- The pipeline installs `requirements.txt` (which U2 updated to declare `streamlit>=1.40`), so the same dependency set is used locally, in CI, and on the hosting platform.
- Python 3.12 is the runner version, consistent with the resolution recorded in U1's tech-stack-decisions.
- The coverage gate (NFR4.2.1) is satisfied without amending Contract 2: U3 runs `pytest` exactly as the contract states, and the floor lives in the project's own pytest configuration, which U1 owns.
