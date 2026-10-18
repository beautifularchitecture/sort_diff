# RAID Log

## Sources

- `ideation/feasibility/feasibility-assessment.md` — risk analysis and viability verdict
- `ideation/feasibility/constraint-register.md` — constraint IDs referenced below
- `ideation/feasibility/feasibility-questions.md` — confirmed answers Q1–Q6

## Risks

| ID | Risk | Likelihood | Impact | Response |
|----|------|-----------|--------|----------|
| R1 | An algorithm is implemented incorrectly | Low | Medium | Accuracy check against a trusted reference sort (Python's built-in sorted) flags failures automatically |
| R2 | Scope creep beyond the three algorithms / storage / styling (C1–C3) | Medium | Medium | Constraint register marks these hard; revisit only through an explicit scope change |
| R3 | "Step" definition differs between algorithms, making comparisons confusing | Low | Medium | Decide the step-counting convention once during design and apply it consistently |
| R4 | Future small-host deployment (Q6: B) distracts from v1 | Low | Low | C11 records it as out of v1; hosting is a later decision |

## Assumptions

| ID | Assumption | Validation if it matters later |
|----|-----------|-------------------------------|
| A1 | Inputs are classroom-sized (tens to low hundreds of strings) | Revisit only if someone wants to sort large lists |
| A2 | Python and Streamlit can be installed locally (Q1, Q3) | Confirmed by the builder's own environment |
| A3 | No institution-level privacy or accessibility rules apply (Q2: A) | Re-check if the app is adopted by a school formally |
| A4 | Free local distribution is acceptable to all intended users (Q6: A) | Re-check if a class needs shared hosted access |

## Issues

None open. No blocking problems have been raised at this stage.

## Dependencies

| ID | Dependency | Type | Notes |
|----|-----------|------|-------|
| D1 | Python 3 runtime | Technical | Assumed present in the execution environment |
| D2 | Streamlit package | Technical | Installed locally; no version pin chosen yet |
| D3 | A trusted reference sort for accuracy checking | Technical | Python's standard library sorted() serves this |

## Assumptions & Open Questions

- [assumption] Nothing in this log blocks the initiative; the feasibility verdict is "feasible" with only low-likelihood risks.
- [assumption] Step-counting definition (R3) is deferred to design rather than resolved here — it is a design decision, not a feasibility blocker.
