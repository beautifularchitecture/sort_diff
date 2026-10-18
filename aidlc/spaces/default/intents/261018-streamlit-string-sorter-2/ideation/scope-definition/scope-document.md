# Scope Document

## Sources

- `ideation/scope-definition/scope-definition-questions.md` — Q1: A (MVP = the app as described), Q2: A (side-by-side results), Q3: A (both input methods), Q4: A (value-first sequencing), Q5: A (no extra exclusions) (confirmed)
- `ideation/intent-capture/intent-statement.md` — problem statement, target customer, success metrics
- `ideation/feasibility/constraint-register.md` — C1–C11
- `ideation/feasibility/feasibility-assessment.md` — feasibility verdict and risk analysis

## In Scope (v1)

The minimum viable version is the application exactly as described, with these capabilities:

1. **String input** — both manual entry by the user and selection from a provided word list in the UI (Q3: A).
2. **Sorting on request** — a button runs the chosen input through the sorting algorithms.
3. **Three algorithms** — bubble sort, selection sort, and quick sort, written specifically for this app (C1; build-vs-buy decision).
4. **Accuracy checking** — each algorithm's result is verified against a trusted reference sort, and correctness is shown (intent success metric).
5. **Step counts** — the number of steps each algorithm took is tracked and displayed (intent success metric).
6. **Side-by-side results** — all three algorithms run on the same input and their results and step counts are displayed together for direct comparison (Q2: A).

## Out of Scope (v1)

| Excluded | Constraint |
|----------|-----------|
| Algorithms beyond bubble, selection, and quick | C1 |
| File I/O or persistent storage | C2 |
| Complex UI styling beyond basic Streamlit | C3 |
| Personal data, payments, user accounts | C5 |
| Integrations with external systems or data sources | C6 |
| Any cost to users (free distribution only) | C7 |
| Hosting requirements (local now; a small host is a later possibility only) | C11 |

Confirmed complete: no further exclusions beyond the above (Q5: A).

## Success Criteria (from intent-capture)

- Accurate sorting results for all inputs, verified by the accuracy check
- Clear display of step counts and comparisons
- Intuitive, simple UI

## Sequencing Preference

Value-first (Q4: A): build the slice that takes input, sorts it, and shows results with step counts as early as possible; the three-algorithm comparison falls out of that same slice since Q2 makes side-by-side the delivery shape.

## Scope-vs-Timeline Check

No deadline applies (feasibility Q4: A), so no capability is pulled forward or cut for time. The scope is bounded by the constraints and the MVP definition alone.

## Assumptions & Open Questions

- [assumption] "Steps" will be defined consistently across the three algorithms in design; the scope requires comparable counts but does not define the counting convention.
- [assumption] The provided word list is bundled with the app (no external data source, per C6).
- [assumption] Classroom-sized inputs (feasibility A1) — no large-input mode is in scope.
