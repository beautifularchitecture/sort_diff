# Code Generation Plan — delivery-pipeline (U3)

## Summary

- Builds: the GitHub Actions CI workflow that runs the whole repository's checks on push to `main`, plus a structure test for it.
- Touches: `.github/workflows/ci.yml` (new), `tests/test_workflow.py` (new), `requirements.txt` (add `pyyaml` as a test-only dependency).
- Tests: standard strategy, test-after: workflow structure tests parsing the committed YAML, about 7 tests, run with `pytest tests/test_workflow.py -q`.

## Goals

- Implement the CI workflow so it realizes the approved design: `infrastructure-design/cicd-pipeline.md` (one serial `checks` job, push-to-`main` only, `if: always()` gate steps, `permissions: contents: read`, bare `pytest`), `infrastructure-design/infrastructure-specification.md`, `nfr-design/security-design.md` (SD-1..SD-7), and Contract 2 (the exact commands U3 invokes).
- No deploy step: Streamlit Community Cloud rebuilds from the pushed `main` commit (SD-5). No stored credential (nfr-requirements Q3 B); no `secrets.*` reference (SD-6).
- Coverage floor rides in the project pytest configuration (`pyproject.toml` addopts, U1-owned), not in the workflow command (SD-4). U3 invokes bare `pytest` per Contract 2.
- This is a packaging-kind unit: no application/domain code, no UI. The single production artifact is the workflow YAML; the single test artifact is its structure test.

## Traceability (plan step → design IDs)

| Plan step | Design IDs |
|---|---|
| 1 Workflow skeleton and trigger | FR7.3, SD-1, US5.2, cicd-pipeline.md Pipeline Overview |
| 2 Single serial `checks` job | SD-2, nfr-design Q1 A, infrastructure-design Q1 A |
| 3 Install step provisioning all gate tooling | SD-2, SD-7, Contract 2, requirements.txt |
| 4 Black and Ruff gate steps with `if: always()` | FR7.3, NFR4.1.1, SD-2, SD-3 |
| 5 Bare `pytest` gate step with `if: always()` | NFR4.2.1, SD-4, Contract 2 |
| 6 Least-privilege token and no-secrets posture | NFR3.4.1, SD-6, nfr-design Q5 B |
| 7 No deploy step; platform-managed deploy | FR7.2, FR7.3, SD-5, nfr-requirements Q3 B |
| 8 Workflow structure tests | NFR4.1.1, NFR4.2.1, NFR3.4.1, SD-1..SD-7 |
| 9 Step 5 artifacts (summary, traceability, manifest) | Step 5 artifacts |

## Implementation Steps

1. [x] **Workflow skeleton and trigger (`.github/workflows/ci.yml`).** A YAML workflow triggered on `push` to `main` only — no `pull_request` trigger (SD-1, FR7.3). Top-level `name` and `on:` block. Source: cicd-pipeline.md, SD-1.
2. [x] **Single serial `checks` job.** One job `checks` on `runs-on: ubuntu-latest`, with steps running in order (nfr-design Q1 A; infrastructure-design Q1 A). Source: cicd-pipeline.md Job: checks.
3. [x] **Install step.** Step 2 `actions/setup-python@v5` with `python-version: '3.12'`; step 3 `pip install -r requirements.txt` — the U2-owned file already declares `streamlit`, `pytest`, `pytest-cov`, `black`, `ruff`, so this one step provisions every gate tool (SD-2, SD-7). Source: Contract 2, SD-2, SD-7.
4. [x] **Format and lint gate steps.** Steps 4–5: `black --check .` and `ruff check .`, each with `if: always()` so a failure does not skip the later gates (SD-2, SD-3; NFR4.1.1). Source: cicd-pipeline.md Job: checks, SD-3.
5. [x] **Test gate step.** Step 6: bare `pytest` (exactly as Contract 2 states) with `if: always()`; the coverage floor rides in the project pytest configuration, not this command (SD-4; NFR4.2.1). Source: Contract 2, SD-4.
6. [x] **Least-privilege token.** A top-level `permissions: contents: read` block so the automatic `GITHUB_TOKEN` cannot write (SD-6; nfr-design Q5 B); no `secrets.*` reference and no secret-sourced `env` anywhere in the file (NFR3.4.1). Source: SD-6.
7. [x] **No deploy step.** The workflow ends at `pytest`; deployment is Streamlit Community Cloud's push integration, observed out-of-band (SD-5; nfr-requirements Q3 B). Source: SD-5.
8. [x] **Workflow structure tests (`tests/test_workflow.py`).** Test-after (team posture). Parse the committed `.github/workflows/ci.yml` with PyYAML and assert the structure the design fixes:
   - the workflow parses as valid YAML (top-level mapping);
   - the trigger is `push` on `main`, and there is no `pull_request` trigger (SD-1);
   - exactly one job named `checks` runs on `ubuntu-latest` (nfr-design Q1 A);
   - the step sequence contains `actions/setup-python` with `python-version: '3.12'`, `pip install -r requirements.txt`, `black --check .`, `ruff check .`, and `pytest` in that order (SD-2, SD-7);
   - the Black, Ruff, and pytest steps each carry `if: always()` (SD-3);
   - the top-level `permissions` is exactly `{contents: read}` (SD-6);
   - the file text contains no `secrets.` reference and no `deploy` step (SD-5, SD-6);
   - the pytest step's `run` is exactly `pytest` with no extra args (SD-4, Contract 2).
   Source: NFR4.1.1, NFR4.2.1, NFR3.4.1, SD-1..SD-7.
9. [x] **Step 5 artifacts.** Write `code-summary.md`, `traceability.json` (every NFR/FR/BR ID this unit carries; every OK target an existing file), and `source-manifest.json` listing every application-source path created or modified (`.github/workflows/ci.yml`, `tests/test_workflow.py`, `requirements.txt`). Source: Step 5.

