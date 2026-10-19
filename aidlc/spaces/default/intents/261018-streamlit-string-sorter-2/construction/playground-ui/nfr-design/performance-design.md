# Performance Design — playground-ui (U2)

Implements the requirements in `nfr-requirements/performance-requirements.md` (NFR1.1, NFR2.1, NFR2.2, NFR3.6). Consumes `nfr-requirements/performance-requirements.md`, `nfr-requirements/security-requirements.md`, `nfr-requirements/tech-stack-decisions.md`, `functional-design/functional-spec.md`, and `contract-design/contract-summary.md`.

## Design Decisions

| ID | Decision | Implements |
|---|---|---|
| PD-1 | No caching. `run_all` is called fresh on every Sort press; `st.cache_data` is not used (NFR design Q2, option A). Input is classroom-sized, so recomputation is cheap and always reflects the current widgets. | NFR3.6 |
| PD-2 | Results are recomputed from the current widget values on every rerun (NFR design Q3, option B). No results are stored in `st.session_state`; the displayed output is a pure function of the widgets. | NFR3.6 |
| PD-3 | The three result columns are built in a single pass and rendered with `st.columns(3)`, one column per `AlgorithmResult` in `[bubble, selection, quick]` order. No pagination, lazy loading, or async work. | NFR2.2 |
| PD-4 | The shared list is built and de-duplicated once per rerun, before the 100-string cap check and the single `normalize` call. No repeated normalization. | NFR2.1, NFR2.2 |

## Performance Budget

- **Latency target:** none numeric (inherited NFR Q4 A). The 100-string hard cap (NFR3.6) bounds the worst case: three sorts over ≤100 strings plus three `check` calls, all in-process.
- **Throughput:** not applicable — one interactive user, one run per button press.
- **Resource pooling / connection pooling / CDN:** not applicable; no external services and no persistent connections.
- **Async or background processing:** not used; Streamlit renders synchronously per interaction.

## Referenced Upstream

- `requirements.md` — NFR1, NFR2, NFR3.
- `contract-summary.md` — Contract 1 result types, Contract 2 run interface.
- `functional-spec.md` — Part 5 result panels.
