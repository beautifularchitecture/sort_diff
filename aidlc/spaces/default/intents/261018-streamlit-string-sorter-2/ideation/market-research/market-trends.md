# Market Trends

## Sources

- `ideation/market-research/market-research-questions.md` — Q5: A (no relevant trends or constraints), Q6: A (free, shared as source code or run locally), Q4: B (educators first)
- `ideation/intent-capture/intent-statement.md` — educational/demonstration trigger

## Purpose

Industry signals relevant to a small educational sorting demonstration. The person building this confirmed that no trends or constraints need to shape v1; this document records what was considered and why it was set aside, so the decision is visible rather than assumed.

## Signals Considered

- **Browser-based, no-install expectations**: teaching tools are expected to run in a browser without student setup. Streamlit already delivers this, so it constrains nothing beyond the platform already chosen.
- **Classroom projection norms**: readable output and clear labels when projected in a lesson. This is a quality expectation, not a market trend with a measurable threshold, and v1's simple interface already points at it.
- **Curriculum alignment (first CS course)**: sorting is a standard early-algorithms topic. The three chosen algorithms (bubble, selection, quick) are the canonical taught set, so the app aligns naturally without extra work.
- **Accessibility expectations**: worth revisiting if the app ever leaves a personal/classroom context; not a v1 driver per the person's answer (Q5: none relevant).

## Direction of Travel (informational)

- Algorithm-visualization teaching tools keep moving toward animation and multi-language coverage (the VisuAlgo-class tools). This app deliberately stays a small step-count demonstration rather than chasing that direction.
- No regulatory shifts apply: no personal data, no payments, no student accounts.

## Strategic Read

No trend changes what v1 should be. The confirmed answer (Q5: none relevant — simple local demo) is consistent with the intent statement's scope: a simple Streamlit app, free, run locally, with no accounts or storage. Trends above are recorded for context only and impose no v1 requirements.

## Assumptions & Open Questions

- [assumption] The app stays in a personal/classroom context for v1; if it is deployed for a class later, accessibility and browser-support expectations deserve a fresh look.
- [assumption] No measurable performance or availability targets are market-driven at this stage; success metrics remain those confirmed in intent-capture (accurate sorting, clear step counts and comparisons, intuitive UI).
