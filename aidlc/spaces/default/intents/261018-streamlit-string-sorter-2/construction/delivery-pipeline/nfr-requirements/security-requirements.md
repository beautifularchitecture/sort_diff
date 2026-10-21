# Security Requirements — delivery-pipeline (U3)

## Sources

Derived from the consumed upstream artifacts `requirements` (FR7 deployment, NFR1–NFR4) and `contract-summary` (Contract 2 app-packaging-interface, the commands U3 invokes), and the confirmed answers to the pipeline's NFR questions.

## Requirements

| ID | Requirement | Source | Verification |
|---|---|---|---|
| NFR3.1 | The pipeline holds no long-lived deploy credential in the repository. Deployment uses the hosting platform's no-secret push mechanism (Streamlit Community Cloud auto-deploys on push to `main`), so no token, key, or password is written into workflow files or committed config. | NFR Q3 (B), NFR3.4 | Code review of the workflow: no `secrets.*` deploy token, no embedded credential; `.gitignore` excludes local env files. |
| NFR3.2 | The pipeline performs no network access to external systems beyond the hosting platform's own deploy integration, and reads no data source. It only installs dependencies from PyPI and runs the checks. | NFR3.4, NFR2.3 | Code review: workflow steps are limited to checkout, Python setup, `pip install -r requirements.txt`, Black, Ruff, pytest, and the platform deploy. |
| NFR3.3 | The pipeline collects no personal data and requires no accounts beyond the repository owner's hosting account. | NFR3.3 | Design review; no identity inputs exist in the workflow. |
| NFR4.1 | CI enforces the team code-quality gates: `black --check` and `ruff check` fail the pipeline on any finding, mirroring the team rule that lint/format failure blocks merge. | NFR Q4 (A), NFR4.1 | Workflow review: the Black and Ruff steps run before deploy and their non-zero exit fails the job. |

## Out of Scope for This Unit

- Authentication, sessions, and access control (NFR3.3): not applicable — the pipeline runs against a public demo repository and a free hosting account.
- Secret rotation and credential lifecycle: no secret is stored (NFR3.1), so there is nothing to rotate.
- Per-string or per-input sanitization: user input is handled by U1/U2 (SD-1..SD-6); the pipeline never processes user strings.

## Threat Considerations

- **Credential leakage through the repository**: mitigated by NFR3.1. No deploy credential exists in the repository; the platform's push integration carries no committable secret.
- **Supply-chain risk from dependencies**: low; the pipeline installs the project's declared minimum-version ranges from PyPI (NFR Q2 A). No lockfile is added, consistent with the project-wide pin strategy, so a compromised dependency is bounded by the upstream project's own release process.
- **Untrusted pull-request code**: not applicable in this intent — the pipeline triggers on push to `main` only (NFR Q1 B), so no contributor-supplied branch code runs under the repo's credentials. The repository has no stored deploy credential in any case.
- **Information disclosure**: none. The workflow logs only check output; no secrets are echoed.
