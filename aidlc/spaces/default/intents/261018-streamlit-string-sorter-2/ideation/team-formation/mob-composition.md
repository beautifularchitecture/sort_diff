# Mob Composition

## Sources

- `ideation/team-formation/team-formation-questions.md` — Q1: A (solo), Q2: A (builder drives, AI specialists build under direction), Q4: A (builder decides alone at gates)
- `ideation/scope-definition/intent-backlog.md` — slices B1–B5 and value-first sequencing

## Working Model

There is no human mob to compose: one builder works with AI specialists, one leading each stage, and the builder decides at every gate (Q2: A, Q4: A). The composition below maps who does what, in the spirit of mob roles — whoever is "at the keyboard" for a stage is the driver; the builder is always a navigator and the decision-maker.

## Role Mapping

| Role | Who | Notes |
|------|-----|-------|
| Driver (per stage) | The AI specialist leading that stage | Types the artifacts and code for the stage |
| Navigator | The builder | Directs, answers the stage's questions, decides at gates |
| Second navigator (optional) | Reviewer specialist, where a stage configures one | Spots issues before the gate; advisory only |

## Per-Slice Composition

| Slice | Lead specialist | Builder's involvement |
|-------|----------------|----------------------|
| B1 Sorting engine (bubble, selection, quick, step counts, accuracy) | Developer | Answers design questions; approves at the gate |
| B2 Sort-and-display flow (side-by-side results) | Developer (with design input) | Approves the display shape at the gate |
| B3 Manual string entry | Developer | Confirms input behavior at the gate |
| B4 Word-list selection | Developer | Confirms the bundled word list at the gate |
| B5 Accuracy indication | Quality | Approves how correctness is shown |

## Session Norms

- Work happens in short sessions as time allows (Q3: A); each stage picks up from the written workflow record, so gaps between sessions cost nothing in context.
- Every artifact the AI specialists produce is reviewed and approved by the builder at the stage gate before the next stage starts (Q4: A — no other reviewers).
- No rotation cadence, standups, or syncs: unnecessary ceremony for a solo builder (Q5: A — recorded defaults are fine).

## Assumptions & Open Questions

- [assumption] The value-first build order from the backlog (B1 → B2 → B3/B4 → B5) is how Construction will batch the work; the delivery-planning stage will confirm the exact batching.
- [assumption] "Under my direction" (Q2: A) means the builder answers each stage's questions and approves its output — not that the builder writes the code personally.
