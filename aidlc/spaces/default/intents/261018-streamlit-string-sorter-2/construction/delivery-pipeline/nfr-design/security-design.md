# Security Design — delivery-pipeline (U3)

Implements the requirements in `nfr-requirements/security-requirements.md` (NFR3.4.1, NFR3.4.2, NFR2.3.1, NFR4.1.1, NFR4.2.1) and the tech decisions in `nfr-requirements/tech-stack-decisions.md`. Consumes `nfr-requirements/security-requirements.md`, `nfr-requirements/tech-stack-decisions.md`, and `contract-design/contract-summary.md`.

> **Answer-namespace note.** Two stages asked Q1–Q5: the earlier **nfr-requirements** stage (settled requirements) and **this stage** (nfr-design). Citations below always name the stage, e.g. "nfr-requirements Q1 B" for the push-to-`main` trigger and "nfr-design Q1 A" for the serial-job structure, so no label resolves ambiguously.

## Design Decisions

| ID | Decision | Implements |
|---|---|---|
| SD-1 | The workflow runs on push to `main` only (no pull-request trigger), per **nfr-requirements Q1 B**. This is what keeps the unit's no-identity / no-personal-data property intact: no untrusted PR context is ever exercised. | NFR2.3.1, NFR3.4.1; nfr-requirements Q1 B |
| SD-2 | One serial job (per **nfr-design Q1 A**): checkout → `actions/setup-python` pinned to `python-version: "3.12"` (per **nfr-design Q4 A**) → `pip install -r requirements.txt` → `black --check .` → `ruff check .` → `pytest`. The single install step provisions *all* gate tooling, because the U2-owned `requirements.txt` already declares the app runtime plus the development/test tooling — `streamlit>=1.40`, `pytest>=8.0`, `pytest-cov>=5.0`, `black>=24.0`, `ruff>=0.4` (verified on disk). No U3-owned provisioning step is needed, so NFR3.4.2's closed step list is satisfied. | NFR2.3.1, NFR3.4.2, NFR4.1.1; nfr-design Q1 A, Q4 A |
| SD-3 | Every gate step runs even after an earlier one fails, and the job fails at the end if any step failed (per **nfr-design Q3 B**). **Q3 B supersedes the fail-at-first-gate clause of nfr-design Q1 A** — the job is still serial, but failure propagation is continue-then-fail-at-end, so all failing gates are visible in one run. The skeleton below uses `if: always()` on the three gate steps to implement this. | NFR4.1.1, NFR4.2.1; nfr-design Q3 B |
| SD-4 | The 80% sorting-logic coverage floor is enforced by the project's pytest configuration in `pyproject.toml` `[tool.pytest.ini_options]` `addopts` (for example `--cov=sorting_core --cov-fail-under=80`), which U1 owns (per **nfr-design Q2 A**). U3 invokes `pytest` exactly as Contract 2 states and does not alter the command. The floor depends on `pytest-cov`, which the SD-2 install step provides via the U2-owned `requirements.txt`; U3 does not change the dependency declaration. | NFR4.2.1; nfr-design Q2 A |
| SD-5 | No deploy step exists in the workflow. Deployment is Streamlit Community Cloud's no-secret push integration, which rebuilds from the pushed `main` commit (per **nfr-requirements Q3 B**). A platform deploy failure surfaces out-of-band (platform dashboard); the Actions run covers the checks only, and there is no retry (per **nfr-requirements Q5 A**). Deployment being platform-owned is a second reason no identity or personal data exists in this unit. | NFR2.3.1, NFR3.4.1; nfr-requirements Q3 B, Q5 A |
| SD-6 | No `secrets.*` reference is used for a deploy credential, and no `env` value is sourced from a secret. In line with the confirmed **nfr-design Q5 B**, the automatic `GITHUB_TOKEN` that Actions provides is allowed to remain available in the workflow context (unused by any current step) should a future change reintroduce a step that needs it; no step echoes environment contents. The workflow skeleton sets `permissions: contents: read` so that token cannot write. | NFR3.4.1; nfr-design Q5 B |
| SD-7 | The install step uses `pip install -r requirements.txt` with the project's minimum-version ranges and no lockfile (per **nfr-requirements Q2 A**). | NFR3.4.2, NFR2.3.1; nfr-requirements Q2 A |

## Boundary Behaviour

- **Failed check on `main`**: with SD-1 (push-to-`main` trigger) a failed run cannot block the merge that already landed; its effect is a visibly failed run and, because SD-5 leaves deploy to the platform's push integration, the deploy proceeds regardless. This is the recorded, human-accepted deviation from the team's before-merge gate (see `security-requirements.md` Accepted Risks).
- **Q1 A / Q3 B reconciliation (recorded, not inferred)**: SD-3 records that nfr-design Q3 B supersedes the fail-at-first-gate clause of nfr-design Q1 A. The job stays serial per Q1 A; only the failure-propagation behavior follows Q3 B.
- **Failed platform deploy**: under SD-5 no workflow step observes it; the previous deployment stays live and the fix is a new commit (nfr-requirements Q5 A, no retry).
- **Secret exposure**: SD-6 keeps every credential out of the workflow; the only token present is Actions' automatic `GITHUB_TOKEN`, whose permissions the skeleton reduces to read-only, and which no current step uses.

Illustrative workflow skeleton (interface-level, abbreviated):

```yaml
on:
  push:
    branches: [main]
permissions:
  contents: read
jobs:
  checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -r requirements.txt
      - if: always()
        run: black --check .
      - if: always()
        run: ruff check .
      - if: always()
        run: pytest
```

## Threats Considered

| Threat | Treatment |
|---|---|
| Stored credential leakage | SD-6 (no `secrets.*`, no secret-sourced `env`) |
| `GITHUB_TOKEN` abuse by a compromised dependency | SD-6 (`permissions: contents: read` bounds the token; no step uses it) |
| Untrusted pull-request code running under repo context | SD-1 (push-to-`main` only; no PR trigger) |
| Unpinned dependency install (PyPI supply chain) | Accepted risk under nfr-requirements Q2 A; recorded in `security-requirements.md` |
| Unpinned third-party action refs (mutable major tags) | Accepted risk: `actions/checkout@v4` and `actions/setup-python@v5` are pinned by major tag, not commit SHA — the same accepted supply-chain class as the unpinned PyPI install; recorded here rather than mitigated |
| Deploy failure silently passing | SD-5 (failure surfaces out-of-band on the platform dashboard; the run is checks-only) |
| Environment disclosure through logs | SD-6 (no step echoes environment contents) |

## Referenced Upstream

- `security-requirements.md` — NFR3.4.1, NFR3.4.2, NFR2.3.1, NFR4.1.1, NFR4.2.1.
- `tech-stack-decisions.md` — CI platform, runtime, coverage-gate ownership, trigger, deployment model.
- `contract-summary.md` — Contract 2 (exact commands U3 invokes).
