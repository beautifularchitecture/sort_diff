# CI Configuration

## Workflow
- File: `.github/workflows/ci.yml`
- Name: `CI`
- Trigger: `push` to `main` only (no `pull_request`) — meets FR7.3 / AC5.2.3
- Permissions: `contents: read` (least privilege)
- Job: single serial job `checks` on `ubuntu-latest`

## Steps (in order, each with `if: always()`)
1. Checkout (`actions/checkout@v4`)
2. Set up Python (`actions/setup-python@v5`) with `python-version: "3.12"`
3. Install dependencies (`pip install -r requirements.txt`)
4. Black format check (`black --check .`)
5. Ruff lint check (`ruff check .`)
6. Tests (`pytest`)

## Notes
- Bare `pytest` command; coverage floor (≥80% on `sorting_core`) is enforced via `pyproject.toml` `addopts` as required by NFR4.2.1.
- No `secrets.*` references, no `deploy` step, no artifact publishing credentials — meets NFR3.4.1.
- Workflow structure validated by `tests/test_workflow.py` (7 tests pass).
