# User Stories — Observation Diary

## Interpretations

<!-- HTML comments carry the protocol's illustrative shape; real entries follow. -->

- Interpreted "full autopilot" (human directive, this session) as covering mid-stage story-plan questions: requirements analysis already answered every product question, so the plan proceeds directly to generation and the human reviews the combined output at the completion gate. Approval gates and summary confirmation remain human stops (the engine enforces this regardless of Guard Policy).
- Interpreted step-count semantics (FR4) as: total element comparisons is the primary comparable metric across all three algorithms; swap counts are a separate complementary display. This matches the accepted assumptions in requirements.md and avoids inventing a second counting scheme.
- Interpreted "side-by-side" (FR5.2) as a single results view showing all three algorithm columns plus the input — one screen, no navigation, matching NFR2 simplicity.

## Deviations

- Story US5.1 (local run) prioritized as Should Have even though FR7.1 is a functional requirement — MoSCoW ranking here is about user-facing value ordering for the MVP boundary discussion at Delivery Planning, not about dropping the requirement; the traceability row for FR7 still points at US5.1 and US5.2 with status OK.
- No mob round dispatched: the directive's effective support_agents is empty (collaborators off for this scope), so the stage runs lead-only per the ensemble protocol; no contribution files are owed.

## Tradeoffs

- Chose breakdown by feature area (mapping 1:1 to FR groups) over breakdown by persona: the app has one screen and the personas share the same journey, so persona-based splitting would produce overlapping stories with duplicated acceptance criteria.
- Kept accuracy (FR3) and step counting (FR4) inside a single story (US3.2) rather than splitting them: they are displayed in the same result panel and share the "compare against reference / comparable metric" theme; splitting would create two tightly coupled small stories instead of one honest Small story.
- Accepted mild INVEST tension on US3.1/US3.2/US4.2 ("depends on US2.1 at runtime"): these stories are independently buildable and testable with synthetic algorithm outputs; the runtime dependency is documented rather than hidden.

## Open questions

- None carried into the gate; all requirements-level questions were answered in requirements-analysis, and this stage surfaced no new ambiguities.
