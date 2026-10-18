# Feasibility Assessment

## Sources

- `ideation/feasibility/feasibility-questions.md` — Q1: A (no integrations), Q2: A (no compliance), Q3: A (skills comfortable), Q4: A (no budget/deadline), Q5: A (no blockers), Q6: B (local now, maybe small host later) (confirmed)
- `ideation/intent-capture/intent-statement.md` — problem statement, target customer, success metrics, v1 scope
- `ideation/market-research/build-vs-buy.md` — build-from-scratch decision
- `ideation/market-research/competitive-analysis.md` — positioning as a free classroom aid

## Verdict

**Feasible.** The initiative is a small, standalone Streamlit application with no integrations, no user data, no accounts, and no regulatory exposure. The team is comfortable with the required technology, has no deadline, and faces no organizational blockers. The main risks are correctness of the sorting logic and the scope discipline to keep v1 small — both are low-risk and controllable.

## Technical Viability

| Aspect | Assessment |
|--------|------------|
| Core capability | Three well-understood sorting algorithms (bubble, selection, quick) on string data; each is textbook material with known step/comparison behavior |
| Accuracy checking | Comparing algorithm output against a trusted reference sort (e.g. Python's built-in sorted) is straightforward and cheap for classroom-sized inputs |
| Step counting | Requires instrumenting each algorithm as it runs — the reason the algorithms are written by hand rather than called from a library (see build-vs-buy) |
| User interface | Streamlit supplies the web UI, input widgets, and result display; no frontend expertise needed |
| Distribution | Free, shared as source code or run locally; a later small-host deployment is possible but not required for v1 |

## Risk Analysis

| Risk | Likelihood | Impact | Notes |
|------|-----------|--------|-------|
| Incorrect algorithm implementation | Low | Medium | Each algorithm is simple; accuracy checking against a reference sort catches errors automatically |
| Scope creep (extra algorithms, storage, styling) | Medium | Medium | Explicitly excluded in intent-capture; the constraint register records this as a deliberate boundary |
| Step counts hard to define consistently across algorithms | Low | Medium | A definitional decision (what counts as a "step") must be made once in design; educational tools commonly count comparisons/swaps/pass executions |
| Future small-host deployment exposes the app more widely | Low | Low | No user data to leak; risk is cosmetic (uptime of a free demo) |
| Quick sort performance on adversarial input | Low | Low | Classroom-sized inputs make worst-case behavior a non-issue |

## Dependencies

- Python 3 and Streamlit available in the execution environment (already assumed by the chosen platform).
- A trusted reference sort for accuracy checking (Python's standard library provides one).
- No external services, APIs, databases, or third-party accounts.

## What This Assessment Does Not Cover

- Detailed architecture, data models, or interface design — those belong to later design stages.
- Non-functional targets (performance numbers, availability) — none are market-driven at this stage; any needed targets are set in the non-functional requirements stages.

## Assumptions & Open Questions

- [assumption] Classroom-sized inputs (tens to low hundreds of strings); no large-dataset performance claim is being made.
- [assumption] "Deployed to a small host later" (Q6: B) is a possibility, not a v1 requirement; nothing in v1 is designed around hosting.
- [assumption] The builder can install Python packages locally (Streamlit), which Q1: A and Q3: A take as given.
