# Rough Mockups — Wireframes

## Sources

- `ideation/rough-mockups/rough-mockups-questions.md` — Q1: A (one page), Q2: A (three columns), Q3: A (one text box), Q4: A (picker beside manual box), Q5: A (sorted list + step count only), Q6: A (desktop only), Q7: A (basic accessibility) (confirmed)
- `ideation/scope-definition/scope-document.md` — six in-scope capabilities
- `ideation/scope-definition/intent-backlog.md` — B1–B5 value stream

## Screen 1 — Main (only) screen

One single page: input area on top, results below (Q1: A).

```text
+----------------------------------------------------------------------+
|  Sorting Algorithm Playground                                         |
|  (h1; page header landmark, Streamlit default)                        |
+----------------------------------------------------------------------+
|  1. INPUT                              |  2. CHOOSE FROM WORD LIST   |
|  +-----------------------------------+ |  +-------------------------+ |
|  | Type or paste strings,            | |  | Pick words (multiselect)| |
|  | one per line                      | |  | apple                   | |
|  |                                   | |  | banana                  | |
|  | pear                              | |  | cherry     [ x ]        | |
|  | apple                             | |  | delta     [ x ]         | |
|  | mango                             | |  | ...                     | |
|  |                                   | |  +-------------------------+ |
|  +-----------------------------------+ |  Picked words join the same   |
|  Manual entry (text_area)              |  list as typed strings        |
|                                        |                               |
|  [ Sort ]  (primary button)            |                               |
+----------------------------------------------------------------------+
|  3. RESULTS                                                    (main) |
|  +------------------------+ +------------------------+ +----------------+
|  | Bubble Sort            | | Selection Sort        | | Quick Sort     |
|  |                        | |                        | |                |
|  | apple                  | | apple                  | | apple          |
|  | mango                  | | mango                  | | mango          |
|  | pear                   | | pear                   | | pear           |
|  |                        | |                        | |                |
|  | Steps: 3              | | Steps: 3              | | Steps: 3       |
|  | Accuracy: OK          | | Accuracy: OK          | | Accuracy: OK   |
|  +------------------------+ +------------------------+ +----------------+
|   column 1 of 3                column 2 of 3              column 3 of 3  |
+----------------------------------------------------------------------+
```

Layout notes:

- Desktop browsers only (Q6: A) — the wide three-column layout targets a laptop screen; no phone layout work in v1.
- Two input sources side by side (Q3, Q4): the text area and the bundled-word multiselect feed **one shared list** to sort; picked words and typed lines appear together.
- One **Sort** button runs all three algorithms on the same list (scope: side-by-side comparison, Q2: A).
- Three equal columns align the **Steps** lines so counts compare at a glance; each column ends with its accuracy indication (B5). Accuracy is a required result field from the scope (capability 4), not extra detail beyond Q5's "sorted list + step count".
- Empty results area before the first sort: a short hint line ("Press Sort to compare the three algorithms").
- Results detail is deliberately minimal (Q5: A): sorted list + step count + accuracy, no swap/comparison breakdown.
- All three columns share one ordering rule for strings (case sensitivity, whitespace trimming) — decided in design, not here; see Assumptions.

Accessibility note per screen: heading h1 = "Sorting Algorithm Playground"; primary landmarks header (title) + main (input and results); input area is the keyboard entry point, focus order input → word picker → Sort button → results; each result column labeled with its algorithm name as a heading (h3 under the h1).

## Out-of-view states

- **No input yet + Sort pressed**: results columns show "Nothing to sort yet — add strings above." (empty state, not an error).
- **Duplicate strings**: allowed; duplicates appear in the sorted output (no dedup — not in scope).

## Assumptions & Open Questions

- [assumption] Step counts being equal across algorithms in the sketch is illustrative; real counts follow the step-counting convention defined in design, not here.
- [assumption] "Accuracy: OK" is the placeholder for the verified-against-reference indication (B5); its exact wording is a design/later-stage detail.
- [assumption] String comparison semantics (case sensitivity, leading/trailing whitespace on pasted lines) are not fixed here — design must pick one rule so all three columns visibly agree on ordering; the accuracy check compares against the same rule.
- [Q1] Should the shared input list show typed + picked items merged in one visible place (my plan: yes — merged view under the text area), or only implicitly? Flagged for refined mockups if you care.
