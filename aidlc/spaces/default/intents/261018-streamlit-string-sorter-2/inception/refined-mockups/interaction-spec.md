# Interaction Specification

Component-level specifications for the single Streamlit screen, using the component-spec template. Every component maps to a native Streamlit widget (see `design-system-mapping.md`); no custom widgets or CSS.

## Sources

- `inception/refined-mockups/mockups.md` (screen states A–C)
- `inception/refined-mockups/refined-mockups-questions.md` (D1–D10)
- `inception/user-stories/stories.md` (US1–US4)

---

## String Input (manual entry)

| Field | Value |
|---|---|
| Component | Manual string input |
| Description | Accepts typed/pasted strings, one per line (US1.1) |
| Category | input |

### States

| State | Description | Trigger |
|---|---|---|
| default | Empty text area with visible label | page load |
| focus | Keyboard focus inside the area | Tab / click |
| filled | One or more non-empty lines present | user types/pastes |
| error | Sort pressed while effectively empty | empty input + Sort (message rendered by Empty-Input Message component, not here) |

### Props / Inputs

| Prop | Type | Required | Default | Description |
|---|---|---|---|---|
| label | string | yes | "Type or paste strings, one per line" | Visible label (not placeholder-only) |
| key | string | yes | "manual_input" | Stable widget key |

### Behaviour

- Lines are split on newlines; commas also delimit within a line (D9/AC1.1.4 — commas always delimit; embedded commas are not representable in v1).
- On Sort: trim each token, drop empty tokens, lowercase ASCII capitals (normalization D9), pass the cleaned list to the sort pipeline.
- Non-ASCII characters pass through unchanged (D10).

### Responsive Behaviour

| Breakpoint | Behaviour |
|---|---|
| mobile (<768px) | Stacks above word list (Streamlit columns reflow); not in testing scope (D6) |
| tablet (768–1024px) | Side-by-side as desktop |
| desktop (>1024px) | Left column of the input row |

### Accessibility

| Requirement | Implementation |
|---|---|
| ARIA role | Streamlit renders a labelled `<textarea>` |
| Keyboard interaction | Standard text editing; Tab moves to next widget |
| Label / aria-label | Visible `label` parameter |
| Contrast ratio | Streamlit default theme meets AA for label text |
| Screen reader | Announces label + text area; value changes read on focus |
| Focus management | Tab order: text area → multiselect → Sort |

---

## Word List Picker

| Field | Value |
|---|---|
| Component | Bundled word-list multiselect |
| Description | Lets the user pick words from the fixed bundled list (US1.2) |
| Category | input |

### States

| State | Description | Trigger |
|---|---|---|
| default | Empty multiselect with visible label | page load |
| focus | Keyboard focus | Tab / click |
| has-selection | One or more words selected (chips shown) | user picks |
| empty-list | Not applicable — bundled list is always populated in the package | — |

### Props / Inputs

| Prop | Type | Required | Default | Description |
|---|---|---|---|---|
| label | string | yes | "Pick words" | Visible label |
| options | list[str] | yes | bundled word list (shipped constant, ~20–30 words) | Fixed options; no external fetch (FR1.5/AC1.2.3) |
| key | string | yes | "word_picker" | Stable widget key |

### Behaviour

- Selected words join the same list as typed strings on Sort (shared list, D2). Merge order: typed tokens first, then picked words (duplicates kept — no dedup).
- Clearing all picks is allowed; combined emptiness with the text area triggers the empty-input path.

### Responsive Behaviour

| Breakpoint | Behaviour |
|---|---|
| mobile (<768px) | Stacks below text area; not in testing scope |
| tablet (768–1024px) | Side-by-side as desktop |
| desktop (>1024px) | Right column of the input row |

### Accessibility

| Requirement | Implementation |
|---|---|
| ARIA role | Streamlit multiselect (listbox pattern) |
| Keyboard interaction | Arrow keys navigate options; Enter/Backspace manage selection; Tab exits |
| Label / aria-label | Visible `label` parameter |
| Contrast ratio | Streamlit default theme |
| Screen reader | Announces label, options, and selected count |
| Focus management | In tab order after text area, before Sort |

---

## Sort Button

| Field | Value |
|---|---|
| Component | Sort trigger |
| Description | Single primary action that runs all three algorithms on the shared list (US2.1) |
| Category | input / feedback |

### States

| State | Description | Trigger |
|---|---|---|
| default | Enabled primary button | page load |
| hover / focus | Streamlit default styling | mouse / Tab |
| pressed | Sort runs synchronously; results replace previous | click / Enter / Space |
| disabled | Never disabled in v1 (empty-input message is the feedback path — D3) | — |

