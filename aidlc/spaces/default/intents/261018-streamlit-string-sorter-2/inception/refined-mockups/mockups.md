# Refined Mockups

Mid-to-high fidelity representation of the single Streamlit screen. ASCII wireframes describe structure and content; visual styling is Streamlit default (no custom CSS — design decision D4).

## Sources

- `ideation/rough-mockups/wireframes.md` (refined per D7–D10)
- `inception/user-stories/stories.md` (US1.1–US4.2)
- `inception/refined-mockups/refined-mockups-questions.md` (decisions D1–D10)

---

## Screen 1 — Main (only) screen

### State A: Default (page load, no sort yet)

```text
+======================================================================+
|  Sorting Algorithm Playground                          (h1)          |
+======================================================================+
|  1. INPUT                                         2. WORD LIST      |
|  +-------------------------------------+  +-----------------------+ |
|  | Type or paste strings,              |  | Pick words            | |
|  | one per line                        |  | (multiselect)         | |
|  |                                     |  |                       | |
|  |                                     |  | apple                 | |
|  |                                     |  | banana                | |
|  |                                     |  | cherry                | |
|  |                                     |  | ... (bundled list)    | |
|  +-------------------------------------+  +-----------------------+ |
|                                                                      |
|  [ Sort ]                                              (primary btn)  |
|                                                                      |
|  ------------------------------------------------------------------  |
|  3. RESULTS                                                           |
|  ℹ Press Sort to compare the three algorithms                        |
|                                                                      |
+======================================================================+
```

- Title (h1): **Sorting Algorithm Playground** (page header landmark).
- Input label: "Type or paste strings, one per line" (visible `label` on `st.text_area`, not placeholder-only).
- Word-list label: "Pick words" (visible `label` on `st.multiselect`); picked words are shown as chips inside the widget by Streamlit.
- Sort button disabled only by Streamlit defaults; pressing it with no input shows State B (error message, no sort) — the button is not disabled (FR6.1 requires a message, not prevention).
- Results area before first sort: `st.info` hint line (empty state, not an error).

### State B: Sort pressed with no input

```text
|  [ Sort ]                                                             |
|                                                                      |
|  ⚠ Enter or select at least one string                               |
|                                                                      |
|  3. RESULTS                                                           |
|  ℹ Press Sort to compare the three algorithms                        |
```

- `st.warning` with the exact FR6.1 string. No algorithms run; results area unchanged.
- Message appears directly below the Sort button, above results (inline near the cause — UX heuristic 9).

### State C: Success (input provided, Sort pressed)

```text
+======================================================================+
|  Sorting Algorithm Playground                          (h1)          |
+======================================================================+
|  1. INPUT                                         2. WORD LIST      |
|  +-------------------------------------+  +-----------------------+ |
|  | pear                                 |  | cherry       [ x ]    | |
|  | apple                                |  | delta         [ x ]   | |
|  | mango                                |  |                       | |
|  +-------------------------------------+  +-----------------------+ |
|  [ Sort ]                                                             |
|                                                                      |
|  Input to sort: apple, cherry, delta, mango, pear                    |
|                                                                      |
|  3. RESULTS                                                           |
|  +---------------------+ +---------------------+ +------------------+ |
|  | Bubble Sort         | | Selection Sort      | | Quick Sort       | |
|  |                     | |                     | |                  | |
|  | apple               | | apple               | | apple            | |
|  | cherry              | | cherry              | | cherry           | |
|  | delta               | | delta               | | delta            | |
|  | mango               | | mango               | | mango            | |
|  | pear                | | pear                | | pear             | |
|  |                     | |                     | |                  | |
|  | Comparisons: 10     | | Comparisons: 10     | | Comparisons: 8   | |
|  | Swaps: 4            | | Swaps: 3            | | Swaps: 4         | |
|  | ✓ Accuracy: Pass    | | ✓ Accuracy: Pass    | | ✓ Accuracy: Pass | |
|  +---------------------+ +---------------------+ +------------------+ |
+======================================================================+
```

- **Input echo** (FR5.4, US3.1/AC3.1.1): one line under the Sort button listing the normalized list that was actually sorted (comma-separated, lowercase, empty lines dropped — D9). This makes the typed+picked merge visible (D2).
- Three equal columns (US2.1/US3.1). Each column:
  - Algorithm name as a heading (h3 under the h1).
  - Sorted list, one string per line, matching the echo's normalization.
  - **Comparisons: N** — the comparable step metric (D7, FR4.2).
  - **Swaps: N** — separate count (FR4.3).
  - **✓ Accuracy: Pass** / **✗ Accuracy: Fail** — text + icon, never color alone (D5). Pass means exact order match against Python `sorted()` (FR3.1–FR3.2).
- Illustrative counts above are examples; real counts follow the step-counting convention in functional design.
- Re-sorting (State D): pressing Sort with edited input replaces the echo and all three columns in place — no animation, no history (user-flow branch table).

### Failure variant (accuracy fail)

If any algorithm's output diverges from the reference (implementation bug — should not happen in a correct build):

```text
|  ✗ Accuracy: Fail         |
```

Same column layout; only the accuracy line changes. The other two columns still show their own independent pass/fail (US3.2/AC3.2.4).

---

## Edge-case rendering (same screen, State C variants)

| Input | Rendering notes |
|-------|-----------------|
| Single string (`mango`) | Echo shows `mango`; each column lists `mango`; comparisons/swaps at algorithm-defined minimal counts; Accuracy: Pass (US4.2/AC4.2.1) |
| All identical (`pear`, `pear`, `pear`) | Echo shows three `pear` lines (duplicates kept — no dedup); columns list all three; Accuracy: Pass (AC4.2.2) |
| Empty lines in pasted input | Dropped before sorting; echo shows the cleaned list only (D9, AC4.2.3) |
| Non-ASCII (`café`) | Passed through, sorted by code point; accuracy still vs `sorted()` on the same list (D10) |
| Mixed case typed (`Banana`) | Echo shows `banana` (normalization applied once, at input processing — D9) |

---

## Accessibility landmarks & focus order (per screen)

- Landmarks: header (h1 title) + main (input, button, results) — Streamlit default structure.
- Focus order: text area → multiselect → Sort button → (results contain no focusable elements). Matches visual reading order.
- Each result column heading is an h3 under the page h1 (no skipped levels).
- Warning and info messages use Streamlit's alert widgets, which expose `role="alert"` / live regions to assistive tech.

## Out of scope (unchanged from rough mockups)

No account/login, no saving, no file upload/download, no per-algorithm animation or step replay, no multi-page navigation, no phone-specific layout.
