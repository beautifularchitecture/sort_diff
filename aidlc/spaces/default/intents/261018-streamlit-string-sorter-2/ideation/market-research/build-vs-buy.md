# Build vs Buy vs Borrow

## Sources

- `ideation/market-research/market-research-questions.md` — Q3: A (build from scratch), Q1: A (closest comparisons are free visualization sites), Q6: A (free, shared as source code or run locally)
- `ideation/intent-capture/intent-statement.md` — simple Streamlit app, three string sorting algorithms, step counts, accuracy checking

## Purpose

Whether to build this app, buy something ready-made, or borrow an existing open-source implementation. The person building this chose to build from scratch for full control on a small app (Q3).

## Options Considered

### Build from scratch — chosen

- **What it means**: implement bubble sort, selection sort, and quick sort for strings, with step counting and accuracy checking, as a small Streamlit app written by hand.
- **Why it wins**: the app is small and the requirements are precise (three algorithms, step counts, accuracy checks, manual or word-list input). Full control over the exact demonstration behavior an educator needs; no licence questions; no unfamiliar code to adapt.
- **Cost**: the algorithm logic and UI are small enough that the build is measured in hours, not weeks. This is the main reason the option is affordable.

### Fork or borrow an open-source Streamlit/sorting demo — not chosen

- **What it means**: start from an existing demo and adapt it.
- **Why not**: candidate demos vary in quality and maintenance, and typically cover one algorithm or omit accuracy checking and step counts. Adapting someone else's structure can cost more than writing the small amount of code this needs, and leaves the result shaped by someone else's choices.

### Use an existing Python library for the algorithm logic — not chosen

- **What it means**: call library implementations instead of writing the three algorithms.
- **Why not**: the point of the app is to demonstrate how the algorithms behave step by step and count those steps. Library implementations do not expose their inner steps, so the educational core of the app would still need hand-written logic.

### Buy or license a ready-made teaching tool — not chosen

- **What it means**: license a commercial edtech product that teaches sorting.
- **Why not**: heavy and paid for a short in-lesson demonstration; the alternatives (VisuAlgo, Python Tutor, course platforms) are free or institutional purchases that do not give this educator the small, ownable tool being built.

## Decision

**Build from scratch.** The app's value is its simplicity, exact step-count demonstration, and being free and under the builder's control. No buy option fits a free personal/classroom aid, and no borrow option saves meaningful effort for the specific behavior required.

## Assumptions & Open Questions

- [assumption] No existing open-source demo was formally surveyed or scored; the borrow option was rejected on general grounds (quality variance, missing step counts and accuracy checks), not on a shortlist.
- [assumption] "Full control" is worth the build cost because the app is small; this holds as long as v1 stays limited to the three algorithms and simple Streamlit UI confirmed in intent-capture.
