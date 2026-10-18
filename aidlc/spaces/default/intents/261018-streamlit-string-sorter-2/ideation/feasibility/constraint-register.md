# Constraint Register

## Sources

- `ideation/feasibility/feasibility-questions.md` — confirmed answers Q1–Q6
- `ideation/intent-capture/intent-statement.md` — v1 scope boundaries
- `aidlc/spaces/default/memory/org.md` — trunk-based development, squash-merge to `main`, deploy-on-merge to staging with a manual production gate

## Purpose

Every constraint that bounds the initiative, classified by type, with its source and whether it is hard (must hold) or soft (should hold).

## Constraints

| ID | Constraint | Type | Strength | Source |
|----|-----------|------|----------|--------|
| C1 | v1 implements only bubble sort, selection sort, and quick sort | Scope | Hard | intent-capture (Q8: D — advanced algorithms excluded) |
| C2 | No file I/O or persistent storage in v1 | Scope | Hard | intent-capture (Q8: D) |
| C3 | No complex UI styling beyond basic Streamlit | Scope | Hard | intent-capture (Q8: D) |
| C4 | Application is a simple Streamlit app | Technical | Hard | initial description, intent-capture |
| C5 | No personal data, payments, or user accounts | Regulatory | Hard | feasibility Q2: A |
| C6 | No integrations with external systems or data sources | Technical | Hard | feasibility Q1: A |
| C7 | Distribution is free (source code / run locally) | Business | Hard | market-research Q6: A |
| C8 | Work happens on personal time with no fixed deadline | Organizational | Soft | feasibility Q4: A |
| C9 | Trunk-based development; work merges to `main` via short-lived branches, squash-merged | Process | Hard | org rules (team defaults) |
| C10 | Deploy-on-merge to staging; production requires separate human approval | Process | Hard | org rules (team defaults); applies only if/when the app is hosted |
| C11 | Possible future deployment to a small host must not become a v1 requirement | Scope | Soft | feasibility Q6: B |

## Notes

- C1–C3 are deliberate scope boundaries that keep the app classroom-sized; they are the most likely source of tension if the app is later extended.
- C5 and C6 eliminate the usual security/compliance constraint surface for this initiative.
- C10 is recorded for completeness; with no hosting in v1 (C11), it has no effect until a deployment decision is made.

## Assumptions & Open Questions

- [assumption] The org-level process constraints (C9, C10) are the team defaults; no narrower project rule has been affirmed yet.
- [assumption] Nothing in a future host's terms of service restricts a free educational demo — unverified, and only relevant if hosting happens.
