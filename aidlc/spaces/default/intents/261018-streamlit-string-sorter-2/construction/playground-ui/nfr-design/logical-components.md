# Logical Components — playground-ui (U2)

The playground-ui unit is a single Streamlit process. It owns presentation and orchestration only (ADR-004) and consumes the sorting-core package (U1) in-process. It has no queues, external stores, or backend services.

## Components

| Logical component | Responsibility | Pattern | Notes |
|---|---|---|---|
| SortingPlaygroundApp | Owns the Streamlit page: text area, word-list multiselect, Sort button, shared-list build and de-duplication, 100-string cap, calls to U1, and rendering of the input echo plus three result columns. | Synchronous script, recomputed each rerun (PD-2) | Entry point `app.py` (Contract 2) |
| WordListProvider | Exposes the fixed bundled word list as read-only picker options. | Module-level constant (SD-4) | No I/O, no network |

Consumed (not owned by this unit), from `domain-design/components.md`:

| Consumed component | Used for |
|---|---|
| InputProcessor (`normalize`) | Turn the shared list into a `SortInput` |
| SortingEngine (`run_all`) | Produce three `AlgorithmResult`s |
| AccuracyChecker (`check`) | Produce one `AccuracyCheck` per result |

## Isolation and Blast Radius

- **Single failure domain.** The UI and U1 run in one process; a crash in either ends the Streamlit rerun. There is no partial-service degradation to design for.
- **Error propagation (SD-6).** U1 exceptions are not caught; the enclosing rerun surfaces them as a Streamlit error panel. Nothing is silently swallowed and no state is corrupted because results are recomputed from widgets (PD-2).
- **Shared resources.** None across units — no shared files, caches, connections, or counters. Each rerun rebuilds its own list and receives fresh U1 results.

## Quality Obligations

- NFR4.1: Black, Ruff, snake_case apply to `app.py` and its tests (team code style).
- NFR4.2: pytest unit tests cover the UI wiring; the ~80% line-coverage floor is held for the unit in Build and Test.

## Deployment View

- One entry script, `app.py`, at the repository root; run locally with `streamlit run app.py` (Contract 2).
- Deployed to Streamlit Community Cloud by U3 (delivery-pipeline); this unit contributes no infrastructure of its own.

## Referenced Upstream

- `requirements.md` — NFR2, NFR3.
- `contract-summary.md` — Contracts 1 and 2.
- `functional-spec.md` — Part 2 components and contracts.
