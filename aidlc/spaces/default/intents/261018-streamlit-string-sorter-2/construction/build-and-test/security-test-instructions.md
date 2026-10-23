# Security Test Instructions

Test strategy: **Standard**. Security NFRs exist for this project, so the static and behavioural checks below are included under the stage's soft-guideline clause.

## Targets and checks

| Target | Check | Where |
|--------|-------|-------|
| NFR2.1 / NFR3.1 (U2) — user strings are inert | AST scan for `unsafe_allow_html`, `eval`, `exec`, and any builtin `compile` in `app.py`; input is only ever sorted as text | `tests/ui/test_app.py::test_source_uses_no_unsafe_html_and_no_eval_or_exec` |
| NFR2.2 / NFR3.1 (U2) — no markup injection | Plain Streamlit text/markdown APIs; no raw HTML | same test + grep |
| NFR3.2 (U1) — no I/O, network, or process access in the core | Static scan for `open`, `socket`, `requests`, `urllib` imports | grep + source inspection |
| NFR3.2 (U2) — no file, network, or persistent storage in the UI | Static scan | grep + source inspection |
| NFR3.4.1 — no secrets, credentials, or deployment in CI | Workflow contains no `secrets.` and no `deploy` (case-insensitive), top-level `permissions: contents: read` | `tests/test_workflow.py::test_least_privilege_and_no_secrets_or_deploy` |
| NFR3.4.2 — closed, minimal workflow step list | Steps limited to checkout, setup-python, install, Black, Ruff, pytest | `tests/test_workflow.py::test_gate_steps_in_order_with_always`, `::test_bare_pytest_command` |
| NFR3.6 / SD-3 — resource exhaustion is bounded | 101-string input refused; no sorting runs | `tests/ui/test_app.py::test_over_cap_input_shows_limit_message_and_runs_no_sorting` |

## How to run

```bash
grep -RnE --exclude-dir=__pycache__ "unsafe_allow_html|(^|[^.[:alnum:]_])eval\(|(^|[^.[:alnum:]_])exec\(|(^|[^.[:alnum:]_])open\(|import (socket|requests|urllib)|from (socket|requests|urllib)" app.py sorting_core tests
pytest tests/ui/test_app.py tests/test_workflow.py -q
```

Expected: the grep finds only docstring mentions in `app.py` and the AST keyword check in `tests/ui/test_app.py` (no executable use); the two test files pass.

Static-scan result at verification time: 3 matches, all documentation or scan-target references — no dangerous API call in application code.

## Out of scope

No authentication, authorization, transport-security, DAST, or dependency-audit service applies at this stage: the app has no accounts, no secrets, no server-side data store, and no deployed environment. Hosting/TLS security is platform-owned and is validated in the deployment stages.
