# Team Assessment

## Sources

- `ideation/team-formation/team-formation-questions.md` — Q1: A (solo builder), Q2: A (human drives, AI specialists build under direction), Q3: A (a few hours as time allows), Q4: A (no other reviewers), Q5: A (recorded defaults fine) (confirmed)
- `ideation/scope-definition/intent-backlog.md` — 5 Must-Have slices (B1–B5)
- `ideation/feasibility/feasibility-assessment.md` — feasible, Python + Streamlit comfortable, no integrations

## Availability

| Member | Role | Capacity |
|--------|------|----------|
| The builder (you) | Solo builder, decision-maker at every gate | A few hours here and there, as time allows |
| AI specialists (product, design, architect, developer, quality, and the rest of the roster) | Design and building work, one specialist leading each stage, under the builder's direction at the gates | On demand, per stage |

No other people, contractors, or external services are involved (Q1: A, Q4: A).

## Capacity Assessment

- Work volume is small: five Must-Have slices for a simple app with no integrations.
- No deadline applies (feasibility Q4: A), so scattered hours are sufficient; nothing needs batching into fixed sessions.
- The main capacity risk is simple: long gaps between sessions slow momentum, not correctness — each stage is self-contained and the workflow record carries the context.

## Skill Gap Analysis

See `skill-matrix.md` for the required-versus-available breakdown. Headline: no gaps that block delivery; the builder is comfortable with both Python and Streamlit (feasibility Q3: A).

## Topology

A single stream-aligned builder (stream: this app) supported by AI specialists on demand — a one-person team with specialists, not a multi-team setup. No platform, enabling, or complicated-subsystem teams apply at this size.

## RACI (light)

| Activity | Responsible | Accountable | Consulted | Informed |
|----------|------------|-------------|-----------|----------|
| Every stage's questions and answers | Builder | Builder | — | — |
| Stage artifacts (design, code, tests) | AI specialist for that stage | Builder (approves at the gate) | — | — |
| Stage approval / scope changes | Builder | Builder | — | — |
| Build and run the app | Developer specialist | Builder | Quality specialist (tests) | — |

## Assumptions & Open Questions

- [assumption] The AI specialist roster available in this workflow covers every stage the plan runs; no external expert is needed.
- [assumption] "A few hours here and there" is enough because the work is small; if the app grows, capacity becomes a real constraint worth revisiting.
- [assumption] No onboarding checklist is needed — there is no one to onboard.
