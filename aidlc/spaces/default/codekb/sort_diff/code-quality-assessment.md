# Code Quality Assessment — sort_diff

## Ratings (good / fair / poor)
- **Naming clarity**: good — descriptive names; one exception, `Counter` shadows `collections.Counter` (fair on that point).
- **Function size**: good — all functions are short; `render_results` and `main` are the longest, both under 30 lines.
- **Error handling**: good at the boundary (`TypeError`/`ValueError` in `normalize`, `engine`, `checker`); deliberately propagated to the UI. Fair on `quick_sort`: no depth guard.
- **Test presence**: good — tests exist for every module, including UI and CI structure. About 82 test functions (static `def test_` count; parametrized cases not expanded).
- **Duplication**: fair — split rule duplicated between `app.py` and `sorting_core/normalize.py`; `app.py` re-implements `sorting_core.runner.run_all`.
- **Dead code**: good — no commented-out blocks; `sorting_core.run_all` is exported but unused by the app (documented as a convenience).

## Test Coverage
- Coverage gate: `--cov=sorting_core --cov-fail-under=80` in `pyproject.toml`. The coverage run is not measured in this scan.
- `app.py` is not in the coverage target; only the AppTest run exercises it.
- Coverage of `app.py` is therefore unmeasured by the gate.

## Linting and Formatting
- Ruff `E,F,I,W`, line-length 88; Black line-length 88 (`pyproject.toml`).
- Enforced in CI as `black --check .` and `ruff check .` before `pytest`.
- Gate not executed in this scan.
- No `# noqa`, `# type: ignore`, or `pragma: no cover` markers were found in hand-written code.

## CI/CD
- `.github/workflows/ci.yml`: one job, push to `main` only, no pull-request trigger, `permissions: contents: read`, no secrets, no deploy step (asserted by `tests/test_workflow.py`).
- Gaps: actions pinned by tag, not commit SHA; no pip cache; dependencies unpinned.

## Documentation
- `README.md`: setup, run, checks, and single-test instructions (working tree). A "Docker Hub credentials" section describes a Docker publish flow that `ci.yml` does not implement; it is stale.
- `AGENTS.md`: commands and critical constraints.
- Module docstrings are present and specific in every `sorting_core` module and `app.py`.
- Duplication risk: setup commands appear in both `README.md` and `AGENTS.md`.

## Technical Debt
- Unpinned, mixed runtime and dev dependencies in `requirements.txt`; no lock file.
- Python version mismatch: devcontainer 3.11 versus CI and `pyproject` 3.12.
- Devcontainer disables Streamlit XSRF protection in `postAttachCommand` (security review item for `devsecops-agent`).
- `quick_sort` is recursive with a worst case of O(n²) and O(n) recursion depth; the core has no size cap (the UI caps at 100).
- Stale docstring in `tests/ui/test_app.py` referring to `--cov=app`.
- Working tree has uncommitted changes to `README.md` and `intents.json`.
