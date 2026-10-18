## Sources

- [desc] Initial description: Streamlit app — enter strings manually or pick from a word list, sort with bubble/selection/quick, see results and step counts.
- [scope] Workflow-selected scope: `feature`.
- Upstream artifacts: `ideation/scope-definition/scope-document.md` (side-by-side results, both input methods, no complex styling C3); `ideation/scope-definition/intent-backlog.md` (B1–B5).

## Q1. How many screens/views should the app have?

[Answer]:A

A. One single page with everything on it (input, sort button, results)
B. A small number of tabs or sections (for example: input on one tab, results on another)
X. Other (please specify)

## Q2. How should the three algorithms' results sit next to each other?

This sets the main layout of the results area (side-by-side is confirmed; this is about arrangement).

[Answer]:A

A. Three columns, one per algorithm, aligned so step counts line up
B. Stacked vertically, one block per algorithm
X. Other (please specify)

## Q3. How should manual string entry work?

[Answer]:A

A. One big text box — type or paste many strings, one per line
B. One string at a time, with an "Add" button building up the list
X. Other (please specify)

## Q4. How should word-list selection work?

The word list is bundled with the app (no external source).

[Answer]:A

A. A picker (checkboxes or multiselect) next to the manual box; picked words join the same list to sort
B. A separate section; you pick words there, then they become the input
X. Other (please specify)

## Q5. How much detail should each algorithm's result show?

[Answer]:A

A. Just the sorted list and the step count — clean and simple
B. Sorted list, step count, plus a small breakdown (for example comparisons vs swaps)
X. Other (please specify)

## Q6. Which devices do you care about?

[Answer]:

A. Desktop browser only — this is a learning tool on a laptop
B. Desktop first, but keep it usable on a phone if Streamlit allows it for free
X. Other (please specify)

## Q7. Accessibility — any requirements to record?

[Answer]:

A. Basic only: sensible labels, keyboard works, readable text (Streamlit defaults)
B. Aim for WCAG AA — stronger contrast and clearer structure from the start
X. Other (please specify)
