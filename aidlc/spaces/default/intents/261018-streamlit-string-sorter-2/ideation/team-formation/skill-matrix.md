# Skill Matrix

## Sources

- `ideation/team-formation/team-formation-questions.md` — confirmed answers Q1–Q5
- `ideation/feasibility/feasibility-assessment.md` — technology comfort (Python + Streamlit both comfortable)
- `ideation/scope-definition/intent-backlog.md` — the work the skills must cover

## Required vs Available

| Skill | Required for | Available? | Source |
|-------|-------------|-----------|--------|
| Python programming | B1 sorting engine, all slices | Yes — builder is comfortable | feasibility Q3: A |
| Streamlit UI | B2–B4 input and display flows | Yes — builder is comfortable | feasibility Q3: A |
| Sorting-algorithm knowledge (bubble, selection, quick) | B1 | Yes — textbook algorithms; AI specialists supply the implementation under the builder's direction | backlog B1 |
| Test design (correctness checking) | B5 accuracy indication | Yes — accuracy check against a reference sort; quality specialist supports test design | backlog B5 |
| Product thinking (scope, prioritization) | Whole initiative | Yes — product specialist led ideation; builder decides at gates | stage record |
| Architecture/design | Later design stages | Yes — architect specialist | stage record |
| CI / deployment | Not required for v1 (local app, no hosting) | Not needed | constraint C11 |

## Gap Analysis

**No blocking gaps.** Every required skill is either held by the builder or supplied by an AI specialist during its stage. The only soft spot: the builder's Streamlit experience is comfortable but not deep (feasibility Q3 said both are comfortable, so this is a note, not a gap) — the design specialist's guidance covers that.

## Remediation Plan

None needed. If the app is later extended (more algorithms, hosting), revisit: deployment/CI skills and possibly deeper Streamlit patterns.

## Assumptions & Open Questions

- [assumption] "Comfortable" with Streamlit (feasibility Q3: A) means able to read and tweak generated Streamlit code, not necessarily author complex layouts unaided.
- [assumption] No certifications, domain expertise, or compliance knowledge are required (feasibility Q2: A — no regulatory surface).
