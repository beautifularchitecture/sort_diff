# Integration Test Instructions

Test strategy: **Standard**. Unit tests are owned per unit by Code Generation; this document covers the boundaries between units, plus how to run the integrated suite.

## Boundaries under test

1. **UI → core pipeline (U2 → U1).** `InputProcessor.normalize` → `SortingEngine.run_all` → `AccuracyChecker.check`, wired in `app.py` and driven through `streamlit.testing.v1.AppTest` (`tests/ui/test_app.py`). Assertions: three columns render in bubble/selection/quick order; displayed comparison/swap counts equal the core's counts; typed and multi-select inputs are de-duplicated into one sort; the empty-input and over-cap guards stop the pipeline; core exceptions propagate to Streamlit.
2. **Repository commands → CI workflow (U3 → U1/U2).** `tests/test_workflow.py` parses `.github/workflows/ci.yml` and asserts the workflow runs install, Black, Ruff, and bare `pytest` in order with `if: always()`.
3. **Algorithms → reference sort (U1 internal).** Every algorithm's output is compared with `sorted()` in `tests/test_algorithms.py`, with counts checked against hand-computed examples.

## How to run

Authoritative integrated run (the CI command):

```bash
pytest
```

Scoped runs:

```bash
pytest tests/ui/ --cov=app --cov-report=term-missing --cov-fail-under=80 -q
pytest tests/test_workflow.py -q
```

**Important — project `addopts`.** `pyproject.toml` adds `--cov=sorting_core --cov-report=term-missing --cov-fail-under=80` to every invocation. The workflow-only scoped run imports no application code, so it exits 1 with `Total coverage: 0.00%` even though all 7 tests pass. The coverage floor is measured by the full-suite `pytest` run, which is what CI runs. Do not add `--no-cov` or lower the floor to make a scoped run green.

## Coverage targets

| Component | Target | Source | Measured |
|-----------|--------|--------|----------|
| `sorting_core` | ≥ 80% line coverage | NFR4.2 / NFR4.2.1 | 100.00% (166 statements, 0 missed) — full suite |
| `app.py` | ≥ 80% line coverage | NFR4.2 (U2 test command) | 100% (56 statements, 0 missed) — UI run |

## Test data

- Bundled word list from `WordListProvider` (non-empty, read-only).
- Hand-computed count examples: bubble `[3,1,2]` → 3 comparisons / 2 swaps; selection → 3 / 2; quick → 2 / 2.
- Edge inputs: empty, single element, all-identical, duplicates, non-ASCII, and adversarial strings such as `<script>alert(1)</script>` and `__import__('os')` (sorted as inert text).

## Expected outcome

`116 passed`, coverage floor reached, exit 0. Any assertion failure on a boundary is a real integration defect and must be fixed before the stage can pass; a coverage-only failure on a scoped subset is a measurement artifact, not a test failure.
