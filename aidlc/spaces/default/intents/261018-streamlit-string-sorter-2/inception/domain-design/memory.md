# Domain Design — Observation Diary

## Interpretations

- The stage asks for logical building blocks (code I write), not infrastructure. Streamlit is recorded as the only external dependency, and the standard-library `sorted()` is noted as a reference, not a dependency.
- Story-level traceability (the stage uses `stories.md` when it exists) maps US1.1–US4.2 to components. US5.x has no component surface and is recorded as Deferred to the stage that owns it.
- Entity capture stays at ownership and shape level (identifier and attribute names). Types and validation are deferred to Functional Design.

## Deviations

- Traceability uses story IDs rather than FR IDs because `stories.md` exists, as the stage definition requires.
- Four ADRs rather than one: each significant choice (decomposition, algorithm grouping, accuracy separation, thin UI) has its own context and rejected alternatives.

## Tradeoffs

- Recommended Option A (five components) over Option B (inline word list) and Option C (single module). The cost is one more component in exchange for an explicit owner of the FR1.5 bundled-list contract and a cleaner split of verification from sorting.
- Chose synchronous in-process calls over any async or event style. A single button press drives one request cycle on classroom-sized input, so events would add machinery with no benefit.

## Open questions

- The component-boundary choice (Option A) is the gated decision. It is recorded with its recommendation and goes to the human at summary confirmation and the completion gate.
- Exact bundled word list contents remain a Code Generation detail, as previously recorded.
