## Sources

- [desc] Initial description: simple Streamlit app — strings entered or picked from a list, sorted by bubble/selection/quick sort, with accuracy and step counts shown.
- [scope] Workflow-selected scope: `feature`.
- [memory:M1] `memory/org.md` — Way of Working, Walking Skeleton, Testing Posture, Deployment, and Code Style defaults. This is a new project, so these are suggestions to confirm, not practices already in place.

## Q1. How should changes land in the code?

The repo is empty today, so this is about the everyday habit from here on.

[Answer]:A

A. A short-lived branch off `main`, squash-merged into `main` within a day or two — the org default
B. Commit straight to `main`
C. Longer-lived feature branches, merged when the feature is finished
X. Other (please specify)

## Q2. Build a thin end-to-end slice first? A walking skeleton is a minimal version that runs the whole way through, built first to prove the pieces connect before the real features go in.

[Answer]:B

A. Yes — build the thin end-to-end slice first
B. No — go straight at the three sorting algorithms and the UI
X. Other (please specify)

## Q3. How should tests fit in?

[Answer]:A

A. Tests after each piece is implemented — pytest, with roughly 80% line coverage on the sorting logic (the org default for this scope)
B. Tests written first, then the code (test-driven)
C. Behaviour scenarios agreed first, then the code (BDD)
D. No automated tests for now — manual checks only
X. Other (please specify)

## Q4. How should the app be deployed?

[Answer]:B

A. Deploy to staging on merge; production needs a separate manual approval — the org default
B. Deploy to production automatically on every merge
C. No deployment pipeline for now — it runs locally
X. Other (please specify)

## Q5. What code style should we hold to?

[Answer]:A

A. Python defaults — Black formatter, Ruff linter, snake_case (the org default)
B. No formatter or linter config for now — plain Python
X. Other (please specify)

## Consolidated Summary Confirmation

Does this all look correct before I finalize the practices artifact?

- Looks correct
- Request changes

[Answer]: Looks correct

## Assumption Confirmation

Two assumptions went into these questions — confirm how to treat them:

1. [assumption] "The org default" means the framework's shipped defaults in `memory/org.md`; this project has no team practices of its own yet.
2. [assumption] No deployment target is named yet (Streamlit Cloud, container, or internal hosting) — it stays open for Requirements Analysis.

A. Accept assumptions
B. Convert to follow-up questions

[Answer]: A. Accept assumptions
