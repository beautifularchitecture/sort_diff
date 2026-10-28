# Code Generation Plan — uvx-migration (zero-Unit, stage-level)

## Summary

- Builds: remove the local `.venv` setup; run tools and app via `uv` / `uvx`; devcontainer on Python 3.12.
- Touches: `README.md`, `AGENTS.md`, `.gitignore`, `.devcontainer/devcontainer.json`, and the local `.venv/` directory (deleted, not tracked).
- Tests: no new tests (refactor scope). The existing suite must stay green; `uvx black --check .`, `uvx ruff check .`, and the pytest command pass.

## Scope

Requirements FR-1 to FR-10 in `inception/requirements-analysis/requirements.md`. Unchanged paths: `.github/workflows/ci.yml`, `pyproject.toml`, `requirements.txt`, `app.py`, `sorting_core/`.

## Steps

- [x] Step 1: Verify the existing test runner and record the exact commands. Run `uvx --with-requirements requirements.txt pytest` and `uvx black --check .` and `uvx ruff check .` once before editing, and note their results in `code-summary.md` (baseline). Maps to FR-4.
- [x] Step 2: Add `.venv/` as a project entry in `.gitignore`, outside the AI-DLC managed block. Maps to FR-7.
- [x] Step 3: Rewrite the setup and run sections of `README.md` to use `uv` / `uvx` only: remove `python3 -m venv`, `source .venv/bin/activate`, and `pip install`; document `uv run --with-requirements requirements.txt streamlit run app.py`; document the CI check commands and the single-test command with `--no-cov`. Maps to FR-2, FR-3, FR-4, FR-5.
- [x] Step 4: Update `AGENTS.md` setup and command sections to the same uv commands; remove venv instructions. Maps to FR-6.
- [x] Step 5: Change the devcontainer image to a Python 3.12 image in `.devcontainer/devcontainer.json`. Maps to FR-8.
- [x] Step 6: Delete the local `.venv/` directory (`rm -rf .venv`), after confirming it is not tracked by git. Maps to FR-1.
- [x] Step 7: Verify: `test ! -d .venv`; the grep checks in FR-2 and FR-6 print `0`; `git diff -- .github/workflows/ci.yml pyproject.toml requirements.txt app.py sorting_core` is empty (FR-9, FR-10); the commands in the README pass (FR-4, FR-5 with a real test name).

Testing Contract: no new tests are written. Test strategy is minimal; the scope adds no new-test floor; the existing suite stays green (Step 1 and Step 7).

## Testing Contract

```json
{
  "version": 1,
  "methodology": "test-after",
  "source": "team",
  "ordering": "Implement each testable piece — each sorting algorithm, then the UI wiring — and then write and run that piece's tests before moving on to the next piece.",
  "scope": "refactor",
  "test_strategy": "minimal",
  "project_type": "brownfield",
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
    "strategy": "minimal",
    "strategy_volume": [
      "One verifiable test per requirement at the narrowest effective level.",
      "At least one happy-path unit test per component.",
      "Unit tests are the default; a bugfix/security scope floor may require an integration or E2E regression when that is the narrowest level that reproduces the defect."
    ],
    "scope_floor": [
      "Keep the existing test suite green.",
      "This scope adds no extra new-test floor beyond the selected test strategy."
    ],
    "combination_rule": "Apply every selected-strategy obligation and every scope-floor obligation; neither replaces the other, and a targeted scope regression may add the narrowest necessary test type beyond the strategy default."
  },
  "plan_profile": {
    "methodology": "test-after",
    "runner_step": "Verify the existing test runner/configuration and record the exact unit-scoped command.",
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
      "Verify the existing test runner/configuration and record the exact unit-scoped command.",
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
  "input_sha256": "sha256:e8a9b62659ec7757abc59cda002915ddfc3a3b866c27dce22bf43740d7559dd8",
  "contract_sha256": "sha256:5ada12b95fccbc9a2a417736747d4d01ff465452be251d22cedd2b14e6c5e685"
}
```
