# Test Results

Date: 2026-10-22
Intent: `261018-streamlit-string-sorter-2`
Verification environment: `.venv` Python 3.14.8, pytest 9.1.1, Black and Ruff from `requirements.txt`. CI pins Python 3.12.

## Build status

| Step | Command | Result | Exit |
|------|---------|--------|------|
| Byte-compile | `python -m compileall -q app.py sorting_core` | No errors | 0 |
| Import (warnings as errors) | `PYTHONWARNINGS=error python -c "import app"` | Imports cleanly | 0 |
| Dependency import | `python -c "import streamlit, yaml, black, ruff"` | All present | 0 |
| App boot (headless) | `timeout 20 streamlit run app.py --server.headless true --server.port 8599` | `Local URL` printed | 124 (expected timeout after boot) |
| Format | `black --check .` | 18 files unchanged | 0 |
| Lint | `ruff check .` | All checks passed | 0 |
| Full suite | `pytest` | 116 passed, coverage floor reached | 0 |

## Test results per test type

| Test type | Files | Tests | Result |
|-----------|-------|-------|--------|
| Unit — algorithms and counting | `tests/test_algorithms.py` | 97 | Passed |
| Unit/integration — UI wiring | `tests/ui/test_app.py` | 12 | Passed |
| Structural — CI workflow | `tests/test_workflow.py` | 7 | Passed |
| **Total** | | **116** | **Passed** |

## Coverage

Full suite (`pytest`):

| Module | Statements | Missed | Coverage |
|--------|-----------|--------|----------|
| `sorting_core/__init__.py` | 8 | 0 | 100% |
| `sorting_core/algorithms.py` | 60 | 0 | 100% |
| `sorting_core/checker.py` | 14 | 0 | 100% |
| `sorting_core/engine.py` | 16 | 0 | 100% |
| `sorting_core/normalize.py` | 20 | 0 | 100% |
| `sorting_core/runner.py` | 12 | 0 | 100% |
| `sorting_core/types.py` | 27 | 0 | 100% |
| `sorting_core/words.py` | 9 | 0 | 100% |
| **TOTAL** | **166** | **0** | **100.00%** |

Floor: 80% (NFR4.2). Result: met with 20 points of headroom.

UI-scoped run (`pytest tests/ui/ --cov=app ...`): `app.py` 56 statements, 0 missed, 100%; combined total 96% (the run exercises only part of `sorting_core`, which is covered fully by its own suite).

## Failure details

1. **U1 scoped run, first attempt — `coverage.exceptions.DataError: Couldn't use data file ... no such table: meta`.** Cause: two pytest processes ran concurrently and shared the same `.coverage` data file. Resolution: re-ran the command serially → 97 passed, 100% coverage, exit 0. No code defect.
2. **U3 scoped run — exit 1 with `Required test coverage of 80% not reached. Total coverage: 0.00%`.** All 7 workflow tests passed. Cause: `pyproject.toml` adds `--cov=sorting_core --cov-fail-under=80` to every run, and the workflow test imports no application code, so no coverage is collected. This is a measurement artifact, not a test failure; the project-wide floor is demonstrated by the full-suite run, which is the CI command. Documented in `integration-test-instructions.md`; no configuration was weakened.
3. **Streamlit smoke boot — exit 124.** Expected: `timeout` terminates a successfully booted server after the Local URL appears. Not a failure.

No test failed. No Build-and-Test failure loop-back was triggered, so this stage records no Loop-Back Log.

## Test type coverage matrix

| Test type | Target artifact | Executed | Status |
|-----------|-----------------|----------|--------|
| Unit | `tests/test_algorithms.py`, `tests/test_checker.py`, `tests/test_normalize.py` | Yes | Covered |
| Integration | `tests/ui/test_app.py`, `tests/test_workflow.py` | Yes | Covered |
| Edge cases | empty, single, all-identical, duplicates, non-ASCII, 101-string cap, hostile strings | Yes | Covered |
| Security (static + behavioural) | AST/API scan, workflow least-privilege tests | Yes | Covered |
| Performance (bounded input) | 100-string cap tests | Yes | Covered |
| Build smoke | compileall, import, Streamlit headless boot | Yes | Covered |
| Deployment observation | AC5.2.x against a live environment | No | Deferred — owned by Deployment Pipeline / Deployment Execution |

