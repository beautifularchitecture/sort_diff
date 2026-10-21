# NFR Design Questions — delivery-pipeline (U3)

Settled earlier and not repeated here: Python 3.12 with minimum-version dependency ranges, push-to-`main`-only CI trigger (Q1 B), `pip install -r requirements.txt` with no lockfile (Q2 A), no stored deploy credential (Q3 B), fail the run on test/coverage/lint (Q4 A), no deploy retry (Q5 A), 80% coverage gate via the project pytest configuration.

## Q1: CI job structure

How should the Actions workflow be laid out?

A. One job on `main` that runs checkout → Python setup → install → Black check → Ruff check → pytest, failing at the first failing gate (simple; serial; the whole point is the pass/fail signal on `main`)
B. Separate parallel jobs for format, lint, and test so all three report at once even if one fails
X. Other (please specify)

[Answer]:

## Q2: Where the coverage gate is configured

The 80% floor is enforced through the project's pytest configuration, not by changing Contract 2's `pytest` command. Where should that configuration live?

A. In `pyproject.toml` under `[tool.pytest.ini_options]` `addopts` (single source alongside the existing Black/Ruff config; U1 owns it and U3 relies on it)
B. In a dedicated `pytest.ini` at the repo root
X. Other (please specify)

[Answer]:

## Q3: How failures surface

When a gate fails, what should the workflow do?

A. Stop at the first failing step and let the failed step's log be the error surface; no artifact upload, no notification step (keeps the workflow minimal; GitHub's own run status is the signal)
B. Continue running later steps so all failures are visible in one run, then fail the job at the end
X. Other (please specify)

[Answer]:

## Q4: Python setup mechanism

How should the runner get Python 3.12?

A. `actions/setup-python` with `python-version: "3.12"` (official action; matches the project's language decision)
B. A pinned container image that already contains Python 3.12
X. Other (please specify)

[Answer]:

## Q5: Secret hygiene in the workflow

Given there is no deploy credential, what else must the workflow avoid?

A. No `secrets.*` references at all, no `env` values sourced from secrets, and no step that echoes environment contents; the only credential-like input is the automatic `GITHUB_TOKEN` that Actions provides, used by no step
B. Allow `GITHUB_TOKEN` for the deploy step if a later change reintroduces one
X. Other (please specify)

[Answer]:

---

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]: Looks correct
