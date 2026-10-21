# NFR Requirements Questions — delivery-pipeline (U3)

Inception NFRs that touch this unit: NFR1 Correctness (CI must actually verify the sort results), NFR2.3 and NFR3.4 (self-contained, no external integrations beyond Streamlit Community Cloud), NFR3.5 (free distribution), NFR4.1 Code Quality (Black + Ruff enforced), NFR4.2 (pytest ~80% coverage runs in CI).

Already answered project-wide in `construction/sorting-core/nfr-requirements/nfr-requirements-questions.md` and carried into this unit: Python 3.12 with minimum-version dependency ranges (Q6 C), best-effort reliability with no SLO (Q4 A), no per-run logging beyond the hosting platform's logs (Q5 A), no external integrations or accounts (Q3 A). Those are inherited, not re-asked. U2's infrastructure-design already settled hosting (Streamlit Community Cloud) and that the UI runs as a separate CI job. The questions below cover only what is genuinely new to the pipeline and deployment layer.

## Q1: CI trigger and gating order

When should the pipeline run, and what must pass before deploy?

A. On every push to `main` and every pull request: run install → Black check → Ruff check → pytest (with the 80% coverage floor), and deploy to Streamlit Community Cloud only after all checks pass on a `main` push (team practice: failure blocks merge)
B. On push to `main` only: run the checks and deploy in the same job, no pull-request gate
X. Other (please specify)

[Answer]:

## Q2: Dependency install step and pinned CI environment

How should CI install dependencies before running the checks?

A. `pip install -r requirements.txt` on the runner, using the project's Python 3.12 and the same minimum-version ranges U1/U2 declared (no lockfile)
B. Add a lockfile (for example `pip-compile`) and install from it for fully reproducible CI
X. Other (please specify)

[Answer]:

## Q3: Deployment credentials

How should the pipeline authenticate to Streamlit Community Cloud to deploy on merge to `main`?

A. Store the deploy credential as a GitHub Actions repository secret (never in the repository), and have the workflow read it from the environment
B. Use a no-secret mechanism (for example a hosted Git integration that auto-deploys on push, with no credential in the workflow)
X. Other (please specify)

[Answer]:

## Q4: Coverage and lint strictness in CI

How strict should the CI checks be?

A. Fail the pipeline if any test fails or the sorting-logic coverage floor (80%) is not met, or if `black --check` or `ruff check` reports any issue — mirroring the team Code Style rule that lint/format failure blocks merge
B. Report coverage and lint as warnings that do not fail the build
X. Other (please specify)

[Answer]:

## Q5: Deployment failure handling

If the tests and lint pass but the deploy step to Streamlit Community Cloud fails, what should happen?

A. Fail the pipeline run and surface the error; the previous deployment stays live, and the fix is a new commit (no automatic retry)
B. Retry the deploy step a fixed number of times before failing
X. Other (please specify)

[Answer]:

---

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]:
