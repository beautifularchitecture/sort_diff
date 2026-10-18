# Intent Backlog

## Sources

- `ideation/scope-definition/scope-document.md` — in-scope capabilities and sequencing preference (value-first)
- `ideation/scope-definition/scope-definition-questions.md` — confirmed answers Q1–Q5
- `ideation/feasibility/constraint-register.md` — hard constraints C1–C3

## Purpose

A prioritized list of capability slices (proto-Units) for the next phases to elaborate. Order reflects the value-first sequencing choice (Q4: A); priority uses MoSCoW against the v1 MVP definition.

## Backlog

| # | Slice | MoSCoW | Depends on | Value |
|---|-------|--------|------------|-------|
| B1 | Core sorting engine — bubble, selection, and quick sort for lists of strings, each reporting its step count, with accuracy checked against a reference sort | Must Have | — | The educational core: correct algorithms with comparable step counts |
| B2 | Sort-and-display flow — input a list, press the button, see each algorithm's sorted output side by side with its step count | Must Have | B1 | The first end-to-end useful slice (value-first sequencing) |
| B3 | Manual string entry — the user types or pastes the strings to sort | Must Have | B2 | One of the two confirmed input methods (Q3: A) |
| B4 | Word-list selection — a bundled list of words in the UI the user can pick strings from | Must Have | B2 | The second confirmed input method (Q3: A) |
| B5 | Accuracy indication — show, per algorithm, whether the result matched the reference sort | Must Have | B1 | Success metric from intent-capture; falls inside B1/B2 naturally but listed so it is never dropped |

## Notes

- B1–B5 together are the MVP (Q1: A: the app exactly as described). Nothing here is Should/Could/Won't — the description already is the minimum, and the hard constraints (C1–C3) keep it there.
- Because Q2 makes side-by-side comparison the delivery shape, B2 naturally exercises all three algorithms at once; there is no separate "add the second algorithm" slice.
- Sequencing within the Must Haves follows the table order: B1 → B2 → B3/B4 (either order) → B5 verification polish. Later phases will turn these into units and a delivery plan.

## Value Stream (summary)

Input (manual or word list) → button press → three algorithms run with step counting → accuracy check against reference → side-by-side results displayed. Every slice above sits on this stream; no slice exists off it.

## Assumptions & Open Questions

- [assumption] The step-counting convention (defined in design, not here) applies uniformly so B1's counts are comparable in B2.
- [assumption] B5 may be absorbed into B1/B2 during unit breakdown rather than standing alone; either treatment is acceptable as long as accuracy checking ships.
