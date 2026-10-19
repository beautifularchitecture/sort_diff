# Functional Design — playground-ui (U2)

Single-page Streamlit application that renders input, runs all three sorting algorithms via sorting-core (U1), and displays the three results side by side with metrics and accuracy per algorithm.

## Part 1: Purpose and Scope

This unit owns the presentation and orchestration layer only (ADR-004): Streamlit widgets, the Sort trigger, the FR6.1 empty-input guard, the bundled word-list picker, and rendering. Sorting-core owns normalization, sorting, counting, and verification. playground-ui holds no sorting, normalization, or verification logic of its own.

Scope per `unit-of-work.md` (U2) and `unit-of-work-story-map.md` (U2 carries US1.1, US1.2, US3.1, US3.2, US4.1, US5.1): text area, multiselect, Sort button, input echo, three result columns, empty-state hint; bundled word list as read-only picker options; local run via `streamlit run`; deployed by U3. Behavior is bounded by `requirements.md` (FR1–FR7, NFR1–NFR4).

## Part 2: Components and Contracts

Component catalogue from domain-design/components.md:

- `SortingPlaygroundApp` — wires Streamlit widgets to domain components. Calls InputProcessor.normalize once per Sort press with typed entries plus picked words; runs SortingEngine.run_all on the same SortInput; calls AccuracyChecker.check per AlgorithmResult; renders input echo and three result columns.
- `WordListProvider` — exposes the fixed bundled word list as read-only picker options (FR1.5, AC1.2.1–AC1.2.3). No network access or file I/O at runtime.

Contracts from contract-design/contract-summary.md:

- Contract 1 (sorting-core API, U1 → U2): `normalize(entries) → SortInput`, `run_all(sort_input) → list[AlgorithmResult]` (exactly three, order [bubble, selection, quick]), `check(result, sort_input) → AccuracyCheck`. Boundaries: `TypeError` when entries is not a list of strings; `ValueError` on run_id mismatch; no other exceptions cross the boundary.
- Contract 2 (app packaging, U2 → U3): entrypoint `app.py`; dependencies `requirements.txt` (declares streamlit; owned by U2); local run `streamlit run app.py`; test/lint/format commands as written.

External dependencies: Streamlit (UI framework runtime). Python's `sorted()` is standard library, used by U1's AccuracyChecker as the reference; not an external dependency.

## Part 3: Shared List Construction

The shared list is the input passed to U1. It is built from two sources:

- Typed entries: everything the user types or pastes into the text area (US1.1, AC1.1.1–AC1.1.4).
- Picked words: words selected from the bundled word-list multiselect (US1.2, AC1.2.1–AC1.2.3).

Per Q2 (Option C), typed entries and picked words are combined and de-duplicated before sorting, so the same string entered twice (typed and picked) sorts once. Picked words are treated as the input list for all three algorithms (AC1.2.2). The bundled list itself is read-only and shipped with the app (AC1.2.3).

## Part 4: Sort Trigger and Empty Input (Q1)

On Sort press:

1. Build the shared list from typed entries and picked words.
2. If the shared list is empty, render the exact FR6.1 message `Enter or select at least one string`, do not run any algorithm, produce no result panels, and hide the three algorithm columns (Q1, Option A).
3. Otherwise, call InputProcessor.normalize(shared_list) → SortInput, then SortingEngine.run_all(sort_input), then AccuracyChecker.check per result, and render.

The empty-state hint is shown only when nothing has been entered yet (before the first Sort press); after Sort with empty input, the FR6.1 warning replaces it (US4.1, AC4.1.1–AC4.1.2).

## Part 5: Result Panels (Q3, Q4)

When input is non-empty, render the input echo and three result columns side by side (US3.1, AC3.1.1–AC3.1.3). Each column shows:

- algorithm name (bubble sort, selection sort, quick sort)
- the sorted list
- `Comparisons: N` on its own line under the column heading (Q3, Option A)
- `Swaps: N` on its own line under the column heading (Q3, Option A)
- `Accuracy: pass` or `Accuracy: fail` (Q4, Option A)

Counts are displayed as full integers with no truncation (AC3.2.5). The comparison definition is shared across all three algorithms so numbers are directly comparable (AC3.2.1). Each algorithm is verified independently (AC3.2.4, US4.2).

## Part 6: Edge Cases

- Single string input: returned as the sorted result with minimal/zero step counts; accuracy passes (US4.2, AC4.2.1).
- All-identical strings: same list returned correctly; counts recorded correctly; accuracy passes for all three algorithms (US4.2, AC4.2.2).
- Empty tokens after parsing: dropped by U1's normalization; do not corrupt the sorted output (FR6.4, AC4.2.3).

## Part 7: Data Flow

```
user input + bundled-word picks  →  SortingPlaygroundApp
                                      │
                                      +-- normalize() ──→ InputProcessor ──→ SortInput
                                      │                                   │
                                      ←────── SortInput ──────────────────┘
                                      │
                                      +-- run_all() ─────────→ SortingEngine ──→ AlgorithmResult ×3
                                      │                                   │
                                      ←──── AlgorithmResult ×3 ───────────┘
                                      │
                                      +-- check() ×3 ────────→ AccuracyChecker ──→ AccuracyCheck ×3
                                      │                                   │
                                      ←──── AccuracyCheck ×3 ─────────────┘
                                      │
                                    [Render: input echo + 3 columns]
```

Text fallback: SortingPlaygroundApp collects typed entries and picked words into one shared list, builds a SortInput through InputProcessor, runs all three algorithms through SortingEngine on the same SortInput, verifies each AlgorithmResult through AccuracyChecker, then renders the input echo and three result columns.

## Part 8: Traceability

All U1 behavior (normalization, sorting, counting, accuracy) is implemented in sorting-core and covered by functional-design artifacts there. playground-ui's functional design covers the UI surface: combined input (Q2), empty-input guard (Q1), per-algorithm metrics display (Q3), accuracy display (Q4), local run (US5.1), and continuous deployment (US5.2). Acceptance criteria for U2's stories are listed in user-stories/stories.md (US1.1, US1.2, US2.1, US3.1, US3.2, US4.1, US4.2, US5.1, US5.2); implementation lives in `app.py` under the repository root.

## Open Questions

None — Q1–Q4 answered; Contract 2's Python-version/pin question remains open for U3 delivery-pipeline (not blocking this unit).
