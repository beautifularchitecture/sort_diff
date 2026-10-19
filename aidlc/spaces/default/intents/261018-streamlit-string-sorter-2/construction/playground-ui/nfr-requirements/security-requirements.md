# Security Requirements — playground-ui (U2)

Derived from inception NFR2 (Simplicity and Usability) and NFR3 (Scope and Constraints), and the confirmed answers to this unit's NFR Q1 and Q3. Consumes `functional-spec.md`, `rules.md`, `requirements.md`, and `contract-summary.md`. This is the reviewed artifact for the stage.

## Requirements

| ID | Requirement | Source | Verification |
|---|---|---|---|
| NFR3.1 | All user-typed and picked strings are treated as inert plain text. The UI never evaluates, executes, or deserializes them, and never passes them to `eval`, `exec`, or a template engine. | NFR2.1, NFR Q3 (A) | Code review of `app.py`; unit test with `__import__('os')` and `<script>alert(1)</script>` rendered as literal text. |
| NFR3.2 | The UI performs no file I/O, network access, or persistent storage at runtime. The bundled word list is a module-level constant, loaded from source, not read from disk at run time. | NFR3.2, functional-spec Part 2 | Static check: no `open`, `socket`, `requests`, or `urllib` in `app.py`; word list defined in code. |
| NFR3.3 | The UI collects no personal data and has no authentication or authorization. | NFR3.3 | Design review; no identity inputs exist. |

## Threat Considerations

- **Stored XSS through echoed input:** user strings are echoed back and shown in result columns (functional-spec Part 5). Mitigated by NFR3.1 and the rendering decision (NFR Q3 A): render through Streamlit's default text APIs, which HTML-escape, and never `unsafe_allow_html=True`. Sorting-core produces no markup (U1 NFR2.2), so escaping at the UI is the single control point.
- **Resource exhaustion:** mitigated by the 100-string hard cap (NFR3.6) checked before any algorithm runs.
- **Injection through the word-list picker:** the bundled list is a fixed constant (NFR3.2), not user-editable or remotely fetched, so it cannot inject content.

## Out of Scope for This Unit

- Authentication, sessions, and access control (NFR3.3): not applicable to a single-page demo with no accounts.
- Transport security (TLS): provided by the Streamlit Community Cloud hosting platform, not this unit.

## Referenced Upstream

- `functional-spec.md` (this unit) — Part 2 components, Part 5 result panels.
- `rules.md` (this unit) — BR1.2 exact empty-input warning.
- `requirements.md` — NFR2, NFR3.
- `contract-summary.md` — Contract 1 boundaries (TypeError, ValueError).
- `technology-stack` — not applicable on this greenfield run.
