# Refined Mockups — Questions & Design Decisions

## Sources

- `ideation/rough-mockups/wireframes.md` and `user-flow.md` — Q1–Q7 already confirmed there (one page, three columns, one text box, picker beside it, minimal results, desktop only, basic accessibility)
- `inception/user-stories/stories.md` — US1.1–US5.2
- `inception/requirements-analysis/requirements.md` — FR1–FR7, NFR1–NFR4
- Human instruction: full autopilot for this workflow

## Design Decisions (made under full autopilot; human confirms at summary confirmation)

### D1. How is each user story represented in the UI?

| Story | UI representation |
|-------|-------------------|
| US1.1 | `st.text_area` — "Type or paste strings, one per line" |
| US1.2 | `st.multiselect` over the bundled word list, beside the text area (`st.columns(2)`) |
| US2.1 | Single primary `st.button` "Sort" under the input row |
| US3.1 | Three equal result columns (`st.columns(3)`); input echoed above results |
| US3.2 | Each column shows Comparisons, Swaps, Accuracy (pass/fail text + icon) |
| US4.1 | `st.warning("Enter or select at least one string")`; no sort runs |
| US4.2 | Handled in logic; UI shows correct results/counts for these inputs (no special controls) |
| US5.1/US5.2 | No UI surface; deployment concern |

### D2. Interaction patterns

None beyond native Streamlit widgets — no modals, wizards, or progressive disclosure (NFR2.1 simplicity, single screen from rough-mockups Q1). Typed lines and picked words merge into one shared list (rough wireframe plan, Q1 resolution: merged view — the effective list is echoed above the results so the merge is visible, US3.1/AC3.1.1).

### D3. Screen states

| State | Trigger | Presentation |
|-------|---------|--------------|
| Default (page load) | app start | Empty input; results area shows `st.info("Press Sort to compare the three algorithms")` |
| Error (empty input) | Sort pressed, no strings | `st.warning("Enter or select at least one string")` — exact FR6.1 wording; no sort runs |
| Success | Sort pressed with input | Echo normalized input; three result columns with list, comparisons, swaps, accuracy |
| Re-sort | Edit + Sort again | Results replaced in place (no history — storage out of scope) |
| Loading | — | Not needed: synchronous run on classroom-sized inputs (rough-mockups assumption, feasibility A1) |

### D4. Design system / component library

Streamlit built-in components only — no custom CSS, no external component library (NFR2.1, NFR2.3 self-contained). `design-system-mapping.md` maps every UI element to its Streamlit widget.

### D5. Accessibility target

WCAG 2.1 Level AA where Streamlit's rendering allows (rough mockups chose "basic accessibility"; AA is the checklist target). Pass/fail accuracy is shown as **text plus icon**, never color alone. Focus order follows Streamlit's DOM order, which matches the visual order of the single-column page. See `accessibility-checklist.md`.

### D6. Responsive behaviour

Desktop/laptop only (rough-mockups Q6:A). The three-column results row targets a laptop viewport; Streamlit's default fluid layout handles narrower windows by reflow, but no mobile-specific design or testing is in scope (NFR3.6 classroom-sized, single-screen desktop app).

### D7. Results detail (supersedes rough-mockups Q5)

Rough mockups sketched "Steps: N + accuracy" only. Requirements-analysis later specified the full metrics (FR4.2 comparisons as the comparable metric, FR4.3 swaps separately, FR5.3 display fields). **Requirements win**: each column shows Comparisons, Swaps, and Accuracy. The rough wireframe's "Steps" label is replaced by the explicit "Comparisons" label so "steps" has one meaning (reviewer Minor finding on US3.2, adopted).

### D8. Empty-input message wording

Exact FR6.1 string: `Enter or select at least one string`. This supersedes the rough mockups' placeholder "Nothing to sort yet — add strings above."

### D9. Input normalization display

Normalized (lowercase) forms are what get sorted and echoed (FR1.3, FR1.4, US1.1/AC1.1.2–AC1.1.3). The echo above results shows the list after normalization, so all three columns visibly agree on ordering. Empty lines from pasted input are dropped before sorting (US4.2/AC4.2.3 concrete behavior, closing the reviewer's untestability finding at design level: implementation will remove empty entries pre-sort).

### D10. Non-ASCII characters

Passed through unchanged and sorted by Python's default code-point order (consistent with FR2.4 lexicographic ASCII/Unicode as-is and the accuracy check against `sorted()`, which does the same). No rejection or stripping — the normalization rule only lowercases ASCII capitals. Recorded here so US1.1's parser tests have a settled behavior (reviewer Major finding #3, closed at design level).

## Ambiguity Analysis

No vague language, contradictions, or missing details remain after D1–D10. All rough-mockup open questions are resolved. Proceeding to artifact generation; the human confirms at summary confirmation and the completion gate.

## Consolidated Summary Confirmation

Here is the combined summary of this stage's decisions. Please confirm it.

**Screen**: One Streamlit page, desktop-first — title, input row (text area + word-list multiselect side by side), single Sort button, input echo, three equal result columns. Streamlit default widgets and theme only; no custom CSS (D4).

**Decisions D1–D10** (full detail in the questions file above):
- D1–D3: Every story maps to the one screen; states are default / empty-input warning / success / re-sort; no loading state (synchronous, classroom-sized).
- D5: Accessibility target WCAG 2.1 AA for items Streamlit controls; accuracy is text + icon, never color alone.
- D6: Desktop/laptop only (per rough-mockups Q6); no mobile design or testing.
- D7: Results show **Comparisons** (the step metric), **Swaps**, and **Accuracy** — requirements supersede the rough sketch's minimal "Steps" label.
- D8: Empty-input message uses the exact FR6.1 string "Enter or select at least one string".
- D9: Input echo shows the normalized (lowercase, empty-lines-dropped) list that was actually sorted.
- D10: Non-ASCII characters pass through unchanged, sorted by code point (closes the review's non-ASCII open corner at design level).

**Artifacts**: mockups.md (screen states A–C + edge-case rendering), interaction-spec.md (6 component specs), design-system-mapping.md (widget map + constants), accessibility-checklist.md (POUR checklist + testing plan).

**Open items for later stages**: exact bundled word-list contents deferred to Code Generation; screen-reader announcement wording verified empirically in Build and Test.

[Answer]: Looks correct
