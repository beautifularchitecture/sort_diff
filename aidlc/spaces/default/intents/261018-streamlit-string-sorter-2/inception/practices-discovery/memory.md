<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->
- 2026-10-18T08:17:54Z — Ordinary interview answers were refused by `log answer` while the consolidated summary checkpoint decision was the stage's latest decision; they were accepted once ordinary decisions (the learnings questions) were recorded after it. Record the interview answers before the summary checkpoint, or expect to re-log them after. The `[Answer]:` lines in practices-discovery-questions.md remain the source of truth for Q1-Q5 and the assumption confirmation.
- 2026-10-18T08:17:54Z — Q4 (deploy to production automatically on every merge) was recorded as the team's affirmed practice. The human's explicit choice steps past the org default of staging-on-merge with a manual production approval, which org.md itself frames as a team decision rather than a guardrail.

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->
- 2026-10-18T08:17:54Z — The interview asked only the five declared practice areas. The evidence draft's extra uncertainties (deployment target, step-count definition, word-list source) were not turned into questions; they were left to Requirements Analysis, on the strength of the Say Hello pace feedback.

## Tradeoffs
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->
- 2026-10-18T08:17:54Z — Org-derived draft rules ("never hardcode secrets", "handle exceptions at the UI/backend boundary") were dropped from discovered-rules.md. The stage contract admits only human-stated hard constraints, so those stay org defaults instead of being promoted to project rules.
- 2026-10-18T08:17:54Z — Ran lead-only (collaborators off): the draft had no independent spoke review, so the only check on it was the human interview.

## Open questions
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->
- 2026-10-18T08:17:54Z — No deployment target is named yet (Streamlit Cloud, container, or internal hosting); confirm before the deployment pipeline is designed.
