# Performance Requirements — playground-ui (U2)

Derived from inception NFR1 (Correctness), NFR2 (Simplicity and Usability), and NFR3 (Scope and Constraints), and the confirmed answers to this unit's NFR Q1 and Q4. Consumes `functional-spec.md`, `rules.md`, `requirements.md`, and `contract-summary.md`.

## Requirements

| ID | Requirement | Source | Verification |
|---|---|---|---|
| NFR1.1 | The UI displays the per-algorithm accuracy result exactly as `AccuracyChecker.check` returns it; it never recomputes, overrides, or hides a `fail`. | NFR1.1, functional-spec Part 5 | UI test: a forced `AccuracyCheck(passed=False)` renders `Accuracy: fail`. |
| NFR2.1 | The UI uses Streamlit defaults only — no custom CSS, theming, or heavy components. | NFR2.1, ADR-004 | Design review of `app.py`; no `st.markdown(..., unsafe_allow_html=True)` and no custom style assets. |
| NFR2.2 | Each result column clearly shows algorithm name, sorted list, `Comparisons: N`, `Swaps: N`, and `Accuracy: pass|fail` (functional-spec Part 5). | NFR2.2, AC3.1.1–AC3.1.3, AC3.2.5 | UI test asserting all five elements per column. |
| NFR3.6 | Inputs are classroom-sized. The UI enforces a hard cap of 100 strings in the shared list: above it, the UI refuses to sort and shows a message stating the 100-string limit. No numeric latency target applies; responsiveness for up to 100 strings is sufficient. | NFR3.6, NFR Q1 (A), NFR Q4 (A) | UI test: 101 strings shows the limit message and produces no result columns; 100 strings sorts normally. |

## Budgets and Notes

- **Latency budget:** none numeric. The inherited project answer (NFR Q4 A) sets no end-to-end target; the 100-string hard cap bounds the worst case.
- **Throughput:** not applicable — single interactive user, one run per button press.
- **Resource use:** Streamlit session memory only; no caching, no background workers.
- **Cap enforcement point:** the cap is measured on the de-duplicated shared list built from typed entries plus picked words (functional-spec Part 3), immediately before `normalize`.

## Referenced Upstream

- `functional-spec.md` (this unit) — display decisions Q1–Q4.
- `rules.md` (this unit) — BR2.1 per-algorithm metrics rendering, BR2.2 per-algorithm accuracy rendering.
- `requirements.md` — NFR1, NFR2, NFR3.
- `contract-summary.md` — Contract 1 result types and Contract 2 run interface.
- `technology-stack` — not applicable on this greenfield run (no separate technology-stack artifact exists).
