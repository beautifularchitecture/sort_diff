# Domain Design — Questions & Design Decisions

## Sources

- `inception/requirements-analysis/requirements.md` (FR1–FR7, NFR1–NFR4)
- `inception/user-stories/stories.md` (US1.1–US5.2)
- `inception/refined-mockups/` artifacts (single-screen Streamlit UI, D1–D10)
- Human instruction: full autopilot for this workflow

## Design Decisions (made under full autopilot; human confirms at summary confirmation)

### D1. Component boundary decomposition

Presented three viable decompositions (full trade-off table in `components.md` Rationale and ADR-001):

- **Option A — five components** (recommended): `SortingPlaygroundApp` (UI/orchestration) + four domain components `InputProcessor`, `SortingEngine`, `AccuracyChecker`, `WordListProvider`. Pros: each FR family has one owner; domain logic pytest-testable without a Streamlit runtime; bundled-list contract (FR1.5) has an explicit home. Cons: five components is the upper bound of right-sizing for this app. Reversibility: high — components are modules, not services.
- **Option B — four components**: same as A but the bundled word list is a constant inside `SortingPlaygroundApp` (no `WordListProvider`). Pros: one less component. Cons: the FR1.5 contract (fixed, shipped, non-empty, no external fetch) has no owning component and no independent test surface.
- **Option C — single domain module**: one `SortDomain` component owning parsing, all three algorithms, and verification. Pros: minimal ceremony. Cons: mixes three distinct concerns and change rates; the ~80% sorting-coverage floor and the accuracy contract are harder to bound.

**Recommendation: Option A** — chosen. Every FR family maps to exactly one owner, and entity ownership stays unambiguous. The team confirms or overrides at the gate.

### D2. Algorithm grouping

All three algorithms live in one `SortingEngine` behind a shared result contract (algorithm name, sorted list, comparisons, swaps), not one component per algorithm. Rationale: FR2.5 requires the same input for all three in one run; they share the comparison-counting definition (FR4.2); three components for three functions would be ceremony over a shared contract. Recorded as ADR-002.

### D3. Accuracy as a separate component

`AccuracyChecker` is its own component, not folded into `SortingEngine` or the UI. Rationale: verification against Python `sorted()` (FR3) is a distinct concern with a distinct change rate from the sorting implementations; separating it keeps algorithm tests and verification tests independent and makes the pass/fail contract explicit. Recorded as ADR-003.

### D4. UI as thin orchestrator

`SortingPlaygroundApp` holds no business logic: on Sort press it orchestrates normalize → sort-all-three → verify → render, and renders the exact FR6.1 warning on an empty shared list. Rationale: the team testing posture (pytest, ~80% on sorting logic) requires the domain to run without a Streamlit runtime. Recorded as ADR-004.

### D5. Entity ownership

Exactly one owner per entity (ownership + shape only; full schema belongs to Functional Design):

| Entity | Owner | Identifier | Attributes (names only) |
|--------|-------|------------|-------------------------|
| SortInput | InputProcessor | run_id | run_id, raw_entries, normalized_strings |
| AlgorithmResult | SortingEngine | run_id + algorithm | run_id, algorithm, sorted_strings, comparisons, swaps |
| AccuracyCheck | AccuracyChecker | run_id + algorithm | run_id, algorithm, passed |
| BundledWordList | WordListProvider | list_version | words |

Cross-component references: `AlgorithmResult → SortInput` (each result derived from one input); `AccuracyCheck → AlgorithmResult` (each check verifies one result).

### D6. Interaction style

All component interactions are synchronous in-process calls, driven by the Sort button (no async, no events — classroom-sized inputs, single request/response cycle). The dependency graph is acyclic: the UI calls the four domain components; no domain component calls another (results flow as arguments through the UI orchestrator).

## Ambiguity Analysis

No vague language, contradictions, or missing details after D1–D6. The component-boundary choice (D1) is the one gated decision; the recommendation proceeds under autopilot and is flagged in the summary confirmation. Proceeding to artifact generation.

## Consolidated Summary Confirmation

Here is the combined summary of this stage's decisions. Please confirm it.

**Decomposition (Option A, 5 components)**: `SortingPlaygroundApp` (thin Streamlit UI/orchestrator) + `InputProcessor` (normalize typed+picked entries), `SortingEngine` (bubble/selection/quick with shared comparison+swap counting), `AccuracyChecker` (pass/fail vs Python `sorted()`), `WordListProvider` (fixed bundled list, FR1.5).

**Entities (4, one owner each)**: SortInput → InputProcessor; AlgorithmResult → SortingEngine; AccuracyCheck → AccuracyChecker; BundledWordList → WordListProvider. Cross-references: results → input; checks → results.

**Interactions**: all sync in-process; UI orchestrates the button-press pipeline; domain components never call each other; acyclic graph.

**ADRs**: ADR-001 decomposition (alternatives B/C rejected with rationale); ADR-002 one SortingEngine for all three algorithms; ADR-003 separate AccuracyChecker; ADR-004 thin UI for pytest-testable domain.

**Traceability**: US1.1–US4.2 all map to components (OK); US5.1 deferred to build-and-test, US5.2 deferred to deployment-pipeline.

[Answer]: Looks correct
