# Security Design — playground-ui (U2)

Implements the requirements in `nfr-requirements/security-requirements.md` (NFR3.1, NFR3.2, NFR3.3) and `nfr-requirements/performance-requirements.md` (NFR2.1, NFR3.6). Consumes `nfr-requirements/security-requirements.md`, `nfr-requirements/performance-requirements.md`, `nfr-requirements/tech-stack-decisions.md`, `functional-design/functional-spec.md`, and `contract-design/contract-summary.md`.

## Design Decisions

| ID | Decision | Implements |
|---|---|---|
| SD-1 | All user-typed and picked strings are treated as inert data. The UI never calls `eval`, `exec`, `compile`, or a template engine on them. | NFR3.1 |
| SD-2 | User strings reach the screen only through Streamlit's default text/table APIs (`st.text`, `st.write` with plain strings, `st.table`). `unsafe_allow_html=True` is never used, so Streamlit's own escaping is the single output-encoding control. This realizes the escaping obligation U1 recorded as a caller responsibility. | NFR2.1, NFR2.2 |
| SD-3 | The 100-string cap is enforced in the UI on the de-duplicated shared list, immediately before `normalize`. Above the cap, the UI refuses to sort and shows a message stating the limit. This realizes the cap obligation U1 recorded as a caller responsibility. | NFR3.6 |
| SD-4 | The UI performs no file I/O, network access, or persistent storage. The bundled word list is a module-level constant in source. | NFR3.2, NFR3.3 |
| SD-5 | No user identity is accepted, stored, or transmitted. | NFR3.3 |
| SD-6 | Exceptions raised by sorting-core (`TypeError`, `ValueError`, `RecursionError`) are not caught; they propagate and Streamlit renders the traceback (NFR design Q1, option B). Errors are surfaced, never swallowed. | NFR3.1 |

## Boundary Behaviour

- The UI passes a `list[str]` to `normalize`; Contract 1's `TypeError`/`ValueError` boundaries are therefore not expected on the happy path.
- Under SD-6 a boundary exception is visible to the user as Streamlit's error panel. This is acceptable for a free, local, non-sensitive demo: it is loud (never silent) and leaks no data beyond the user's own input.
- The 100-string cap (SD-3) also bounds quick-sort recursion depth, so the `RecursionError` risk noted in U1's review is not reachable at classroom size under this design.

Snippet (interface level, illustrative):

```python
if len(shared_list) > 100:
    st.error("Input exceeds the 100-string limit.")
else:
    sort_input = normalize(shared_list)
    results = run_all(sort_input)
```

## Caller Obligations Realized

This unit *is* the caller that U1's `security-design.md` names. Both obligations it records are discharged here:

- Escape output before rendering → SD-2 (plain-text rendering, no unsafe HTML).
- Cap input at 100 strings before `normalize` → SD-3.

## Threats Considered

| Threat | Treatment |
|---|---|
| Stored XSS through echoed input | SD-1, SD-2 (Streamlit escaping; no `unsafe_allow_html`) |
| Code injection through input text | SD-1, SD-6 (surfaced, not executed) |
| Resource exhaustion through large input | SD-3 (100-string hard cap) |
| Unexpected I/O or secret exposure in the UI | SD-4 |
| Identity / PII collection | SD-5 |

## Referenced Upstream

- `requirements.md` — NFR2, NFR3.
- `contract-summary.md` — Contract 1 boundaries.
- `functional-spec.md` — Part 3 shared list, Part 4 empty-input guard.