## Test Considerations (for code writer)

- The workflow is the production artifact; GitHub Actions itself is its end-to-end test. The pytest structure test is the unit/integration layer for this unit, asserting the committed YAML matches the design's fixed facts.
- Add `pyyaml>=6.0` to `requirements.txt` as a test-only dependency for parsing the workflow; this is what makes the structure test runnable under the CI install step.
- Do not assert on GitHub-side behaviour the test cannot observe (e.g. that the deploy platform actually rebuilds); assert only on the committed file's structure.
- Do not weaken the 80% coverage floor or the workflow's gates to make a step pass; surface any gap instead.
- The workflow's step order and `if: always()` markers are the point of SD-3 (nfr-design Q3 B): a failing Black must not skip pytest.

## Non-Functional Notes

- The workflow performs no network access beyond `pip install` from PyPI (NFR3.4.2); no data source is read.
- No secrets, no deploy credential, no identity (NFR3.4.1, NFR2.3.1; SD-5, SD-6).
- YAML follows the repository's formatting conventions; no Black/Ruff changes needed for YAML, but the Python test file follows Black/Ruff/snake_case (NFR4.1.1).

## Testing Contract

```json
{
  "version": 1,
  "methodology": "test-after",
  "source": "team",
  "ordering": "Implement each testable piece — each sorting algorithm, then the UI wiring — and then write and run that piece's tests before moving on to the next piece.",
  "scope": "feature",
  "test_strategy": "standard",
  "project_type": "greenfield",
  "applicable_notes": [
    {
      "layer": "org",
      "text": "We treat tests as a first-class deliverable in every Bolt. The specific\nmethodology (TDD, BDD, ATDD, or classic test-after) is affirmed at\npractices-discovery and recorded in `team.md` under this heading with explicit\n`Methodology` and `Ordering` fields; Code Generation resolves those fields\nindependently from coverage, tooling, and scope notes.\n\nWhen no posture has been affirmed, our default per scope is:\n- **Methodology**: test-after\n- **Ordering**: implement each applicable testable layer, then write and run\n  that layer's tests.\n- `mvp`, `enterprise`, `feature`, `infra`, `classic` add an 80% line-coverage\n  floor and CI execution before merge.\n- `bugfix`, `security-patch` add a targeted regression for the specific\n  bug/vulnerability and require the existing suite to remain green.\n- `express` uses the Minimal strategy: requirement-driven unit tests (one per\n  requirement, with a happy-path floor per component); existing tests remain\n  green.\n- `poc`, `refactor`, `workshop` add no extra new-test floor and require the\n  existing suite to remain green.\n\nThe active `Test Strategy` still applies in every scope and determines test\nvolume/types. Scope floors are additive; they never reduce or replace the\nselected strategy.\n\nBuild and Test verifies defined coverage floors and affirmed quality targets;\nthey may not be weakened to make a step pass.\n\nAffirm a stricter posture in `team.md` if the team commits to one."
    },
    {
      "layer": "team",
      "text": "- **Methodology**: test-after\n- **Methodology evidence**: The human chose \"tests after each piece is implemented\" in the interview (Q3, answer A — the org default for this scope), so tests are written after each piece of code rather than first.\n- **Ordering**: Implement each testable piece — each sorting algorithm, then the UI wiring — and then write and run that piece's tests before moving on to the next piece.\n- **Tooling**: pytest for unit tests; the test suite runs in CI before merge.\n- **Coverage**: roughly 80% line coverage on the sorting logic (the three algorithms), held as a floor in Build and Test and never weakened to make a step pass.\n- **Scope notes**: focus on correctness and step-count accuracy for bubble sort, selection sort, and quick sort; no BDD feature files unless a later stage introduces them."
    }
  ],
  "obligations": {
    "strategy": "standard",
    "strategy_volume": [
      "Five to eight tests per component.",
      "Unit tests plus integration tests for key boundaries.",
      "Add E2E, performance, or security tests when requirements demand them."
    ],
    "scope_floor": [
      "Meet an 80% line-coverage floor.",
      "Run the selected tests in CI before merge."
    ],
    "combination_rule": "Apply every selected-strategy obligation and every scope-floor obligation; neither replaces the other, and a targeted scope regression may add the narrowest necessary test type beyond the strategy default."
  },
  "plan_profile": {
    "methodology": "test-after",
    "runner_step": "Bootstrap the minimal test runner/configuration and record the exact unit-scoped command.",
    "runner_ready_before_first_test": true,
    "testable_layers": [
      "Data model / database behavior",
      "Repository / data access",
      "Business logic",
      "API / endpoint",
      "Frontend behavior"
    ],
    "steps": [
      "Project structure and production configuration skeleton.",
      "Bootstrap the minimal test runner/configuration and record the exact unit-scoped command.",
      "Data model / database behavior - implement.",
      "Data model / database behavior - write and run its tests after implementation.",
      "Repository / data access - implement.",
      "Repository / data access - write and run its tests after implementation.",
      "Business logic - implement.",
      "Business logic - write and run its tests after implementation.",
      "API / endpoint - implement.",
      "API / endpoint - write and run its tests after implementation.",
      "Frontend behavior - implement.",
      "Frontend behavior - write and run its tests after implementation.",
      "Environment/build configuration.",
      "Documentation and traceability."
    ]
  },
  "input_sha256": "sha256:43e2ce67a9fc94f414b7e3f4a8779aa72dec0d741bec78b6fadea13a42ddfdad",
  "contract_sha256": "sha256:e154f7554fa204574257c53f960d41fc0ea68813e93b20163f448966f784149e"
}
```
