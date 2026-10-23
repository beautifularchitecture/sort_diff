# Quality Gates

| Gate | Command | Condition | Purpose |
|------|---------|-----------|---------|
| Format | `black --check .` | `if: always()` | Enforces code style (NFR4.1) |
| Lint | `ruff check .` | `if: always()` | Enforces lint rules (NFR4.1.1) |
| Tests + Coverage | `pytest` | `if: always()` | Runs all tests with `--cov=sorting_core --cov-fail-under=80` from `pyproject.toml` (NFR4.2, NFR4.2.1) |

## Enforcement
- Gates run in order: Black → Ruff → pytest.
- Each gate uses `if: always()` so earlier failures don't skip later gates (visibility of all issues).
- Job fails if any gate fails.
- Least privilege: `permissions: contents: read`. No secrets or deployment steps.

## Verification
- Local: `black --check . && ruff check . && pytest` all pass.
- Structural tests: `tests/test_workflow.py` validates trigger, job structure, step order, permissions, and absence of secrets/deploy.
