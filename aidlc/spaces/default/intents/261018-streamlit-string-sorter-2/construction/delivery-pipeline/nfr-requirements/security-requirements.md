# Security Requirements — delivery-pipeline (U3)

## Sources

Derived from the consumed upstream artifacts `requirements` (FR7 deployment, NFR1–NFR4) and `contract-summary` (Contract 2 app-packaging-interface, the commands U3 invokes), and the confirmed answers to the pipeline's NFR questions.

## Requirements

| ID | Requirement | Source | Verification |
|---|---|---|---|
| NFR3.4.1 | The pipeline holds no long-lived deploy credential in the repository. Deployment is the hosting platform's no-secret push integration (Streamlit Community Cloud rebuilds on push to `main`), so no token, key, or password is written into workflow files or committed config, and the Actions workflow performs no deploy API call. | NFR Q3 (B), NFR3.4 | Code review of the workflow: no `secrets.*`, no deploy step, no embedded credential; `.gitignore` excludes local env files. |
| NFR3.4.2 | The Actions workflow's steps are limited to checkout, Python setup, `pip install -r requirements.txt`, Black check, Ruff check, and pytest with the coverage gate. It performs no network access to external systems beyond installing declared dependencies from PyPI, and reads no data source. | NFR3.4, NFR2.3 | Code review: the workflow step list contains no other network or data step. |
| NFR2.3.1 | The pipeline collects no personal data and requires no accounts beyond the repository owner's hosting account. | NFR3.3 | Design review; no identity inputs exist in the workflow. |
| NFR4.1.1 | CI enforces the team code-quality gates: `black --check` and `ruff check` fail the Actions run on any finding. The run gates deploy (Streamlit Community Cloud rebuilds from the pushed commit regardless), so the practical effect is a visibly failed run on `main`, not a pre-merge block. This is a recorded deviation from the team's "lint/format failure blocks merge" rule, accepted because the confirmed trigger is push-to-`main` only (NFR Q1 B). | NFR Q4 (A), NFR4.1 | Workflow review: the Black and Ruff steps run before the test gate and their non-zero exit fails the job. |
| NFR4.2.1 | CI enforces the test and coverage gate: the run fails if any test fails or the ~80% sorting-logic coverage floor is not met. Because Contract 2 fixes the consumer command as exactly `pytest`, the floor is enforced by the project-owned pytest configuration (`pyproject.toml` / `pytest.ini` carrying `--cov-fail-under=80`), which U1 owns; U3 invokes `pytest` exactly as Contract 2 states and does not alter the command. | NFR Q4 (A), NFR4.2 | Workflow review: the test step is `pytest`; the upstream pytest configuration carries the coverage options and exits non-zero below the floor. |

## Out of Scope for This Unit

- Authentication, sessions, and access control (NFR3.3): not applicable — the pipeline runs against a public demo repository and a free hosting account.
- Secret rotation and credential lifecycle: no secret is stored (NFR3.4.1), so there is nothing to rotate.
- Per-string or per-input sanitization: user input is handled by U1/U2 (SD-1..SD-6); the pipeline never processes user strings.
- Deploy-status detection inside the workflow: under the Q3 B no-secret model there is no workflow deploy step, so the workflow cannot observe a platform deploy failure. Deploy failures surface out-of-band on the platform dashboard; the Actions run covers the checks.

## Threat Considerations

- **Credential leakage through the repository**: mitigated by NFR3.4.1. No deploy credential exists in the repository; the platform's push integration carries no committable secret.
- **Supply-chain risk from dependencies**: accepted risk. Under the confirmed Q2 A decision (no lockfile, minimum-version ranges), every CI run installs the newest matching releases from PyPI; a compromised upstream release could run in CI. This is the human's explicitly confirmed choice (NFR Q2 A) and is recorded here as an accepted risk rather than mitigated. Upper bounds on the ranges would reduce it but would depart from the confirmed project-wide pin strategy.
- **Untrusted pull-request code**: not applicable in this intent — the pipeline triggers on push to `main` only (NFR Q1 B), so no contributor-supplied branch code runs under the repository's context.
- **Information disclosure**: none. The workflow logs only check output; no secrets are echoed.

## Accepted Risks

| Risk | Basis | Accepted by |
|---|---|---|
| Unpinned dependency install in CI (supply chain) | NFR Q2 (A) — no lockfile, minimum-version ranges | Human, via the confirmed Q2 answer |
| Code-quality failures do not block merge (push-to-`main` trigger) | NFR Q1 (B) — push to `main` only, no PR gate | Human, via the confirmed Q1 answer |
