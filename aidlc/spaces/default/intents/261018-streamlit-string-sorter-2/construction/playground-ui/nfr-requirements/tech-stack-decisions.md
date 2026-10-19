# Tech Stack Decisions — playground-ui (U2)

Consumes `functional-spec.md`, `rules.md`, `requirements.md`, and `contract-summary.md`.

## Decisions

| Area | Decision | Rationale | Source |
|---|---|---|---|
| Language | Python 3.12 | Inherited from U1 NFR Q6 (C); matches the CI target in contract-summary. | NFR Q6 (C), contract-summary (open question) |
| UI framework | Streamlit | Single-page interactive app; declared as the runtime dependency in `requirements.txt` (Contract 2). | ADR-004, functional-spec Part 2 |
| Streamlit pinning | Minimum version range, `streamlit>=1.40` | Matches the project's minimum-version range strategy (U1 NFR Q6 C); allows patch updates. | NFR Q2 (A) |
| Dependency declaration | UI deps in `requirements.txt`; sorting-core adds no runtime dependency | Contract 2; U2 owns `requirements.txt`. | contract-summary Contract 2 |
| Entry point / run | `app.py`; local run `streamlit run app.py` | Contract 2 build-and-run interface. | contract-summary Contract 2 |
| Test framework | pytest | Team testing posture. | team.md, NFR4.2 |
| Formatter and linter | Black and Ruff | Team code style. | team.md Code Style, NFR4.1 |
| Naming | snake_case modules, functions, and variables | Team code style. | team.md, NFR4.1 |

## Notes

- NFR4.1 (Black, Ruff, snake_case) and NFR4.2 (pytest, ≥80% line coverage) apply to this unit's UI code exactly as they do to `sorting-core`; the coverage floor is held in Build and Test.
- The Streamlit version range resolves the UI half of the open Contract 2 question; the Python version was already resolved by U1.
- The bundled word list is a source-level constant (no data file), so the UI adds no data dependency.

## Referenced Upstream

- `functional-spec.md` (this unit) — Part 2 components.
- `rules.md` (this unit) — UI behavior rules.
- `requirements.md` — NFR3.5 (free), NFR4.
- `contract-summary.md` — Contract 2.
- `technology-stack` — not applicable on this greenfield run.
