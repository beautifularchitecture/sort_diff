# Refined Mockups — Observation Diary

## Interpretations

- Requirements-analysis output supersedes rough-mockups where they conflict: the rough sketch's minimal "Steps: N + accuracy" results (Q5: A) was expanded to Comparisons + Swaps + Accuracy per FR4.2/FR4.3/FR5.3 and stories US3.2. Recorded as D7 so downstream stages don't re-litigate it.
- The rough mockups' open question [Q1] (merged typed+picked view) resolved as: yes — the normalized shared list is echoed above results after each sort (D2, input-echo component), which also satisfies US3.1/AC3.1.1 without adding a new live-updating merged panel.
- "Basic accessibility" from rough-mockups Q7 interpreted as targeting WCAG 2.1 AA for the items within Streamlit's control (D5); out-of-control items documented as relying on Streamlit defaults rather than claimed as verified.
- Reviewer Major finding #3 (non-ASCII behavior) closed at design level: pass through unchanged, sorted by code point (D10) — consistent with FR2.4 and the `sorted()` accuracy reference.
- Reviewer Major finding #2 (AC4.2.3 untestable "appropriately") given concrete design behavior: empty tokens dropped at input processing before sorting; echo shows cleaned list (D9).

## Deviations

- Sort button deliberately NOT disabled on empty input: FR6.1 requires the message on press, so the feedback path is the warning, not prevention (D3/interaction-spec Sort states). This departs from the UX-guide "disable invalid actions" heuristic with rationale: the requirement mandates a message, and disabling would suppress it.
- No loading state designed (rough-mockups assumption retained): synchronous classroom-sized runs make a spinner noise; revisit only if functional design finds a reason.

## Tradeoffs

- Chose caption-style input echo over a dedicated "merged list" panel: less visual weight, still makes the merge inspectable; a live panel would update on every keystroke/pick with little added value for v1.
- Accuracy shown as text + Unicode icon rather than a badge/pill component: keeps D4 (no custom styling) while satisfying P3 (not color-alone); a styled badge would need custom CSS.
- Accessibility R3 (live-region announcement of results) accepted as Streamlit-dependent: spec'd for empirical verification in Build and Test instead of promising a guarantee design cannot enforce.

## Open questions

- Bundled word-list contents (exact ~20–30 words) deferred to Code Generation as an implementation constant; design only requires it be fixed, shipped in-package, and non-empty.
- None other; all rough-mockups questions and reviewer design-relevant findings are closed in D1–D10.
