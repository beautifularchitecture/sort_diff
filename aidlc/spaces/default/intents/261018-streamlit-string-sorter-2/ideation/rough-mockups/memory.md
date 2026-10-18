<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->

## Tradeoffs
- 2026-10-18T03:43:03Z — merged typed and picked strings into one shared input list feeding one Sort run; keeps the flow single-path (input → sort → side-by-side) instead of two separate sort triggers.

## Open questions
- 2026-10-18T03:43:03Z — string comparison rule (case sensitivity, whitespace trimming on pasted lines) left for design; all three columns must use the same rule or accuracy checks disagree across algorithms.
- 2026-10-18T03:43:03Z — accuracy indication wording ("Accuracy: OK" placeholder in the sketch) is cosmetic; exact wording not fixed yet.
