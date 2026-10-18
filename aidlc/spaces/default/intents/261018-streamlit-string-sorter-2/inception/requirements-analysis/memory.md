<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->
- 2026-10-18T09:31:09Z — read Q5's "Other" answer as an input-normalization rule (lowercase conversion plus a stated allowed charset), not as a hard input filter; the human's words "even if you encounter capital you make is small" describe transformation, so FR1.3 states normalize-then-sort and the allowed set as what the app accepts after normalization.
- 2026-10-18T09:31:09Z — reconciled Q2 (textbook loop iterations) with Q3 (total element comparisons as the comparable metric) by making both explicit in FR4: each algorithm counts textbook steps, and the displayed comparable number is element comparisons; the human's two answers could not both be a single count.

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->
- 2026-10-18T09:31:09Z — recorded the advisory review receipt after the reviewer sub-agent returned its review in text but did not write the review file; the orchestrator wrote the review file verbatim from the sub-agent's response so the engine's verdict command could bind it, rather than re-dispatching the reviewer for a file write.

## Tradeoffs
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->
- 2026-10-18T09:31:09Z — kept FR4.1 and FR4.2 as separate requirements (textbook steps vs comparable comparisons) instead of collapsing them into one definition; a single merged definition would have silently dropped one of the human's two answers, and the advisory reviewer flagged the split as a minor clarity note rather than an error.

## Open questions
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->
- 2026-10-18T09:31:09Z — advisory reviewer flagged FR1.3's allowed-charset wording as possibly read as reject-vs-normalize, and FR4's two-count split as underspecified; both were judged minor at review and left for design-stage clarification rather than a requirements revision.