## Final Target Verification Matrix

| # | Target ID | Source | Expected | Actual | Evidence | Owning stage | Verdict |
|---|-----------|--------|----------|--------|----------|--------------|---------|
| 1 | NFR4.2, NFR4.2.1 | `requirements.md`; U1/U2/U3 NFR requirements | `sorting_core` line coverage ≥ 80% | 100.00% (166/166 statements) | `/tmp/opencode/pytest-full.log` | build-and-test | Met |
| 2 | NFR4.2 (U2) | `playground-ui/.../unit-test-instructions.md` | `app.py` line coverage ≥ 80% | 100% (56/56) | `/tmp/opencode/pytest-u2.log` | build-and-test | Met |
| 3 | NFR4.1, NFR4.1.1 | `requirements.md`; tech-stack NFR | Black check passes | 18 files unchanged | `black --check .` | build-and-test | Met |
| 4 | NFR4.1, NFR4.1.1 | `requirements.md`; tech-stack NFR | Ruff check passes | All checks passed | `ruff check .` | build-and-test | Met |
| 5 | NFR4.2.1 | delivery-pipeline NFR requirements | CI runs bare `pytest` under the coverage gate with `if: always()` | Present and asserted | `tests/test_workflow.py::test_bare_pytest_command`, `::test_gate_steps_in_order_with_always` | build-and-test (live run: ci-pipeline) | Met |
| 6 | NFR4.1.1 | delivery-pipeline NFR requirements | Black and Ruff gate steps, in order, each `if: always()` | Present and asserted | `tests/test_workflow.py::test_gate_steps_in_order_with_always` | build-and-test | Met |
| 7 | NFR3.4.1 | security NFR requirements | No secrets, no deploy, least-privilege token | No `secrets.`/`deploy`; `permissions: contents: read` | `tests/test_workflow.py::test_least_privilege_and_no_secrets_or_deploy` | build-and-test | Met |
| 8 | NFR3.4.2 | security NFR requirements | Closed workflow step list, no extra network access | Only checkout, setup-python, install, Black, Ruff, pytest | `tests/test_workflow.py` (7 tests) | build-and-test | Met |
| 9 | NFR2.3.1, NFR3.3 | security NFR requirements | No identity, accounts, or personal data | No auth/identity/PII code or dependency | source inspection | build-and-test | Met |
| 10 | NFR3.6, SD-3 | U2 NFR requirements / performance design | 101 strings refused; ≤100 accepted | Refusal message shown, no sorting; happy path sorts | `tests/ui/test_app.py::test_over_cap_input_shows_limit_message_and_runs_no_sorting` | build-and-test | Met |
| 11 | NFR3.6 | U2 NFR requirements | No numeric latency target; responsive at classroom size | No target defined; work bounded by the 100-string cap | `performance-test-instructions.md`, U2 perf design | build-and-test | Met (constraint satisfied; no numeric target) |
| 12 | NFR2.1 (U1) | sorting-core NFR requirements | Hostile strings treated as inert text | Sorted literally; no eval/deserialize | `tests/test_algorithms.py` (unicode/duplicates), `tests/ui/test_app.py::test_source_uses_no_unsafe_html_and_no_eval_or_exec` | build-and-test | Met |
| 13 | NFR2.2 (U1) | sorting-core NFR requirements | Core emits no HTML/markup | Returns plain strings and counts only | source inspection | build-and-test | Met |
| 14 | NFR3.1 (U2) | playground-ui NFR requirements | No `unsafe_allow_html`, `eval`, or `exec` | AST scan clean | `tests/ui/test_app.py::test_source_uses_no_unsafe_html_and_no_eval_or_exec` | build-and-test | Met |
| 15 | NFR3.2 (U1) | sorting-core NFR requirements | No file, network, or process access | No matching imports/calls | static scan (`security-test-instructions.md`) | build-and-test | Met |
| 16 | NFR3.2 (U2) | playground-ui NFR requirements | No I/O, network, or persistent storage | No matching imports/calls | static scan | build-and-test | Met |
| 17 | NFR1.1 (U2) | playground-ui NFR requirements | Accuracy shown exactly as returned | Accuracy column matches core result | `tests/ui/test_app.py::test_happy_path_renders_three_columns_with_pass_accuracy` | build-and-test | Met |
| 18 | NFR2.2 (U2), NFR1.1 | playground-ui NFR requirements | Per-column name, list, comparisons, swaps, accuracy | All five rendered per column | `tests/ui/test_app.py` happy-path and counts tests | build-and-test | Met |
| 19 | NFR1.1, NFR1.2, NFR4.3 | `requirements.md`; U1 NFR requirements | Every sort equals `sorted()`; counts follow BR2.1/BR2.2 | All cases match; hand-computed counts match | `tests/test_algorithms.py`, `tests/test_checker.py` | build-and-test | Met |
| 20 | FR7.3, AC5.2.3 | `requirements.md`; `stories.md` | Trigger on push to `main` only, no PR trigger | Asserted | `tests/test_workflow.py::test_triggers_on_push_to_main_only` | build-and-test | Met |
| 21 | NFR3.1 (project) | `requirements.md` | Only bubble, selection, quick exist | Exactly three algorithms exported | source inspection, `tests/test_algorithms.py` | build-and-test | Met |
| 22 | FR1.5, AC1.2.3 | `requirements.md`; `stories.md` | Bundled, non-empty, read-only list; no network fetch | Tuple constant in `sorting_core/words.py`; tests pass | `tests/ui/test_app.py::test_word_list_is_non_empty_and_read_only` | build-and-test | Met |
| 23 | FR6.1, AC4.1.1 | `requirements.md`; `stories.md` | Exact empty-input message | Message rendered, no result columns | `tests/ui/test_app.py::test_empty_input_shows_exact_message_and_no_result_columns` | build-and-test | Met |
| 24 | FR1.3, AC1.1.2 | `requirements.md`; `stories.md` | Lowercase ASCII A–Z normalization | Normalization tests pass | `tests/test_normalize.py` | build-and-test | Met |
| 25 | FR3.1, AC3.2.3 | `requirements.md`; `stories.md` | Accuracy checked against `sorted()` | Pass/fail matches reference | `tests/test_checker.py` | build-and-test | Met |
| 26 | FR4.1–FR4.4, AC3.2.1, AC3.2.2, AC3.2.5 | `requirements.md`; `stories.md` | Comparison/swap/accuracy counts displayed per algorithm | Counts equal core counters and render as full integers | `tests/test_algorithms.py`, `tests/ui/test_app.py::test_counts_match_sorting_core_and_render_as_full_integers` | build-and-test | Met |
| 27 | FR2.4, AC2.1.2 | `requirements.md`; `stories.md` | Lexicographic order honored | Unicode and duplicate cases ordered correctly | `tests/test_algorithms.py::test_unicode_lexicographic_order` | build-and-test | Met |
| 28 | FR6.2–FR6.4, AC4.2.1–AC4.2.3 | `requirements.md`; `stories.md` | Single, all-identical, and empty-token edge cases | All render/sort correctly | `tests/test_algorithms.py`, `tests/test_normalize.py`, `tests/ui/test_app.py` | build-and-test | Met |
| 29 | NFR3.5 | `requirements.md` | Free/open-source distribution; no paid service | Only free OSS dependencies; no paid integration | `requirements.txt`, source inspection | build-and-test | Met |
| 30 | Build integrity | `build-instructions.md` | Code compiles, imports, and the app boots | compileall, import, and headless boot all succeeded | command outputs above | build-and-test | Met |
| 31 | Integration boundaries | `code-generation-plan.md` per unit | UI→core and workflow→commands seams hold | All boundary tests pass | `tests/ui/test_app.py`, `tests/test_workflow.py` | build-and-test | Met |

Result: 31/31 in-scope targets Met, 0 Unverified, 0 Not Met. No target was deferred with an unverified verdict.