### Props / Inputs

| Prop | Type | Required | Default | Description |
|---|---|---|---|---|
| label | string | yes | "Sort" | Button text |
| key | string | yes | "sort_button" | Stable widget key |
| type | string | no | "primary" | Visual primacy |

### Behaviour

- On press: build the shared list (typed + picked, normalized, empties dropped). If empty → render Empty-Input Message and stop (AC4.1.1–4.1.2). Else run bubble, selection, and quick sort on the same list, check each against `sorted()`, render Result Column × 3 and the input echo.
- Runs synchronously; no loading indicator (classroom-sized inputs, D3).

### Responsive Behaviour

| Breakpoint | Behaviour |
|---|---|
| all | Full-width button below the input row (Streamlit default block layout) |

### Accessibility

| Requirement | Implementation |
|---|---|
| ARIA role | Native button (Streamlit) |
| Keyboard interaction | Enter or Space activates |
| Label / aria-label | Visible button text "Sort" |
| Contrast ratio | Streamlit primary button theme (AA) |
| Screen reader | Announces "Sort button"; results update announced via live region (see Result Column) |
| Focus management | Tab order: after multiselect, before results (no focus trap) |

---

## Result Column (× 3)

| Field | Value |
|---|---|
| Component | Algorithm result panel |
| Description | Displays one algorithm's sorted list, counts, and accuracy (US3.1, US3.2) |
| Category | display |

### States

| State | Description | Trigger |
|---|---|---|
| placeholder | Info hint "Press Sort to compare the three algorithms" | page load / before first sort |
| populated | Algorithm name, sorted list, comparisons, swaps, accuracy | successful Sort |
| replaced | Previous contents replaced in place on re-sort | Sort pressed again |
| partial-fail | One column shows Accuracy: Fail while others may Pass | accuracy mismatch (bug condition) |

### Props / Inputs

| Prop | Type | Required | Default | Description |
|---|---|---|---|---|
| algorithm_name | string | yes | "Bubble Sort" / "Selection Sort" / "Quick Sort" | Column heading (h3) |
| sorted_list | list[str] | yes | — | Strings to render, one per line |
| comparisons | int | yes | — | Total element comparisons (the step metric — D7) |
| swaps | int | yes | — | Swap count |
| accuracy_pass | bool | yes | — | Exact order match vs `sorted()` |

### Behaviour

- Accuracy rendered as `✓ Accuracy: Pass` or `✗ Accuracy: Fail` — icon + text, never color alone (D5).
- Each column is independent (AC3.2.4); counts are full integers, no truncation (AC3.2.5).
- Live region: results container announces update politely to screen readers after a Sort.

### Responsive Behaviour

| Breakpoint | Behaviour |
|---|---|
| mobile (<768px) | Streamlit columns stack vertically; not in testing scope (D6) |
| tablet (768–1024px) | Three columns as desktop |
| desktop (>1024px) | Three equal columns |

### Accessibility

| Requirement | Implementation |
|---|---|
| ARIA role | Region under main; headings h3 |
| Keyboard interaction | No focusable content inside |
| Label / aria-label | Algorithm name heading per column |
| Contrast ratio | Streamlit default text (AA) |
| Screen reader | Heading navigation reaches each column; accuracy line read as text ("check mark, Accuracy colon, Pass") |
| Focus management | N/A (display only); update announced via live region |

---

## Input Echo

| Field | Value |
|---|---|
| Component | Sorted-input display line |
| Description | Shows the normalized list actually sorted (FR5.4, US3.1/AC3.1.1) |
| Category | display |

### States

| State | Description | Trigger |
|---|---|---|
| absent | Not shown before first successful sort | page load / empty-input error |
| shown | "Input to sort: a, b, c" under the Sort button | successful Sort |

### Behaviour

- Comma-separated rendering of the normalized, empty-dropped list (D9). Makes the typed+picked merge visible (D2).

### Accessibility

Plain text line inside main; announced with the results live-region update.

---

## Empty-Input Message

| Field | Value |
|---|---|
| Component | Empty-input warning |
| Description | Tells the user why nothing ran and what to do (US4.1) |
| Category | feedback |

### States

| State | Description | Trigger |
|---|---|---|
| shown | "Enter or select at least one string" | Sort pressed with effectively empty shared list |
| hidden | Not rendered otherwise | any non-empty input |

### Behaviour

- Exact FR6.1 string. No algorithms run (AC4.1.2). Clears on next Sort press (re-evaluated each run).

### Accessibility

| Requirement | Implementation |
|---|---|
| ARIA role | Streamlit `st.warning` → alert live region |
| Keyboard interaction | N/A |
| Screen reader | Announced immediately when rendered |
